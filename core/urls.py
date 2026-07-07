from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('explorar', views.explorar, name='explorar'),
    path('perfil', views.perfil, name='perfil'),
    path('config', views.config, name='config'),
    path('trilhas', views.trilhas, name='trilhas'),
    path('conteudos', views.conteudos, name='conteudos'),
    path('desafios', views.desafios, name='desafios'),
    path('ao-vivo', views.ao_vivo, name='ao_vivo'),
    path('insumos', views.insumos, name='insumos'),
    path('networking', views.networking, name='networking'),
    path('u/<slug:handle>', views.user_profile, name='user_profile'),
]
