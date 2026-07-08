from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Count
from core.utils import render
from cursos.models import Modulo, Trilha, TrilhaModulo, Desafio, ProgressoModulo, ProgressoDesafio
from guild.models import Community, Thread, Comment


def _time_ago(dt):
    from django.utils import timezone
    now = timezone.now()
    diff = now - dt
    if diff.days == 0:
        mins = diff.seconds // 60
        if mins < 1:
            return 'agora'
        if mins < 60:
            return f'há {mins}min'
        hours = mins // 60
        return f'há {hours}h' if hours < 24 else 'ontem'
    if diff.days == 1:
        return 'ontem'
    return f'há {diff.days} dias'


def resolve_user(handle):
    try:
        u = User.objects.get(username=handle)
        p = u.perfil
        return {
            'handle': u.username,
            'nome_completo': u.get_full_name() or u.username,
            'iniciais': p.iniciais,
            'role': p.role,
            'karma': p.karma,
            'bio': p.bio,
        }
    except User.DoesNotExist:
        return {
            'handle': handle,
            'nome_completo': handle.replace('-', ' ').title(),
            'iniciais': handle[:2].upper(),
            'role': 'Membro Mundu',
            'karma': 0,
            'bio': '',
        }


# ============ EXPLORAR ============



def get_trending_topics(limit=5):
    qs = Thread.objects.exclude(tag='').values('tag').annotate(
        posts=Count('id')
    ).order_by('-posts')[:limit]
    return [{"label": t['tag'], "posts": t['posts'], "trend": f"+{t['posts']}"} for t in qs]


def get_who_to_follow(limit=3):
    from usuarios.models import Perfil
    qs = Perfil.objects.exclude(usuario__username='gabriel').order_by('-karma')[:limit]
    return [{
        'handle': p.usuario.username,
        'nome_completo': p.usuario.get_full_name() or p.usuario.username,
        'iniciais': p.iniciais,
        'role': p.role,
        'karma': p.karma,
        'bio': p.bio,
    } for p in qs]


def build_unified_feed(sort="for-you"):
    items = []
    threads = Thread.objects.select_related('community').annotate(reply_count=Count('comments')).order_by('-created_at')[:10]
    for t in threads:
        author = resolve_user(t.author_handle)
        payload = {
            'id': t.id, 'slug': t.slug, 'title': t.title,
            'author': t.author_handle, 'community_slug': t.community.slug,
            'community': t.community.name, 'time_ago': _time_ago(t.created_at),
            'replies': t.reply_count, 'upvotes': t.upvotes, 'tag': t.tag,
            'post_type': t.post_type, 'preview': t.preview, 'body': t.body,
            'url': t.url,
        }
        items.append({
            "kind": "thread", "id": str(t.id), "actor": author, "actor_handle": t.author_handle,
            "verb": "postou em r/" + t.community.slug,
            "time_ago": _time_ago(t.created_at), "_sort": t.created_at.timestamp(),
            "engagement": {"upvotes": t.upvotes, "comments": t.reply_count},
            "payload": payload,
        })
    from brain.models import BrainNote
    public_notes = BrainNote.objects.filter(is_public=True).order_by('-likes')[:5]
    for pn in public_notes:
        author = resolve_user(pn.user.username)
        items.append({
            "kind": "public_note", "id": str(pn.id), "actor": author, "actor_handle": pn.user.username,
            "verb": "compartilhou uma nota",
            "time_ago": _time_ago(pn.date) if hasattr(pn, 'date') else 'recentemente',
            "_sort": pn.likes * 2 + pn.comments_count,
            "engagement": {"likes": pn.likes, "comments": pn.comments_count, "saves": 0},
            "payload": {
                'id': str(pn.id), 'title': pn.title, 'author_handle': pn.user.username,
                'body': pn.content, 'source_label': pn.source,
                'likes': pn.likes, 'comments': pn.comments_count, 'saves': 0,
                'time_ago': _time_ago(pn.date) if hasattr(pn, 'date') else 'recentemente',
                'tags': pn.tags,
            },
        })
    if sort == "following":
        items = [it for it in items if it["actor_handle"] != "mundu"]
    elif sort == "community":
        items = [it for it in items if it["kind"] == "thread"]
    elif sort == "popular":
        items.sort(key=lambda it: (
            it["engagement"].get("likes", 0) + it["engagement"].get("upvotes", 0) +
            it["engagement"].get("comments", 0) * 3 + it["engagement"].get("saves", 0) * 2
        ), reverse=True)
        return items
    items.sort(key=lambda it: it["_sort"], reverse=True)
    return items


