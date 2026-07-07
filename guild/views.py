from core.utils import render
from django.http import Http404

USERS = {
    "gabriel": {"handle": "gabriel", "nome_completo": "Gabriel Lasaro", "iniciais": "GL", "role": "Estrategista · V4 Company", "bio": "Aprendendo liderança em público. Coleciono frameworks que sobrevivem ao mundo real.", "karma": 1420, "joined_at": "Jan 2024", "followers": 87, "following": 142, "is_self": True},
    "mariana-reis": {"handle": "mariana-reis", "nome_completo": "Mariana Reis", "iniciais": "MR", "role": "Tech Lead · Stone", "bio": "Liderando squad de 9 devs há 2 anos.", "karma": 3890, "joined_at": "Mar 2023", "followers": 412, "following": 89},
    "bruno-tavares": {"handle": "bruno-tavares", "nome_completo": "Bruno Tavares", "iniciais": "BT", "role": "Estagiário em transição · 24 anos", "bio": "Primeiro emprego há 8 meses.", "karma": 678, "joined_at": "Set 2024", "followers": 56, "following": 203},
    "camila-souza": {"handle": "camila-souza", "nome_completo": "Camila Souza", "iniciais": "CS", "role": "Founder · SaaS B2B", "bio": "Levei 3 anos pra entender pricing.", "karma": 5120, "joined_at": "Jul 2022", "followers": 890, "following": 76},
    "diego-almeida": {"handle": "diego-almeida", "nome_completo": "Diego Almeida", "iniciais": "DA", "role": "Coach Executivo", "bio": "Especialista em conversas difíceis.", "karma": 2340, "joined_at": "Mai 2023", "followers": 234, "following": 112},
    "pedro-vianna": {"handle": "pedro-vianna", "nome_completo": "Pedro Vianna", "iniciais": "PV", "role": "Eng Manager · 12 devs", "bio": "Time grande, ritual curto.", "karma": 1780, "joined_at": "Out 2023", "followers": 145, "following": 89},
    "camila-faria": {"handle": "camila-faria", "nome_completo": "Camila Faria", "iniciais": "CF", "role": "Head de Pessoas · Ex-Nubank", "bio": "10 anos liderando times de gente.", "karma": 8920, "joined_at": "Jan 2024", "followers": 4310, "following": 56, "is_creator": True},
    "lucas-pestana": {"handle": "lucas-pestana", "nome_completo": "Lucas Pestana", "iniciais": "LP", "role": "Founder · Vertical SaaS", "bio": "Já contratei errado mais vezes que acertei.", "karma": 5640, "joined_at": "Fev 2024", "followers": 2180, "following": 102, "is_creator": True},
    "marina-costa": {"handle": "marina-costa", "nome_completo": "Marina Costa", "iniciais": "MC", "role": "Estrategista de Pricing", "bio": "Cobrar bem é justiça com seu produto.", "karma": 7340, "joined_at": "Jan 2024", "followers": 3870, "following": 89, "is_creator": True},
    "pedro-mendes": {"handle": "pedro-mendes", "nome_completo": "Pedro Mendes", "iniciais": "PM", "role": "Professor Convidado · Harvard Online", "bio": "Método de caso é meu martelo.", "karma": 6180, "joined_at": "Mar 2024", "followers": 2950, "following": 23, "is_creator": True},
    "rafael-santos": {"handle": "rafael-santos", "nome_completo": "Rafael Santos", "iniciais": "RS", "role": "Tech Lead · Stone", "bio": "Engenharia humana. Rituals de time que respiram.", "karma": 4290, "joined_at": "Fev 2024", "followers": 1620, "following": 78, "is_creator": True},
    "ana-lima": {"handle": "ana-lima", "nome_completo": "Ana Lima", "iniciais": "AL", "role": "Coach Executiva", "bio": "Conversa difícil é minha especialidade.", "karma": 5120, "joined_at": "Jan 2024", "followers": 2410, "following": 64, "is_creator": True},
}

