from django.utils import timezone
from django.contrib.auth.models import User


class StreakMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            perfil = request.user.perfil
            hoje = timezone.localdate()
            if perfil.ultimo_login != hoje:
                if perfil.ultimo_login == hoje - timezone.timedelta(days=1):
                    perfil.streak_dias += 1
                    perfil.adicionar_xp(10)
                elif perfil.ultimo_login is not None:
                    perfil.streak_dias = 0
                perfil.ultimo_login = hoje
                perfil.save(update_fields=['streak_dias', 'ultimo_login', 'xp_total', 'nivel'])
        return self.get_response(request)
