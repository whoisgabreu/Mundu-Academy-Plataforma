from django.contrib import admin
from .models import (
    Achievement,
    Badge,
    CoinTransaction,
    Mission,
    Perfil,
    Reward,
    Skill,
    Title,
    UserAchievement,
    UserBadge,
    UserMission,
    UserReward,
    UserTitle,
    XPEvent,
)


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'nivel', 'xp_total', 'moedas', 'streak_dias', 'cargo']
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


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['nome', 'icone', 'cor', 'xp_bonus', 'ativo']
    list_filter = ['ativo', 'cor']
    search_fields = ['nome']


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'badge', 'earned_at']
    search_fields = ['usuario__username', 'badge__nome']


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ['nome', 'nivel_minimo', 'ativo']
    list_filter = ['ativo']


@admin.register(UserTitle)
class UserTitleAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'titulo', 'earned_at']


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'meta', 'xp', 'moedas', 'ativo']
    list_filter = ['tipo', 'ativo']


@admin.register(UserMission)
class UserMissionAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'mission', 'progresso', 'concluida']
    list_filter = ['concluida']


@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ['nome', 'custo_moedas', 'ativo']
    list_filter = ['ativo']


@admin.register(UserReward)
class UserRewardAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'reward', 'redeemed_at']


@admin.register(CoinTransaction)
class CoinTransactionAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'quantidade', 'descricao', 'created_at']


@admin.register(XPEvent)
class XPEventAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'xp', 'origem', 'nivel_anterior', 'nivel_atual', 'created_at']
    list_filter = ['origem']