guild_communities = [
    {"id": "c1", "slug": "gestao-pessoas", "name": "Gestão de Pessoas", "members": 3420, "posts_today": 28, "online_now": 142, "icon": "users", "color": "primary", "description": "Para quem lidera gente — feedbacks, 1:1s, contratação e cultura.", "description_long": "A casa de quem lidera pessoas. Aqui debatemos casos reais de feedback, conflito, contratação, ramp-up de novos contratados, cultura de time e tudo o que envolve a parte humana da liderança. Curadoria leve — todo post precisa trazer um caso ou pergunta concreta.", "rules": ["Casos reais > opiniões abstratas. Se não viveu, não posta.", "Anonimize nomes de empresas e pessoas envolvidas.", "Resposta com framework cita a fonte (Library, Feed, livro).", "Sem auto-promoção fora da quinta-feira de divulgação."], "moderators": ["mariana-reis", "diego-almeida"], "created_at": "Jan 2024", "related": ["soft-skills", "carreira-inicial"]},
    {"id": "c2", "slug": "tech-produto", "name": "Tech & Produto", "members": 2780, "posts_today": 41, "online_now": 218, "icon": "cpu", "color": "secondary", "description": "Engenharia, produto, design e a interseção entre eles.", "description_long": "Para quem constrói: devs, PMs, designers e tech leads. Casos de arquitetura, ritual de time, métricas de produto, design system — desde que tragam aprendizado replicável.", "rules": ["Stack-agnóstico — discuta o problema antes da ferramenta.", "Code reviews ficam em PR, não aqui.", "Mostre métricas quando for falar de impacto."], "moderators": ["pedro-vianna"], "created_at": "Fev 2024", "related": ["empreendedorismo", "vendas-growth"]},
    {"id": "c3", "slug": "soft-skills", "name": "Soft Skills", "members": 4120, "posts_today": 19, "online_now": 88, "icon": "sparkles", "color": "accent", "description": "Comunicação, negociação, presença executiva e mindset.", "description_long": "O músculo invisível que decide promoções. Discutimos negociação, conversas difíceis, comunicação executiva, gestão de energia e tudo que não está no contrato mas pesa todo dia.", "rules": ["Práticas, não filosofias. Traga o que vai usar amanhã.", "Storytelling sim, autoajuda não."], "moderators": ["diego-almeida"], "created_at": "Jan 2024", "related": ["gestao-pessoas", "carreira-inicial"]},
    {"id": "c4", "slug": "empreendedorismo", "name": "Empreendedorismo", "members": 1980, "posts_today": 33, "online_now": 167, "icon": "rocket", "color": "primary", "description": "Founders, sócios e quem tá tirando ideia do papel.", "description_long": "Founder solo, co-founder, primeiro CEO contratado. Validação, primeiro hire, primeiro cliente B2B, captação. Foco em decisão real com dado real.", "rules": ["Pitch de produto vai em /sextou", "Compartilhe métrica antes de pedir conselho."], "moderators": ["camila-souza"], "created_at": "Jan 2024", "related": ["vendas-growth", "tech-produto"]},
    {"id": "c5", "slug": "carreira-inicial", "name": "Carreira Inicial", "members": 5230, "posts_today": 52, "online_now": 311, "icon": "graduation-cap", "color": "secondary", "description": "Para o time de 16-30 anos: primeiro emprego, transição e crescimento.", "description_long": "A maior comunidade da Mundu. Aqui estão os early-career: estagiários, juniores, recém-formados e quem está mudando de área aos 30. Pergunta crua é bem-vinda.", "rules": ["Pergunta boba é a mais respondida.", "Salário e oferta sempre podem virar thread.", "Nada de printscreen de currículo público."], "moderators": ["bruno-tavares", "mariana-reis"], "created_at": "Dez 2023", "related": ["soft-skills", "tech-produto"]},
    {"id": "c6", "slug": "vendas-growth", "name": "Vendas & Growth", "members": 1670, "posts_today": 22, "online_now": 94, "icon": "trending-up", "color": "accent", "description": "Pipeline, prospecção, copy e tudo que faz a receita crescer.", "description_long": "SDRs, AEs, growth marketers, founders que vendem. Casos de outbound, copy que converteu, ICP refinado.", "rules": ["Sem cold pitch para a comunidade.", "Compartilhe número (taxa, ROI) quando for case."], "moderators": ["camila-souza"], "created_at": "Fev 2024", "related": ["empreendedorismo", "tech-produto"]},
]

