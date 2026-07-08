# Mundu Academy — Anchored Summary

## Goal
Wire every page to real Django models, removing all hardcoded placeholder data.

## Constraints & Preferences
- URL structure for video player: `/watch/<modulo_slug>/<ordem>/` instead of `/watch/<aula_id>/`
- Controls overlay uses solid Mundu green (`bg-primary`) with gradient from `--gradient-primary`
- Top overlay (50% width, left-aligned) covers YouTube title; auto-hides together with bottom controls
- Progress bar tracks video time; click to seek; timestamp shows current/total duration
- Custom controls hide after 4s (changed from 6s→4500ms→4000ms)
- `APPEND_SLASH = True` (changed from False)
- New apps are tenant-scoped: `live/`, `social/`, `resources/`
- Perfil extended with `bio`, `empresa`, `localizacao`, `linkedin`, `instagram`, `role` computed property
- LiveStream model embeds YouTube lives + scheduling (data_agendamento)
- Resource thumbnails use public URLs (not uploaded files)
- Chat messages are user-only (no system messages for now)

## Progress

### Done
- Replaced gradient bottom bar with solid `bg-primary` + progress bar (track/fill/thumb) + timestamp
- Added top overlay (`#top-controls`) at 50% width, left-aligned, with aula title, auto-hides with controls overlay
- Increased central play button size: `w-16 h-16` → `w-20 h-20`, icon `32×32` → `40×40`
- Applied `--gradient-primary` (from `.btn-primary`) to both top and bottom overlays
- Changed auto-hide timer from 3000ms → 6000ms → 4500ms → 4000ms
- Added `slug` field to `Modulo` model with auto-`slugify` in `save()`, `prepopulated_fields` in admin
- Created data migration (0009) to populate slugs for existing modules
- Changed URL pattern to `watch/<slug:modulo_slug>/<int:ordem>/`
- Updated `streaming/views.py` to lookup by `modulo.slug` + `aula.ordem`
- Updated `core/views.py` to pass `slug` and `ordem` in module/aula dicts
- Updated sidebar link in `player.html` and aula link in `conteudos.html`
- Set `APPEND_SLASH = True` in `mundu/settings.py`
- Created 3 new apps and their models: `live/` (LiveStream, LiveChatMessage, LivePoll, LivePollVote), `social/` (Follow, Notification), `resources/` (ResourceCategory, Resource)
- Added `Certificate` model to `cursos/models.py`
- Registered all new models and Certificate in admin
- Added all 3 new apps to `TENANT_APPS`
- Extended `Perfil` model with `bio`, `empresa`, `localizacao`, `linkedin`, `instagram`, `data_criacao`, and `role` property; created and applied migration
- Updated `core/utils.py` `_get_current_user()` to include all new Perfil fields
- Wired `library/views.py` to real `Summary`, `Framework`, `FrameworkReview` models; updated template references from `.id` to `.framework_id`
- Wired `brain/views.py` to real `BrainNote`, `BrainSavedItem`, `BrainStreak`, `BrainFork`, `BrainFollower` models; enriched user data from real DB
- Wired Ao Vivo (`/ao-vivo`) view to real `LiveStream` (ao_vivo, upcoming, replays), `LiveChatMessage`, `LivePoll` models; empty state when no live
- Replaced all hardcoded `{% set %}` blocks in `ao_vivo.html` with `live_now`, `upcoming`, `replays`, `chat_messages`, `active_poll` context variables
- Wired Guild pages (Home, Community, Thread) to real `Community`, `Thread`, `Comment` models — all views rewritten in `guild/views.py` with ORM queries, user enrichment via `Perfil`, comment tree building, and `time_ago` computation from `created_at`
- Created `Vote` model with GenericForeignKey for per-user upvote/downvote on Threads and Comments
- Added `created_at` and `url` to `Thread`, `created_at` to `Comment`, `karma` to `Perfil`
- Created `seed_guild` management command that populates 6 communities, 5 threads, and nested comments
- Removed all hardcoded dicts (`USERS`, `guild_communities`, `guild_threads`, `COMMENTS`, `library_frameworks`) from `core/views.py` — wired `build_unified_feed()`, `explorar()`, `user_profile()` to real DB queries
- Removed hardcoded notifications from `core/utils.py` — wired `_get_notifications()` and `render()` to real `Notification` model from `social/` app
- Rewrote `core/api.py` — all endpoints now use real DB models
- Wired **Config** (`/config`) — `PerfilModelForm` (new `usuarios/forms.py`) with fields: first_name, last_name, cargo, empresa, localizacao, linkedin, instagram, bio; GET prepopulates, POST saves + redirects
- Wired **Insumos** (`/insumos`) — `ResourceCategory.objects.all()` → cats, `Resource.objects.all()` → insumos enriched dicts
- Wired **Perfil** (`/perfil`) — stats (xp, certs, desafios, conexoes) from DB; trilhas em progresso from ProgressoModulo; certificados from Certificate; networking from Follow; progresso tab (streak + total horas)
- Wired **Networking** (`/networking`) — posts from Thread (author enrichment, upvotes, replies); quem seguir from Perfil; trends from Thread tags aggregation
- Wired **Explorar** (`/explorar`) — continue_watching from ProgressoModulo (logged in); challenges from Desafio model; recommended/collabs/cases from FeaturedContent model; removed `_continue_watching`/`_challenges` hardcoded lists and all 3 hardcoded dicts
- Wired **Index** (`/`) — trending_topics from Thread tags dynamic query; added `followed_count` context
- Fixed `/my-brain` 500 error — added `@login_required` decorator
- Created `Achievement` (with `descricao`), `UserAchievement`, `Skill` models in `usuarios/models.py` — full admin registration
- Created `FeaturedContent` model in `cursos/models.py` with admin registration (list_editable ordem/ativo)
- Wired **Perfil** achievements/skills — removed `{% set %}` hardcoded blocks, now from `UserAchievement` + `Skill` models
- Wired **Explorar** recommended/collabs/cases — removed 3 hardcoded dicts (`_recommended`, `_collabs`, `_cases`), now from `FeaturedContent` model
- Extended `seed_db` with FeaturedContent; created `seed_usuarios` for achievements+skills
- Merged duplicate `### Done` sections
- **Phase A — Template cleanup**: Removed `{% set %}` overriding context in `insumos.html` (cats + insumos), `networking.html` (sug + trends), `desafios.html` (conquistas + unlockables). Removed fallback hardcoded topics in `core/views.py:135`.
- **Desafios view** rewired: passes `streak_dias`, `daily_done`/`daily_total`, `weekly_done`/`weekly_total`, `conquistas` from Achievement/UserAchievement, `unlockables` from context. Template now uses dynamic values for streak counter, progress counts, achievements grid, unlockables.
- **Phase B — Seed data**: Extended `seed_db` with `_seed_aulas()` (19 aulas across 6 módulos) and `_seed_certificados()`. Created `seed_resources` (6 cats + 8 resources), `seed_library` (3 summaries + 6 frameworks), `seed_live` (5 lives + 1 poll).
- **Phase C — Gamification**: Added `ultimo_login` (DateField) to Perfil. Created `usuarios/middleware.py` (StreakMiddleware) that tracks daily login streak, awards +10 XP per day, resets streak on miss. Registered in `MIDDLEWARE` settings. Migration `usuarios 0006`.
- **XP awards in API**: `create_post` → +10 XP, `create_comment` → +5 XP, `quick_note` → +10 XP, `complete_challenge` → +XP do desafio, `update_progress 100%` → +XP do módulo + Certificate. Video progress tracking endpoint at `api/progresso`. Challenge complete endpoint at `api/desafio/<id>/completar`. My XP endpoint at `api/xp`.
- **Phase D — Quiz system**: Created `Quiz`, `Questao`, `Alternativa`, `TentativaQuiz` models in `cursos/models.py`. Registered in admin with `AlternativaInline`. Created `quiz.html` template, `quiz_view` in `core/views.py`, `submit_quiz` API endpoint in `core/api.py`, seed data (`_seed_quizzes` in `seed_db`). Migration applied (cursos 0012).
- **Phase E — Quiz results & integration**: Added `respostas` JSONField to `TentativaQuiz` (cursos 0013), `percentual` property. Created `quiz_resultado` view + template with per-question feedback. Updated `submit_quiz` API to store answers. Redirect on approval to `/quiz/<id>/resultado`. Linked quizzes from `conteudos.html` (per-module quiz link with XP badge). Added `quiz` context to `conteudos` view.
- All 15+ views return 200 (index, explorar, perfil, config, insumos, networking, desafios, ao_vivo, conteudos, trilhas, my_brain, library, player, guild_home, community).

