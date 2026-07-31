from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models import Avg, Count
from django.utils.text import slugify
import json

from guild.models import Thread, Comment, Vote, Community
from library.models import Framework, FrameworkReview
from brain.models import BrainNote, BrainFork
from social.models import Follow, Notification
from usuarios.models import Perfil


def json_body(request):
    try:
        return json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        return {}


def _vote(request, model_class, object_id):
    payload = json_body(request)
    direction = payload.get('direction')
    if direction not in ('up', 'down', None):
        return JsonResponse({"erro": "direction deve ser 'up', 'down' ou null"}, status=400)

    obj = get_object_or_404(model_class, id=object_id)
    ct = ContentType.objects.get_for_model(model_class)

    existing = Vote.objects.filter(usuario=request.user, content_type=ct, object_id=obj.id).first()

    if direction is None:
        if existing:
            obj.upvotes -= existing.valor
            obj.save()
            existing.delete()
        return JsonResponse({"ok": True, "object_id": object_id, "direction": None})

    new_valor = 1 if direction == 'up' else -1

    if existing:
        delta = new_valor - existing.valor
        existing.valor = new_valor
        existing.save()
    else:
        delta = new_valor
        Vote.objects.create(usuario=request.user, content_type=ct, object_id=obj.id, valor=new_valor)

    obj.upvotes += delta
    obj.save()
    return JsonResponse({"ok": True, "object_id": object_id, "direction": direction, "upvotes": obj.upvotes})


@csrf_exempt
@require_POST
def vote_post(request, post_id):
    return _vote(request, Thread, post_id)


@csrf_exempt
@require_POST
def vote_comment(request, comment_id):
    return _vote(request, Comment, comment_id)


