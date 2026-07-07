from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
import json


USERS = {
    "gabriel": {"handle": "gabriel", "nome_completo": "Gabriel Lasaro"},
    "camila-faria": {"handle": "camila-faria", "nome_completo": "Camila Faria"},
    "mariana-reis": {"handle": "mariana-reis", "nome_completo": "Mariana Reis"},
    "bruno-tavares": {"handle": "bruno-tavares", "nome_completo": "Bruno Tavares"},
    "camila-souza": {"handle": "camila-souza", "nome_completo": "Camila Souza"},
    "diego-almeida": {"handle": "diego-almeida", "nome_completo": "Diego Almeida"},
    "lucas-pestana": {"handle": "lucas-pestana", "nome_completo": "Lucas Pestana"},
    "pedro-mendes": {"handle": "pedro-mendes", "nome_completo": "Pedro Mendes"},
    "marina-costa": {"handle": "marina-costa", "nome_completo": "Marina Costa"},
    "rafael-santos": {"handle": "rafael-santos", "nome_completo": "Rafael Santos"},
    "ana-lima": {"handle": "ana-lima", "nome_completo": "Ana Lima"},
    "pedro-vianna": {"handle": "pedro-vianna", "nome_completo": "Pedro Vianna"},
}

guild_communities = [{"id": "c1", "slug": "gestao-pessoas"}, {"id": "c2", "slug": "tech-produto"}, {"id": "c3", "slug": "soft-skills"}, {"id": "c4", "slug": "empreendedorismo"}, {"id": "c5", "slug": "carreira-inicial"}, {"id": "c6", "slug": "vendas-growth"}]

guild_threads = [
    {"id": "t1", "title": "Como vocês conduzem 1:1...", "author": "mariana-reis", "community_slug": "gestao-pessoas"},
    {"id": "t2", "title": "Aplicando o framework WRAP...", "author": "bruno-tavares", "community_slug": "carreira-inicial"},
    {"id": "t3", "title": "Pricing: por que aumentei 30%...", "author": "camila-souza", "community_slug": "empreendedorismo"},
    {"id": "t4", "title": "Alguém usa o Conflict Canvas?", "author": "diego-almeida", "community_slug": "soft-skills"},
    {"id": "t5", "title": "Stand-up de 9 min...", "author": "pedro-vianna", "community_slug": "tech-produto"},
]

library_frameworks = [
    {"id": "fw1", "title": "1:1 Canvas"},
    {"id": "fw2", "title": "Feedback SBI"},
    {"id": "fw3", "title": "OKR Trimestral"},
    {"id": "fw4", "title": "Conflict Canvas"},
    {"id": "fw5", "title": "Decision Journal"},
    {"id": "fw6", "title": "Stand-up 9 minutos"},
]

my_brain_notes = [
    {"id": "n1", "title": "SBI funciona quando o gatilho é claro", "is_public": False},
    {"id": "n2", "title": "Decisão difícil = listar opções fora do binário", "is_public": True},
    {"id": "n3", "title": "Pricing — desconto é veneno doce", "is_public": True},
    {"id": "n4", "title": "Conflict Canvas: começar sempre pelo medo", "is_public": False},
]

NOTIFICATIONS = [
    {"id": "no1", "is_read": False},
    {"id": "no2", "is_read": False},
    {"id": "no3", "is_read": False},
    {"id": "no4", "is_read": True},
    {"id": "no5", "is_read": True},
    {"id": "no6", "is_read": True},
]


def json_body(request):
    try:
        return json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        return {}


def get_community(slug):
    return next((c for c in guild_communities if c["slug"] == slug), None)


def get_post(post_id):
    return next((t for t in guild_threads if t["id"] == post_id), None)


def get_framework(framework_id):
    return next((f for f in library_frameworks if f["id"] == framework_id), None)


# === POST & COMMENT VOTES ===

@csrf_exempt
@require_POST
def vote_post(request, post_id):
    payload = json_body(request)
    direction = payload.get('direction')
    if direction not in ('up', 'down', None):
        return JsonResponse({"erro": "direction deve ser 'up', 'down' ou null"}, status=400)
    post = get_post(post_id)
    if not post:
        return JsonResponse({"erro": "post não encontrado"}, status=404)
    return JsonResponse({"ok": True, "post_id": post_id, "direction": direction})


@csrf_exempt
@require_POST
def vote_comment(request, comment_id):
    payload = json_body(request)
    direction = payload.get('direction')
    if direction not in ('up', 'down', None):
        return JsonResponse({"erro": "direction deve ser 'up', 'down' ou null"}, status=400)
    return JsonResponse({"ok": True, "comment_id": comment_id, "direction": direction})


