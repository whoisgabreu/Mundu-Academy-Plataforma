from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from core.utils import render, NOTIFICATIONS
from cursos.models import Modulo, Trilha, TrilhaModulo, Desafio, ProgressoModulo, ProgressoDesafio


USERS = {
    "gabriel": {"handle": "gabriel", "nome_completo": "Gabriel Lasaro", "iniciais": "GL", "role": "Estrategista · V4 Company", "bio": "Aprendendo liderança em público. Coleciono frameworks que sobrevivem ao mundo real.", "karma": 1420, "joined_at": "Jan 2024", "followers": 87, "following": 142, "is_self": True},
    "mariana-reis": {"handle": "mariana-reis", "nome_completo": "Mariana Reis", "iniciais": "MR", "role": "Tech Lead · Stone", "bio": "Liderando squad de 9 devs há 2 anos.", "karma": 3890, "joined_at": "Mar 2023", "followers": 412, "following": 89},
    "bruno-tavares": {"handle": "bruno-tavares", "nome_completo": "Bruno Tavares", "iniciais": "BT", "role": "Estagiário em transição · 24 anos", "bio": "Primeiro emprego há 8 meses.", "karma": 678, "joined_at": "Set 2024", "followers": 56, "following": 203},
    "camila-souza": {"handle": "camila-souza", "nome_completo": "Camila Souza", "iniciais": "CS", "role": "Founder · SaaS B2B", "bio": "Levei 3 anos pra entender pricing.", "karma": 5120, "joined_at": "Jul 2022", "followers": 890, "following": 76},
    "diego-almeida": {"handle": "diego-almeida", "nome_completo": "Diego Almeida", "iniciais": "DA", "role": "Coach Executivo", "bio": "Especialista em conversas difíceis.", "karma": 2340, "joined_at": "Mai 2023", "followers": 234, "following": 112},
    "camila-faria": {"handle": "camila-faria", "nome_completo": "Camila Faria", "iniciais": "CF", "role": "Head de Pessoas · Ex-Nubank", "bio": "10 anos liderando times de gente.", "karma": 8920, "joined_at": "Jan 2024", "followers": 4310, "following": 56, "is_creator": True},
    "lucas-pestana": {"handle": "lucas-pestana", "nome_completo": "Lucas Pestana", "iniciais": "LP", "role": "Founder · Vertical SaaS", "bio": "Já contratei errado mais vezes que acertei.", "karma": 5640, "joined_at": "Fev 2024", "followers": 2180, "following": 102, "is_creator": True},
    "marina-costa": {"handle": "marina-costa", "nome_completo": "Marina Costa", "iniciais": "MC", "role": "Estrategista de Pricing", "bio": "Cobrar bem é justiça com seu produto.", "karma": 7340, "joined_at": "Jan 2024", "followers": 3870, "following": 89, "is_creator": True},
    "pedro-mendes": {"handle": "pedro-mendes", "nome_completo": "Pedro Mendes", "iniciais": "PM", "role": "Professor Convidado · Harvard Online", "bio": "Método de caso é meu martelo.", "karma": 6180, "joined_at": "Mar 2024", "followers": 2950, "following": 23, "is_creator": True},
    "rafael-santos": {"handle": "rafael-santos", "nome_completo": "Rafael Santos", "iniciais": "RS", "role": "Tech Lead · Stone", "bio": "Engenharia humana. Rituals de time que respiram.", "karma": 4290, "joined_at": "Fev 2024", "followers": 1620, "following": 78, "is_creator": True},
    "ana-lima": {"handle": "ana-lima", "nome_completo": "Ana Lima", "iniciais": "AL", "role": "Coach Executiva", "bio": "Conversa difícil é minha especialidade.", "karma": 5120, "joined_at": "Jan 2024", "followers": 2410, "following": 64, "is_creator": True},
}

def get_user(handle):
    return USERS.get(handle, {"handle": handle, "nome_completo": handle.replace("-", " ").title(), "iniciais": (handle[:2] if handle else "?").upper(), "role": "Membro Mundu", "bio": "", "karma": 0, "joined_at": "—", "followers": 0, "following": 0})


