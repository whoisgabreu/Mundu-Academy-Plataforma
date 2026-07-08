from django.core.management.base import BaseCommand
from cursos.models import Modulo, Trilha, TrilhaModulo, Desafio, FeaturedContent, Aula, Certificate, Quiz, Questao, Alternativa
from django.contrib.auth.models import User
import secrets


class Command(BaseCommand):
    help = 'Popula o banco com dados iniciais de exemplo'

    def handle(self, *args, **kwargs):
        self._seed_modulos()
        self._seed_trilhas()
        self._seed_desafios()
        self._seed_featured_content()
        self._seed_aulas()
        self._seed_certificados()
        self._seed_quizzes()
        self.stdout.write(self.style.SUCCESS('Banco populado com sucesso!'))

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

    def _seed_featured_content(self):
        items = [
            {'tipo': 'recommended', 'titulo': 'Sales Machine: Vendas Previsíveis', 'subtitulo': 'Masterclass com Aaron Ross', 'thumbnail': 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=600&q=80', 'duracao': '2h 15min', 'xp': 200, 'participantes': 1240, 'ordem': 0},
            {'tipo': 'recommended', 'titulo': 'Liderança na Prática', 'subtitulo': 'Curso completo • 8 módulos', 'thumbnail': 'https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=600&q=80', 'duracao': '6h', 'xp': 450, 'participantes': 890, 'ordem': 1},
            {'tipo': 'recommended', 'titulo': 'Branding Pessoal', 'subtitulo': 'Construa sua marca', 'thumbnail': 'https://images.unsplash.com/photo-1493612276216-ee3925520721?w=600&q=80', 'duracao': '3h 30min', 'xp': 280, 'participantes': 2100, 'ordem': 2},
            {'tipo': 'collab', 'titulo': 'G4 Educação x MUNDU', 'subtitulo': 'Gestão de Alta Performance', 'thumbnail': 'https://images.unsplash.com/photo-1542744173-8e7e53415bb0?w=600&q=80', 'duracao': '4h', 'xp': 600, 'participantes': 3200, 'badge': 'Exclusivo', 'ordem': 0},
            {'tipo': 'collab', 'titulo': 'StartSe Partnership', 'subtitulo': 'Inovação e Tecnologia', 'thumbnail': 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=600&q=80', 'duracao': '3h 20min', 'xp': 500, 'participantes': 1890, 'badge': 'Novo', 'ordem': 1},
            {'tipo': 'case', 'titulo': 'Como cresci 300% em 6 meses', 'subtitulo': 'por Lucas Ferreira • Case aprovado', 'thumbnail': 'https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=600&q=80', 'xp': 100, 'participantes': 456, 'badge': 'Case Oficial', 'ordem': 0},
            {'tipo': 'case', 'titulo': 'Estratégia de Comunidade', 'subtitulo': 'por Marina Costa • Case aprovado', 'thumbnail': 'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=600&q=80', 'xp': 100, 'participantes': 312, 'badge': 'Case Oficial', 'ordem': 1},
        ]
        for dados in items:
            FeaturedContent.objects.get_or_create(
                titulo=dados['titulo'],
                defaults=dados
            )
        self.stdout.write(f'  OK: {len(items)} conteúdos em destaque criados')

    def _seed_aulas(self):
        youtube_ids = {
            'Fundamentos de Marketing Digital': [
                '3q3k65Bk9mk', 'B2VzLby_jyI', '1W3ddFmh1hA', 'a5GCiEsVFGc',
            ],
            'Copywriting Avançado': [
                'dQw4w9WgXcQ', 'jNQXAC9IVRw', 'kJQP7kiw5Fk',
            ],
            'Gestão de Tráfego Pago': [
                '9bZkp7q19f0', 'JGwWNGJdvx8', 'RgKAFK5djSk', 'hT_nvWreIhg',
            ],
            'Vendas Consultivas B2B': [
                'kXYiU_JCYtU', 'CevxZvSJLk8', 'lp-EO5I60KA',
            ],
            'Negociação Avançada': [
                'fJ9rUzIMcZQ', 'dQw4w9WgXcQ',
            ],
            'SEO e Conteúdo Orgânico': [
                'hF515-0Tduk', 'YQHsXMglC9A', 'lx6UqJ3hGk4',
            ],
        }
        created = 0
        ordem_counter = {}
        for modulo in Modulo.objects.all():
            ids = youtube_ids.get(modulo.titulo, [])
            ordem_counter[modulo.id] = 1
            for vid in ids:
                aula, was = Aula.objects.get_or_create(
                    modulo=modulo, ordem=ordem_counter[modulo.id],
                    defaults={
                        'titulo': f'{modulo.titulo} — Aula {ordem_counter[modulo.id]}',
                        'descricao': f'{modulo.titulo} — aula prática número {ordem_counter[modulo.id]}.',
                        'url_video': f'https://www.youtube.com/watch?v={vid}',
                        'duracao': f'{10 + ordem_counter[modulo.id] % 20} min',
                        'is_preview': ordem_counter[modulo.id] == 1,
                    }
                )
                if was:
                    created += 1
                ordem_counter[modulo.id] += 1
        self.stdout.write(f'  OK: {created} aulas criadas')

    def _seed_certificados(self):
        user = User.objects.filter(is_superuser=True).first()
        if not user:
            self.stdout.write('  SKIP: nenhum admin encontrado para certificados')
            return
        mods = Modulo.objects.all()[:2]
        for m in mods:
            Certificate.objects.get_or_create(
                usuario=user, modulo=m,
                defaults={'codigo': f'CERT-{m.id}-{secrets.token_hex(4).upper()}'}
            )
        self.stdout.write(f'  OK: {len(mods)} certificados criados')

    def _seed_quizzes(self):
        qdata = [
            {'modulo_titulo': 'Fundamentos de Marketing Digital', 'titulo': 'Fundamentos de Marketing', 'xp_total': 100, 'questoes': [
                {'enunciado': 'O que é Marketing Digital?', 'alternativas': [
                    ('Conjunto de estratégias de marketing no ambiente digital', True),
                    ('Apenas anúncios no Google', False),
                    ('Vender produtos em lojas físicas', False),
                    ('Usar apenas redes sociais', False),
                ]},
                {'enunciado': 'SEO significa Search Engine Optimization.', 'tipo': 'verdadeiro_falso', 'alternativas': [
                    ('Verdadeiro', True), ('Falso', False),
                ]},
                {'enunciado': 'Qual é o principal objetivo do funil de marketing?', 'alternativas': [
                    ('Guiar o lead até a conversão', True),
                    ('Aumentar seguidores no Instagram', False),
                    ('Criar conteúdo viral', False),
                    ('Reduzir custos operacionais', False),
                ]},
            ]},
            {'modulo_titulo': 'Gestão de Tráfego Pago', 'titulo': 'Tráfego Pago', 'xp_total': 150, 'questoes': [
                {'enunciado': 'O que é CTR?', 'alternativas': [
                    ('Click Through Rate — taxa de cliques', True),
                    ('Cost Total Revenue', False),
                    ('Conversion Tracking Rate', False),
                    ('Customer Turnover Ratio', False),
                ]},
                {'enunciado': 'Qual plataforma é mais indicada para campanhas B2B?', 'alternativas': [
                    ('LinkedIn Ads', True),
                    ('TikTok Ads', False),
                    ('Snapchat Ads', False),
                    ('Pinterest Ads', False),
                ]},
                {'enunciado': 'ROAS é a métrica que calcula o retorno sobre o investimento em anúncios.', 'tipo': 'verdadeiro_falso', 'alternativas': [
                    ('Verdadeiro', True), ('Falso', False),
                ]},
            ]},
        ]
        for qd in qdata:
            mod = Modulo.objects.filter(titulo=qd['modulo_titulo']).first()
            if not mod:
                continue
            quiz, _ = Quiz.objects.get_or_create(modulo=mod, titulo=qd['titulo'], defaults={'xp_total': qd['xp_total']})
            for i, q in enumerate(qd['questoes']):
                questao, _ = Questao.objects.get_or_create(quiz=quiz, enunciado=q['enunciado'][:50], defaults={
                    'tipo': q.get('tipo', 'multipla_escolha'), 'ordem': i,
                })
                for j, (texto, correta) in enumerate(q['alternativas']):
                    Alternativa.objects.get_or_create(questao=questao, ordem=j, defaults={'texto': texto, 'correta': correta})
        self.stdout.write('  OK: quizzes criados')