guild_threads = [
    {"id": "t1", "slug": "1-1-com-alguem-que-nao-confia", "title": "Como vocês conduzem 1:1 com alguém que não confia em você ainda?", "author": "mariana-reis", "community_slug": "gestao-pessoas", "community": "Gestão de Pessoas", "time_ago": "há 2h", "replies": 34, "upvotes": 128, "tag": "discussão", "post_type": "text", "preview": "Acabei de assumir um time herdado e percebi que duas pessoas estão na defensiva. Já vi o vídeo da Camila Faria sobre feedback...", "body": "Acabei de assumir um time herdado de 9 devs e percebi que duas pessoas estão claramente na defensiva...\n\n**Pergunta concreta**: vocês começam o 1:1 falando do trabalho ou da pessoa?"},
    {"id": "t2", "slug": "wrap-em-2-ofertas-funcionou", "title": "Aplicando o framework WRAP para escolher entre 2 ofertas de emprego — funcionou", "author": "bruno-tavares", "community_slug": "carreira-inicial", "community": "Carreira Inicial", "time_ago": "há 5h", "replies": 18, "upvotes": 89, "tag": "case", "post_type": "text", "preview": "Compartilhando o caso porque o método salvou minha decisão. Usei as 4 etapas do WRAP em uma planilha simples...", "body": "Compartilhando o caso porque o método salvou minha decisão.\n\n**Contexto**: 24 anos, estagiário virando CLT em uma. Recebi outra oferta 55% maior..."},
    {"id": "t3", "slug": "aumentei-30-pct-e-perdi-5", "title": "Pricing: por que aumentei 30% e perdi só 5% dos clientes", "author": "camila-souza", "community_slug": "empreendedorismo", "community": "Empreendedorismo", "time_ago": "há 8h", "replies": 47, "upvotes": 215, "tag": "case", "post_type": "text", "preview": "Inspirada no resumo da Marina Costa, refiz minha tabela de preços usando a Value Ladder. Resultado abaixo...", "body": "Inspirada no resumo da Marina Costa (Library), refiz minha tabela de preços usando a Value Ladder.\n\n**Antes**: 1 plano de R$199/mês..."},
    {"id": "t4", "slug": "conflict-canvas-preenchido", "title": "Alguém usa o Conflict Canvas? Compartilho o meu preenchido", "author": "diego-almeida", "community_slug": "soft-skills", "community": "Soft Skills", "time_ago": "ontem", "replies": 22, "upvotes": 76, "tag": "framework", "post_type": "text", "preview": "Tive uma conversa difícil com meu CTO essa semana. Preenchi o canvas antes e o efeito foi notável...", "body": "Tive uma conversa difícil com meu CTO essa semana sobre uma decisão técnica que eu discordava..."},
    {"id": "t5", "slug": "standup-9min-time-de-12", "title": "Stand-up de 9 min funciona pra time de 12? Estamos testando", "author": "pedro-vianna", "community_slug": "tech-produto", "community": "Tech & Produto", "time_ago": "ontem", "replies": 31, "upvotes": 102, "tag": "discussão", "post_type": "text", "preview": "Adaptamos o template do Rafael Santos. Com 12 pessoas, demos um cap de 30s por update e está dando certo...", "body": "Adaptamos o template do Rafael Santos (Feed) pro nosso time de 12.\n\n**Adaptações**:..."},
]

COMMENTS = {
    "t1": [
        {"id": "cm1", "author": "diego-almeida", "body": "3 meses é a média que eu vejo na coachada. Mas tem um truque: não comece pelo trabalho nem pela vida pessoal — comece pelo **que eles fizeram bem na semana**. Tira a defensiva sem invadir.", "upvotes": 47, "time_ago": "há 1h", "children": [
            {"id": "cm1a", "author": "mariana-reis", "body": "Vou testar amanhã. Faz sentido — começar reconhecendo desarma sem ser pessoal demais.", "upvotes": 12, "time_ago": "há 45min", "children": []},
            {"id": "cm1b", "author": "pedro-vianna", "body": "Faço algo parecido — abro com 'me conta uma coisa que tu construiu essa semana que ninguém viu'. Funciona pra dev porque dev sempre quer mostrar código.", "upvotes": 9, "time_ago": "há 30min", "children": []},
        ]},
        {"id": "cm2", "author": "camila-souza", "body": "Eu tive caso similar e o que mudou foi parar de fazer 1:1 toda semana. Marquei a cada 2 semanas e o intervalo respirou.", "upvotes": 28, "time_ago": "há 1h", "children": []},
        {"id": "cm3", "author": "bruno-tavares", "body": "Falando do outro lado (sou liderado): silêncio às vezes é só timidez. Pergunta direta ajuda mais que pergunta aberta.", "upvotes": 19, "time_ago": "há 50min", "children": []},
    ],
    "t2": [
        {"id": "cm4", "author": "camila-souza", "body": "Parabéns pela maturidade da decisão! O W é o mais difícil — a maioria nem cogita alternativa.", "upvotes": 34, "time_ago": "há 4h", "children": []},
        {"id": "cm5", "author": "diego-almeida", "body": "A parte de 'Prepare to be wrong' é a mais subestimada. Ter plano B tira a ansiedade da escolha.", "upvotes": 21, "time_ago": "há 3h", "children": []},
    ],
    "t3": [
        {"id": "cm6", "author": "lucas-pestana", "body": "A âncora do Scale a R$549 é um golpe de mestre. O Pro fica barato por comparação, não por valor absoluto.", "upvotes": 47, "time_ago": "há 7h", "children": []},
        {"id": "cm7", "author": "marina-costa", "body": "Fico feliz que o resumo ajudou! O dado de 5% de churn é raro — a maioria das pessoas tem medo do desconto e nem testa.", "upvotes": 39, "time_ago": "há 6h", "children": []},
        {"id": "cm8", "author": "pedro-mendes", "body": "Case show! O maior aprendizado é que cliente não compra barato — compra valor. Você precificou o valor que entrega.", "upvotes": 28, "time_ago": "há 5h", "children": []},
    ],
    "t4": [
        {"id": "cm9", "author": "ana-lima", "body": "O que eu temo perder mudou minha carreira como coach. Ver líderes usando isso é gratificante demais.", "upvotes": 31, "time_ago": "há 20h", "children": []},
    ],
    "t5": [
        {"id": "cm10", "author": "rafael-santos", "body": "Legal que adaptaram! Sobre o trade-off: a solução não é alongar a daily, é criar um canal async de 'riscos silenciosos'.", "upvotes": 18, "time_ago": "há 12h", "children": []},
        {"id": "cm11", "author": "mariana-reis", "body": "Aqui no time (11 devs) resolvemos abrindo a daily com 'alguém tem algo fora do radar?'. Isso captura o que não cabe no update.", "upvotes": 14, "time_ago": "há 10h", "children": []},
    ],
}


