from django.http import JsonResponse
from .models import Curso


def status(request):
    return JsonResponse({
        'status': 'Online',
        'mensagem': 'Backend Django e PostgreSQL configurados!'
    })


def get_cursos(request):
    try:
        cursos = Curso.objects.all()
        data = [
            {
                'id': c.id,
                'titulo': c.titulo,
                'instrutor': c.instrutor,
                'progresso': c.progresso,
            }
            for c in cursos
        ]
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)