### Blocked
- (none)

## Key Decisions
- **`var(--gradient-primary)` over solid `bg-primary`**: Both overlays now use the same gradient as `.btn-primary` (linear-gradient 135°), consistent with the platform's visual identity
- **URL structure `/watch/<slug>/<ordem>/`**: Replaces flat `/watch/<id>/` to avoid 404s when new aulas are added without a matching ID route; enables descriptive, module-scoped URLs
- **Auto-slugify on `save()`**: Slugs are generated from `titulo` if empty, but can be manually overridden in admin
- **Social features in `social/` app**: Follow + Notification live together, leaves room for future models (Block, Report, Mention) without refactoring
- **Library/Brain wired first**: Simplest pages because model fields match template variable names almost exactly; minimal template changes needed
- **Ao Vivo template uses empty states**: When no live is active, shows a message instead of breaking; Agenda/Replays tabs also have fallback content
- `ao_vivo.html` `|time` filter replaced with `strftime('%H:%M')` because Jinja2 doesn't have Django's `|time`.
- Desafios unlockables kept as static list in view (no model yet); can be extracted to `Unlockable` model later.
- Quiz questions use inline `Alternativa` in admin via `AlternativaInline`.
- StreakMiddleware uses `update_fields` to avoid race conditions on Perfil save.
- Seed commands use `get_or_create` to be idempotent.

