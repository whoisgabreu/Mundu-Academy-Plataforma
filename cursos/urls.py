from django.urls import path
from . import views

urlpatterns = [
    path('status', views.status, name='api_status'),
    path('cursos', views.get_cursos, name='api_cursos'),
]
