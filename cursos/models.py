from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from embed_video.fields import EmbedVideoField


class Modulo(models.Model):
    NIVEIS = [
        ('Iniciante', 'Iniciante'),
        ('Intermediário', 'Intermediário'),
        ('Avançado', 'Avançado'),
    ]

    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    descricao = models.TextField(blank=True)
    thumbnail = models.URLField(blank=True)
    total_aulas = models.IntegerField(default=0)
    duracao_total = models.CharField(max_length=50, blank=True)
    xp_total = models.IntegerField(default=0)
    nivel = models.CharField(max_length=20, choices=NIVEIS, default='Iniciante')
    tem_certificado = models.BooleanField(default=True)
    num_secoes = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'
        ordering = ['titulo']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo


class ProgressoModulo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progressos_modulo')
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name='progressos')
    progresso = models.IntegerField(default=0)  # 0–100
    data_inicio = models.DateTimeField(auto_now_add=True)
    data_conclusao = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('usuario', 'modulo')
        verbose_name = 'Progresso de Módulo'
        verbose_name_plural = 'Progressos de Módulo'

    def __str__(self):
        return f'{self.usuario.username} → {self.modulo.titulo} ({self.progresso}%)'


class Trilha(models.Model):
    OBJETIVOS = [('Carreira', 'Carreira'), ('Habilidade', 'Habilidade')]

    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    thumbnail = models.URLField(blank=True)
    area = models.CharField(max_length=100)
    nivel = models.CharField(max_length=100)
    objetivo = models.CharField(max_length=20, choices=OBJETIVOS, default='Habilidade')
    duracao_total = models.CharField(max_length=50, blank=True)
    xp_total = models.IntegerField(default=0)
    tem_certificado = models.BooleanField(default=True)
    modulos = models.ManyToManyField(Modulo, through='TrilhaModulo', blank=True)

    class Meta:
        verbose_name = 'Trilha'
        verbose_name_plural = 'Trilhas'
        ordering = ['titulo']

    def __str__(self):
        return self.titulo


class TrilhaModulo(models.Model):
    trilha = models.ForeignKey(Trilha, on_delete=models.CASCADE)
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)
    ordem = models.IntegerField(default=0)
    bloqueado = models.BooleanField(default=False)
    prerequisito = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ('trilha', 'modulo')
        ordering = ['ordem']
        verbose_name = 'Módulo da Trilha'
        verbose_name_plural = 'Módulos das Trilhas'

    def __str__(self):
        return f'{self.trilha.titulo} → {self.modulo.titulo}'


class Desafio(models.Model):
    TIPOS = [
        ('daily', 'Diário'),
        ('weekly', 'Semanal'),
        ('special', 'Especial'),
    ]

    tipo = models.CharField(max_length=20, choices=TIPOS)
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    xp = models.IntegerField(default=0)
    meta = models.IntegerField(default=1)
    icon = models.CharField(max_length=50, default='target')
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Desafio'
        verbose_name_plural = 'Desafios'

    def __str__(self):
        return f'[{self.get_tipo_display()}] {self.titulo}'


class ProgressoDesafio(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progressos_desafio')
    desafio = models.ForeignKey(Desafio, on_delete=models.CASCADE, related_name='progressos')
    progresso = models.IntegerField(default=0)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('usuario', 'desafio')
        verbose_name = 'Progresso de Desafio'
        verbose_name_plural = 'Progressos de Desafios'

    def __str__(self):
        return f'{self.usuario.username} → {self.desafio.titulo} ({self.progresso}/{self.desafio.meta})'


# Mantido para compatibilidade com a tabela já existente no PostgreSQL
class Aula(models.Model):
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name='aulas')
    titulo = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)
    url_video = EmbedVideoField(help_text="Cole a URL do YouTube ou Vimeo aqui")
    duracao = models.CharField(max_length=20, blank=True, help_text="Ex: 15:30")
    ordem = models.IntegerField(default=0)
    is_preview = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
        ordering = ['ordem']
        unique_together = ('modulo', 'ordem')

    def __str__(self):
        return f'{self.modulo.titulo} — {self.titulo}'


