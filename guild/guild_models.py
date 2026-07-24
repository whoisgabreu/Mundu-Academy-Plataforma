from django.conf import settings
from django.db import models


class GuildMembership(models.Model):
    ROLE_CHOICES = [
        ('member', 'Membro'),
        ('moderator', 'Moderador'),
        ('admin', 'Administrador'),
    ]

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='guild_membership',
    )
    community = models.ForeignKey(
        'guild.Community',
        on_delete=models.CASCADE,
        related_name='memberships',
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    xp = models.PositiveIntegerField(default=0)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Integrante da Guilda'
        verbose_name_plural = 'Integrantes das Guildas'
        ordering = ['-xp', 'joined_at']

    def __str__(self):
        return f'{self.usuario.username} em {self.community.name}'


class GuildMission(models.Model):
    community = models.ForeignKey(
        'guild.Community',
        on_delete=models.CASCADE,
        related_name='missions',
    )
    titulo = models.CharField(max_length=140)
    descricao = models.TextField(blank=True)
    meta = models.PositiveIntegerField(default=1)
    xp = models.PositiveIntegerField(default=0)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Missao da Guilda'
        verbose_name_plural = 'Missoes das Guildas'
        ordering = ['community', 'titulo']

    def __str__(self):
        return f'{self.community.name} - {self.titulo}'


class GuildMissionProgress(models.Model):
    membership = models.ForeignKey(
        GuildMembership,
        on_delete=models.CASCADE,
        related_name='mission_progress',
    )
    mission = models.ForeignKey(
        GuildMission,
        on_delete=models.CASCADE,
        related_name='progress',
    )
    progresso = models.PositiveIntegerField(default=0)
    concluida = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('membership', 'mission')
        verbose_name = 'Progresso de Missao da Guilda'
        verbose_name_plural = 'Progressos de Missoes da Guilda'

    @property
    def percentual(self):
        if self.mission.meta == 0:
            return 0
        return min(int(self.progresso / self.mission.meta * 100), 100)

    def __str__(self):
        return f'{self.membership.usuario.username} - {self.mission.titulo}'
