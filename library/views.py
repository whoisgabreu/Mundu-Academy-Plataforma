from django.shortcuts import get_object_or_404
from django.http import Http404
from core.utils import render

USERS = {
    "camila-faria": {"handle": "camila-faria", "nome_completo": "Camila Faria", "iniciais": "CF", "role": "Head de Pessoas · Ex-Nubank"},
    "lucas-pestana": {"handle": "lucas-pestana", "nome_completo": "Lucas Pestana", "iniciais": "LP", "role": "Founder · Vertical SaaS"},
    "diego-almeida": {"handle": "diego-almeida", "nome_completo": "Diego Almeida", "iniciais": "DA", "role": "Coach Executivo"},
    "pedro-mendes": {"handle": "pedro-mendes", "nome_completo": "Pedro Mendes", "iniciais": "PM", "role": "Professor Convidado · Harvard Online"},
    "rafael-santos": {"handle": "rafael-santos", "nome_completo": "Rafael Santos", "iniciais": "RS", "role": "Tech Lead · Stone"},
    "mariana-reis": {"handle": "mariana-reis", "nome_completo": "Mariana Reis", "iniciais": "MR", "role": "Tech Lead · Stone"},
    "bruno-tavares": {"handle": "bruno-tavares", "nome_completo": "Bruno Tavares", "iniciais": "BT", "role": "Estagiário em transição · 24 anos"},
    "pedro-vianna": {"handle": "pedro-vianna", "nome_completo": "Pedro Vianna", "iniciais": "PV", "role": "Eng Manager · 12 devs"},
    "ana-lima": {"handle": "ana-lima", "nome_completo": "Ana Lima", "iniciais": "AL", "role": "Coach Executiva"},
    "camila-souza": {"handle": "camila-souza", "nome_completo": "Camila Souza", "iniciais": "CS", "role": "Founder · SaaS B2B"},
}

def get_user(handle):
    return USERS.get(handle, {"handle": handle, "nome_completo": handle.replace("-", " ").title(), "iniciais": (handle[:2] if handle else "?").upper(), "role": "Membro Mundu"})