# ============ VIEWS ============

def index(request):
    sort = request.GET.get('sort', 'for-you')
    if sort not in ('for-you', 'following', 'popular', 'community'):
        sort = 'for-you'
    feed = build_unified_feed(sort=sort)
    topics = get_trending_topics(5)
    if not topics:
        topics = []
    from social.models import Follow
    followed_count = 0
    if request.user.is_authenticated:
        followed_count = Follow.objects.filter(seguidor=request.user).count()
    return render(request, 'index.html', {
        'feed': feed,
        'sort': sort,
        'trending_topics': topics,
        'who_to_follow': get_who_to_follow(3),
        'followed_count': followed_count,
    })


def explorar(request):
    guild_threads_qs = Thread.objects.select_related('community').annotate(
        reply_count=Count('comments')
    ).order_by('-upvotes')[:3]
    guild_hot = []
    for t in guild_threads_qs:
        guild_hot.append({
            'id': str(t.id), 'slug': t.slug, 'title': t.title,
            'author': t.author_handle, 'community_slug': t.community.slug,
            'community': t.community.name, 'time_ago': _time_ago(t.created_at),
            'replies': t.reply_count, 'upvotes': t.upvotes, 'tag': t.tag,
            'post_type': t.post_type, 'preview': t.preview,
        })

    from library.models import Framework
    frameworks_top = Framework.objects.all()[:6]

    # Continue watching — módulos em progresso
    continue_watching = []
    if request.user.is_authenticated:
        pms = ProgressoModulo.objects.filter(
            usuario=request.user, progresso__gt=0, progresso__lt=100
        ).select_related('modulo')[:3]
        for pm in pms:
            m = pm.modulo
            continue_watching.append({
                'id': str(m.id), 'title': m.titulo,
                'subtitle': f'{m.nivel} • Módulo',
                'thumbnail': m.thumbnail,
                'duration': m.duracao_total or '—',
                'xp': m.xp_total, 'progress': pm.progresso, 'type': 'course',
            })

    # Challenges — from Desafio model
    from cursos.models import Desafio, ProgressoDesafio, FeaturedContent
    prog_map = {}
    if request.user.is_authenticated:
        for pd in ProgressoDesafio.objects.filter(usuario=request.user):
            prog_map[pd.desafio_id] = pd.progresso
    challenges = []
    for d in Desafio.objects.filter(ativo=True)[:2]:
        prog = prog_map.get(d.id, 0)
        label = {'daily': 'Diário', 'weekly': 'Semanal', 'special': 'Especial'}.get(d.tipo, 'Desafio')
        challenges.append({
            'type': d.tipo, 'label': label,
            'title': d.titulo, 'description': d.descricao,
            'xp': d.xp, 'progress': prog,
            'progress_text': f'{prog} de {d.meta} concluído' if d.meta > 1 else ('Concluído' if prog >= d.meta else 'Não iniciado'),
        })

    # Featured content from DB
    def _fc_dict(qs):
        return [{
            'id': str(fc.id),
            'title': fc.titulo,
            'subtitle': fc.subtitulo,
            'thumbnail': fc.thumbnail,
            'duration': fc.duracao,
            'xp': fc.xp,
            'type': fc.tipo,
            'badge': fc.badge,
            'participants': fc.participantes,
        } for fc in qs]

    recommended_qs = FeaturedContent.objects.filter(ativo=True, tipo='recommended').order_by('ordem')
    collabs_qs = FeaturedContent.objects.filter(ativo=True, tipo='collab').order_by('ordem')
    cases_qs = FeaturedContent.objects.filter(ativo=True, tipo='case').order_by('ordem')

    return render(request, 'explorar.html', {
        'continue_watching': continue_watching,
        'recommended': _fc_dict(recommended_qs),
        'collabs': _fc_dict(collabs_qs),
        'cases': _fc_dict(cases_qs),
        'challenges': challenges,
        'library_frameworks_top': frameworks_top,
        'library_reads': [],
        'guild_hot': guild_hot,
    })