@csrf_exempt
@require_POST
def create_post(request):
    payload = json_body(request)
    required = ['community_slug', 'title', 'post_type']
    missing = [k for k in required if not payload.get(k)]
    if missing:
        return JsonResponse({"erro": f"campos faltando: {', '.join(missing)}"}, status=400)
    if not get_community(payload['community_slug']):
        return JsonResponse({"erro": "comunidade inválida"}, status=404)
    return JsonResponse({"ok": True, "post": {"community_slug": payload['community_slug'], "title": payload['title'], "post_type": payload['post_type'], "body": payload.get('body', ''), "url": payload.get('url', '')}}, status=201)


@csrf_exempt
@require_POST
def create_comment(request):
    payload = json_body(request)
    if not payload.get('post_id') or not payload.get('body'):
        return JsonResponse({"erro": "post_id e body são obrigatórios"}, status=400)
    if not get_post(payload['post_id']):
        return JsonResponse({"erro": "post não encontrado"}, status=404)
    return JsonResponse({"ok": True, "comment": {"post_id": payload['post_id'], "body": payload['body'], "parent_id": payload.get('parent_id')}}, status=201)


@csrf_exempt
@require_POST
def join_community(request, slug):
    if not get_community(slug):
        return JsonResponse({"erro": "comunidade não encontrada"}, status=404)
    payload = json_body(request)
    joined = bool(payload.get('joined', True))
    return JsonResponse({"ok": True, "slug": slug, "joined": joined})


@csrf_exempt
@require_POST
def follow_user(request, handle):
    if handle not in USERS:
        return JsonResponse({"erro": "usuário não encontrado"}, status=404)
    payload = json_body(request)
    following = bool(payload.get('following', True))
    return JsonResponse({"ok": True, "handle": handle, "following": following})


@csrf_exempt
@require_POST
def fork_framework(request, framework_id):
    fw = get_framework(framework_id)
    if not fw:
        return JsonResponse({"erro": "framework não encontrado"}, status=404)
    payload = json_body(request)
    fork_name = payload.get('name', f"{fw['title']} (meu fork)")
    return JsonResponse({"ok": True, "fork": {"framework_id": framework_id, "name": fork_name, "owner": "gabriel"}}, status=201)


@csrf_exempt
@require_POST
def review_framework(request, framework_id):
    fw = get_framework(framework_id)
    if not fw:
        return JsonResponse({"erro": "framework não encontrado"}, status=404)
    payload = json_body(request)
    rating = payload.get('rating')
    text = (payload.get('text') or '').strip()
    if not isinstance(rating, int) or rating < 1 or rating > 5:
        return JsonResponse({"erro": "rating deve ser inteiro entre 1 e 5"}, status=400)
    if not text:
        return JsonResponse({"erro": "review precisa de texto"}, status=400)
    return JsonResponse({"ok": True, "review": {"framework_id": framework_id, "rating": rating, "text": text}}, status=201)


@csrf_exempt
@require_POST
def share_to_guild(request):
    payload = json_body(request)
    source_type = payload.get('source_type')
    source_id = payload.get('source_id')
    community_slug = payload.get('community_slug', 'gestao-pessoas')
    if not source_type or not source_id:
        return JsonResponse({"erro": "source_type e source_id são obrigatórios"}, status=400)
    if not get_community(community_slug):
        return JsonResponse({"erro": "comunidade inválida"}, status=404)
    return JsonResponse({"ok": True, "shared": {"source_type": source_type, "source_id": source_id, "community_slug": community_slug}}, status=201)


@csrf_exempt
@require_POST
def toggle_note_public(request, note_id):
    note = next((n for n in my_brain_notes if n["id"] == note_id), None)
    if not note:
        return JsonResponse({"erro": "nota não encontrada"}, status=404)
    payload = json_body(request)
    is_public = bool(payload.get('is_public', not note.get("is_public")))
    note["is_public"] = is_public
    return JsonResponse({"ok": True, "note_id": note_id, "is_public": is_public})


@require_GET
def list_notifications(request):
    return JsonResponse({
        "notifications": NOTIFICATIONS,
        "unread_count": sum(1 for n in NOTIFICATIONS if not n.get("is_read")),
    })


@csrf_exempt
@require_POST
def read_notification(request, notif_id):
    notif = next((n for n in NOTIFICATIONS if n["id"] == notif_id), None)
    if not notif:
        return JsonResponse({"erro": "notificação não encontrada"}, status=404)
    notif["is_read"] = True
    return JsonResponse({"ok": True, "id": notif_id})


@csrf_exempt
@require_POST
def read_all_notifications(request):
    for n in NOTIFICATIONS:
        n["is_read"] = True
    return JsonResponse({"ok": True, "marked": len(NOTIFICATIONS)})


@csrf_exempt
@require_POST
def quick_note(request):
    payload = json_body(request)
    note = {
        "title": payload.get("title", "Nota rápida"),
        "content": payload.get("content", ""),
        "source": payload.get("source", ""),
    }
    return JsonResponse({"ok": True, "note": note}, status=201)
