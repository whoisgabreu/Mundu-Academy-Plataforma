# Mundu Academy — Documentação do Sistema

> **Versão:** Julho 2026  
> **Stack:** Django 6.0 + Jinja2 + django-tenants + PostgreSQL

---

## Índice

1. [Visão Geral](#1-visão-geral)
2. [Apps e Modelos](#2-apps-e-modelos)
3. [Administração (Django Admin)](#3-administração-django-admin)
4. [Rotas (URLs)](#4-rotas-urls)
5. [API Endpoints](#5-api-endpoints)
6. [Sistema de Gamificação](#6-sistema-de-gamificação)
7. [Seed Data (Comandos)](#7-seed-data-comandos)
8. [Como Usar — Guia Prático](#8-como-usar--guia-prático)
9. [Configurações Importantes](#9-configurações-importantes)

---

## 1. Visão Geral

A plataforma é multi‑tenant (cada cliente tem seu próprio schema no banco).  
Todas as páginas consomem dados reais do banco — não há mais dados fixos no código.

### Fluxo do Aluno
```
Página Inicial → Explorar → Conteúdos (módulos + aulas) → Watch (player)  
             → Trilhas → Desafios → Quiz → Ao Vivo  
             → Biblioteca → My Brain → Networking → Perfil
```

---

## 2. Apps e Modelos

### `cursos` — Núcleo acadêmico

| Modelo | Campos principais | Uso |
|--------|------------------|-----|
| `Modulo` | `titulo`, `slug`, `descricao`, `thumbnail`, `total_aulas`, `duracao_total`, `xp_total`, `nivel`, `tem_certificado`, `num_secoes` | Módulo de aprendizado. Slug é auto‑gerado no `save()`. |
| `Aula` | `modulo` (FK), `titulo`, `descricao`, `url_video`, `duracao`, `ordem`, `is_preview` | Aula dentro de um módulo. `ordem` define a posição. |
| `ProgressoModulo` | `usuario` (FK), `modulo` (FK), `progresso` (0-100), `ultimo_acesso` | Progresso do aluno no módulo. |
| `Trilha` | `titulo`, `descricao`, `thumbnail`, `area`, `nivel`, `objetivo`, `duracao_total`, `xp_total`, `tem_certificado` | Trilha de aprendizado (conjunto de módulos). |
| `TrilhaModulo` | `trilha` (FK), `modulo` (FK), `ordem`, `bloqueado`, `prerequisito` | Associação módulo → trilha. |
| `Desafio` | `titulo`, `descricao`, `icone`, `tipo`, `meta`, `xp_recompensa`, `ativo` | Desafios diários/semanais. |
| `ProgressoDesafio` | `usuario` (FK), `desafio` (FK), `progresso` (contador), `concluido_em` | Progresso individual do desafio. |
| `FeaturedContent` | `titulo`, `descricao`, `url`, `thumbnail`, `tipo` (recommended/collab/case), `ordem`, `ativo` | Conteúdos em destaque na página Explorar. |
| `Certificate` | `usuario` (FK), `modulo` (FK), `codigo`, `criado_em` | Certificado emitido ao concluir 100% do módulo. |
| `Quiz` | `modulo` (FK), `titulo`, `descricao`, `ordem`, `xp_total`, `aprovacao_percentual` | Quiz de um módulo. |
| `Questao` | `quiz` (FK), `enunciado`, `tipo` (multipla_escolha/verdadeiro_falso), `ordem` | Questão do quiz. |
| `Alternativa` | `questao` (FK), `texto`, `correta`, `ordem` | Alternativa de resposta. |
| `TentativaQuiz` | `usuario` (FK), `quiz` (FK), `pontuacao`, `total_questoes`, `aprovado`, `respostas` (JSON), `concluido_em` | Tentativa do aluno. `percentual` property. |

### `usuarios` — Perfil e gamificação

| Modelo | Campos principais | Uso |
|--------|------------------|-----|
| `Perfil` | `user` (OneToOne), `xp_total`, `nivel`, `streak_dias`, `ultimo_login`, `cargo`, `bio`, `empresa`, `localizacao`, `linkedin`, `instagram`, `data_criacao`, `karma` | Estende User. Propriedades: `role`, `nome_nivel`, `xp_proximo_nivel`, `xp_percentual`, `iniciais`. |
| `Achievement` | `titulo`, `descricao`, `icone`, `tipo`, `xp_recompensa` | Conquista disponível. |
| `UserAchievement` | `usuario` (FK), `achievement` (FK), `concluido_em` | Conquista desbloqueada pelo aluno. |
| `Skill` | `usuario` (FK), `nome`, `nivel` (1-10) | Habilidade do perfil. |

### `live` — Ao Vivo

| Modelo | Campos | Uso |
|--------|--------|-----|
| `LiveStream` | `titulo`, `descricao`, `url_youtube`, `data_agendamento`, `status` (ao_vivo/agendado/replay), `thumbnail`, `carga_horaria` | Live programada ou replay. |
| `LiveChatMessage` | `live` (FK), `usuario` (FK), `mensagem`, `criado_em` | Mensagem do chat ao vivo. |
| `LivePoll` | `live` (FK), `pergunta`, `opcoes` (JSON), `ativo` | Enquete ao vivo. |
| `LivePollVote` | `poll` (FK), `usuario` (FK), `opcao` (int) | Voto na enquete. |

### `social` — Social

| Modelo | Campos | Uso |
|--------|--------|-----|
| `Follow` | `seguidor` (FK), `seguido` (FK), `criado_em` | Seguir usuário. |
| `Notification` | `usuario` (FK), `tipo`, `titulo`, `descricao`, `url`, `lida`, `criado_em` | Notificação do usuário. |

### `resources` — Insumos

| Modelo | Campos | Uso |
|--------|--------|-----|
| `ResourceCategory` | `nome`, `icone`, `slug` | Categoria de recurso. |
| `Resource` | `categoria` (FK), `titulo`, `descricao`, `url`, `thumbnail` (URL pública), `tipo` | Recurso/insumo. |

### `guild` — Comunidade

| Modelo | Campos | Uso |
|--------|--------|-----|
| `Community` | `slug`, `nome`, `descricao`, `icone`, `membros_count` | Comunidade da guild. |
| `Thread` | `community` (FK), `title`, `slug`, `body`, `author_handle`, `tag`, `upvotes`, `preview`, `created_at`, `url` | Post da comunidade. |
| `Comment` | `thread` (FK), `parent` (FK self), `author_handle`, `body`, `upvotes`, `created_at` | Comentário (suporta aninhamento). |
| `Vote` | `usuario` (FK), `content_type` (GFK), `object_id`, `valor` (1/-1) | Voto em thread/comentário. |

### `brain` — My Brain

| Modelo | Campos | Uso |
|--------|--------|-----|
| `BrainNote` | `usuario` (FK), `titulo`, `conteudo`, `source_type`, `source_id`, `tags` (JSON), `criado_em` | Nota mental. |
| `BrainSavedItem` | `usuario` (FK), `titulo`, `url`, `descricao`, `tipo` | Item salvo. |
| `BrainStreak` | `usuario` (FK), `dias_consecutivos`, `ultima_data` | Streak do brain. |
| `BrainFork` | `usuario` (FK), `note` (FK), `criado_em` | Fork de nota. |
| `BrainFollower` | `usuario` (FK), `note` (FK) | Seguidor de nota. |

### `library` — Biblioteca

| Modelo | Campos | Uso |
|--------|--------|-----|
| `Summary` | `titulo`, `autor`, `descricao`, `thumbnail`, `url`, `categoria`, `duracao`, `nivel` | Resumo/library. |
| `Framework` | `framework_id` (CharField), `nome`, `descricao`, `icone`, `categoria`, `nivel` | Framework da biblioteca. |
| `FrameworkReview` | `framework` (FK), `usuario` (FK), `nota`, `comentario`, `criado_em` | Review de framework. |

---

## 3. Administração (Django Admin)

Acesse `/admin/` com superusuário.

### Apps registrados

| App | Modelos no admin | Inlines |
|-----|------------------|---------|
| **Cursos** | Curso, Modulo, Aula, Trilha, Desafio, ProgressoModulo, ProgressoDesafio, Certificate, FeaturedContent, Quiz, Questao, TentativaQuiz | AulaInline (Modulo), TrilhaModuloInline (Trilha), AlternativaInline (Questao) |
| **Usuários** | Perfil, Achievement, UserAchievement, Skill | — |
| **Live** | LiveStream, LiveChatMessage, LivePoll, LivePollVote | — |
| **Social** | Follow, Notification | — |
| **Resources** | ResourceCategory, Resource | — |
| **Guild** | Community, Thread, Comment, Vote | — |
| **Brain** | BrainNote, BrainSavedItem, BrainStreak, BrainFork, BrainFollower | — |
| **Library** | Summary, Framework, FrameworkReview | — |

### FeaturedContent

No admin, na listagem de `FeaturedContent`:
- Campos editáveis inline: `ordem`, `ativo`
- Filtros por `tipo`
- Os tipos disponíveis: `recommended`, `collab`, `case`

---

## 4. Rotas (URLs)

### Páginas principais

| Rota | View | Descrição |
|------|------|-----------|
| `/` | `core.views.index` | Home com trending topics |
| `/explorar` | `core.views.explorar` | Explorar cursos |
| `/perfil` | `core.views.perfil` | Perfil do usuário logado |
| `/config` | `core.views.config` | Configurações (editar perfil) |
| `/trilhas` | `core.views.trilhas` | Trilhas de aprendizado |
| `/conteudos` | `core.views.conteudos` | Módulos e aulas |
| `/desafios` | `core.views.desafios` | Desafios gamificados |
| `/ao-vivo` | `core.views.ao_vivo` | Lives, agenda, replays |
| `/insumos` | `core.views.insumos` | Recursos |
| `/networking` | `core.views.networking` | Feed social |
| `/u/<handle>` | `core.views.user_profile` | Perfil público |
| `/quiz/<id>` | `core.views.quiz_view` | Página do quiz |
| `/quiz/<id>/resultado` | `core.views.quiz_resultado` | Resultado do quiz |
| `/watch/<modulo_slug>/<ordem>/` | `streaming.views.player` | Player de vídeo |
| `/guild` | `guild.views.home` | Home da guild |
| `/g/<slug>` | `guild.views.community` | Comunidade |
| `/g/<community_slug>/post/<post_slug>` | `guild.views.thread_detail` | Thread |
| `/library` | `library.views.library_home` | Biblioteca |
| `/library/framework/<slug>` | `library.views.framework_detail` | Framework |
| `/my-brain` | `brain.views.my_brain` | My Brain |

### Autenticação

| Rota | View |
|------|------|
| `/login` | `django.contrib.auth.views.LoginView` |
| `/logout` | `django.contrib.auth.views.LogoutView` |
| `/registro` | `core.auth_views.registro` |

---

## 5. API Endpoints

Todas as rotas abaixo são prefixadas com `/api/`.

### Guild / Social

| Método | Rota | Função | XP |
|--------|------|--------|----|
| POST | `/api/vote` | Votar (1/-1) em thread ou comentário | — |
| POST | `/api/create_post` | Criar thread na comunidade | +10 |
| POST | `/api/create_comment` | Comentar em thread | +5 |
| POST | `/api/join_community` | Entrar em comunidade | — |
| POST | `/api/follow` | Seguir usuário | — |
| POST | `/api/fork` | Fork de nota do brain | — |
| POST | `/api/review` | Review de framework | — |
| POST | `/api/share` | Compartilhar | — |
| GET | `/api/notes` | Listar notas do brain | — |
| GET | `/api/notifications` | Notificações não lidas | — |

### Progresso / Gamificação

| Método | Rota | Função | XP |
|--------|------|--------|----|
| POST | `/api/progresso` | Atualizar progresso do módulo (0-100). Se 100%, emite certificado + XP do módulo | +xp_modulo |
| POST | `/api/desafio/<id>/completar` | Completar um desafio | +xp_desafio |
| GET | `/api/xp` | Dados de XP do usuário | — |
| POST | `/api/quiz/<id>/submit` | Enviar respostas do quiz | +xp_quiz se aprovado |

### Payloads

**progresso:**
```json
{"modulo_id": 1, "progresso": 75}
```

**create_post:**
```json
{"community_slug": "dev", "title": "...", "body": "...", "tag": "discussão"}
```

**create_comment:**
```json
{"thread_slug": "meu-post", "body": "...", "parent_id": null}
```

**submit_quiz:**
```json
{"respostas": {"1": 3, "2": 1, "3": 5}}
```

**vote:**
```json
{"content_type": "thread", "object_id": 1, "valor": 1}
```

---

## 6. Sistema de Gamificação

### Streak (Sequência de Dias)

`usuarios/middleware.StreakMiddleware`:
- Toda requisição de usuário logado verifica `Perfil.ultimo_login`
- Se `ultimo_login != hoje`: incrementa streak + 10 XP
- Se gap > 1 dia: reseta streak para 1, mantém 10 XP
- Usa `update_fields` para evitar race conditions

### Níveis

- `Perfil.nivel` começa em 1
- Para subir: XP >= `nivel * 500`
- `adicionar_xp(valor)` incrementa XP e auto‑level‑up
- Propriedades: `nome_nivel` (ex: "Bronze III"), `xp_proximo_nivel`, `xp_percentual`

### XP Awards

| Ação | XP |
|------|----|
| Post na comunidade | 10 |
| Comentário | 5 |
| Quick note (brain) | 10 |
| Completar desafio | XP do desafio |
| Concluir módulo (100%) | XP do módulo + certificado |
| Quiz aprovado | XP do quiz |
| Login diário (streak) | 10 |

---

## 7. Seed Data (Comandos)

> Execute sempre com: `python3 manage.py tenant_command <comando> --schema=mundu`

| Comando | App | O que cria |
|---------|-----|------------|
| `seed_db` | `cursos` | 6 módulos, 19 aulas, 2 trilhas, 6 desafios, 7 featured contents, 2 certificados, 2 quizzes (6 questões cada) |
| `seed_resources` | `resources` | 6 categorias, 8 recursos |
| `seed_library` | `library` | 3 summaries, 6 frameworks |
| `seed_live` | `live` | 5 lives (1 ao vivo, 1 agendada, 3 replays), 1 enquete |
| `seed_guild` | `guild` | 6 comunidades, 5 threads com comentários aninhados |
| `seed_usuarios` | `usuarios` | Achievements, skills de exemplo |

> ⚠️ Todos os comandos usam `get_or_create` — são **idempotentes**.

---

## 8. Como Usar — Guia Prático

### Cadastrar um novo Módulo

1. Admin → **Cursos → Módulos** → Adicionar módulo
2. Preencher título, descrição, thumbnail URL, XP, nível
3. O slug é gerado automaticamente do título, mas pode ser editado
4. Salvar

### Adicionar Aulas

1. Dentro do Módulo, usar **Aula inline** no admin
2. Criar aulas com título, URL do YouTube, duração, ordem
3. `is_preview` = True → aula liberada sem login

### Criar um Quiz

1. Admin → **Cursos → Quiz** → Adicionar quiz
2. Vincular ao módulo, definir XP, percentual de aprovação (ex: 70)
3. Salvar
4. Dentro do quiz, adicionar **Questões** (inline)
5. Dentro de cada questão, adicionar **Alternativas** (inline), marcando a correta

### Criar um Desafio

1. Admin → **Cursos → Desafios**
2. Tipo pode ser diário ou semanal
3. `meta` = quantidade de ações para completar
4. XP de recompensa é concedido via API

### Criar uma Live

1. Admin → **Live → Live Streams**
2. Status: `ao_vivo` (aparece no player), `agendado` (aparece na agenda), `replay` (aparece em replays)
3. URL do YouTube, data de agendamento, thumbnail

### Cadastrar Insumos

1. Admin → **Resources → Resource Categories** (criar categorias)
2. Admin → **Resources → Resources** (criar recursos vinculados à categoria)
3. Thumbnail deve ser URL pública (não upload)

### Featured Content (Explorar)

1. Admin → **Cursos → Featured Contents**
2. `tipo` deve ser `recommended`, `collab` ou `case`
3. A ordem e ativo são editáveis na listagem

### Emitir Certificado Manualmente

1. Admin → **Cursos → Certificates**
2. Selecionar usuário, módulo, gerar código único

### Gerenciar Conquistas (Achievements)

1. Admin → **Usuários → Achievements**
2. Criar com título, descrição, tipo e XP de recompensa
3. Admin → **Usuários → User Achievements** — vincular conquista ao usuário

---

## 9. Configurações Importantes

### `mundu/settings.py`

```
APPEND_SLASH = True
MIDDLEWARE = [..., 'usuarios.middleware.StreakMiddleware']
TENANT_APPS = ['live', 'social', 'resources', 'cursos', 'guild', 'brain', 'library', ...]
```

### Jinja2

- Templates usam Jinja2, **não** Django Templates
- CSRF: `{{ csrf_input }}` no form, `getCookie('csrftoken')` no JS
- Loops: `{% for x in list %} ... {{ loop.index }} ... {% endfor %}`
- Filtro de tempo: `strftime` (não existe `|time` do Django)

### URLs do Player

Formato: `/watch/<modulo_slug>/<ordem_da_aula>/`  
Exemplo: `/watch/fundamentos-de-marketing-digital/3/`

### Multi‑tenant

- Schema público: contém usuários globais
- Schema `mundu`: contém todos os dados da plataforma
- Comandos de seed sempre com: `python3 manage.py tenant_command <cmd> --schema=mundu`
- Migrations: `python3 manage.py migrate` (public) + `python3 manage.py tenant_command migrate --schema=mundu` (tenant)

### FeaturedContent TIPOS

| Valor no banco | Uso na template |
|----------------|-----------------|
| `recommended` | `item.type == 'recommended'` |
| `collab` | `item.type == 'collab'` |
| `case` | `item.type == 'case'` |

### Skill → Template

- `Skill.nivel` (1-10) → `pct = f"{nivel}0%"` no template

### TentativaQuiz

- `respostas` é JSON: `{"id_questao": "id_alternativa"}`
- `percentual` é property que calcula `pontuacao / total_questoes * 100`
