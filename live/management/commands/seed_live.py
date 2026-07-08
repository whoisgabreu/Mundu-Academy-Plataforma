from django.core.management.base import BaseCommand
from live.models import LiveStream, LivePoll
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Popula lives de exemplo'

    def handle(self, *args, **kwargs):
        self._seed_lives()
        self._seed_polls()
        self.stdout.write(self.style.SUCCESS('Lives populadas com sucesso!'))

    def _seed_lives(self):
        now = timezone.now()
        dados = [
            {
                'titulo': 'Marketing Digital na Prática',
                'descricao': 'Aula ao vivo sobre SEO, tráfego pago e conteúdo orgânico.',
                'url_embed': 'https://www.youtube.com/embed/3q3k65Bk9mk',
                'thumbnail': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=600&q=80',
                'ao_vivo': True,
                'data_agendamento': now - timedelta(hours=1),
                'data_inicio': now - timedelta(hours=1),
            },
            {
                'titulo': 'Copywriting para Conversão',
                'descricao': 'Técnicas avançadas de copy para landing pages que convertem.',
                'url_embed': 'https://www.youtube.com/embed/dQw4w9WgXcQ',
                'thumbnail': 'https://images.unsplash.com/photo-1455390582262-044cdead277a?w=600&q=80',
                'ao_vivo': False,
                'data_agendamento': now + timedelta(days=3, hours=14),
            },
            {
                'titulo': 'Gestão de Tráfego Pago — Live Semanal',
                'descricao': 'Análise de campanhas ao vivo e otimização de anúncios.',
                'url_embed': 'https://www.youtube.com/embed/9bZkp7q19f0',
                'thumbnail': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600&q=80',
                'ao_vivo': False,
                'data_agendamento': now + timedelta(days=7, hours=10),
            },
            {
                'titulo': 'Vendas B2B: Case G4 Educação',
                'descricao': 'Replay da live sobre vendas consultivas com o time G4.',
                'url_embed': 'https://www.youtube.com/embed/kXYiU_JCYtU',
                'thumbnail': 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=600&q=80',
                'ao_vivo': False,
                'data_agendamento': now - timedelta(days=14),
                'data_inicio': now - timedelta(days=14, hours=1),
                'data_fim': now - timedelta(days=14, hours=-1),
            },
            {
                'titulo': 'SEO e Conteúdo Orgânico — Replay',
                'descricao': 'Replay completo da masterclass sobre SEO on-page e off-page.',
                'url_embed': 'https://www.youtube.com/embed/hF515-0Tduk',
                'thumbnail': 'https://images.unsplash.com/photo-1493612276216-ee3925520721?w=600&q=80',
                'ao_vivo': False,
                'data_agendamento': now - timedelta(days=30),
                'data_inicio': now - timedelta(days=30, hours=1),
                'data_fim': now - timedelta(days=30, hours=-1),
            },
        ]
        for d in dados:
            LiveStream.objects.get_or_create(titulo=d['titulo'], defaults=d)
        self.stdout.write(f'  OK: {len(dados)} lives criadas')

    def _seed_polls(self):
        live = LiveStream.objects.filter(ao_vivo=True).first()
        if live:
            LivePoll.objects.get_or_create(
                stream=live, pergunta='Qual tema você quer no próximo módulo?',
                defaults={
                    'opcoes': [
                        {'text': 'Growth Marketing', 'votos': 12},
                        {'text': 'Vendas B2B', 'votos': 8},
                        {'text': 'Liderança', 'votos': 5},
                    ],
                    'ativa': True,
                }
            )
            self.stdout.write('  OK: 1 enquete criada')
        else:
            self.stdout.write('  SKIP: nenhuma live ativa para enquete')
