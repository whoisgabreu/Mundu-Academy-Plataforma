from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from core.utils import render
from cursos.models import Aula, Modulo, Quiz, TentativaQuiz


@login_required(login_url='/login')
def player_aula(request, modulo_slug, ordem):
    modulo = get_object_or_404(Modulo, slug=modulo_slug)
    aula = get_object_or_404(Aula.objects.select_related('modulo'), modulo=modulo, ordem=ordem)
    aulas_modulo = Aula.objects.filter(
        modulo=aula.modulo
    ).order_by('ordem')
    quiz = Quiz.objects.filter(aula=aula).first() or Quiz.objects.filter(modulo=aula.modulo).first()
    quiz_feito = False
    if quiz:
        quiz_feito = TentativaQuiz.objects.filter(
            usuario=request.user, quiz=quiz, aprovado=True
        ).exists()
    return render(request, 'streaming/player.html', {
        'aula': aula,
        'aulas_modulo': aulas_modulo,
        'quiz': quiz,
        'quiz_feito': quiz_feito,
    })
