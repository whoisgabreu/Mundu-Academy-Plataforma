from django.db import models
from django.conf import settings


class Follow(models.Model):
    seguidor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seguindo')
    seguido = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seguidores')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('seguidor', 'seguido')
        verbose_name = 'Seguir'
        verbose_name_plural = 'Seguindo/Seguidores'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.seguidor.username} → {self.seguido.username}'


class Notification(models.Model):
    TYPES = [
        ('like', 'Like'),
        ('reply', 'Resposta'),
        ('follow', 'Seguidor'),
        ('achievement', 'Conquista'),
        ('system', 'Sistema'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notificacoes')
    tipo = models.CharField(max_length=20, choices=TYPES)
    mensagem = models.TextField()
    link = models.URLField(blank=True)
    lida = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'
        ordering = ['-created_at']

    def __str__(self):
        return f'[{self.get_tipo_display()}] {self.usuario.username}: {self.mensagem[:50]}'
