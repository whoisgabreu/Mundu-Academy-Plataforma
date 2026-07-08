from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from usuarios.models import Achievement, UserAchievement, Skill


class Command(BaseCommand):
    help = 'Popula achievements e skills de exemplo'

    def handle(self, *args, **kwargs):
        self._seed_achievements()
        self._seed_skills()
        self.stdout.write(self.style.SUCCESS('Usuarios populados com sucesso!'))

    def _seed_achievements(self):
        dados = [
            {'titulo': 'Primeiro Curso', 'descricao': 'Complete seu primeiro curso', 'icone': 'rocket', 'cor_gradiente': 'from-orange-500 to-red-500'},
            {'titulo': 'Streak 7 dias', 'descricao': 'Mantenha streak por 7 dias', 'icone': 'flame', 'cor_gradiente': 'from-orange-400 to-yellow-500'},
            {'titulo': 'Idealizador', 'descricao': 'Crie um tópico na comunidade', 'icone': 'lightbulb', 'cor_gradiente': 'from-yellow-400 to-amber-500'},
            {'titulo': 'Desafiante', 'descricao': 'Complete 5 desafios', 'icone': 'target', 'cor_gradiente': 'from-pink-500 to-purple-500'},
        ]
        for d in dados:
            Achievement.objects.get_or_create(titulo=d['titulo'], defaults=d)
        self.stdout.write(f'  OK: {len(dados)} achievements criados')

    def _seed_skills(self):
        dados = [
            {'nome': 'Growth Marketing', 'nivel': 7, 'icone': 'trending-up'},
            {'nome': 'Vendas B2B', 'nivel': 5, 'icone': 'bar-chart-3'},
            {'nome': 'Copywriting', 'nivel': 6, 'icone': 'pen-tool'},
            {'nome': 'SEO', 'nivel': 4, 'icone': 'search'},
            {'nome': 'Tráfego Pago', 'nivel': 8, 'icone': 'target'},
            {'nome': 'Liderança', 'nivel': 3, 'icone': 'users'},
        ]
        user = User.objects.first()
        if user:
            for d in dados:
                Skill.objects.get_or_create(usuario=user, nome=d['nome'], defaults=d)
            self.stdout.write(f'  OK: {len(dados)} skills criadas para {user.username}')
        else:
            self.stdout.write('  SKIP: nenhum usuário encontrado')