@login_required(login_url='/login')
def perfil(request):
    from cursos.models import Certificate, ProgressoModulo, ProgressoDesafio, Desafio
    from social.models import Follow
    from django.db.models import Count, Sum, F, Q

    user = request.user
    perfil = user.perfil

    # Stats
    cert_count = Certificate.objects.filter(usuario=user).count()
    desafios_vencidos = ProgressoDesafio.objects.filter(
        usuario=user, progresso__gte=F('desafio__meta')
    ).count()
    conexoes = Follow.objects.filter(seguidor=user).count()

    stats = [
        {'label': 'XP Total', 'value': f"{perfil.xp_total:,}".replace(',', '.'), 'icon': 'zap', 'color': 'text-yellow-400', 'bg': 'bg-yellow-400/10'},
        {'label': 'Cursos Concluídos', 'value': str(cert_count), 'icon': 'book-open', 'color': 'text-blue-400', 'bg': 'bg-blue-400/10'},
        {'label': 'Desafios Vencidos', 'value': str(desafios_vencidos), 'icon': 'trophy', 'color': 'text-amber-400', 'bg': 'bg-amber-400/10'},
        {'label': 'Conexões', 'value': str(conexoes), 'icon': 'users', 'color': 'text-purple-400', 'bg': 'bg-purple-400/10'},
    ]

    # Trilhas em Progresso
    progressos_mod = ProgressoModulo.objects.filter(
        usuario=user, progresso__gt=0
    ).select_related('modulo')[:5]
    trilhas_progresso = []
    for pm in progressos_mod:
        trilhas_progresso.append({
            'titulo': pm.modulo.titulo,
            'progresso': pm.progresso,
            'duracao': pm.modulo.duracao_total or '—',
            'aulas_concluidas': round(pm.progresso / 100 * pm.modulo.total_aulas) if pm.modulo.total_aulas else 0,
            'total_aulas': pm.modulo.total_aulas,
        })

    # Networking — conexoes recentes
    recent_follows = Follow.objects.filter(seguidor=user).select_related('seguido__perfil')[:5]
    conexoes_recentes = []
    for f in recent_follows:
        p = f.seguido.perfil
        conexoes_recentes.append({
            'iniciais': p.iniciais,
            'nome': f.seguido.get_full_name() or f.seguido.username,
            'role': p.role,
            'handle': f.seguido.username,
        })

    # Sugestoes
    seguir_ids = Follow.objects.filter(seguidor=user).values_list('seguido_id', flat=True)
    from usuarios.models import Perfil
    sugestoes_qs = Perfil.objects.exclude(
        Q(usuario=user) | Q(usuario__id__in=list(seguir_ids) + [1])
    ).order_by('-karma')[:3]
    sugestoes = []
    for p in sugestoes_qs:
        sugestoes.append({
            'iniciais': p.iniciais,
            'nome': p.usuario.get_full_name() or p.usuario.username,
            'role': p.role or 'Membro Mundu',
            'handle': p.usuario.username,
        })

    # Certificados
    certs = Certificate.objects.filter(usuario=user).select_related('modulo', 'trilha')[:6]
    certificates = []
    for c in certs:
        nome = c.modulo.titulo if c.modulo else (c.trilha.titulo if c.trilha else 'Curso')
        emissor = 'MUNDU Academy'
        certificates.append({
            'title': nome,
            'issuer': emissor,
            'date': c.emitido_em.strftime('%b %Y') if c.emitido_em else '',
            'hours': 0,
        })

    # Progresso tab data
    total_hours = sum(
        (pm.progresso / 100) * (int(pm.modulo.duracao_total.split('h')[0]) if 'h' in pm.modulo.duracao_total else 0)
        for pm in ProgressoModulo.objects.filter(usuario=user).select_related('modulo')
    )

    # Achievements — from UserAchievement
    from usuarios.models import UserAchievement, Skill as SkillModel
    acs = UserAchievement.objects.filter(usuario=user).select_related('achievement')
    achievements = [{
        'icon': ua.achievement.icone,
        'title': ua.achievement.titulo,
        'color': ua.achievement.cor_gradiente,
    } for ua in acs]

    # Skills
    skill_levels = SkillModel.objects.filter(usuario=user).order_by('-nivel')[:6]
    SKILL_COLORS = [
        ('text-emerald-400', 'bg-emerald-400'),
        ('text-blue-400', 'bg-blue-400'),
        ('text-purple-400', 'bg-purple-400'),
        ('text-amber-400', 'bg-amber-400'),
        ('text-rose-400', 'bg-rose-400'),
        ('text-cyan-400', 'bg-cyan-400'),
    ]
    skills = []
    for i, s in enumerate(skill_levels):
        color, bg = SKILL_COLORS[i % len(SKILL_COLORS)]
        skills.append({
            'name': s.nome,
            'level': s.nivel,
            'color': color,
            'bg': bg,
            'icon': s.icone,
            'pct': f'{s.nivel}0%',
        })

    return render(request, 'perfil.html', {
        'stats': stats,
        'trilhas_progresso': trilhas_progresso,
        'achievements': achievements,
        'skills': skills,
        'certificates': certificates,
        'conexoes_recentes': conexoes_recentes,
        'sugestoes': sugestoes,
        'streak_dias': perfil.streak_dias,
        'total_hours': f'{int(total_hours)}h {int((total_hours % 1) * 60):02d}min' if total_hours else '0h',
        'joined_at': perfil.data_criacao.strftime('%b %Y') if perfil.data_criacao else 'Jan 2024',
        'cargo': perfil.cargo or 'Aprendiz',
    })