library_summaries = [
    {"id": "l1", "title": "Como construir um Segundo Cérebro", "author": "Tiago Forte", "read_time": "12 min", "tag": "Produtividade", "excerpt": "O método CODE (Capture · Organize · Destile · Express) aplicado ao aprendizado de liderança.", "thumbnail": "https://images.unsplash.com/photo-1455390582262-044cdead277a?w=800&q=80", "saves": 2340},
    {"id": "l2", "title": "Liderança Servidora na prática", "author": "Curado por Mundu", "read_time": "9 min", "tag": "Liderança", "excerpt": "Resumo do livro de Robert Greenleaf com os 4 hábitos que líderes de alta performance usam diariamente.", "thumbnail": "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=800&q=80", "saves": 1890},
    {"id": "l3", "title": "O método de Caso de Harvard", "author": "Curado por Mundu", "read_time": "15 min", "tag": "Método", "excerpt": "Como usar discussão de caso para acelerar tomada de decisão em times sêniores.", "thumbnail": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=800&q=80", "saves": 1456},
    {"id": "l4", "title": "Negociação: o livro do Chris Voss em 10 min", "author": "Curado por Mundu", "read_time": "10 min", "tag": "Soft Skills", "excerpt": "Os 5 princípios de Never Split the Difference adaptados para negociação interna.", "thumbnail": "https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=800&q=80", "saves": 2102},
]

library_frameworks = [
    {"id": "fw1", "slug": "1-1-canvas", "title": "1:1 Canvas", "description": "Template editável para conduzir 1:1s memoráveis com seu time.", "long_description": "Um canvas em 6 quadrantes para tirar o 1:1 do piloto automático.", "format": "Notion + PDF", "uses": 4320, "active_now": 142, "version": "v2.3", "last_edit_at": "há 2 dias", "last_editor_handle": "camila-faria", "forks": 87, "rating": 4.8, "reviews_count": 156, "xp": 30, "color": "primary"},
    {"id": "fw2", "slug": "feedback-sbi", "title": "Feedback SBI", "description": "Estrutura Situação · Comportamento · Impacto pronta para preencher.", "long_description": "Quando o gatilho fica claro, dar feedback fica simples.", "format": "Notion", "uses": 3210, "active_now": 89, "version": "v1.8", "last_edit_at": "há 4h", "last_editor_handle": "camila-faria", "forks": 124, "rating": 4.9, "reviews_count": 203, "xp": 25, "color": "secondary"},
    {"id": "fw3", "slug": "okr-trimestral", "title": "OKR Trimestral", "description": "Planilha + canvas para definir e acompanhar OKRs de time.", "long_description": "Inspirado no método do John Doerr (Measure What Matters).", "format": "Notion + Sheets", "uses": 5680, "active_now": 218, "version": "v3.1", "last_edit_at": "há 1 dia", "last_editor_handle": "lucas-pestana", "forks": 312, "rating": 4.6, "reviews_count": 287, "xp": 40, "color": "accent"},
    {"id": "fw4", "slug": "conflict-canvas", "title": "Conflict Canvas", "description": "Mapa visual para preparar uma conversa difícil antes que ela aconteça.", "long_description": "8 quadrantes pra preencher antes de uma conversa difícil.", "format": "PDF editável", "uses": 2104, "active_now": 67, "version": "v2.0", "last_edit_at": "há 6h", "last_editor_handle": "diego-almeida", "forks": 56, "rating": 4.9, "reviews_count": 142, "xp": 35, "color": "primary"},
    {"id": "fw5", "slug": "decision-journal", "title": "Decision Journal", "description": "Diário de decisões para revisitar julgamentos e aprender com erros.", "long_description": "Inspirado no diário de decisões do Annie Duke.", "format": "Notion", "uses": 1789, "active_now": 34, "version": "v1.5", "last_edit_at": "há 3 dias", "last_editor_handle": "pedro-mendes", "forks": 41, "rating": 4.7, "reviews_count": 89, "xp": 20, "color": "secondary"},
    {"id": "fw6", "slug": "standup-9-minutos", "title": "Stand-up 9 minutos", "description": "Template de daily que cabe em 9 min mesmo com time grande.", "long_description": "Adaptação do daily ágil para times grandes (10+ pessoas).", "format": "PDF", "uses": 980, "active_now": 22, "version": "v1.2", "last_edit_at": "há 12h", "last_editor_handle": "rafael-santos", "forks": 28, "rating": 4.5, "reviews_count": 47, "xp": 15, "color": "accent"},
]

FRAMEWORK_REVIEWS = {
    "fw1": [{"id": "rv1", "author_handle": "mariana-reis", "rating": 5, "text": "Usei o 1:1 Canvas no meu time herdado e em 3 semanas a temperatura mudou.", "time_ago": "há 4 dias", "helpful": 47}, {"id": "rv2", "author_handle": "pedro-vianna", "rating": 5, "text": "Forkei e adaptei pra time de 12.", "time_ago": "há 1 semana", "helpful": 32}, {"id": "rv3", "author_handle": "bruno-tavares", "rating": 4, "text": "Como liderado, ajudou demais.", "time_ago": "há 2 semanas", "helpful": 21}],
    "fw2": [{"id": "rv4", "author_handle": "diego-almeida", "rating": 5, "text": "O SBI sozinho não funciona — funciona com a versão que a Camila adicionou aqui.", "time_ago": "há 3 dias", "helpful": 64}, {"id": "rv5", "author_handle": "mariana-reis", "rating": 5, "text": "Tem 6 meses que uso. Já dei 40+ feedbacks com esse template e ZERO virou conflito.", "time_ago": "há 5 dias", "helpful": 58}],
    "fw3": [{"id": "rv6", "author_handle": "lucas-pestana", "rating": 4, "text": "OKR é difícil de implementar bem. Esse template ajuda a NÃO definir 12 OKRs.", "time_ago": "há 6 dias", "helpful": 89}, {"id": "rv7", "author_handle": "camila-souza", "rating": 5, "text": "Forkei pra startup early-stage e cortei o ritual semanal.", "time_ago": "há 1 semana", "helpful": 41}],
    "fw4": [{"id": "rv8", "author_handle": "ana-lima", "rating": 5, "text": "Como coach, recomendo pra TODO cliente meu antes de conversa difícil.", "time_ago": "há 2 dias", "helpful": 76}],
    "fw5": [],
    "fw6": [{"id": "rv9", "author_handle": "mariana-reis", "rating": 4, "text": "Time de 9 → 11min de stand-up. Antes era 22min.", "time_ago": "há 4 dias", "helpful": 19}],
}


def library_list(request):
    return render(request, "library.html", {
        "summaries": library_summaries,
        "frameworks": library_frameworks,
    })


def framework_detail(request, slug):
    framework = None
    for fw in library_frameworks:
        if fw["slug"] == slug:
            framework = fw
            break
    if framework is None:
        raise Http404("Framework not found")

    editor = get_user(framework["last_editor_handle"])

    reviews = FRAMEWORK_REVIEWS.get(framework["id"], [])
    for review in reviews:
        review["author_user"] = get_user(review["author_handle"])

    related = [fw for fw in library_frameworks if fw["color"] == framework["color"] and fw["id"] != framework["id"]][:3]

    return render(request, "framework.html", {
        "framework": framework,
        "editor": editor,
        "reviews": reviews,
        "related_frameworks": related,
    })
