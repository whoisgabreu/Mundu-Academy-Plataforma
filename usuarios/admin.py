from django.contrib import admin
from .models import Perfil, Achievement, UserAchievement, Skill


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'nivel', 'xp_total', 'streak_dias', 'cargo']
    search_fields = ['usuario__username', 'usuario__email']
    list_filter = ['nivel']
    readonly_fields = ['iniciais', 'nome_nivel', 'xp_proximo_nivel', 'xp_percentual']


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'icone', 'created_at']


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'achievement', 'earned_at']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'nome', 'nivel']
