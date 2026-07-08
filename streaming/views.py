from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from core.utils import render
from cursos.models import Aula, Modulo


@login_required(login_url='/login')
def player_aula(request, modulo_slug, ordem):
    modulo = get_object_or_404(Modulo, slug=modulo_slug)
    aula = get_object_or_404(Aula.objects.select_related('modulo'), modulo=modulo, ordem=ordem)
    aulas_modulo = Aula.objects.filter(
        modulo=aula.modulo
    ).order_by('ordem')
    return render(request, 'streaming/player.html', {
        'aula': aula,
        'aulas_modulo': aulas_modulo,
    })
