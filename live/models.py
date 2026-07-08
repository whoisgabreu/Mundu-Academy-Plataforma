from django.db import models
from django.conf import settings


class LiveStream(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    url_embed = models.URLField(help_text="URL de embed do YouTube (ex: https://www.youtube.com/embed/...)")
    thumbnail = models.URLField(blank=True)
    ao_vivo = models.BooleanField(default=False)
    data_agendamento = models.DateTimeField(null=True, blank=True)
    data_inicio = models.DateTimeField(null=True, blank=True)
    data_fim = models.DateTimeField(null=True, blank=True)
    modulo = models.ForeignKey('cursos.Modulo', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Live Stream'
        verbose_name_plural = 'Live Streams'
        ordering = ['-data_agendamento']

    def __str__(self):
        return self.titulo


class LiveChatMessage(models.Model):
    stream = models.ForeignKey(LiveStream, on_delete=models.CASCADE, related_name='mensagens')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mensagem = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Mensagem do Chat'
        verbose_name_plural = 'Mensagens do Chat'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.usuario.username}: {self.mensagem[:50]}'


class LivePoll(models.Model):
    stream = models.ForeignKey(LiveStream, on_delete=models.CASCADE, related_name='enquetes')
    pergunta = models.CharField(max_length=300)
    opcoes = models.JSONField(default=list, help_text='Lista de objetos: [{"text": "...", "votos": 0}]')
    ativa = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Enquete'
        verbose_name_plural = 'Enquetes'
        ordering = ['-created_at']

    def __str__(self):
        return self.pergunta


class LivePollVote(models.Model):
    poll = models.ForeignKey(LivePoll, on_delete=models.CASCADE, related_name='votos')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    opcao_index = models.IntegerField(help_text='Índice da opção escolhida em opcoes[]')

    class Meta:
        unique_together = ('poll', 'usuario')
        verbose_name = 'Voto em Enquete'
        verbose_name_plural = 'Votos em Enquetes'

    def __str__(self):
        return f'{self.usuario.username} votou em {self.poll.pergunta[:30]}'