def get_user(handle):
    user = USERS.get(handle)
    if user is None:
        return {
            "handle": handle,
            "nome_completo": "Membro Mundu",
            "iniciais": handle[:2].upper(),
            "role": "Membro",
            "bio": "",
            "karma": 0,
            "joined_at": "",
            "followers": 0,
            "following": 0,
        }
    return user


def _enrich_post(post):
    post = post.copy()
    post["author_user"] = get_user(post["author"])
    return post


def _enrich_comment(comment):
    comment = comment.copy()
    comment["author_user"] = get_user(comment["author"])
    comment["children"] = [_enrich_comment(c) for c in comment.get("children", [])]
    return comment


def _count_comments(comment_list):
    total = 0
    for c in comment_list:
        total += 1
        total += _count_comments(c.get("children", []))
    return total


def guild_home(request):
    threads = [_enrich_post(t) for t in guild_threads]
    ctx = {
        "communities": guild_communities,
        "threads": threads,
    }
    return render(request, "guild.html", ctx)


def community_detail(request, slug):
    community = None
    for c in guild_communities:
        if c["slug"] == slug:
            community = c
            break
    if community is None:
        raise Http404("Comunidade não encontrada")

    sort = request.GET.get("sort", "hot")
    posts = [p for p in guild_threads if p["community_slug"] == slug]
    if sort == "new":
        posts = sorted(posts, key=lambda p: p["time_ago"])
    elif sort == "top":
        posts = sorted(posts, key=lambda p: p["upvotes"], reverse=True)
    else:
        posts = sorted(posts, key=lambda p: p["upvotes"], reverse=True)

    posts = [_enrich_post(p) for p in posts]

    related = [c for c in guild_communities if c["slug"] in community.get("related", [])]
    moderators = [get_user(h) for h in community.get("moderators", [])]

    ctx = {
        "community": community,
        "posts": posts,
        "sort": sort,
        "related_communities": related,
        "moderators": moderators,
    }
    return render(request, "community.html", ctx)


def thread_detail(request, community_slug, post_slug):
    community = None
    for c in guild_communities:
        if c["slug"] == community_slug:
            community = c
            break
    if community is None:
        raise Http404("Comunidade não encontrada")

    post = None
    for p in guild_threads:
        if p["slug"] == post_slug and p["community_slug"] == community_slug:
            post = p
            break
    if post is None:
        raise Http404("Post não encontrado")

    post = _enrich_post(post)

    raw_comments = COMMENTS.get(post["id"], [])
    comments = [_enrich_comment(c) for c in raw_comments]
    total_comments = _count_comments(comments)

    related = [c for c in guild_communities if c["slug"] in community.get("related", [])]
    moderators = [get_user(h) for h in community.get("moderators", [])]

    ctx = {
        "community": community,
        "post": post,
        "comments": comments,
        "total_comments": total_comments,
        "related_communities": related,
        "moderators": moderators,
    }
    return render(request, "thread.html", ctx)
