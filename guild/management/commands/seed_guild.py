from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth.models import User


COMMUNITIES = [
    {"slug": "gestao-pessoas", "name": "Gestão de Pessoas", "members": 3420, "posts_today": 28, "online_now": 142, "icon": "users", "color": "primary", "description": "Para quem lidera gente — feedbacks, 1:1s, contratação e cultura.", "description_long": "A casa de quem lidera pessoas. Aqui debatemos casos reais de feedback, conflito, contratação, ramp-up de novos contratados, cultura de time e tudo o que envolve a parte humana da liderança.", "rules": ["Casos reais > opiniões abstratas. Se não viveu, não posta.", "Anonimize nomes de empresas e pessoas envolvidas.", "Resposta com framework cita a fonte (Library, Feed, livro).", "Sem auto-promoção fora da quinta-feira de divulgação."], "moderators": ["mariana-reis", "diego-almeida"], "created_at": "Jan 2024", "related": ["soft-skills", "carreira-inicial"]},
    {"slug": "tech-produto", "name": "Tech & Produto", "members": 2780, "posts_today": 41, "online_now": 218, "icon": "cpu", "color": "secondary", "description": "Engenharia, produto, design e a interseção entre eles.", "description_long": "Para quem constrói: devs, PMs, designers e tech leads. Casos de arquitetura, ritual de time, métricas de produto, design system.", "rules": ["Stack-agnóstico — discuta o problema antes da ferramenta.", "Code reviews ficam em PR, não aqui.", "Mostre métricas quando for falar de impacto."], "moderators": ["pedro-vianna"], "created_at": "Fev 2024", "related": ["empreendedorismo", "vendas-growth"]},
    {"slug": "soft-skills", "name": "Soft Skills", "members": 4120, "posts_today": 19, "online_now": 88, "icon": "sparkles", "color": "accent", "description": "Comunicação, negociação, presença executiva e mindset.", "rules": ["Práticas, não filosofias. Traga o que vai usar amanhã.", "Storytelling sim, autoajuda não."], "moderators": ["diego-almeida"], "created_at": "Jan 2024", "related": ["gestao-pessoas", "carreira-inicial"]},
    {"slug": "empreendedorismo", "name": "Empreendedorismo", "members": 1980, "posts_today": 33, "online_now": 167, "icon": "rocket", "color": "primary", "description": "Founders, sócios e quem tá tirando ideia do papel.", "rules": ["Pitch de produto vai em /sextou", "Compartilhe métrica antes de pedir conselho."], "moderators": ["camila-souza"], "created_at": "Jan 2024", "related": ["vendas-growth", "tech-produto"]},
    {"slug": "carreira-inicial", "name": "Carreira Inicial", "members": 5230, "posts_today": 52, "online_now": 311, "icon": "graduation-cap", "color": "secondary", "description": "Para o time de 16-30 anos: primeiro emprego, transição e crescimento.", "rules": ["Pergunta boba é a mais respondida.", "Salário e oferta sempre podem virar thread.", "Nada de printscreen de currículo público."], "moderators": ["bruno-tavares", "mariana-reis"], "created_at": "Dez 2023", "related": ["soft-skills", "tech-produto"]},
    {"slug": "vendas-growth", "name": "Vendas & Growth", "members": 1670, "posts_today": 22, "online_now": 94, "icon": "trending-up", "color": "accent", "description": "Pipeline, prospecção, copy e tudo que faz a receita crescer.", "rules": ["Sem cold pitch para a comunidade.", "Compartilhe número (taxa, ROI) quando for case."], "moderators": ["camila-souza"], "created_at": "Fev 2024", "related": ["empreendedorismo", "tech-produto"]},
]

THREADS = [
    {"community_slug": "gestao-pessoas", "slug": "1-1-com-alguem-que-nao-confia", "title": "Como vocês conduzem 1:1 com alguém que não confia em você ainda?", "author": "mariana-reis", "body": "Acabei de assumir um time herdado de 9 devs e percebi que duas pessoas estão claramente na defensiva.\n\n**Pergunta concreta**: vocês começam o 1:1 falando do trabalho ou da pessoa?", "tag": "discussão", "upvotes": 128, "created_delta": 2},
    {"community_slug": "carreira-inicial", "slug": "wrap-em-2-ofertas-funcionou", "title": "Aplicando o framework WRAP para escolher entre 2 ofertas de emprego — funcionou", "author": "bruno-tavares", "body": "Compartilhando o caso porque o método salvou minha decisão.\n\n**Contexto**: 24 anos, estagiário virando CLT em uma. Recebi outra oferta 55% maior...", "tag": "case", "upvotes": 89, "created_delta": 5},
    {"community_slug": "empreendedorismo", "slug": "aumentei-30-pct-e-perdi-5", "title": "Pricing: por que aumentei 30% e perdi só 5% dos clientes", "author": "camila-souza", "body": "Inspirada no resumo da Marina Costa (Library), refiz minha tabela de preços usando a Value Ladder.\n\n**Antes**: 1 plano de R$199/mês...", "tag": "case", "upvotes": 215, "created_delta": 8},
    {"community_slug": "soft-skills", "slug": "conflict-canvas-preenchido", "title": "Alguém usa o Conflict Canvas? Compartilho o meu preenchido", "author": "diego-almeida", "body": "Tive uma conversa difícil com meu CTO essa semana sobre uma decisão técnica que eu discordava...", "tag": "framework", "upvotes": 76, "created_delta": 24},
    {"community_slug": "tech-produto", "slug": "standup-9min-time-de-12", "title": "Stand-up de 9 min funciona pra time de 12? Estamos testando", "author": "pedro-vianna", "body": "Adaptamos o template do Rafael Santos pro nosso time de 12.\n\n**Adaptações**:...", "tag": "discussão", "upvotes": 102, "created_delta": 30},
]