guild_communities = [
    {"id": "c1", "slug": "gestao-pessoas", "name": "Gestão de Pessoas", "members": 3420, "posts_today": 28, "online_now": 142, "icon": "users", "color": "primary", "description": "Para quem lidera gente — feedbacks, 1:1s, contratação e cultura.", "description_long": "A casa de quem lidera pessoas.", "rules": ["Casos reais > opiniões abstratas. Se não viveu, não posta.", "Anonimize nomes de empresas e pessoas envolvidas.", "Resposta com framework cita a fonte (Library, Feed, livro).", "Sem auto-promoção fora da quinta-feira de divulgação."], "moderators": ["mariana-reis", "diego-almeida"], "created_at": "Jan 2024", "related": ["soft-skills", "carreira-inicial"]},
    {"id": "c2", "slug": "tech-produto", "name": "Tech & Produto", "members": 2780, "posts_today": 41, "online_now": 218, "icon": "cpu", "color": "secondary", "description": "Engenharia, produto, design e a interseção entre eles.", "description_long": "Para quem constrói: devs, PMs, designers e tech leads.", "rules": ["Stack-agnóstico — discuta o problema antes da ferramenta.", "Code reviews ficam em PR, não aqui.", "Mostre métricas quando for falar de impacto."], "moderators": ["pedro-vianna"], "created_at": "Fev 2024", "related": ["empreendedorismo", "vendas-growth"]},
    {"id": "c3", "slug": "soft-skills", "name": "Soft Skills", "members": 4120, "posts_today": 19, "online_now": 88, "icon": "sparkles", "color": "accent", "description": "Comunicação, negociação, presença executiva e mindset.", "rules": ["Práticas, não filosofias. Traga o que vai usar amanhã.", "Storytelling sim, autoajuda não."], "moderators": ["diego-almeida"], "created_at": "Jan 2024", "related": ["gestao-pessoas", "carreira-inicial"]},
    {"id": "c4", "slug": "empreendedorismo", "name": "Empreendedorismo", "members": 1980, "posts_today": 33, "online_now": 167, "icon": "rocket", "color": "primary", "description": "Founders, sócios e quem tá tirando ideia do papel.", "rules": ["Pitch de produto vai em /sextou", "Compartilhe métrica antes de pedir conselho."], "moderators": ["camila-souza"], "created_at": "Jan 2024", "related": ["vendas-growth", "tech-produto"]},
    {"id": "c5", "slug": "carreira-inicial", "name": "Carreira Inicial", "members": 5230, "posts_today": 52, "online_now": 311, "icon": "graduation-cap", "color": "secondary", "description": "Para o time de 16-30 anos: primeiro emprego, transição e crescimento.", "rules": ["Pergunta boba é a mais respondida.", "Salário e oferta sempre podem virar thread.", "Nada de printscreen de currículo público."], "moderators": ["bruno-tavares", "mariana-reis"], "created_at": "Dez 2023", "related": ["soft-skills", "tech-produto"]},
    {"id": "c6", "slug": "vendas-growth", "name": "Vendas & Growth", "members": 1670, "posts_today": 22, "online_now": 94, "icon": "trending-up", "color": "accent", "description": "Pipeline, prospecção, copy e tudo que faz a receita crescer.", "rules": ["Sem cold pitch para a comunidade.", "Compartilhe número (taxa, ROI) quando for case."], "moderators": ["camila-souza"], "created_at": "Fev 2024", "related": ["empreendedorismo", "tech-produto"]},
]

guild_threads = [
    {"id": "t1", "slug": "1-1-com-alguem-que-nao-confia", "title": "Como vocês conduzem 1:1 com alguém que não confia em você ainda?", "author": "mariana-reis", "community_slug": "gestao-pessoas", "community": "Gestão de Pessoas", "time_ago": "há 2h", "replies": 34, "upvotes": 128, "tag": "discussão", "post_type": "text", "preview": "Acabei de assumir um time herdado e percebi que duas pessoas estão na defensiva.", "body": "Acabei de assumir um time herdado de 9 devs..."},
    {"id": "t2", "slug": "wrap-em-2-ofertas-funcionou", "title": "Aplicando o framework WRAP para escolher entre 2 ofertas de emprego — funcionou", "author": "bruno-tavares", "community_slug": "carreira-inicial", "community": "Carreira Inicial", "time_ago": "há 5h", "replies": 18, "upvotes": 89, "tag": "case", "post_type": "text", "preview": "Compartilhando o caso porque o método salvou minha decisão.", "body": "Compartilhando o caso porque o método salvou minha decisão."},
    {"id": "t3", "slug": "aumentei-30-pct-e-perdi-5", "title": "Pricing: por que aumentei 30% e perdi só 5% dos clientes", "author": "camila-souza", "community_slug": "empreendedorismo", "community": "Empreendedorismo", "time_ago": "há 8h", "replies": 47, "upvotes": 215, "tag": "case", "post_type": "text", "preview": "Inspirada no resumo da Marina Costa, refiz minha tabela de preços.", "body": "Inspirada no resumo da Marina Costa (Library), refiz minha tabela de preços."},
    {"id": "t4", "slug": "conflict-canvas-preenchido", "title": "Alguém usa o Conflict Canvas? Compartilho o meu preenchido", "author": "diego-almeida", "community_slug": "soft-skills", "community": "Soft Skills", "time_ago": "ontem", "replies": 22, "upvotes": 76, "tag": "framework", "post_type": "text", "preview": "Tive uma conversa difícil com meu CTO essa semana.", "body": "Tive uma conversa difícil com meu CTO essa semana."},
    {"id": "t5", "slug": "standup-9min-time-de-12", "title": "Stand-up de 9 min funciona pra time de 12? Estamos testando", "author": "pedro-vianna", "community_slug": "tech-produto", "community": "Tech & Produto", "time_ago": "ontem", "replies": 31, "upvotes": 102, "tag": "discussão", "post_type": "text", "preview": "Adaptamos o template do Rafael Santos.", "body": "Adaptamos o template do Rafael Santos (Feed) pro nosso time de 12."},
]