@login_required(login_url='/login')
def config(request):
    from usuarios.forms import PerfilModelForm
    from cursos.models import Certificate
    from social.models import Follow
    from usuarios.models import Perfil

    if request.method == 'POST':
        form = PerfilModelForm(request.POST, instance=request.user.perfil, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('/perfil')
    else:
        form = PerfilModelForm(instance=request.user.perfil, user=request.user)

    cert_count = Certificate.objects.filter(usuario=request.user).count()
    followers_count = Follow.objects.filter(seguido=request.user).count()

    total_perfis = Perfil.objects.count()
    user_rank = Perfil.objects.filter(xp_total__gt=request.user.perfil.xp_total).count() + 1
    top_percent = round(user_rank / max(total_perfis, 1) * 100)

    return render(request, 'config.html', {
        'form': form,
        'cert_count': cert_count,
        'followers_count': followers_count,
        'top_percent': top_percent,
    })


@login_required(login_url='/login')
def conteudos(request):
    modulos_db = Modulo.objects.prefetch_related('aulas').all()
    from cursos.models import Quiz
    quizzes = {q.modulo_id: q for q in Quiz.objects.all()}
    progressos = {p.modulo_id: p.progresso for p in ProgressoModulo.objects.filter(usuario=request.user)}
    modules = []
    for mod in modulos_db:
        prog = progressos.get(mod.id, 0)
        concluidas = int(mod.total_aulas * prog / 100)
        aulas = [
            {'id': a.id, 'titulo': a.titulo, 'duracao': a.duracao,
              'youtube_id': a.url_video, 'is_preview': a.is_preview,
              'ordem': a.ordem}
            for a in mod.aulas.all()
        ]
        quiz = quizzes.get(mod.id)
        modules.append({
            'id': str(mod.id), 'title': mod.titulo, 'description': mod.descricao,
            'slug': mod.slug,
            'thumbnail': mod.thumbnail, 'totalLessons': mod.total_aulas,
            'completedLessons': concluidas, 'progress': prog,
            'totalDuration': mod.duracao_total, 'xpTotal': mod.xp_total,
            'level': mod.nivel, 'certificate': mod.tem_certificado,
            'sections_count': mod.num_secoes,
            'aulas': aulas,
            'quiz': {'id': quiz.id, 'titulo': quiz.titulo, 'xp_total': quiz.xp_total} if quiz else None,
        })
    return render(request, 'conteudos.html', {'modules': modules})


@login_required(login_url='/login')
def trilhas(request):
    progressos = {p.modulo_id: p.progresso for p in ProgressoModulo.objects.filter(usuario=request.user)}
    trilhas_list = []
    for trilha in Trilha.objects.prefetch_related('trilhamodulo_set__modulo').all():
        tms = TrilhaModulo.objects.filter(trilha=trilha).order_by('ordem').select_related('modulo')
        modulos_proc = []
        for tm in tms:
            prog = progressos.get(tm.modulo_id, 0)
            modulos_proc.append({
                'id': f'm{tm.modulo_id}', 'title': tm.modulo.titulo,
                'duration': tm.modulo.duracao_total, 'xp': tm.modulo.xp_total,
                'completed': prog == 100, 'inProgress': 0 < prog < 100,
                'locked': tm.bloqueado, 'prerequisite': tm.prerequisito,
            })
        total = len(modulos_proc)
        concluidos = sum(1 for m in modulos_proc if m['completed'])
        progresso_trilha = int(concluidos / total * 100) if total else 0
        trilhas_list.append({
            'id': str(trilha.id), 'title': trilha.titulo, 'description': trilha.descricao,
            'thumbnail': trilha.thumbnail, 'area': trilha.area, 'level': trilha.nivel,
            'objective': trilha.objetivo, 'totalModules': total,
            'totalDuration': trilha.duracao_total, 'xpTotal': trilha.xp_total,
            'progress': progresso_trilha, 'hasCertificate': trilha.tem_certificado,
            'modules': modulos_proc,
        })
    return render(request, 'trilhas.html', {'trilhas': trilhas_list})


@login_required(login_url='/login')
@login_required(login_url='/login')
def desafios(request):
    prog_map = {p.desafio_id: p.progresso for p in ProgressoDesafio.objects.filter(usuario=request.user)}
    def _build(tipo):
        result = []
        for d in Desafio.objects.filter(tipo=tipo, ativo=True):
            prog = prog_map.get(d.id, 0)
            result.append({'titulo': d.titulo, 'desc': d.descricao, 'xp': d.xp, 'prog': prog, 'meta': d.meta, 'icon': d.icon, 'comp': prog >= d.meta})
        return result

    daily_list = _build('daily')
    weekly_list = _build('weekly')
    daily_done = sum(1 for d in daily_list if d['comp'])
    weekly_done = sum(1 for w in weekly_list if w['comp'])

    perfil = request.user.perfil
    streak_dias = perfil.streak_dias

    from usuarios.models import Achievement, UserAchievement
    user_ach = {ua.achievement_id for ua in UserAchievement.objects.filter(usuario=request.user).select_related('achievement')}
    all_achievements = Achievement.objects.all()
    conquistas = []
    for a in all_achievements:
        unlocked = a.id in user_ach
        conquistas.append({
            'titulo': a.titulo,
            'icon': a.icone,
            'cor_gradiente': a.cor_gradiente,
            'unlocked': unlocked,
        })
    total_achs = len(conquistas)
    unlocked_achs = sum(1 for c in conquistas if c['unlocked'])

    # Unlockables — from a simple model or static for now
    unlockables = [
        {'titulo': 'Avatar Mestre', 'desc': 'Avatar exclusivo', 'icon': 'gem', 'prog': 42, 'meta': 50, 'pct': 84},
        {'titulo': 'Tema Dark Gold', 'desc': 'Tema premium', 'icon': 'sparkles', 'prog': 12, 'meta': 30, 'pct': 40},
    ]

    return render(request, 'desafios.html', {
        'daily': daily_list,
        'weekly': weekly_list,
        'streak_dias': streak_dias,
        'daily_done': daily_done,
        'daily_total': len(daily_list),
        'weekly_done': weekly_done,
        'weekly_total': len(weekly_list),
        'conquistas': conquistas,
        'total_conquistas': total_achs,
        'unlocked_conquistas': unlocked_achs,
        'unlockables': unlockables,
    })


@login_required(login_url='/login')
def ao_vivo(request):
    from django.utils import timezone
    from live.models import LiveStream, LiveChatMessage, LivePoll

    live_now = LiveStream.objects.filter(ao_vivo=True).first()
    upcoming = LiveStream.objects.filter(
        ao_vivo=False, data_agendamento__gte=timezone.now()
    ).order_by('data_agendamento')[:10]
    replays = LiveStream.objects.filter(
        ao_vivo=False, data_fim__isnull=False
    ).order_by('-data_fim')[:10]

    chat_messages = []
    active_poll = None
    if live_now:
        chat_messages = LiveChatMessage.objects.filter(stream=live_now)[:50]
        active_poll = LivePoll.objects.filter(stream=live_now, ativa=True).first()

    return render(request, 'ao_vivo.html', {
        'live_now': live_now,
        'upcoming': upcoming,
        'replays': replays,
        'chat_messages': chat_messages,
        'active_poll': active_poll,
    })


@login_required(login_url='/login')
def insumos(request):
    from resources.models import Resource, ResourceCategory

    cats = ['Todos'] + [c.nome for c in ResourceCategory.objects.all()]
    qs = Resource.objects.select_related('categoria').all()
    insumos_list = []
    for r in qs:
        views = r.visualizacoes
        if views >= 1000:
            meta = f'{views//1000}k views'
        else:
            meta = f'{views} views'
        insumos_list.append({
            'id': str(r.id), 'title': r.titulo, 'desc': r.descricao,
            'meta': meta, 'author': r.autor, 'thumb': r.thumbnail,
            'new': r.novo, 'trend': r.em_alta, 'prem': r.premium,
            'fmt': r.formato,
        })
    return render(request, 'insumos.html', {
        'cats': cats,
        'insumos': insumos_list,
    })


@login_required(login_url='/login')
def networking(request):
    from social.models import Follow
    from django.contrib.auth.models import User

    # Posts — recent threads as networking posts
    threads_qs = Thread.objects.select_related('community').annotate(
        reply_count=Count('comments')
    ).order_by('-created_at')[:10]
    posts = []
    for t in threads_qs:
        author = resolve_user(t.author_handle)
        posts.append({
            'id': str(t.id),
            'name': author['nome_completo'],
            'user': f'@{t.author_handle}',
            'iniciais': author['iniciais'],
            'role': author['role'],
            'ver': author.get('karma', 0) > 5,
            'time': _time_ago(t.created_at),
            'content': t.body or t.title,
            'img': '',
            'likes': t.upvotes,
            'coms': t.reply_count,
            'reps': 0,
        })

    # Quem seguir
    sug = []
    if request.user.is_authenticated:
        seguir_ids = Follow.objects.filter(seguidor=request.user).values_list('seguido_id', flat=True)
        exclude_ids = list(seguir_ids) + [request.user.id]
    else:
        exclude_ids = [1]
    from usuarios.models import Perfil
    sug_qs = Perfil.objects.exclude(usuario__id__in=exclude_ids).order_by('-karma')[:3]
    for p in sug_qs:
        sug.append({
            'name': p.usuario.get_full_name() or p.usuario.username,
            'user': f'@{p.usuario.username}',
            'iniciais': p.iniciais,
            'bio': p.role or 'Membro Mundu',
        })

    # Trends — from Thread tags
    trends = []
    tag_counts = Thread.objects.exclude(tag='').values('tag').annotate(
        total=Count('id')
    ).order_by('-total')[:5]
    for tc in tag_counts:
        trends.append({
            'cat': tc['tag'].title(),
            'tags': f'#{tc["tag"].replace(" ", "")}',
            'posts': f'{tc["total"]} posts',
        })

    return render(request, 'networking.html', {
        'posts': posts,
        'sug': sug,
        'trends': trends,
    })


def user_profile(request, handle):
    try:
        u = User.objects.get(username=handle)
        p = u.perfil
    except User.DoesNotExist:
        return render(request, '404.html', {'resource': f"@{handle}"}, status=404)

    from social.models import Follow

    user = {
        'handle': u.username,
        'nome_completo': u.get_full_name() or u.username,
        'iniciais': p.iniciais,
        'role': p.role,
        'bio': p.bio,
        'karma': p.karma,
        'followers': Follow.objects.filter(seguido=u).count(),
        'following': Follow.objects.filter(seguidor=u).count(),
        'joined_at': p.data_criacao.strftime('%b %Y') if p.data_criacao else '',
        'is_self': request.user.is_authenticated and request.user.username == handle,
    }

    threads_qs = Thread.objects.filter(author_handle=handle).select_related('community').annotate(
        reply_count=Count('comments')
    )
    user_posts = []
    for t in threads_qs:
        user_posts.append({
            'slug': t.slug, 'title': t.title, 'community_slug': t.community.slug,
            'community_obj': t.community, 'tag': t.tag,
            'time_ago': _time_ago(t.created_at), 'upvotes': t.upvotes,
            'replies': t.reply_count, 'preview': t.preview,
            'author_user': resolve_user(handle),
        })

    user_comments_raw = Comment.objects.filter(author_handle=handle).select_related('thread__community')
    user_comments = []
    for c in user_comments_raw:
        user_comments.append({
            'id': c.id, 'body': c.body, 'upvotes': c.upvotes,
            'time_ago': _time_ago(c.created_at),
            'post': {
                'slug': c.thread.slug, 'title': c.thread.title,
                'community_slug': c.thread.community.slug,
            },
        })

    tab = request.GET.get('tab', 'posts')
    return render(request, 'profile.html', {
        'user': user, 'posts': user_posts, 'comments': user_comments,
        'tab': tab, 'is_self': user.get('is_self', False),
    })


@login_required(login_url='/login')
def quiz_view(request, quiz_id):
    from cursos.models import Quiz, Questao, Alternativa, TentativaQuiz
    quiz = get_object_or_404(Quiz.objects.prefetch_related('questoes__alternativas'), id=quiz_id)
    questoes = []
    for q in quiz.questoes.all():
        alt_list = [{'id': a.id, 'texto': a.texto, 'ordem': a.ordem} for a in q.alternativas.all()]
        questoes.append({
            'id': q.id, 'enunciado': q.enunciado, 'tipo': q.tipo, 'ordem': q.ordem,
            'alternativas': alt_list,
        })
    tentativa = TentativaQuiz.objects.filter(usuario=request.user, quiz=quiz).order_by('-concluido_em').first()
    return render(request, 'quiz.html', {
        'quiz': quiz,
        'questoes': questoes,
        'tentativa': tentativa,
    })


@login_required(login_url='/login')
def quiz_resultado(request, quiz_id):
    from cursos.models import Quiz, TentativaQuiz, Questao
    quiz = get_object_or_404(Quiz, id=quiz_id)
    tentativa = TentativaQuiz.objects.filter(usuario=request.user, quiz=quiz).order_by('-concluido_em').first()
    if not tentativa:
        return redirect('quiz_view', quiz_id=quiz_id)
    questoes_raw = Questao.objects.filter(quiz=quiz).prefetch_related('alternativas').order_by('ordem')
    primeira_tentativa = TentativaQuiz.objects.filter(usuario=request.user, quiz=quiz).count() == 1
    if primeira_tentativa and tentativa.total_questoes:
        xp_ganho = int(quiz.xp_total * tentativa.pontuacao / tentativa.total_questoes)
    else:
        xp_ganho = 0
    questoes = []
    for q in questoes_raw:
        respostas_json = tentativa.respostas or {}
        resposta_id = respostas_json.get(str(q.id))
        alt_correta = q.alternativas.filter(correta=True).first()
        questoes.append({
            'id': q.id,
            'enunciado': q.enunciado,
            'alternativas': [{'id': a.id, 'texto': a.texto, 'correta': a.correta} for a in q.alternativas.all()],
            'resposta_id': resposta_id,
            'correta_id': alt_correta.id if alt_correta else None,
            'acertou': resposta_id == getattr(alt_correta, 'id', None),
        })
    return render(request, 'quiz_resultado.html', {
        'tentativa': tentativa,
        'questoes': questoes,
        'xp_ganho': xp_ganho,
        'primeira_tentativa': primeira_tentativa,
    })
