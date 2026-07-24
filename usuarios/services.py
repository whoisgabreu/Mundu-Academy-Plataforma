from django.utils import timezone

from usuarios.models import (
    Reward,
    UserBadge,
    UserMission,
    UserTitle,
    XPEvent,
)


def gamification_summary(user):
    perfil = user.perfil
    missions = UserMission.objects.filter(usuario=user).select_related('mission')[:6]
    badges = UserBadge.objects.filter(usuario=user).select_related('badge')[:8]
    titles = UserTitle.objects.filter(usuario=user).select_related('titulo')[:6]
    rewards = Reward.objects.filter(ativo=True).order_by('custo_moedas')[:6]
    recent_events = XPEvent.objects.filter(usuario=user)[:5]

    return {
        'nivel': perfil.nivel,
        'nome_nivel': perfil.nome_nivel,
        'xp_atual': perfil.xp_total,
        'xp_necessario': perfil.xp_proximo_nivel,
        'xp_percentual': perfil.xp_percentual,
        'moedas': perfil.moedas,
        'streak_dias': perfil.streak_dias,
        'titulo_ativo': perfil.titulo_ativo.nome if perfil.titulo_ativo else perfil.nome_nivel,
        'badges': [
            {
                'nome': item.badge.nome,
                'descricao': item.badge.descricao,
                'icone': item.badge.icone,
                'cor': item.badge.cor,
                'earned_at': item.earned_at,
            }
            for item in badges
        ],
        'titulos': [
            {
                'nome': item.titulo.nome,
                'descricao': item.titulo.descricao,
                'earned_at': item.earned_at,
            }
            for item in titles
        ],
        'missoes': [
            {
                'titulo': item.mission.titulo,
                'descricao': item.mission.descricao,
                'tipo': item.mission.tipo,
                'progresso': item.progresso,
                'meta': item.mission.meta,
                'percentual': item.percentual,
                'concluida': item.concluida,
                'xp': item.mission.xp,
                'moedas': item.mission.moedas,
            }
            for item in missions
        ],
        'recompensas': [
            {
                'id': reward.id,
                'nome': reward.nome,
                'descricao': reward.descricao,
                'icone': reward.icone,
                'custo_moedas': reward.custo_moedas,
                'disponivel': perfil.moedas >= reward.custo_moedas,
            }
            for reward in rewards
        ],
        'eventos_xp': [
            {
                'xp': event.xp,
                'origem': event.origem,
                'descricao': event.descricao,
                'level_up': event.level_up,
                'nivel_anterior': event.nivel_anterior,
                'nivel_atual': event.nivel_atual,
                'created_at': event.created_at,
            }
            for event in recent_events
        ],
    }


def leaderboard(limit=10):
    from usuarios.models import Perfil

    return [
        {
            'posicao': index + 1,
            'usuario': perfil.usuario,
            'nome': perfil.usuario.get_full_name() or perfil.usuario.username,
            'xp': perfil.xp_total,
            'nivel': perfil.nivel,
            'badges': UserBadge.objects.filter(usuario=perfil.usuario).count(),
        }
        for index, perfil in enumerate(
            Perfil.objects.select_related('usuario').order_by('-nivel', '-xp_total')[:limit]
        )
    ]


def complete_user_mission(user, mission):
    progress, _ = UserMission.objects.get_or_create(usuario=user, mission=mission)
    if progress.concluida:
        return progress
    progress.progresso = mission.meta
    progress.concluida = True
    progress.completed_at = timezone.now()
    progress.save(update_fields=['progresso', 'concluida', 'completed_at'])
    if mission.xp:
        user.perfil.adicionar_xp(mission.xp, origem='mission', descricao=mission.titulo)
    if mission.moedas:
        user.perfil.moedas += mission.moedas
        user.perfil.save(update_fields=['moedas'])
    if mission.badge:
        UserBadge.objects.get_or_create(usuario=user, badge=mission.badge)
    return progress