COMMENTS = {
    "t1": [
        {"id": "cm1", "author": "diego-almeida", "body": "3 meses é a média que eu vejo na coachada.", "upvotes": 47, "time_ago": "há 1h", "children": [
            {"id": "cm1a", "author": "mariana-reis", "body": "Vou testar amanhã.", "upvotes": 12, "time_ago": "há 45min", "children": []},
            {"id": "cm1b", "author": "pedro-vianna", "body": "Faço algo parecido.", "upvotes": 9, "time_ago": "há 30min", "children": []},
        ]},
        {"id": "cm2", "author": "camila-souza", "body": "Eu tive caso similar.", "upvotes": 28, "time_ago": "há 1h", "children": []},
        {"id": "cm3", "author": "bruno-tavares", "body": "Falando do outro lado.", "upvotes": 19, "time_ago": "há 50min", "children": []},
    ],
    "t2": [
        {"id": "cm4", "author": "camila-souza", "body": "Parabéns pela maturidade da decisão!", "upvotes": 34, "time_ago": "há 4h", "children": []},
        {"id": "cm5", "author": "diego-almeida", "body": "A parte de 'Prepare to be wrong' é a mais subestimada.", "upvotes": 21, "time_ago": "há 3h", "children": []},
    ],
    "t3": [
        {"id": "cm6", "author": "lucas-pestana", "body": "A âncora do Scale a R$549 é um golpe de mestre.", "upvotes": 47, "time_ago": "há 7h", "children": []},
        {"id": "cm7", "author": "marina-costa", "body": "Fico feliz que o resumo ajudou!", "upvotes": 39, "time_ago": "há 6h", "children": []},
    ],
    "t4": [
        {"id": "cm9", "author": "ana-lima", "body": "O que eu temo perder mudou minha carreira.", "upvotes": 31, "time_ago": "há 20h", "children": []},
    ],
    "t5": [
        {"id": "cm10", "author": "rafael-santos", "body": "Legal que adaptaram!", "upvotes": 18, "time_ago": "há 12h", "children": []},
        {"id": "cm11", "author": "mariana-reis", "body": "Aqui no time resolvemos abrindo a daily com 'alguém tem algo fora do radar?'.", "upvotes": 14, "time_ago": "há 10h", "children": []},
    ],
}


# ============ EXPLORAR ============

