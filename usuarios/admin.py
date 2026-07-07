from django.contrib import admin
from .models import Perfil


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'nivel', 'xp_total', 'streak_dias', 'cargo']
    search_fields = ['usuario__username', 'usuario__email']
    list_filter = ['nivel']
    readonly_fields = ['iniciais', 'nome_nivel', 'xp_proximo_nivel', 'xp_percentual']
