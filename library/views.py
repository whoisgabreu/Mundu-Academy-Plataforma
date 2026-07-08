from django.shortcuts import get_object_or_404
from core.utils import render
from .models import Summary, Framework, FrameworkReview


def library_list(request):
    summaries = Summary.objects.all()
    frameworks = Framework.objects.all()
    return render(request, "library.html", {
        "summaries": summaries,
        "frameworks": frameworks,
    })


def framework_detail(request, slug):
    framework = get_object_or_404(Framework, slug=slug)

    reviews = framework.reviews.all()
    for review in reviews:
        review.author_user = {
            "handle": review.author_handle,
            "nome_completo": review.author_handle.replace("-", " ").title(),
            "iniciais": "".join(w[0].upper() for w in review.author_handle.split("-")[:2]),
            "role": "Membro Mundu",
        }

    related = Framework.objects.filter(color=framework.color).exclude(pk=framework.pk)[:3]

    return render(request, "framework.html", {
        "framework": framework,
        "editor": {
            "handle": framework.last_editor_handle,
            "nome_completo": framework.last_editor_handle.replace("-", " ").title(),
            "iniciais": "".join(w[0].upper() for w in framework.last_editor_handle.split("-")[:2]),
            "role": "Membro Mundu",
        },
        "reviews": reviews,
        "related_frameworks": related,
    })
