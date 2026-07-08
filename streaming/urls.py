from django.urls import path
from . import views

urlpatterns = [
    path('<slug:modulo_slug>/<int:ordem>/', views.player_aula, name='stream_player'),
]