## Next Steps
- *(none — all phases completed)*

## Critical Context
- `APPEND_SLASH = True` fixed 404 on `/watch/2` (pattern required `/` suffix).
- Templates use Jinja2, so `{% set %}` has block scope; all hardcoded `{% set %}` blocks have been removed.
- Framework model has `framework_id` (CharField) for the string ID ("fw1"); Django's auto `id` is the integer PK.
- `core/utils.py` `_get_current_user()` returns a dict consumed by nearly every template; `role` is computed from Perfil's `cargo` + `empresa`.
- All migrations applied to both public and tenant schemas.
- `FeaturedContent` TIPOS: recommended/collab/case; template expects `item.type` to match.
- `Achievement` lookup by `titulo`; `UserAchievement` uses `select_related('achievement')`.
- `Skill.nivel` (1-10) maps to template `pct` as `{nivel}0%`.
- StreakMiddleware checks `ultimo_login != hoje`; consecutive day = streak+1; gap >1 day = reset to 0.
- Quiz: `Alternativa` related_name `alternativas` (plural); `TentativaQuiz` stores `pontuacao`/`total_questoes`/`aprovado`.
- XP awarded via `perfil.adicionar_xp()` which auto-levels up when XP >= `nivel * 500`.

## Relevant Files
- `cursos/models.py`: Modulo, ProgressoModulo, Trilha, TrilhaModulo, Desafio, ProgressoDesafio, Aula, Certificate, FeaturedContent, Quiz, Questao, Alternativa, TentativaQuiz
- `usuarios/models.py`: Perfil (xp_total, nivel, streak_dias, ultimo_login + properties), Achievement, UserAchievement, Skill
- `usuarios/middleware.py`: StreakMiddleware — tracks daily login streak with +10 XP/day
- `live/models.py`: LiveStream, LiveChatMessage, LivePoll, LivePollVote
- `social/models.py`: Follow, Notification
- `resources/models.py`: ResourceCategory, Resource
- `core/views.py`: All page views wired to DB (index, explorar, perfil, config, insumos, networking, desafios, ao_vivo, conteudos, trilhas, user_profile, quiz_view)
- `core/api.py`: 20 endpoints (vote, create_post, create_comment, join_community, follow, fork, review, share, notes, notifications, progresso, complete_challenge, my_xp, submit_quiz)
- `core/api_urls.py`: All API routes including `progresso`, `desafio/<id>/completar`, `xp`, `quiz/<id>/submit`
- `cursos/views.py`: `quiz_view` (redirect)
- `cursos/admin.py`: All models registered with inlines (AulaInline, TrilhaModuloInline, AlternativaInline)
- `cursos/management/commands/seed_db.py`: Seeds 6 modulos, 2 trilhas, 6 desafios, 7 featured, 19 aulas, 2 certificados, quizzes
- `resources/management/commands/seed_resources.py`: 6 cats + 8 resources
- `library/management/commands/seed_library.py`: 3 summaries + 6 frameworks
- `live/management/commands/seed_live.py`: 5 lives + 1 poll
- `guild/management/commands/seed_guild.py`: 6 communities, 5 threads, nested comments
- `templates/quiz.html`: Quiz page with radio inputs, submit via JS, score feedback
- `templates/`: All templates cleaned of `{% set %}` hardcoded blocks — `insumos.html`, `networking.html`, `desafios.html`, `ao_vivo.html`
- `mundu/settings.py`: MIDDLEWARE includes `usuarios.middleware.StreakMiddleware`
