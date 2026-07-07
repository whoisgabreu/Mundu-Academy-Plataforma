from django.core.management.base import BaseCommand
from cursos.models import Modulo, Trilha, TrilhaModulo, Desafio


class Command(BaseCommand):
    help = 'Popula o banco com dados iniciais de exemplo'

    def handle(self, *args, **kwargs):
        self._seed_modulos()
        self._seed_trilhas()
        self._seed_desafios()
        self.stdout.write(self.style.SUCCESS('Banco populado com sucesso!')  )

    def _seed_modulos(self):
        modulos = [
            {
                'titulo': 'Fundamentos de Marketing Digital',
                'descricao': 'Domine os conceitos essenciais do marketing digital',
                'thumbnail': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=600&q=80',
                'total_aulas': 24, 'duracao_total': '8h 30min', 'xp_total': 850,
                'nivel': 'Iniciante', 'tem_certificado': True, 'num_secoes': 3,
            },
            {
                'titulo': 'Copywriting Avançado',
                'descricao': 'Técnicas avançadas de escrita persuasiva para conversão',
                'thumbnail': 'https://images.unsplash.com/photo-1455390582262-044cdead277a?w=600&q=80',
                'total_aulas': 18, 'duracao_total': '6h 15min', 'xp_total': 720,
                'nivel': 'Intermediário', 'tem_certificado': True, 'num_secoes': 2,
            },
            {
                'titulo': 'Gestão de Tráfego Pago',
                'descricao': 'Aprenda a criar e otimizar campanhas de anúncios',
                'thumbnail': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600&q=80',
                'total_aulas': 32, 'duracao_total': '12h', 'xp_total': 1200,
                'nivel': 'Avançado', 'tem_certificado': True, 'num_secoes': 2,
            },
            {
                'titulo': 'Vendas Consultivas B2B',
                'descricao': 'Domine técnicas de vendas para negócios corporativos',
                'thumbnail': 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=600&q=80',
                'total_aulas': 20, 'duracao_total': '7h 45min', 'xp_total': 900,
                'nivel': 'Intermediário', 'tem_certificado': True, 'num_secoes': 2,
            },
            {
                'titulo': 'Negociação Avançada',
                'descricao': 'Técnicas de persuasão e fechamento de negócios',
                'thumbnail': 'https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=600&q=80',
                'total_aulas': 15, 'duracao_total': '5h 30min', 'xp_total': 700,
                'nivel': 'Avançado', 'tem_certificado': True, 'num_secoes': 2,
            },
            {
                'titulo': 'SEO e Conteúdo Orgânico',
                'descricao': 'Domine o posicionamento orgânico no Google',
                'thumbnail': 'https://images.unsplash.com/photo-1493612276216-ee3925520721?w=600&q=80',
                'total_aulas': 22, 'duracao_total': '7h', 'xp_total': 800,
                'nivel': 'Intermediário', 'tem_certificado': True, 'num_secoes': 3,
            },
        ]

        for dados in modulos:
            Modulo.objects.get_or_create(titulo=dados['titulo'], defaults=dados)

        self.stdout.write(f'  OK: {len(modulos)} modulos criados')

    def _seed_trilhas(self):
        m1 = Modulo.objects.get(titulo='Fundamentos de Marketing Digital')
        m2 = Modulo.objects.get(titulo='Copywriting Avançado')
        m3 = Modulo.objects.get(titulo='Gestão de Tráfego Pago')
        m6 = Modulo.objects.get(titulo='SEO e Conteúdo Orgânico')
        m4 = Modulo.objects.get(titulo='Vendas Consultivas B2B')
        m5 = Modulo.objects.get(titulo='Negociação Avançada')

        trilha1, _ = Trilha.objects.get_or_create(
            titulo='Especialista em Marketing Digital',
            defaults={
                'descricao': 'Domine todas as habilidades necessárias para se tornar um profissional completo em marketing digital.',
                'thumbnail': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&q=80',
                'area': 'Marketing',
                'nivel': 'Iniciante → Avançado',
                'objetivo': 'Carreira',
                'duracao_total': '34h',
                'xp_total': 3570,
                'tem_certificado': True,
            }
        )
        for ordem, (modulo, bloqueado, prereq) in enumerate([
            (m1, False, ''), (m2, False, ''), (m3, False, ''), (m6, True, 'Copywriting Avançado')
        ]):
            TrilhaModulo.objects.get_or_create(
                trilha=trilha1, modulo=modulo,
                defaults={'ordem': ordem, 'bloqueado': bloqueado, 'prerequisito': prereq}
            )

        trilha2, _ = Trilha.objects.get_or_create(
            titulo='Líder de Vendas B2B',
            defaults={
                'descricao': 'Desenvolva competências para liderar equipes de vendas corporativas e fechar grandes contratos.',
                'thumbnail': 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=800&q=80',
                'area': 'Vendas',
                'nivel': 'Intermediário → Avançado',
                'objetivo': 'Habilidade',
                'duracao_total': '13h 15min',
                'xp_total': 1600,
                'tem_certificado': True,
            }
        )
        for ordem, (modulo, bloqueado, prereq) in enumerate([
            (m4, False, ''), (m5, False, ''),
        ]):
            TrilhaModulo.objects.get_or_create(
                trilha=trilha2, modulo=modulo,
                defaults={'ordem': ordem, 'bloqueado': bloqueado, 'prerequisito': prereq}
            )

        self.stdout.write('  OK: 2 trilhas criadas')

    def _seed_desafios(self):
        desafios = [
            {'tipo': 'daily', 'titulo': 'Assistir uma aula completa', 'descricao': 'Complete qualquer aula de um módulo', 'xp': 50, 'meta': 1, 'icon': 'graduation-cap', 'ativo': True},
            {'tipo': 'daily', 'titulo': 'Participar do fórum', 'descricao': 'Comente ou responda em uma discussão', 'xp': 30, 'meta': 1, 'icon': 'message-square', 'ativo': True},
            {'tipo': 'daily', 'titulo': 'Ler material complementar', 'descricao': 'Acesse um PDF ou link de apoio', 'xp': 25, 'meta': 1, 'icon': 'file-text', 'ativo': True},
            {'tipo': 'weekly', 'titulo': 'Maratonista', 'descricao': 'Complete 5 aulas esta semana', 'xp': 200, 'meta': 5, 'icon': 'rocket', 'ativo': True},
            {'tipo': 'weekly', 'titulo': 'Ao Vivo Presente', 'descricao': 'Participe de uma live com presença', 'xp': 250, 'meta': 1, 'icon': 'radio', 'ativo': True},
            {'tipo': 'special', 'titulo': 'Networking Power', 'descricao': 'Conecte-se com 3 membros novos da comunidade', 'xp': 200, 'meta': 3, 'icon': 'users', 'ativo': True},
        ]

        for dados in desafios:
            Desafio.objects.get_or_create(titulo=dados['titulo'], defaults=dados)

        self.stdout.write(f'  OK: {len(desafios)} desafios criados')