COMMENTS_DATA = {
    "1-1-com-alguem-que-nao-confia": [
        {"author": "diego-almeida", "body": "3 meses é a média. Mas tem um truque: comece pelo que eles fizeram bem na semana. Tira a defensiva sem invadir.", "upvotes": 47, "created_delta": 1, "children": [
            {"author": "mariana-reis", "body": "Vou testar amanhã. Faz sentido.", "upvotes": 12, "created_delta": 1.5, "children": []},
            {"author": "pedro-vianna", "body": "Faço algo parecido — abro com 'me conta algo que ninguém viu'.", "upvotes": 9, "created_delta": 2, "children": []},
        ]},
        {"author": "camila-souza", "body": "Eu tive caso similar e o que mudou foi parar de fazer 1:1 toda semana.", "upvotes": 28, "created_delta": 1.2, "children": []},
        {"author": "bruno-tavares", "body": "Falando do outro lado: silêncio às vezes é só timidez.", "upvotes": 19, "created_delta": 1.5, "children": []},
    ],
    "wrap-em-2-ofertas-funcionou": [
        {"author": "camila-souza", "body": "Parabéns pela maturidade da decisão!", "upvotes": 34, "created_delta": 4, "children": []},
        {"author": "diego-almeida", "body": "A parte de 'Prepare to be wrong' é a mais subestimada.", "upvotes": 21, "created_delta": 5, "children": []},
    ],
    "aumentei-30-pct-e-perdi-5": [
        {"author": "lucas-pestana", "body": "A âncora do Scale a R$549 é um golpe de mestre.", "upvotes": 47, "created_delta": 7, "children": []},
        {"author": "marina-costa", "body": "Fico feliz que o resumo ajudou!", "upvotes": 39, "created_delta": 8, "children": []},
    ],
    "conflict-canvas-preenchido": [
        {"author": "ana-lima", "body": "O que eu temo perder mudou minha carreira como coach.", "upvotes": 31, "created_delta": 20, "children": []},
    ],
    "standup-9min-time-de-12": [
        {"author": "rafael-santos", "body": "Legal que adaptaram!", "upvotes": 18, "created_delta": 12, "children": []},
        {"author": "mariana-reis", "body": "Aqui resolvemos abrindo com 'alguém tem algo fora do radar?'.", "upvotes": 14, "created_delta": 14, "children": []},
    ],
}


class Command(BaseCommand):
    help = 'Seeds guild data (communities, threads, comments)'

    def handle(self, *args, **options):
        from guild.models import Community, Thread, Comment

        for data in COMMUNITIES:
            Community.objects.update_or_create(
                slug=data["slug"],
                defaults=data,
            )
        self.stdout.write(f'Created {len(COMMUNITIES)} communities')

        now = timezone.now()
        for data in THREADS:
            community = Community.objects.get(slug=data["community_slug"])
            preview = data["body"][:150] if data["body"] else ""
            created = now - timezone.timedelta(hours=data["created_delta"])
            thread, _ = Thread.objects.update_or_create(
                slug=data["slug"],
                community=community,
                defaults={
                    "title": data["title"],
                    "author_handle": data["author"],
                    "body": data["body"],
                    "preview": preview,
                    "tag": data["tag"],
                    "upvotes": data["upvotes"],
                    "created_at": created,
                },
            )
            # Seed comments
            thread_comments = COMMENTS_DATA.get(data["slug"], [])
            _seed_comments(thread, thread_comments, None, now, data["created_delta"])

        self.stdout.write(f'Created {len(THREADS)} threads with comments')


def _seed_comments(thread, comments_list, parent, now, thread_hours_ago):
    from guild.models import Comment
    for i, data in enumerate(comments_list):
        created = now - timezone.timedelta(hours=data["created_delta"])
        comment = Comment.objects.create(
            thread=thread,
            parent=parent,
            author_handle=data["author"],
            body=data["body"],
            upvotes=data["upvotes"],
            created_at=created,
        )
        _seed_comments(thread, data.get("children", []), comment, now, thread_hours_ago)
