from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def is_professor(user):
    if not user.is_authenticated:
        return False
    if user.is_superuser or user.is_staff:
        return True
    if user.groups.filter(name__iexact='professores').exists():
        return True
    perfil = getattr(user, 'perfil', None)
    cargo = (getattr(perfil, 'cargo', '') or '').lower()
    return 'professor' in cargo or 'mentor' in cargo


def professor_required(view_func):
    @login_required(login_url='/login')
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not is_professor(request.user):
            messages.error(request, 'Acesso restrito a professores.')
            return redirect('/')
        return view_func(request, *args, **kwargs)

    return wrapper
