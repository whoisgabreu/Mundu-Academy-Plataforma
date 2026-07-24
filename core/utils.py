from datetime import date, datetime, time

from django.shortcuts import render as django_render
from django.utils import timezone
from django.utils.dateparse import parse_date, parse_datetime


def coerce_datetime(value):
    if not value:
        return None
    if isinstance(value, datetime):
        dt = value
    elif isinstance(value, date):
        dt = datetime.combine(value, time.min)
    elif isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        dt = parse_datetime(text)
        if dt is None:
            parsed_date = parse_date(text)
            dt = datetime.combine(parsed_date, time.min) if parsed_date else None
        if dt is None:
            return None
    else:
        return None

    if timezone.is_naive(dt):
        return timezone.make_aware(dt, timezone.get_current_timezone())
    return dt


def human_time_ago(value):
    raw_value = value.strip() if isinstance(value, str) else ''
    dt = coerce_datetime(value)
    if dt is None:
        return raw_value or 'recentemente'

    seconds = int((timezone.now() - dt).total_seconds())
    if seconds < 60:
        return 'agora'
    if seconds < 3600:
        return f'há {seconds // 60}min'
    if seconds < 86400:
        return f'há {seconds // 3600}h'
    days = seconds // 86400
    if days == 1:
        return 'ontem'
    return f'há {days} dias'


def time_sort_value(value):
    dt = coerce_datetime(value)
    return dt.timestamp() if dt else 0


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
                'foto': perfil.foto,
                'banner': perfil.banner,
                'localizacao': perfil.localizacao,
                'cidade': perfil.cidade,
                'linkedin': perfil.linkedin,
                'instagram': perfil.instagram,
                'joined_at': perfil.data_criacao,
                'perfil': {
                    'nivel': perfil.nivel,
                    'nome_nivel': perfil.nome_nivel,
                    'xp_total': perfil.xp_total,
                    'xp_proximo_nivel': perfil.xp_proximo_nivel,
                    'xp_percentual': perfil.xp_percentual,
                    'moedas': perfil.moedas,
                    'titulo_ativo': perfil.titulo_ativo.nome if perfil.titulo_ativo else perfil.nome_nivel,
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
            'foto': '',
            'banner': '',
            'localizacao': '',
            'cidade': '',
            'linkedin': '',
            'instagram': '',
            'perfil': {
                'nivel': 1, 'nome_nivel': 'Iniciante', 'xp_total': 0,
                'xp_proximo_nivel': 500, 'xp_percentual': 0, 'moedas': 0,
                'titulo_ativo': 'Iniciante', 'streak': 0,
                'streak_dias': 0,
                'iniciais': (request.user.get_full_name() or request.user.username)[:2].upper(),
                'pilar_favorito': 'Cursos',
            },
        }
    return {
        'nome': 'Visitante', 'nome_completo': 'Visitante',
        'username': 'visitante',
        'role': 'Visitante',
        'cargo': '', 'empresa': '', 'bio': '', 'foto': '', 'banner': '', 'localizacao': '', 'cidade': '',
        'linkedin': '', 'instagram': '',
        'perfil': {
            'nivel': 0, 'nome_nivel': 'Iniciante', 'xp_total': 0,
            'xp_proximo_nivel': 500, 'xp_percentual': 0, 'moedas': 0,
            'titulo_ativo': 'Iniciante', 'streak': 0,
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
    return human_time_ago(dt)


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
