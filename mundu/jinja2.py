from django.templatetags.static import static
from django.urls import reverse
from django.middleware.csrf import get_token
from markupsafe import Markup
from jinja2 import Environment
from embed_video.backends import detect_backend, UnknownBackendException


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
                'cargo': perfil.cargo,
                'empresa': perfil.empresa,
                'bio': perfil.bio,
                'foto': perfil.foto,
                'banner': perfil.banner,
                'localizacao': perfil.localizacao,
                'cidade': perfil.cidade,
                'linkedin': perfil.linkedin,
                'instagram': perfil.instagram,
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
        else:
            current_user = {
                'nome': request.user.get_full_name() or request.user.username,
                'nome_completo': request.user.get_full_name() or request.user.username,
                'username': request.user.username,
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
                    'nivel': 1,
                    'nome_nivel': 'Iniciante',
                    'xp_total': 0,
                    'xp_proximo_nivel': 500,
                    'xp_percentual': 0,
                    'moedas': 0,
                    'titulo_ativo': 'Iniciante',
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
                'nivel': 0,
                'nome_nivel': 'Iniciante',
                'xp_total': 0,
                'xp_proximo_nivel': 500,
                'xp_percentual': 0,
                'moedas': 0,
                'titulo_ativo': 'Iniciante',
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


def get_embed_video(url):
    if not url:
        return None
    try:
        return detect_backend(url)
    except (UnknownBackendException, TypeError):
        return None


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'url_for': url_for,
        'csrf_input': csrf_input,
        'inject_globals': inject_globals,
        'get_embed_video': get_embed_video,
    })
    return env
