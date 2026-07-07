from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from core.utils import render
from cursos.models import Aula


@login_required(login_url='/login')
def player_aula(request, aula_id):
    aula = get_object_or_404(Aula.objects.select_related('modulo'), id=aula_id)
    return render(request, 'streaming/player.html', {
        'aula': aula,
    })