@csrf_exempt
@require_POST
def create_post(request):
    payload = json_body(request)
    required = ['community_slug', 'title', 'post_type']
    missing = [k for k in required if not payload.get(k)]
    if missing:
        return JsonResponse({"erro": f"campos faltando: {', '.join(missing)}"}, status=400)

    community = get_object_or_404(Community, slug=payload['community_slug'])
    base_slug = slugify(payload['title'])[:50]
    slug = base_slug
    counter = 1
    while Thread.objects.filter(community=community, slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    thread = Thread.objects.create(
        community=community,
        slug=slug,
        title=payload['title'],
        author_handle=request.user.username,
        body=payload.get('body', ''),
        preview=payload.get('body', '')[:150],
        post_type=payload.get('post_type', 'text'),
        tag=payload.get('tag', 'discussão'),
        url=payload.get('url', ''),
    )
    request.user.perfil.adicionar_xp(10)
    return JsonResponse({"ok": True, "post": {
        "id": thread.id, "slug": thread.slug, "community_slug": community.slug,
        "title": thread.title, "post_type": thread.post_type,
    }}, status=201)


@csrf_exempt
@require_POST
def create_comment(request):
    payload = json_body(request)
    post_id = payload.get('post_id')
    body = payload.get('body', '').strip()
    if not post_id or not body:
        return JsonResponse({"erro": "post_id e body são obrigatórios"}, status=400)

    thread = get_object_or_404(Thread, id=post_id)
    parent_id = payload.get('parent_id')

    comment = Comment.objects.create(
        thread=thread,
        parent_id=parent_id if parent_id else None,
        author_handle=request.user.username,
        body=body,
    )

    from django.utils import timezone
    Comment.objects.filter(id=comment.id).update(created_at=timezone.now())
    comment.refresh_from_db()

    request.user.perfil.adicionar_xp(5)

    return JsonResponse({"ok": True, "comment": {
        "id": comment.id, "post_id": post_id,
        "body": comment.body, "parent_id": parent_id,
    }}, status=201)


@csrf_exempt
@require_POST
def join_community(request, slug):
    community = get_object_or_404(Community, slug=slug)
    if not request.user.is_authenticated:
        return JsonResponse({"erro": "autenticação obrigatória"}, status=403)
    payload = json_body(request)
    joined = bool(payload.get('joined', True))
    from guild.models import GuildMembership
    if joined:
        previous = GuildMembership.objects.filter(usuario=request.user).first()
        if previous and previous.community_id != community.id:
            previous.community.members = max(previous.community.members - 1, 0)
            previous.community.save(update_fields=['members'])
            previous.delete()
        membership, created = GuildMembership.objects.get_or_create(usuario=request.user, defaults={'community': community})
        if not created and membership.community_id != community.id:
            membership.community = community
            membership.save(update_fields=['community'])
        if created:
            community.members += 1
    elif community.members > 0:
        deleted, _ = GuildMembership.objects.filter(usuario=request.user, community=community).delete()
        if deleted:
            community.members -= 1
    community.save()
    return JsonResponse({"ok": True, "slug": slug, "joined": joined})


@csrf_exempt
@require_POST
def follow_user(request, handle):
    from django.contrib.auth.models import User
    target = get_object_or_404(User, username=handle)
    payload = json_body(request)
    following = bool(payload.get('following', True))

    if following:
        Follow.objects.get_or_create(seguidor=request.user, seguido=target)
        Notification.objects.create(
            usuario=target,
            tipo='follow',
            mensagem=f"{request.user.username} começou a seguir você",
            link=f"/u/{request.user.username}",
        )
    else:
        Follow.objects.filter(seguidor=request.user, seguido=target).delete()

    return JsonResponse({"ok": True, "handle": handle, "following": following})


@csrf_exempt
@require_POST
def fork_framework(request, framework_id):
    fw = get_object_or_404(Framework, framework_id=framework_id)
    payload = json_body(request)
    fork_name = payload.get('name', f"{fw.title} (meu fork)")
    BrainFork.objects.create(
        user=request.user,
        framework_id=fw.framework_id,
        framework_title=fw.title,
        framework_slug=fw.slug,
        my_version_label=fork_name,
    )
    return JsonResponse({"ok": True, "fork": {
        "framework_id": framework_id, "name": fork_name,
        "owner": request.user.username,
    }}, status=201)


@csrf_exempt
@require_POST
def review_framework(request, framework_id):
    payload = json_body(request)
    rating = payload.get('rating')
    text = (payload.get('text') or '').strip()
    if not isinstance(rating, int) or rating < 1 or rating > 5:
        return JsonResponse({"erro": "rating deve ser inteiro entre 1 e 5"}, status=400)
    if not text:
        return JsonResponse({"erro": "review precisa de texto"}, status=400)

    with transaction.atomic():
        fw = get_object_or_404(
            Framework.objects.select_for_update(),
            framework_id=framework_id,
        )
        FrameworkReview.objects.create(
            framework=fw,
            author_handle=request.user.username,
            rating=rating,
            text=text,
            time_ago='agora',
        )
        aggregates = FrameworkReview.objects.filter(framework=fw).aggregate(
            average=Avg('rating'),
            count=Count('id'),
        )
        fw.rating = round(aggregates['average'] or 0, 1)
        fw.reviews_count = aggregates['count'] or 0
        fw.save(update_fields=['rating', 'reviews_count'])

    return JsonResponse({"ok": True, "review": {
        "framework_id": framework_id,
        "rating": rating,
        "text": text,
        "average": fw.rating,
        "reviews_count": fw.reviews_count,
    }}, status=201)


@csrf_exempt
@require_POST
def share_to_guild(request):
    payload = json_body(request)
    source_type = payload.get('source_type')
    source_id = payload.get('source_id')
    community_slug = payload.get('community_slug', 'gestao-pessoas')
    if not source_type or not source_id:
        return JsonResponse({"erro": "source_type e source_id são obrigatórios"}, status=400)

    community = get_object_or_404(Community, slug=community_slug)
    title = f"{source_type}: {source_id}"
    slug = slugify(title)[:50]

    Thread.objects.create(
        community=community,
        slug=slug,
        title=title,
        author_handle=request.user.username,
        body=f"Compartilhado de {source_type}: {source_id}",
        tag='discussão',
    )
    return JsonResponse({"ok": True, "shared": {
        "source_type": source_type, "source_id": source_id,
        "community_slug": community_slug,
    }}, status=201)


@csrf_exempt
@require_POST
def toggle_note_public(request, note_id):
    note = get_object_or_404(BrainNote, id=note_id, user=request.user)
    payload = json_body(request)
    note.is_public = bool(payload.get('is_public', not note.is_public))
    note.save()
    return JsonResponse({"ok": True, "note_id": note_id, "is_public": note.is_public})


@require_GET
def list_notifications(request):
    notifs = Notification.objects.filter(usuario=request.user)[:50]
    data = []
    for n in notifs:
        data.append({
            "id": str(n.id),
            "type": n.tipo,
            "message": n.mensagem,
            "link": n.link,
            "is_read": n.lida,
            "created_at": n.created_at.isoformat() if n.created_at else None,
        })
    return JsonResponse({
        "notifications": data,
        "unread_count": sum(1 for n in data if not n["is_read"]),
    })


@csrf_exempt
@require_POST
def read_notification(request, notif_id):
    notif = get_object_or_404(Notification, id=notif_id, usuario=request.user)
    notif.lida = True
    notif.save()
    return JsonResponse({"ok": True, "id": str(notif.id)})


@csrf_exempt
@require_POST
def read_all_notifications(request):
    Notification.objects.filter(usuario=request.user, lida=False).update(lida=True)
    return JsonResponse({"ok": True})


@csrf_exempt
@require_POST
def quick_note(request):
    payload = json_body(request)
    note = BrainNote.objects.create(
        user=request.user,
        title=payload.get("title", "Nota rápida"),
        content=payload.get("content", ""),
        source=payload.get("source", ""),
        source_type='manual',
        is_public=False,
    )
    request.user.perfil.adicionar_xp(10)
    return JsonResponse({"ok": True, "note": {"id": note.id, "title": note.title}}, status=201)


@csrf_exempt
@require_POST
def update_progress(request):
    from cursos.models import ProgressoModulo, Aula
    payload = json_body(request)
    aula_id = payload.get('aula_id')
    progresso = int(payload.get('progresso', 0))
    if not aula_id:
        return JsonResponse({"erro": "aula_id é obrigatório"}, status=400)
    aula = get_object_or_404(Aula, id=aula_id)
    pm, created = ProgressoModulo.objects.get_or_create(
        usuario=request.user, modulo=aula.modulo,
        defaults={'progresso': 0}
    )
    old = pm.progresso
    pm.progresso = max(pm.progresso, progresso)
    if pm.progresso == 100 and old < 100:
        from cursos.services import issue_certificate
        request.user.perfil.adicionar_xp(aula.modulo.xp_total)
        issue_certificate(request.user, modulo=aula.modulo)
    pm.save()
    return JsonResponse({"ok": True, "progresso": pm.progresso})


@csrf_exempt
@require_POST
def complete_challenge(request, desafio_id):
    from cursos.models import Desafio, ProgressoDesafio
    desafio = get_object_or_404(Desafio, id=desafio_id)
    pd, _ = ProgressoDesafio.objects.get_or_create(
        usuario=request.user, desafio=desafio,
        defaults={'progresso': 0}
    )
    previous_progress = pd.progresso
    pd.progresso = min(desafio.meta, pd.progresso + 1)
    if previous_progress < desafio.meta <= pd.progresso:
        request.user.perfil.adicionar_xp(desafio.xp)
    pd.save()
    return JsonResponse({"ok": True, "progresso": pd.progresso, "meta": desafio.meta})


@require_GET
def my_xp(request):
    p = request.user.perfil
    last_event = request.user.xp_events.first()
    return JsonResponse({
        "xp_total": p.xp_total,
        "nivel": p.nivel,
        "streak_dias": p.streak_dias,
        "nome_nivel": p.nome_nivel,
        "xp_proximo_nivel": p.xp_proximo_nivel,
        "xp_percentual": p.xp_percentual,
        "moedas": p.moedas,
        "titulo_ativo": p.titulo_ativo.nome if p.titulo_ativo else p.nome_nivel,
        "last_event": {
            "xp": last_event.xp,
            "descricao": last_event.descricao,
            "level_up": last_event.level_up,
            "nivel_anterior": last_event.nivel_anterior,
            "nivel_atual": last_event.nivel_atual,
        } if last_event else None,
    })


@csrf_exempt
@require_POST
def submit_quiz(request, quiz_id):
    from cursos.models import Quiz, Questao, TentativaQuiz
    payload = json_body(request)
    respostas = payload.get('respostas', {})
    if not isinstance(respostas, dict):
        return JsonResponse({"erro": "Formato de respostas inválido."}, status=400)
    quiz = get_object_or_404(Quiz.objects.prefetch_related('questoes__alternativas'), id=quiz_id)
    questoes = list(quiz.questoes.all())
    if not questoes:
        return JsonResponse({"erro": "Este quiz ainda não possui perguntas."}, status=400)
    question_ids = {str(question.id) for question in questoes}
    if question_ids - set(respostas):
        return JsonResponse({"erro": "Responda todas as perguntas antes de enviar."}, status=400)
    acertos = 0
    for q in questoes:
        alt_id = respostas.get(str(q.id))
        if alt_id:
            alt = q.alternativas.filter(id=alt_id).first()
            if alt and alt.correta:
                acertos += 1
    total = len(questoes)
    pct = int(acertos / total * 100) if total else 0
    aprovado = pct >= quiz.aprovacao_percentual
    tentativas_feitas = TentativaQuiz.objects.filter(usuario=request.user, quiz=quiz).count()
    if tentativas_feitas >= quiz.max_tentativas:
        return JsonResponse({"erro": "número máximo de tentativas atingido"}, status=403)
    primeira_tentativa = tentativas_feitas == 0
    if primeira_tentativa:
        xp_ganho = int(quiz.xp_total * acertos / total) if total else 0
        if xp_ganho:
            request.user.perfil.adicionar_xp(xp_ganho)
    else:
        xp_ganho = 0
    TentativaQuiz.objects.create(
        usuario=request.user, quiz=quiz,
        pontuacao=acertos, total_questoes=total, aprovado=aprovado,
        respostas=respostas,
    )
    return JsonResponse({
        'acertos': acertos, 'total': total, 'percentual': pct,
        'aprovado': aprovado, 'xp_ganho': xp_ganho,
        'primeira_tentativa': primeira_tentativa,
    })
