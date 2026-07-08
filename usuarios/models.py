from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


NIVEIS_NOME = {
    1: 'Iniciante', 2: 'Explorador', 3: 'Aprendiz',
    4: 'Praticante', 5: 'Especialista', 6: 'Avançado',
    7: 'Estrategista', 8: 'Mestre', 9: 'Expert', 10: 'Lendário',
}


class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    xp_total = models.IntegerField(default=0)
    nivel = models.IntegerField(default=1)
    streak_dias = models.IntegerField(default=0)
    ultimo_login = models.DateField(null=True, blank=True)
    cargo = models.CharField(max_length=100, blank=True, default='Aprendiz')
    bio = models.TextField(blank=True)
    empresa = models.CharField(max_length=200, blank=True)
    localizacao = models.CharField(max_length=200, blank=True)
    linkedin = models.URLField(blank=True)
    instagram = models.CharField(max_length=100, blank=True)
    karma = models.IntegerField(default=0)
    data_criacao = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'

    def __str__(self):
        return f'Perfil de {self.usuario.username}'

    @property
    def iniciais(self):
        nome = self.usuario.get_full_name() or self.usuario.username
        partes = nome.split()
        if len(partes) >= 2:
            return (partes[0][0] + partes[-1][0]).upper()
        return nome[:2].upper()

    @property
    def role(self):
        if self.cargo and self.empresa:
            return f'{self.cargo} · {self.empresa}'
        return self.cargo or self.empresa or 'Membro Mundu'

    @property
    def nome_nivel(self):
        return NIVEIS_NOME.get(self.nivel, 'Iniciante')

    @property
    def xp_proximo_nivel(self):
        return self.nivel * 500

    @property
    def xp_percentual(self):
        if self.xp_proximo_nivel == 0:
            return 0
        return min(int(self.xp_total / self.xp_proximo_nivel * 100), 100)

    def adicionar_xp(self, quantidade):
        self.xp_total += quantidade
        while self.xp_total >= self.xp_proximo_nivel and self.nivel < 10:
            self.xp_total -= self.xp_proximo_nivel
            self.nivel += 1
        self.save()


class Achievement(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    icone = models.CharField(max_length=50, help_text="Nome do ícone Lucide (ex: rocket)")
    cor_gradiente = models.CharField(max_length=100, default='from-orange-500 to-red-500', help_text="Tailwind gradient classes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Conquista'
        verbose_name_plural = 'Conquistas'
        ordering = ['titulo']

    def __str__(self):
        return self.titulo


class UserAchievement(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conquistas')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='usuarios')
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'achievement')
        verbose_name = 'Conquista do Usuário'
        verbose_name_plural = 'Conquistas dos Usuários'

    def __str__(self):
        return f'{self.usuario.username} → {self.achievement.titulo}'


class Skill(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    nome = models.CharField(max_length=100)
    nivel = models.IntegerField(default=1, help_text="1-10")
    icone = models.CharField(max_length=50, default='trending-up', help_text="Nome do ícone Lucide")

    class Meta:
        verbose_name = 'Habilidade'
        verbose_name_plural = 'Habilidades'
        unique_together = ('usuario', 'nome')
        ordering = ['-nivel']

    def __str__(self):
        return f'{self.usuario.username} — {self.nome} ({self.nivel}/10)'