class Certificate(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificados')
    modulo = models.ForeignKey(Modulo, on_delete=models.SET_NULL, null=True, blank=True)
    trilha = models.ForeignKey(Trilha, on_delete=models.SET_NULL, null=True, blank=True)
    codigo = models.CharField(max_length=32, unique=True)
    emitido_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Certificado'
        verbose_name_plural = 'Certificados'
        ordering = ['-emitido_em']

    def __str__(self):
        return f'{self.usuario.username} — {self.modulo or self.trilha}'


class FeaturedContent(models.Model):
    TIPOS = [
        ('recommended', 'Recomendado'),
        ('collab', 'Collab'),
        ('case', 'Case'),
    ]

    tipo = models.CharField(max_length=20, choices=TIPOS)
    titulo = models.CharField(max_length=200)
    subtitulo = models.CharField(max_length=300, blank=True)
    thumbnail = models.URLField(blank=True)
    duracao = models.CharField(max_length=50, blank=True, help_text="Ex: 2h 15min")
    xp = models.IntegerField(default=0)
    participantes = models.IntegerField(default=0)
    badge = models.CharField(max_length=100, blank=True, help_text="Ex: Exclusivo, Novo")
    ordem = models.IntegerField(default=0)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Conteúdo em Destaque'
        verbose_name_plural = 'Conteúdos em Destaque'
        ordering = ['tipo', 'ordem']

    def __str__(self):
        return f'[{self.get_tipo_display()}] {self.titulo}'


class Quiz(models.Model):
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name='quizzes')
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    ordem = models.IntegerField(default=0)
    xp_total = models.IntegerField(default=50, help_text="XP concedido ao passar")
    aprovacao_percentual = models.IntegerField(default=70, help_text="% mínima para aprovação")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'
        ordering = ['modulo', 'ordem']
        unique_together = ('modulo', 'ordem')

    def __str__(self):
        return f'{self.modulo.titulo} — {self.titulo}'


class Questao(models.Model):
    TIPOS = [
        ('multipla_escolha', 'Múltipla Escolha'),
        ('verdadeiro_falso', 'Verdadeiro ou Falso'),
    ]
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questoes')
    enunciado = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPOS, default='multipla_escolha')
    ordem = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Questão'
        verbose_name_plural = 'Questões'
        ordering = ['ordem']

    def __str__(self):
        return f'{self.quiz.titulo} — Q{self.ordem}'


class Alternativa(models.Model):
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE, related_name='alternativas')
    texto = models.CharField(max_length=300)
    correta = models.BooleanField(default=False)
    ordem = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Alternativa'
        verbose_name_plural = 'Alternativas'
        ordering = ['ordem']

    def __str__(self):
        return f'{self.questao.enunciado[:40]} → {self.texto[:30]}'


class TentativaQuiz(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tentativas_quiz')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='tentativas')
    pontuacao = models.IntegerField(default=0)
    total_questoes = models.IntegerField(default=0)
    aprovado = models.BooleanField(default=False)
    respostas = models.JSONField(default=dict, blank=True)
    concluido_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Tentativa de Quiz'
        verbose_name_plural = 'Tentativas de Quiz'
        ordering = ['-concluido_em']

    @property
    def percentual(self):
        if self.total_questoes == 0:
            return 0
        return int(self.pontuacao / self.total_questoes * 100)

    def __str__(self):
        return f'{self.usuario.username} → {self.quiz.titulo} ({self.pontuacao}/{self.total_questoes})'


class Curso(models.Model):
    titulo = models.CharField(max_length=200)
    instrutor = models.CharField(max_length=100)
    progresso = models.IntegerField(default=0)

    class Meta:
        db_table = 'cursos'
        verbose_name = 'Curso (legado)'
        verbose_name_plural = 'Cursos (legado)'

    def __str__(self):
        return self.titulo