_continue_watching = [
    {"id": "1", "title": "Fundamentos de Growth Marketing", "subtitle": "Thiago Nigro • Módulo 3", "thumbnail": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=600&q=80", "duration": "45:30", "xp": 50, "progress": 65, "type": "course"},
    {"id": "2", "title": "Copywriting que Converte", "subtitle": "Ana Lima • Aula 7", "thumbnail": "https://images.unsplash.com/photo-1455390582262-044cdead277a?w=600&q=80", "duration": "32:15", "xp": 40, "progress": 30, "type": "course"},
    {"id": "3", "title": "Estratégias de Precificação", "subtitle": "Pedro Mendes • Aula 2", "thumbnail": "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?w=600&q=80", "duration": "28:00", "xp": 35, "progress": 80, "type": "masterclass"},
]

_recommended = [
    {"id": "4", "title": "Sales Machine: Vendas Previsíveis", "subtitle": "Masterclass com Aaron Ross", "thumbnail": "https://images.unsplash.com/photo-1552664730-d307ca884978?w=600&q=80", "duration": "2h 15min", "xp": 200, "type": "masterclass", "participants": 1240},
    {"id": "5", "title": "Liderança na Prática", "subtitle": "Curso completo • 8 módulos", "thumbnail": "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=600&q=80", "duration": "6h", "xp": 450, "type": "course", "participants": 890},
    {"id": "6", "title": "Branding Pessoal", "subtitle": "Construa sua marca", "thumbnail": "https://images.unsplash.com/photo-1493612276216-ee3925520721?w=600&q=80", "duration": "3h 30min", "xp": 280, "type": "course", "participants": 2100},
]

_collabs = [
    {"id": "8", "title": "G4 Educação x MUNDU", "subtitle": "Gestão de Alta Performance", "thumbnail": "https://images.unsplash.com/photo-1542744173-8e7e53415bb0?w=600&q=80", "duration": "4h", "xp": 600, "type": "collab", "badge": "Exclusivo", "participants": 3200},
    {"id": "9", "title": "StartSe Partnership", "subtitle": "Inovação e Tecnologia", "thumbnail": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=600&q=80", "duration": "3h 20min", "xp": 500, "type": "collab", "badge": "Novo", "participants": 1890},
]

_cases = [
    {"id": "11", "title": "Como cresci 300% em 6 meses", "subtitle": "por Lucas Ferreira • Case aprovado", "thumbnail": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=600&q=80", "xp": 100, "type": "case", "badge": "Case Oficial", "participants": 456},
    {"id": "12", "title": "Estratégia de Comunidade", "subtitle": "por Marina Costa • Case aprovado", "thumbnail": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=600&q=80", "xp": 100, "type": "case", "badge": "Case Oficial", "participants": 312},
]

_challenges = [
    {"type": "weekly", "label": "Semanal", "title": "Maratona de Conteúdo", "description": "Assista 5 aulas completas esta semana e ganhe XP bônus.", "xp": 300, "progress": 60, "progress_text": "3 de 5 aulas concluídas"},
    {"type": "daily", "label": "Diário", "title": "Reflexão do Dia", "description": "Escreva uma reflexão sobre o último conteúdo assistido.", "xp": 50, "progress": 0, "progress_text": "Não iniciado"},
]




library_frameworks = [
    {"id": "fw1", "slug": "1-1-canvas", "title": "1:1 Canvas", "description": "Template editável para conduzir 1:1s memoráveis.", "uses": 4320, "color": "primary"},
    {"id": "fw2", "slug": "feedback-sbi", "title": "Feedback SBI", "description": "Estrutura Situação · Comportamento · Impacto.", "uses": 3210, "color": "secondary"},
    {"id": "fw3", "slug": "okr-trimestral", "title": "OKR Trimestral", "description": "Planilha + canvas para OKRs de time.", "uses": 5680, "color": "accent"},
    {"id": "fw4", "slug": "conflict-canvas", "title": "Conflict Canvas", "description": "Mapa visual para preparar conversas difíceis.", "uses": 2104, "color": "primary"},
    {"id": "fw5", "slug": "decision-journal", "title": "Decision Journal", "description": "Diário de decisões.", "uses": 1789, "color": "secondary"},
    {"id": "fw6", "slug": "standup-9-minutos", "title": "Stand-up 9 minutos", "description": "Template de daily que cabe em 9 min.", "uses": 980, "color": "accent"},
]

public_notes = [
    {"id": "pn1", "author_handle": "mariana-reis", "title": "SBI funciona melhor logo após o gatilho", "body": "Tentei deixar pra dar feedback no 1:1 da semana seguinte.", "source_label": "Vídeo: Como dar feedback que não trava o time", "likes": 156, "comments": 12, "saves": 87, "time_ago": "há 4h", "_sort": 240},
    {"id": "pn2", "author_handle": "bruno-tavares", "title": "WRAP me poupou 6 meses de arrependimento", "body": "Listei 4 opções em vez de 2.", "source_label": "Vídeo: O método de Harvard p/ tomar decisão difícil", "likes": 234, "comments": 28, "saves": 112, "time_ago": "há 7h", "_sort": 420},
    {"id": "pn3", "author_handle": "diego-almeida", "title": "Conflict Canvas: o quadrante 'temer perder' destrava tudo", "body": "Em 5 conversas difíceis essa semana.", "source_label": "Framework: Conflict Canvas", "likes": 312, "comments": 47, "saves": 178, "time_ago": "ontem", "_sort": 1500},
]

followed_handles = ["camila-faria", "mariana-reis", "diego-almeida", "marina-costa", "pedro-mendes", "camila-souza"]
trending_topics = [{"label": "Pricing", "posts": 47, "trend": "+12"}, {"label": "1:1", "posts": 32, "trend": "+8"}, {"label": "Conflict Canvas", "posts": 28, "trend": "+5"}, {"label": "WRAP", "posts": 24, "trend": "+19"}, {"label": "Stand-up", "posts": 19, "trend": "+3"}]


def _ago(minutes):
    if minutes < 60: return f"há {minutes}min"
    if minutes < 1440: return f"há {minutes // 60}h"
    days = minutes // 1440
    return "ontem" if days == 1 else f"há {days} dias"


def get_who_to_follow(limit=3):
    candidates = [u for h, u in USERS.items() if h not in followed_handles and not u.get("is_self") and h != "gabriel"]
    candidates.sort(key=lambda u: u.get("karma", 0), reverse=True)
    return candidates[:limit]


def build_unified_feed(sort="for-you"):
    items = []
    thread_minutes = [120, 300, 480, 1440, 1500]
    for i, t in enumerate(guild_threads):
        author = get_user(t["author"])
        items.append({"kind": "thread", "id": t["id"], "actor": author, "actor_handle": t["author"], "verb": "postou em r/" + t["community_slug"], "time_ago": t["time_ago"], "_sort": thread_minutes[i % len(thread_minutes)], "engagement": {"upvotes": t["upvotes"], "comments": t["replies"]}, "payload": t})
    for pn in public_notes:
        items.append({"kind": "public_note", "id": pn["id"], "actor": get_user(pn["author_handle"]), "actor_handle": pn["author_handle"], "verb": "compartilhou uma nota", "time_ago": pn["time_ago"], "_sort": pn["_sort"], "engagement": {"likes": pn["likes"], "comments": pn["comments"], "saves": pn["saves"]}, "payload": pn})
    fw_minutes = [600, 1200]
    for i, fw in enumerate(library_frameworks[:2]):
        items.append({"kind": "framework", "id": fw["id"], "actor": {"handle": "mundu", "nome_completo": "Mundu Academy", "iniciais": "M", "role": "Curadoria oficial"}, "actor_handle": "mundu", "verb": "lançou um novo framework", "time_ago": _ago(fw_minutes[i % len(fw_minutes)]), "_sort": fw_minutes[i % len(fw_minutes)], "engagement": {"saves": fw["uses"]}, "payload": fw})
    if sort == "following":
        items = [it for it in items if it["actor_handle"] in followed_handles]
    elif sort == "community":
        items = [it for it in items if it["kind"] == "thread"]
    elif sort == "popular":
        items.sort(key=lambda it: (it["engagement"].get("likes", 0) + it["engagement"].get("upvotes", 0) + it["engagement"].get("comments", 0) * 3 + it["engagement"].get("saves", 0) * 2), reverse=True)
        return items
    items.sort(key=lambda it: it["_sort"])
    return items


# ============ VIEWS ============

def index(request):
    sort = request.GET.get('sort', 'for-you')
    if sort not in ('for-you', 'following', 'popular', 'community'):
        sort = 'for-you'
    feed = build_unified_feed(sort=sort)
    return render(request, 'index.html', {
        'feed': feed,
        'sort': sort,
        'trending_topics': trending_topics,
        'who_to_follow': get_who_to_follow(3),
        'followed_count': len(followed_handles),
    })


def explorar(request):
    return render(request, 'explorar.html', {
        'continue_watching': _continue_watching,
        'recommended': _recommended,
        'collabs': _collabs,
        'cases': _cases,
        'challenges': _challenges,
        'library_frameworks_top': library_frameworks[:6],
        'library_reads': [],
        'guild_hot': guild_threads[:3],
    })


@login_required(login_url='/login')
def perfil(request):
    return render(request, 'perfil.html')


@login_required(login_url='/login')
def config(request):
    return render(request, 'config.html')


@login_required(login_url='/login')
def conteudos(request):
    modulos_db = Modulo.objects.prefetch_related('aulas').all()
    progressos = {p.modulo_id: p.progresso for p in ProgressoModulo.objects.filter(usuario=request.user)}
    modules = []
    for mod in modulos_db:
        prog = progressos.get(mod.id, 0)
        concluidas = int(mod.total_aulas * prog / 100)
        aulas = [
            {'id': a.id, 'titulo': a.titulo, 'duracao': a.duracao,
              'youtube_id': a.url_video, 'is_preview': a.is_preview,
              'ordem': a.ordem}
            for a in mod.aulas.all()
        ]
        modules.append({
            'id': str(mod.id), 'title': mod.titulo, 'description': mod.descricao,
            'slug': mod.slug,
            'thumbnail': mod.thumbnail, 'totalLessons': mod.total_aulas,
            'completedLessons': concluidas, 'progress': prog,
            'totalDuration': mod.duracao_total, 'xpTotal': mod.xp_total,
            'level': mod.nivel, 'certificate': mod.tem_certificado,
            'sections_count': mod.num_secoes,
            'aulas': aulas,
        })
    return render(request, 'conteudos.html', {'modules': modules})


@login_required(login_url='/login')
def trilhas(request):
    progressos = {p.modulo_id: p.progresso for p in ProgressoModulo.objects.filter(usuario=request.user)}
    trilhas_list = []
    for trilha in Trilha.objects.prefetch_related('trilhamodulo_set__modulo').all():
        tms = TrilhaModulo.objects.filter(trilha=trilha).order_by('ordem').select_related('modulo')
        modulos_proc = []
        for tm in tms:
            prog = progressos.get(tm.modulo_id, 0)
            modulos_proc.append({
                'id': f'm{tm.modulo_id}', 'title': tm.modulo.titulo,
                'duration': tm.modulo.duracao_total, 'xp': tm.modulo.xp_total,
                'completed': prog == 100, 'inProgress': 0 < prog < 100,
                'locked': tm.bloqueado, 'prerequisite': tm.prerequisito,
            })
        total = len(modulos_proc)
        concluidos = sum(1 for m in modulos_proc if m['completed'])
        progresso_trilha = int(concluidos / total * 100) if total else 0
        trilhas_list.append({
            'id': str(trilha.id), 'title': trilha.titulo, 'description': trilha.descricao,
            'thumbnail': trilha.thumbnail, 'area': trilha.area, 'level': trilha.nivel,
            'objective': trilha.objetivo, 'totalModules': total,
            'totalDuration': trilha.duracao_total, 'xpTotal': trilha.xp_total,
            'progress': progresso_trilha, 'hasCertificate': trilha.tem_certificado,
            'modules': modulos_proc,
        })
    return render(request, 'trilhas.html', {'trilhas': trilhas_list})


@login_required(login_url='/login')
def desafios(request):
    prog_map = {p.desafio_id: p.progresso for p in ProgressoDesafio.objects.filter(usuario=request.user)}
    def _build(tipo):
        result = []
        for d in Desafio.objects.filter(tipo=tipo, ativo=True):
            prog = prog_map.get(d.id, 0)
            result.append({'titulo': d.titulo, 'desc': d.descricao, 'xp': d.xp, 'prog': prog, 'meta': d.meta, 'icon': d.icon, 'comp': prog >= d.meta})
        return result
    return render(request, 'desafios.html', {'daily': _build('daily'), 'weekly': _build('weekly')})


@login_required(login_url='/login')
def ao_vivo(request):
    return render(request, 'ao_vivo.html')


@login_required(login_url='/login')
def insumos(request):
    return render(request, 'insumos.html')


@login_required(login_url='/login')
def networking(request):
    return render(request, 'networking.html')


def user_profile(request, handle):
    if handle not in USERS:
        return render(request, '404.html', {'resource': f"@{handle}"}, status=404)
    user = USERS[handle]
    user_posts = [
        {**t, "author_user": user, "community_obj": next((c for c in guild_communities if c["slug"] == t["community_slug"]), None)}
        for t in guild_threads if t["author"] == handle
    ]
    user_comments = []
    for post_id, comment_tree in COMMENTS.items():
        post_obj = next((t for t in guild_threads if t["id"] == post_id), None)
        def walk(comments):
            for c in comments:
                if c["author"] == handle:
                    user_comments.append({**c, "post": post_obj})
                walk(c.get("children", []))
        walk(comment_tree)
    tab = request.GET.get('tab', 'posts')
    return render(request, 'profile.html', {
        'user': user, 'posts': user_posts, 'comments': user_comments,
        'tab': tab, 'is_self': user.get("is_self", False),
    })
