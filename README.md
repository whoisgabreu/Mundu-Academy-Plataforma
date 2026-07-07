# MUNDU Academy

Plataforma de aprendizado social estruturada em torno de **quatro pilares** que materializam o método **Segundo Cérebro (CODE)** de Tiago Forte, somado ao método de caso de Harvard e microlearning estilo TikTok.

> **Liderança é hábito, não evento.** Capture · Organize · Destile · Expresse.

---

## Sumário

- [Visão do produto](#visão-do-produto)
- [Os 4 pilares](#os-4-pilares)
- [Como rodar](#como-rodar)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Stack técnica](#stack-técnica)
- [Rotas](#rotas)
- [Modelo de dados (mocks)](#modelo-de-dados-mocks)
- [Sistema de templates (Jinja2)](#sistema-de-templates-jinja2)
- [Design system (CSS)](#design-system-css)
- [Componentes globais](#componentes-globais)
- [Convenções e padrões](#convenções-e-padrões)
- [Atalhos de teclado](#atalhos-de-teclado)
- [APIs internas](#apis-internas)
- [Próximos passos](#próximos-passos)

---

## Visão do produto

O diferencial competitivo da Mundu não é "mais uma estante de cursos", é uma **ferramenta de vida** para liderança. A lógica do produto vem de três influências fundidas:

| Influência | O que vira |
|---|---|
| **Segundo Cérebro (Tiago Forte)** | Cada conteúdo tem **Quick Note** que alimenta o repositório pessoal do aluno (My Brain) |
| **Método de caso (Harvard)** | O conteúdo curto apresenta o problema; a discussão crítica acontece na **Guild** |
| **Microlearning (TikTok)** | Vídeos de 1-3 minutos no **Feed**, scroll vertical full-screen com snap |

A plataforma é **curadoria como serviço**: o melhor de Harvard, livros e métodos consagrados, resumidos com a lente Mundu e entregues com framework de aplicação pronto.

---

## Os 4 pilares

```
   CAPTURE    →    ORGANIZE     →     DESTILE     →     EXPRESSE
  The Feed    →   The Library   →    The Guild    →     My Brain
   /feed      →    /library     →     /guild      →    /my-brain
```

| Pilar | Inspiração | O que tem | Rota |
|---|---|---|---|
| **The Feed** | TikTok / Reels | Vídeos curtos verticais (proporção 9:16) com framework destacado, like/comment/save e botão Quick Note. Modo **Para você** (snap scroll) e modo **Explorar** (overlay com busca + grid filtrável) | `/feed` |
| **The Library** | 12min / Substack | **Frameworks editáveis** (1:1 Canvas, Feedback SBI, OKR Trimestral...) e **resumos profundos** de 9-15min. Newsletter inclusa | `/library` |
| **The Guild** | Reddit / Clubhouse | Comunidades por interesse (Gestão, Tech, Soft Skills, Empreendedorismo, Carreira Inicial, Vendas) + threads de discussão estilo Reddit com voto, replies e tags | `/guild` |
| **My Brain** | Obsidian / Notion + Duolingo | **Streak diário** com chama animada, XP/nível, lista de **Quick Notes** capturadas, frameworks salvos. Onde fica a expressão do que foi aprendido | `/my-brain` |

A **navegação** (sidebar desktop + bottom nav mobile) sempre mostra **Início + 4 pilares** — exatamente 5 itens.

---

## Como rodar

### Pré-requisitos

- Python 3.11+
- PostgreSQL acessível (obrigatório — o app falha se `DATABASE_URL` não estiver no `.env`)
- Para smoke testing local sem DB real, use `DATABASE_URL=sqlite:///:memory:`

### Setup

```bash
# 1. Ativar venv (já existe um em .venv/)
.venv\Scripts\activate                  # Windows
source .venv/bin/activate                # Linux/Mac

# 2. Instalar dependências (se ainda não estiverem)
pip install flask flask-cors flask-sqlalchemy python-dotenv psycopg2-binary

# 3. Configurar .env na raiz
echo DATABASE_URL=postgresql://user:senha@host:5432/banco > .env

# 4. Rodar
python app.py

# 5. Acessar
# http://localhost:5001
```

### Smoke test rápido (sem precisar do banco real)

```bash
python -c "
import os, sys
sys.path.insert(0, '.')
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
from app import app
client = app.test_client()
for r in ['/', '/feed', '/library', '/guild', '/my-brain']:
    print(r, '->', client.get(r).status_code)
"
```

---

## Estrutura do projeto

```
Mundu-Academy-main/
├── app.py                          # Flask: rotas, mocks, context processor, API
├── .env                            # DATABASE_URL (não versionado)
├── .venv/                          # Virtualenv local
├── README.md
│
├── templates/
│   ├── base.html                   # Layout base: sidebar, header XP, bottom-nav, Quick Note modal, Toast
│   ├── index.html                  # Home: welcome-strip + drops + hero + carrosséis dos 4 pilares
│   │
│   ├── feed.html                   # The Feed (TikTok-like reels + overlay de busca)
│   ├── library.html                # The Library (frameworks + resumos + newsletter)
│   ├── guild.html                  # The Guild (comunidades + threads)
│   ├── my_brain.html               # My Brain (streak + XP + notas + salvos)
│   │
│   ├── perfil.html                 # [LEGADO] Perfil do usuário
│   ├── config.html                 # [LEGADO] Configurações
│   ├── trilhas.html                # [LEGADO] Trilhas de cursos
│   ├── conteudos.html              # [LEGADO] Cursos/aulas
│   ├── desafios.html               # [LEGADO] Desafios gamificados
│   ├── ao_vivo.html                # [LEGADO] Lives e replays
│   ├── insumos.html                # [LEGADO] Templates / coleções
│   ├── networking.html             # [LEGADO] Posts da comunidade
│   ├── login.html                  # [LEGADO] Login
│   └── registro.html               # [LEGADO] Registro
│
└── static/
    ├── css/
    │   └── style.css               # Design system completo (~3500 linhas)
    ├── js/
    │   └── app.js                  # Sidebar, hero carrossel, chatbot, Quick Note, toast
    └── img/
        ├── mundu-logo-horizontal.webp
        ├── mundu-logo-icon.png
        └── favicon.png
```

> **Templates `[LEGADO]`** — funcionais e em rotas ativas, mas removidos da navegação. O bloco no `base.html` ficou em comentário Jinja `{# ... #}` para resgate fácil quando necessário.

---

## Stack técnica

| Camada | Tecnologia |
|---|---|
| **Backend** | Flask 3 + Flask-CORS + Flask-SQLAlchemy + python-dotenv |
| **DB** | PostgreSQL (obrigatório em produção; SQLite em memória para testes) |
| **Templates** | Jinja2 (servidor) |
| **Estilização** | CSS custom (design tokens em HSL) + Tailwind via CDN para utilitários (somente nos templates legados) |
| **Ícones** | Lucide via CDN + SVGs inline |
| **Tipografia** | Montserrat (Google Fonts) |
| **JS** | Vanilla, sem framework. Carregado via `static/js/app.js` |

Sem build step, sem bundler — abre o template e renderiza direto.

---

## Rotas

### Páginas principais (na nav)

| Rota | View | Template |
|---|---|---|
| `/` | `index()` | `index.html` |
| `/feed` | `feed()` | `feed.html` |
| `/library` | `library()` | `library.html` |
| `/guild` | `guild()` | `guild.html` |
| `/my-brain` | `my_brain()` | `my_brain.html` |

### Rotas legadas (escondidas da nav, mantidas funcionando)

`/perfil`, `/config`, `/trilhas`, `/conteudos`, `/desafios`, `/ao-vivo`, `/insumos`, `/networking`

### API

| Endpoint | Método | Descrição |
|---|---|---|
| `/api/status` | GET | Healthcheck |
| `/api/cursos` | GET | Lista cursos do banco (modelo `Curso`) |
| `/api/quick-note` | POST | Recebe nota do Segundo Cérebro (mock, retorna 201) |

---

## Modelo de dados (mocks)

Todo o conteúdo das páginas vem de listas Python em `app.py` — substituível por DB depois sem mudar templates. As listas:

| Variável | Pilar | Quantidade |
|---|---|---|
| `feed_videos` | The Feed | 6 vídeos com `category`, `framework`, `xp`, `likes`, `comments`, `saves` |
| `library_summaries` | The Library | 4 resumos com `read_time`, `tag`, `excerpt` |
| `library_frameworks` | The Library | 6 frameworks com `format`, `uses`, `xp`, `color` |
| `guild_communities` | The Guild | 6 comunidades com `members`, `posts_today`, `icon`, `color` |
| `guild_threads` | The Guild | 5 threads com `community`, `time_ago`, `replies`, `upvotes`, `tag` |
| `my_brain_notes` | My Brain | 4 notas com `source`, `source_type`, `tags` |
| `my_brain_saved` | My Brain | 5 itens salvos (frameworks + summaries) |
| `my_brain_streak` | My Brain | 7 dias da semana com `active: bool` |
| `continue_watching`, `recommended_content`, `collabs_data`, `cases_data`, `challenges_data` | Home | (legado, ainda usados nos carrosséis da home) |

### `DEFAULT_USER` (context processor)

```python
DEFAULT_USER = {
    "nome": "Aluno Mundu",
    "nome_completo": "Gabriel Lasaro",
    "username": "gabriel",
    "perfil": {
        "nivel": 7,
        "nome_nivel": "Estrategista",
        "xp_total": 1840,
        "xp_proximo_nivel": 2500,
        "xp_percentual": 73,
        "streak": 12,
        "streak_dias": 12,
        "iniciais": "GL",
        "pilar_favorito": "The Feed",
    },
}
```

Disponível como **`current_user`** em todos os templates via `@app.context_processor`. Substitui o que era `request.user` (estilo Django) — todos os templates já usam `current_user`.

---

## Sistema de templates (Jinja2)

`base.html` define **5 blocos** que páginas filhas podem sobrescrever:

| Bloco | Função | Exemplo |
|---|---|---|
| `{% block title %}` | `<title>` da aba | `Mundu Academy - The Feed` |
| `{% block page_title %}` | Título mobile (escondido em desktop) | `The Feed` |
| `{% block main_class %}` | Classe extra no `<main>` | `main-content-feed` (no `feed.html` zera padding) |
| `{% block content %}` | Conteúdo principal | (cada página) |
| `{% block scripts %}` | JS específico da página | (filtros, search overlay etc.) |

### O que o `base.html` provê automaticamente

- **Sidebar desktop** (colapsável, persistido em `localStorage`)
- **Top header** com XP/nível, toggle de tema (claro/escuro), notificações
- **Mobile bottom nav** (5 itens — Início + 4 pilares)
- **Salomão IA** — chatbot mockado (FAB no canto inferior direito)
- **Quick Note modal** — globalmente disponível via `openQuickNote(title, source)`
- **Toast global** — `showToast(msg)`
- **Tema escuro como padrão** (override via `localStorage.theme = 'light'`)

---

## Design system (CSS)

### Tokens (variáveis CSS HSL)

Definidos em `:root` (light) e `.dark` (dark mode default). Estrutura:

| Token | Light | Dark |
|---|---|---|
| `--background` | branco puro | quase preto (`0% 2%`) |
| `--background-card` | `0% 98%` | `0% 5%` |
| `--primary` | verde rico (`145 90% 32%`) | verde vibrante (`145 85% 38%`) |
| `--secondary` | jungle green (`155 80% 25%`) | dark emerald |
| `--accent` | lime forte (`135 85% 40%`) | cyber green (`135 85% 45%`) |
| `--xp-bar`, `--xp-glow` | barras XP | (com glow no dark) |
| `--shadow-glow`, `--shadow-elevated`, `--shadow-card` | sombras com glow verde | mais intenso no dark |

Tipografia: **Montserrat** (300-900). Border radius default `0.375rem` (sharper edges, estética industrial).

### Cores por pilar

Cada pilar tem uma cor que se repete consistentemente (header, ícones, gradientes):

| Pilar | Cor base | Uso |
|---|---|---|
| **The Feed** | Amarelo-âmbar `48 95% 60%` | ⚡ Energia, captura |
| **The Library** | Primary green | 📚 Estrutura, organize |
| **The Guild** | Secondary (jungle) | 💬 Comunidade, social |
| **My Brain** | Accent (lime) | 🧠 Pessoal, gamificação |

### Componentes principais

| Família CSS | Onde se usa |
|---|---|
| `.welcome-strip*` | Header denso da home (avatar + saudação contextual + streak + XP + Quick Note) |
| `.feed-tiktok`, `.feed-reel`, `.feed-reel-frame`, `.reel-action-btn` | Modo TikTok do `/feed` (frame 9:16 centralizado, actions laterais) |
| `.feed-search-overlay`, `.feed-search-grid` | Overlay de busca/explorar do `/feed` |
| `.feed-card*` | Card de vídeo no modo grid (overlay de busca + carrossel da home) |
| `.reel-mini-card` | Mini-reel da home ("Em alta no Feed", proporção 9:16 menor) |
| `.framework-card`, `.library-mini-card` | Frameworks editáveis (Library + carrossel da home) |
| `.summary-card` | Resumos profundos da Library |
| `.community-card`, `.thread-card`, `.guild-hot-item` | Guild |
| `.brain-streak-card`, `.brain-level-card`, `.note-card`, `.saved-item` | My Brain |
| `.pillar-header*`, `.pillar-stat*` | Header padrão de cada página de pilar |
| `.quicknote-*`, `.mundu-toast` | Globais |

### Animações

- `pulse-glow` — pulse genérico (badges live)
- `pulse-dot` — dot de status (avatar online, comunidades ativas)
- `fade-in-up` — entrada padrão de cards (intersection observer ativa via `.animate-fade-in-up`)
- `slide-in-right`, `search-slide-up` — overlays
- `wave` — emoji 👋 da saudação
- `fire-flicker` — chama do streak no My Brain
- `scroll-hint-bounce` — hint inicial do feed

---

## Componentes globais

### Quick Note Modal (Segundo Cérebro)

Disponível em qualquer página via:

```js
openQuickNote(title, source)
```

- `title` — pré-popula com `"Sobre: <title>"`
- `source` — texto exibido como "Fonte"
- Atalho `N` em qualquer página abre nota livre
- `Ctrl+Enter` salva, `Esc` fecha
- Salva via `POST /api/quick-note` (mockado — sempre retorna 201)
- Feedback via toast `🧠 Nota salva no My Brain (+10 XP)`

### Toast

```js
showToast('mensagem')
```

Aparece centralizado embaixo, gradient verde-azulado, some em ~2.8s.

### Salomão IA (Chatbot)

FAB no canto inferior direito. `toggleChatbot()` abre/fecha. Mensagens mockadas — sem chamada real de LLM ainda.

---

## Convenções e padrões

### 1. Nada de Jinja `{{ }}` dentro de `style=""`

O linter de CSS do VS Code não consegue parsear Jinja em style attributes (gera lint errors). Em vez disso:

```html
<!-- ❌ Não use -->
<div style="width: {{ pct }}%; animation-delay: {{ delay }}s">

<!-- ✅ Use data-attrs -->
<div data-pct="{{ pct }}" data-delay="{{ delay }}">
```

E o `base.html` aplica via JS:

```js
document.querySelectorAll('[data-pct]').forEach(el => el.style.width = el.dataset.pct + '%');
document.querySelectorAll('[data-delay]').forEach(el => el.style.animationDelay = el.dataset.delay + 's');
```

### 2. `current_user`, não `request.user`

Flask não tem `request.user`. Use `current_user.perfil.nivel`, etc. — vem do `@app.context_processor`.

### 3. Páginas full-bleed via Jinja block

Quando uma página precisa estourar o padding do `.main-content` (ex.: `/feed`):

```jinja
{% block main_class %}main-content-feed{% endblock %}
```

E no CSS:

```css
.main-content.main-content-feed { padding: 0; gap: 0; }
```

### 4. Templates legados ficam comentados, não deletados

```jinja
{# ========= ABAS LEGADAS — escondidas, manter para reuso =========
<a href="/conteudos">...</a>
<a href="/trilhas">...</a>
...
============================================================== #}
```

### 5. Animações entram via Intersection Observer

Adicione `class="animate-fade-in-up"` em qualquer elemento. O observer em `app.js` cuida do resto. Para staggered animations, use `data-delay="{{ loop.index0 * 0.05 }}"`.

### 6. Cores por pilar consistentes

Use as classes modificadoras já existentes:

```html
<article class="framework-card framework-primary">   <!-- verde -->
<article class="framework-card framework-secondary"> <!-- jungle -->
<article class="framework-card framework-accent">    <!-- lime -->

<article class="community-card community-primary">
<article class="thread-card-tag thread-tag-discussão">
```

---

## Atalhos de teclado

| Tecla | Ação | Onde |
|---|---|---|
| `N` | Abre Quick Note livre | Qualquer página |
| `Esc` | Fecha Quick Note ou Search Overlay | Modal/Overlay aberto |
| `Ctrl + Enter` (ou ⌘+Enter) | Salva Quick Note | Modal aberto |
| `Enter` no input do chat | Envia mensagem | Chatbot Salomão |

Atalhos respeitam foco — não disparam dentro de `<input>`, `<textarea>` ou `contenteditable`.

---

## APIs internas

### `GET /api/status`

```json
{ "status": "Online", "mensagem": "Backend Flask e PostgreSQL configurados!" }
```

### `GET /api/cursos`

Lista todos os registros da tabela `cursos` (modelo `Curso`).

### `POST /api/quick-note`

Body:
```json
{ "title": "string", "content": "string", "source": "string" }
```

Resposta: `201` com o eco do payload. Não persiste — quando for plugar DB, esse é o ponto de entrada.

---

## Próximos passos

Ordem sugerida quando for evoluir do MVP:

1. **Plugar DB real** — substituir as listas Python por modelos SQLAlchemy. O `Curso` já existe; criar `Video`, `Framework`, `Summary`, `Community`, `Thread`, `Note`, `User`.
2. **Auth real** — substituir `DEFAULT_USER` por `flask-login` ou similar. Manter `current_user` como variável de template (apenas trocar a fonte).
3. **Persistir Quick Notes** — fazer `/api/quick-note` salvar de verdade, ligar com a página `/my-brain`.
4. **Vídeos reais no Feed** — trocar `<img>` thumbnails por `<video>` com auto-play em snap, mute por padrão (TikTok-like).
5. **Salomão IA real** — plugar `/api/chat` na Anthropic API com prompt sobre a base curada da Library.
6. **Onboarding** — para novo usuário (sem notas, sem streak), mostrar a antiga **jornada CODE** (welcome-hero + journey) que está comentada no histórico do `index.html`. Pode virar `/sobre` ou um modal de boas-vindas.
7. **Streak real** — calcular via timestamps de notas/atividade, não mockar.
# Mundu-Academy-Plataforma
