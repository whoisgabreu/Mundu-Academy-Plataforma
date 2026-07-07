from django.urls import path
from . import views

urlpatterns = [
    path('<int:aula_id>/', views.player_aula, name='stream_player'),
]
