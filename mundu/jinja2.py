from django.templatetags.static import static
from django.urls import reverse
from django.middleware.csrf import get_token
from markupsafe import Markup
from jinja2 import Environment


def url_for(endpoint, **kwargs):
    if endpoint == 'static':
        return static(kwargs.get('filename', ''))
    return reverse(endpoint, kwargs=kwargs)


def csrf_input(request):
    token = get_token(request)
    return Markup(f'<input type="hidden" name="csrfmiddlewaretoken" value="{token}">')


def inject_globals(request):
    current_user = None
    if request.user.is_authenticated:
        perfil = getattr(request.user, 'perfil', None)
        if perfil:
            current_user = {
                'nome': request.user.get_full_name() or request.user.username,
                'nome_completo': request.user.get_full_name() or request.user.username,
                'username': request.user.username,
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
        else:
            current_user = {
                'nome': request.user.get_full_name() or request.user.username,
                'nome_completo': request.user.get_full_name() or request.user.username,
                'username': request.user.username,
                'perfil': {
                    'nivel': 1,
                    'nome_nivel': 'Iniciante',
                    'xp_total': 0,
                    'xp_proximo_nivel': 500,
                    'xp_percentual': 0,
                    'streak': 0,
                    'streak_dias': 0,
                    'iniciais': (request.user.get_full_name() or request.user.username)[:2].upper(),
                    'pilar_favorito': 'Cursos',
                },
            }
    else:
        current_user = {
            'nome': 'Visitante',
            'nome_completo': 'Visitante',
            'username': 'visitante',
            'perfil': {
                'nivel': 0,
                'nome_nivel': 'Iniciante',
                'xp_total': 0,
                'xp_proximo_nivel': 500,
                'xp_percentual': 0,
                'streak': 0,
                'streak_dias': 0,
                'iniciais': 'VI',
                'pilar_favorito': 'Cursos',
            },
        }

    notifications = []
    unread_count = 0

    return {
        'current_user': current_user,
        'notifications': notifications,
        'unread_count': unread_count,
    }


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'url_for': url_for,
        'csrf_input': csrf_input,
        'inject_globals': inject_globals,
    })
    return env
