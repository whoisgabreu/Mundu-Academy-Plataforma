from django.core.management.base import BaseCommand
from library.models import Summary, Framework


class Command(BaseCommand):
    help = 'Popula summaries e frameworks de exemplo'

    def handle(self, *args, **kwargs):
        self._seed_summaries()
        self._seed_frameworks()
        self.stdout.write(self.style.SUCCESS('Library populada com sucesso!'))

    def _seed_summaries(self):
        dados = [
            {'summary_id': 's1', 'title': 'Hooked: How to Build Habit-Forming Products', 'author': 'Nir Eyal', 'read_time': '12 min', 'tag': 'Produto', 'excerpt': 'O modelo Hook — Trigger, Action, Variable Reward, Investment — explica como produtos formam hábitos.', 'thumbnail': 'https://images.unsplash.com/photo-1553729459-afe8f2e2e5b0?w=400&q=80', 'saves': 1240},
            {'summary_id': 's2', 'title': 'The Mom Test', 'author': 'Rob Fitzpatrick', 'read_time': '8 min', 'tag': 'Empreendedorismo', 'excerpt': 'Como conversar com clientes sem receber falsos positivos. Evite perguntas que sua mãe responderia com sim.', 'thumbnail': 'https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=400&q=80', 'saves': 980},
            {'summary_id': 's3', 'title': 'Never Split the Difference', 'author': 'Chris Voss', 'read_time': '15 min', 'tag': 'Negociação', 'excerpt': 'Técnicas de negociação do ex-negociador do FBI: espelhamento, rotulação, perguntas calibradas.', 'thumbnail': 'https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=400&q=80', 'saves': 1560},
        ]
        for d in dados:
            Summary.objects.get_or_create(summary_id=d['summary_id'], defaults=d)
        self.stdout.write(f'  OK: {len(dados)} summaries criados')

    def _seed_frameworks(self):
        dados = [
            {'framework_id': 'fw1', 'slug': 'wrap', 'title': 'WRAP Decision Model', 'description': 'Estrutura para tomada de decisão em 4 passos: Wide, Reality-test, Attain, Prepare.', 'format': 'Canvas', 'uses': 3420, 'active_now': 128, 'version': '2.1', 'last_edit_at': '2 dias atrás', 'last_editor_handle': 'mariana-reis', 'forks': 89, 'rating': 4.5, 'reviews_count': 42, 'xp': 150, 'color': 'primary'},
            {'framework_id': 'fw2', 'slug': 'conflict-canvas', 'title': 'Conflict Canvas', 'description': 'Framework para navegar conversas difíceis mapeando interesses, emoções e resultados.', 'format': 'Canvas', 'uses': 2180, 'active_now': 73, 'version': '1.3', 'last_edit_at': '1 semana atrás', 'last_editor_handle': 'diego-almeida', 'forks': 45, 'rating': 4.2, 'reviews_count': 28, 'xp': 120, 'color': 'accent'},
            {'framework_id': 'fw3', 'slug': 'score', 'title': 'SCORE Framework', 'description': 'Situation, Complication, Resolution, Example — estrutura para comunicação executiva e apresentações.', 'format': 'Checklist', 'uses': 1560, 'active_now': 42, 'version': '1.0', 'last_edit_at': '3 dias atrás', 'last_editor_handle': 'camila-souza', 'forks': 23, 'rating': 4.0, 'reviews_count': 15, 'xp': 100, 'color': 'secondary'},
            {'framework_id': 'fw4', 'slug': 'feedback-radar', 'title': 'Feedback Radar', 'description': 'Método para dar feedback contínuo em 4 quadrantes: Continue, Stop, Start, Improve.', 'format': 'Template', 'uses': 890, 'active_now': 31, 'version': '2.0', 'last_edit_at': '5 dias atrás', 'last_editor_handle': 'rafael-santos', 'forks': 12, 'rating': 4.8, 'reviews_count': 20, 'xp': 130, 'color': 'primary'},
            {'framework_id': 'fw5', 'slug': 'okr-card', 'title': 'OKR Card', 'description': 'Template para definir Objectives and Key Results de forma simples e rastreável.', 'format': 'Template', 'uses': 4500, 'active_now': 213, 'version': '3.0', 'last_edit_at': '1 dia atrás', 'last_editor_handle': 'pedro-mendes', 'forks': 156, 'rating': 4.6, 'reviews_count': 67, 'xp': 100, 'color': 'secondary'},
            {'framework_id': 'fw6', 'slug': 'ice-prioritization', 'title': 'ICE Prioritization', 'description': 'Priorize iniciativas por Impact, Confidence e Ease. Pontuação de 1 a 10 em cada eixo.', 'format': 'Planilha', 'uses': 3200, 'active_now': 95, 'version': '1.5', 'last_edit_at': '2 semanas atrás', 'last_editor_handle': 'camila-souza', 'forks': 67, 'rating': 4.3, 'reviews_count': 34, 'xp': 80, 'color': 'accent'},
        ]
        for d in dados:
            Framework.objects.get_or_create(framework_id=d['framework_id'], defaults=d)
        self.stdout.write(f'  OK: {len(dados)} frameworks criados')
