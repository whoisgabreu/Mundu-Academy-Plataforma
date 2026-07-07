from django.shortcuts import render as django_render


NOTIFICATIONS = [
    {"id": "no1", "type": "reply", "actor_handle": "diego-almeida", "verb": "respondeu seu comentário em", "target_title": "Como vocês conduzem 1:1 com alguém que não confia em você ainda?", "target_url": "/g/gestao-pessoas/post/1-1-com-alguem-que-nao-confia", "snippet": "3 meses é a média que eu vejo na coachada.", "time_ago": "há 12min", "is_read": False},
    {"id": "no2", "type": "follow", "actor_handle": "camila-faria", "verb": "começou a seguir você", "target_title": None, "target_url": "/u/camila-faria", "snippet": None, "time_ago": "há 2h", "is_read": False},
    {"id": "no3", "type": "mention", "actor_handle": "mariana-reis", "verb": "mencionou você em", "target_title": "Stand-up de 9 min funciona pra time de 12?", "target_url": "/g/tech-produto/post/standup-9min-time-de-12", "snippet": "@gabriel já tinha falado disso no comentário do video da semana passada...", "time_ago": "há 5h", "is_read": False},
    {"id": "no4", "type": "upvote", "actor_handle": None, "verb": "47 pessoas curtiram seu comentário em", "target_title": "Como vocês conduzem 1:1...", "target_url": "/g/gestao-pessoas/post/1-1-com-alguem-que-nao-confia", "snippet": None, "time_ago": "ontem", "is_read": True, "count": 47},
    {"id": "no5", "type": "community", "actor_handle": "bruno-tavares", "verb": "publicou em r/carreira-inicial", "target_title": "Aplicando o framework WRAP para escolher entre 2 ofertas", "target_url": "/g/carreira-inicial/post/wrap-em-2-ofertas-funcionou", "snippet": None, "time_ago": "ontem", "is_read": True},
    {"id": "no6", "type": "follow", "actor_handle": "lucas-pestana", "verb": "começou a seguir você", "target_title": None, "target_url": "/u/lucas-pestana", "snippet": None, "time_ago": "2 dias atrás", "is_read": True},
]

_USERS = {
    "gabriel": {"handle": "gabriel", "nome_completo": "Gabriel Lasaro", "iniciais": "GL"},
    "camila-faria": {"handle": "camila-faria", "nome_completo": "Camila Faria", "iniciais": "CF"},
    "mariana-reis": {"handle": "mariana-reis", "nome_completo": "Mariana Reis", "iniciais": "MR"},
    "diego-almeida": {"handle": "diego-almeida", "nome_completo": "Diego Almeida", "iniciais": "DA"},
    "bruno-tavares": {"handle": "bruno-tavares", "nome_completo": "Bruno Tavares", "iniciais": "BT"},
    "lucas-pestana": {"handle": "lucas-pestana", "nome_completo": "Lucas Pestana", "iniciais": "LP"},
}


def _get_user(handle):
    return _USERS.get(handle, {
        "handle": handle,
        "nome_completo": handle.replace("-", " ").title(),
        "iniciais": (handle[:2] if handle else "?").upper(),
    })


def _get_current_user(request):
    if request.user.is_authenticated:
        perfil = getattr(request.user, 'perfil', None)
        if perfil:
            return {
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
        return {
            'nome': request.user.get_full_name() or request.user.username,
            'nome_completo': request.user.get_full_name() or request.user.username,
            'username': request.user.username,
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
        'perfil': {
            'nivel': 0, 'nome_nivel': 'Iniciante', 'xp_total': 0,
            'xp_proximo_nivel': 500, 'xp_percentual': 0, 'streak': 0,
            'streak_dias': 0, 'iniciais': 'VI', 'pilar_favorito': 'Cursos',
        },
    }


def _get_notifications():
    enriched = []
    for n in NOTIFICATIONS:
        enriched.append({
            **n,
            "actor": _get_user(n["actor_handle"]) if n.get("actor_handle") else None,
        })
    return enriched


def render(request, template, context=None, **kwargs):
    if context is None:
        context = {}
    context.setdefault('current_user', _get_current_user(request))
    context.setdefault('notifications', _get_notifications())
    context.setdefault('unread_count', sum(1 for n in NOTIFICATIONS if not n.get("is_read")))
    context.setdefault('request', request)
    return django_render(request, template, context, **kwargs)
