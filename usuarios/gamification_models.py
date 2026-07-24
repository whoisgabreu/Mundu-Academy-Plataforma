from django.contrib.auth.models import User
from django.db import models


class Badge(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    icone = models.CharField(max_length=50, default='badge-check')
    cor = models.CharField(max_length=40, default='emerald')
    xp_bonus = models.PositiveIntegerField(default=0)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Badge'
        verbose_name_plural = 'Badges'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class UserBadge(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='usuarios')
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'badge')
        verbose_name = 'Badge do Usuario'
        verbose_name_plural = 'Badges dos Usuarios'

    def __str__(self):
        return f'{self.usuario.username} - {self.badge.nome}'


class Title(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    nivel_minimo = models.PositiveIntegerField(default=1)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Titulo'
        verbose_name_plural = 'Titulos'
        ordering = ['nivel_minimo', 'nome']

    def __str__(self):
        return self.nome


class UserTitle(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='titulos')
    titulo = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='usuarios')
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'titulo')
        verbose_name = 'Titulo do Usuario'
        verbose_name_plural = 'Titulos dos Usuarios'

    def __str__(self):
        return f'{self.usuario.username} - {self.titulo.nome}'


class Mission(models.Model):
    TIPOS = [
        ('daily', 'Diaria'),
        ('weekly', 'Semanal'),
        ('special', 'Especial'),
    ]

    titulo = models.CharField(max_length=140)
    descricao = models.TextField(blank=True)
    tipo = models.CharField(max_length=20, choices=TIPOS, default='daily')
    meta = models.PositiveIntegerField(default=1)
    xp = models.PositiveIntegerField(default=0)
    moedas = models.PositiveIntegerField(default=0)
    badge = models.ForeignKey(Badge, on_delete=models.SET_NULL, null=True, blank=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Missao'
        verbose_name_plural = 'Missoes'
        ordering = ['tipo', 'titulo']

    def __str__(self):
        return self.titulo


class UserMission(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='missoes')
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='usuarios')
    progresso = models.PositiveIntegerField(default=0)
    concluida = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('usuario', 'mission')
        verbose_name = 'Missao do Usuario'
        verbose_name_plural = 'Missoes dos Usuarios'

    @property
    def percentual(self):
        if self.mission.meta == 0:
            return 0
        return min(int(self.progresso / self.mission.meta * 100), 100)

    def __str__(self):
        return f'{self.usuario.username} - {self.mission.titulo}'


class Reward(models.Model):
    nome = models.CharField(max_length=120)
    descricao = models.TextField(blank=True)
    custo_moedas = models.PositiveIntegerField(default=0)
    icone = models.CharField(max_length=50, default='gift')
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Recompensa'
        verbose_name_plural = 'Recompensas'
        ordering = ['custo_moedas', 'nome']

    def __str__(self):
        return self.nome


class UserReward(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recompensas')
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE, related_name='usuarios')
    redeemed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Recompensa do Usuario'
        verbose_name_plural = 'Recompensas dos Usuarios'

    def __str__(self):
        return f'{self.usuario.username} - {self.reward.nome}'


class CoinTransaction(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transacoes_moedas')
    quantidade = models.IntegerField()
    descricao = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Transacao de Moedas'
        verbose_name_plural = 'Transacoes de Moedas'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.usuario.username} {self.quantidade:+d}'


class XPEvent(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='xp_events')
    origem = models.CharField(max_length=60, default='manual')
    descricao = models.CharField(max_length=200, blank=True)
    xp = models.PositiveIntegerField(default=0)
    nivel_anterior = models.PositiveIntegerField(default=1)
    nivel_atual = models.PositiveIntegerField(default=1)
    xp_anterior = models.PositiveIntegerField(default=0)
    xp_atual = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Evento de XP'
        verbose_name_plural = 'Eventos de XP'
        ordering = ['-created_at']

    @property
    def level_up(self):
        return self.nivel_atual > self.nivel_anterior

    def __str__(self):
        return f'{self.usuario.username} +{self.xp} XP'
