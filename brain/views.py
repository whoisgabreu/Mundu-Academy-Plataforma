from core.utils import render

VALID_TABS = ['private', 'public', 'saved', 'forks', 'followers']

USERS = {
    "mariana-reis": {"handle": "mariana-reis", "nome_completo": "Mariana Reis", "iniciais": "MR", "role": "Tech Lead · Stone"},
    "bruno-tavares": {"handle": "bruno-tavares", "nome_completo": "Bruno Tavares", "iniciais": "BT", "role": "Estagiário em transição · 24 anos"},
    "diego-almeida": {"handle": "diego-almeida", "nome_completo": "Diego Almeida", "iniciais": "DA", "role": "Coach Executivo"},
}

my_brain_notes = [
    {"id": "n1", "title": "SBI funciona quando o gatilho é claro", "source": "Vídeo: Como dar feedback que não trava o time", "source_type": "aula", "date": "Hoje, 14:32", "content": "Quando o comportamento foi público, dar SBI em público também aumenta credibilidade — não atrasar é parte do impacto.", "tags": ["liderança", "feedback"], "is_public": False},
    {"id": "n2", "title": "Decisão difícil = listar opções fora do binário", "source": "Resumo: O método de Harvard p/ decisão difícil", "source_type": "aula", "date": "Ontem, 19:08", "content": "Sempre que cair em sim/não, perguntar: e se eu pudesse fazer os dois? E se nenhum dos dois? O W de WRAP é o mais subutilizado.", "tags": ["soft skills", "decisão"], "is_public": True, "likes": 23, "comments_count": 4},
    {"id": "n3", "title": "Pricing — desconto é veneno doce", "source": "Vídeo: Pricing por que descontos quebram seu produto", "source_type": "aula", "date": "2 dias atrás", "content": "Se eu der 20% off, preciso vender 25% a mais só pra empatar margem. Não vale a pena — testar value ladder antes.", "tags": ["negócios", "pricing"], "is_public": True, "likes": 47, "comments_count": 8},
    {"id": "n4", "title": "Conflict Canvas: começar sempre pelo medo", "source": "Framework: Conflict Canvas", "source_type": "framework", "date": "Semana passada", "content": "O quadrante 'O que eu temo perder?' destrava 80% da conversa. Antes de listar fatos, listar medos.", "tags": ["soft skills", "conflito"], "is_public": False},
]

my_brain_saved = [
    {"id": "fw1", "title": "1:1 Canvas", "type": "framework"},
    {"id": "fw2", "title": "Feedback SBI", "type": "framework"},
    {"id": "fw4", "title": "Conflict Canvas", "type": "framework"},
    {"id": "l1", "title": "Como construir um Segundo Cérebro", "type": "summary"},
    {"id": "l4", "title": "Negociação: Chris Voss em 10 min", "type": "summary"},
]

my_brain_streak = [
    {"day": "S", "active": True},
    {"day": "T", "active": True},
    {"day": "Q", "active": True},
    {"day": "Q", "active": True},
    {"day": "S", "active": True},
    {"day": "S", "active": True},
    {"day": "D", "active": False},
]

my_brain_forks = [
    {"fork_id": "fork1", "framework_id": "fw2", "framework_title": "Feedback SBI", "framework_slug": "feedback-sbi", "my_version_label": "SBI + Self-reflection", "forked_at": "há 5 dias", "uses_my_version": 12, "note": "Adicionei um quadrante 'O que eu poderia ter feito diferente?' antes do 'I'"},
    {"fork_id": "fork2", "framework_id": "fw4", "framework_title": "Conflict Canvas", "framework_slug": "conflict-canvas", "my_version_label": "Conflict Canvas Async", "forked_at": "há 2 semanas", "uses_my_version": 8, "note": "Versão pra preencher em texto antes de chamada"},
]

brain_followers = [
    {"handle": "bruno-tavares", "since": "Set 2024"},
    {"handle": "mariana-reis", "since": "Dez 2024"},
    {"handle": "diego-almeida", "since": "Jan 2025"},
]

public_notes = [
    {"id": "pn1", "author_handle": "mariana-reis", "title": "SBI funciona melhor logo após o gatilho", "body": "Tentei deixar pra dar feedback no 1:1 da semana seguinte e perdi a janela.", "source_label": "Vídeo: Como dar feedback que não trava o time", "source_handle": "camila-faria", "tags": ["liderança", "feedback"], "likes": 156, "comments": 12, "saves": 87, "time_ago": "há 4h"},
    {"id": "pn2", "author_handle": "bruno-tavares", "title": "WRAP me poupou 6 meses de arrependimento", "body": "Listei 4 opções em vez de 2.", "source_label": "Vídeo: O método de Harvard p/ tomar decisão difícil", "source_handle": "pedro-mendes", "tags": ["soft skills", "decisão"], "likes": 234, "comments": 28, "saves": 112, "time_ago": "há 7h"},
    {"id": "pn3", "author_handle": "diego-almeida", "title": "Conflict Canvas: o quadrante 'temer perder' destrava tudo", "body": "Em 5 conversas difíceis essa semana.", "source_label": "Framework: Conflict Canvas", "source_handle": None, "tags": ["soft skills", "conflito"], "likes": 312, "comments": 47, "saves": 178, "time_ago": "ontem"},
]


def get_user(handle):
    return USERS.get(handle, {"handle": handle, "nome_completo": handle.replace("-", " ").title(), "iniciais": (handle[:2] if handle else "?").upper(), "role": "Membro Mundu"})


def my_brain(request):
    tab = request.GET.get('tab', 'private')
    if tab not in VALID_TABS:
        tab = 'private'

    public_notes_count = len(public_notes)

    brain_karma = 2340

    context = {
        'tab': tab,
        'notes': my_brain_notes,
        'saved_items': my_brain_saved,
        'streak': my_brain_streak,
        'forks': my_brain_forks,
        'followers': brain_followers,
        'public_notes': public_notes,
        'public_notes_count': public_notes_count,
        'brain_karma': brain_karma,
    }

    return render(request, 'my_brain.html', context)
