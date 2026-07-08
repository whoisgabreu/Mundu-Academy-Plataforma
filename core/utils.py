from django.shortcuts import render as django_render


def _get_current_user(request):
    if request.user.is_authenticated:
        perfil = getattr(request.user, 'perfil', None)
        if perfil:
            return {
                'nome': request.user.get_full_name() or request.user.username,
                'nome_completo': request.user.get_full_name() or request.user.username,
                'username': request.user.username,
                'email': request.user.email,
                'role': perfil.role,
                'cargo': perfil.cargo,
                'empresa': perfil.empresa,
                'bio': perfil.bio,
                'localizacao': perfil.localizacao,
                'linkedin': perfil.linkedin,
                'instagram': perfil.instagram,
                'joined_at': perfil.data_criacao,
                'perfil': {
                    'nivel': perfil.nivel,
                    'nome_nivel': perfil.nome_nivel,
                    'xp_total': perfil.xp_total,
                    'xp_proximo_nivel': perfil.xp_proximo_nivel,
                    'xp_percentual': perfil.xp_percentual,
                    'streak': perfil.streak_dias,
                    'streak_dias': perfil.streak_dias,
                    'iniciais': perfil.iniciais,
                    'pilar_favorito': 'Cursos',
                },
            }
        return {
            'nome': request.user.get_full_name() or request.user.username,
            'nome_completo': request.user.get_full_name() or request.user.username,
            'username': request.user.username,
            'email': request.user.email,
            'role': 'Membro Mundu',
            'cargo': '',
            'empresa': '',
            'bio': '',
            'localizacao': '',
            'linkedin': '',
            'instagram': '',
            'perfil': {
                'nivel': 1, 'nome_nivel': 'Iniciante', 'xp_total': 0,
                'xp_proximo_nivel': 500, 'xp_percentual': 0, 'streak': 0,
                'streak_dias': 0,
                'iniciais': (request.user.get_full_name() or request.user.username)[:2].upper(),
                'pilar_favorito': 'Cursos',
            },
        }
    return {
        'nome': 'Visitante', 'nome_completo': 'Visitante',
        'username': 'visitante',
        'role': 'Visitante',
        'cargo': '', 'empresa': '', 'bio': '', 'localizacao': '',
        'linkedin': '', 'instagram': '',
        'perfil': {
            'nivel': 0, 'nome_nivel': 'Iniciante', 'xp_total': 0,
            'xp_proximo_nivel': 500, 'xp_percentual': 0, 'streak': 0,
            'streak_dias': 0, 'iniciais': 'VI', 'pilar_favorito': 'Cursos',
        },
    }


def _get_notifications():
    from social.models import Notification
    from django.contrib.auth.models import User
    user = getattr(Notification, '_request_user', None)
    if user is None:
        return []
    enriched = []
    for n in Notification.objects.filter(usuario=user)[:20]:
        actor = None
        if n.tipo in ('follow', 'reply', 'mention', 'community'):
            try:
                u = User.objects.get(username=n.mensagem.split()[-1] if n.mensagem else '')
                p = u.perfil
                actor = {
                    'handle': u.username,
                    'iniciais': p.iniciais,
                    'nome_completo': u.get_full_name() or u.username,
                }
            except (User.DoesNotExist, IndexError):
                pass
        enriched.append({
            'id': str(n.id),
            'type': n.tipo,
            'actor_handle': n.mensagem.split()[-1] if n.mensagem else '',
            'actor': actor,
            'verb': n.tipo,
            'target_title': n.mensagem,
            'target_url': n.link,
            'snippet': None,
            'time_ago': _time_ago(n.created_at) if n.created_at else '',
            'is_read': n.lida,
        })
    return enriched


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


def render(request, template, context=None, **kwargs):
    if context is None:
        context = {}
    context.setdefault('current_user', _get_current_user(request))
    ctx_user = context.get('current_user', {})
    if ctx_user.get('username') and ctx_user['username'] != 'visitante':
        from social.models import Notification
        notif_qs = Notification.objects.filter(usuario__username=ctx_user['username'])
        notifs = []
        for n in notif_qs[:20]:
            actor = None
            if n.tipo in ('follow', 'reply', 'mention', 'community'):
                from django.contrib.auth.models import User
                try:
                    actor_handle = n.mensagem.split()[-1] if n.mensagem else ''
                    u = User.objects.get(username=actor_handle)
                    p = u.perfil
                    actor = {
                        'handle': u.username,
                        'iniciais': p.iniciais,
                        'nome_completo': u.get_full_name() or u.username,
                    }
                except (User.DoesNotExist, IndexError):
                    pass
            notifs.append({
                'id': str(n.id),
                'type': n.tipo,
                'actor_handle': n.mensagem.split()[-1] if n.mensagem else '',
                'actor': actor,
                'verb': n.tipo,
                'target_title': n.mensagem,
                'target_url': n.link,
                'snippet': None,
                'time_ago': _time_ago(n.created_at) if n.created_at else '',
                'is_read': n.lida,
            })
        context.setdefault('notifications', notifs)
        context.setdefault('unread_count', sum(1 for n in notifs if not n.get('is_read')))
    else:
        context.setdefault('notifications', [])
        context.setdefault('unread_count', 0)
    context.setdefault('request', request)
    return django_render(request, template, context, **kwargs)
