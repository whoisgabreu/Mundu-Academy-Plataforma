from django.core.management.base import BaseCommand
from resources.models import ResourceCategory, Resource


class Command(BaseCommand):
    help = 'Popula categorias e recursos de exemplo'

    def handle(self, *args, **kwargs):
        self._seed_categories()
        self._seed_resources()
        self.stdout.write(self.style.SUCCESS('Resources populados com sucesso!'))

    def _seed_categories(self):
        cats = ['Marketing', 'Vendas', 'Produto', 'Finanças', 'Design', 'IA & Automação']
        for ordem, nome in enumerate(cats):
            ResourceCategory.objects.get_or_create(nome=nome, defaults={'ordem': ordem})
        self.stdout.write(f'  OK: {len(cats)} categorias criadas')

    def _seed_resources(self):
        data = [
            {'titulo': 'Checklist de Lançamento de Produto', 'descricao': 'Template completo com todas as etapas para um lançamento de sucesso', 'url': '#', 'autor': 'Thiago Nigro', 'thumbnail': 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=400&q=80', 'formato': 'PDF', 'em_alta': True, 'visualizacoes': 2000, 'categoria': 'Marketing'},
            {'titulo': 'Planilha de Controle Financeiro', 'descricao': 'Modelo para gestão de fluxo de caixa e projeções', 'url': '#', 'autor': 'Ana Lima', 'thumbnail': 'https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?w=400&q=80', 'formato': 'Planilha', 'premium': True, 'visualizacoes': 5000, 'categoria': 'Finanças'},
            {'titulo': 'Gerador de Títulos para Ads', 'descricao': 'Prompt otimizado para criar títulos que convertem', 'url': '#', 'autor': 'Pedro Mendes', 'thumbnail': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400&q=80', 'formato': 'Prompt', 'novo': True, 'visualizacoes': 1000, 'categoria': 'Marketing'},
            {'titulo': 'Script de Cold Call B2B', 'descricao': 'Roteiro para ligações de prospecção corporativa', 'url': '#', 'autor': 'Carlos Oliveira', 'thumbnail': 'https://images.unsplash.com/photo-1521791136064-7986c2920216?w=400&q=80', 'formato': 'PDF', 'visualizacoes': 3000, 'categoria': 'Vendas'},
            {'titulo': 'Calculadora CAC e LTV', 'descricao': 'Planilha para métricas de marketing e vendas', 'url': '#', 'autor': 'Rafael Costa', 'thumbnail': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&q=80', 'formato': 'Planilha', 'premium': True, 'visualizacoes': 4000, 'categoria': 'Finanças'},
            {'titulo': 'Wireframe Kit UX', 'descricao': 'Componentes Figma para prototipação rápida', 'url': '#', 'autor': 'Marina Costa', 'thumbnail': 'https://images.unsplash.com/photo-1586717791821-3f44a563fa4c?w=400&q=80', 'formato': 'Template', 'novo': True, 'visualizacoes': 1500, 'categoria': 'Design'},
            {'titulo': 'Automação com IA', 'descricao': 'Prompt para automatizar tarefas repetitivas com ChatGPT', 'url': '#', 'autor': 'Lucas Pestana', 'thumbnail': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400&q=80', 'formato': 'Prompt', 'em_alta': True, 'visualizacoes': 6000, 'categoria': 'IA & Automação'},
            {'titulo': 'Roadmap de Produto', 'descricao': 'Template de roadmap ágil para times de produto', 'url': '#', 'autor': 'Camila Souza', 'thumbnail': 'https://images.unsplash.com/photo-1542744173-8e7e53415bb0?w=400&q=80', 'formato': 'PDF', 'visualizacoes': 2500, 'categoria': 'Produto'},
        ]
        created = 0
        for d in data:
            cat = ResourceCategory.objects.filter(nome=d.pop('categoria')).first()
            Resource.objects.get_or_create(titulo=d['titulo'], defaults={**d, 'categoria': cat})
            created += 1
        self.stdout.write(f'  OK: {created} recursos criados')
