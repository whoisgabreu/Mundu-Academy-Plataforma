from django.db import models
from django.contrib.auth.models import User


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
    cargo = models.CharField(max_length=100, blank=True, default='Aprendiz')

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
