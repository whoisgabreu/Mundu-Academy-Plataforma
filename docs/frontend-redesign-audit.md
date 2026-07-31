# Mundu Academy — auditoria e direção do redesign

> Documento de decisão criado antes da implementação visual.
> Objetivo: reconstruir a experiência sem alterar URLs, remover modelos ou
> substituir dados reais por conteúdo de demonstração.

## 1. Diagnóstico do produto atual

A interface atual não possui uma linguagem única. Ela mistura, na mesma
experiência:

- shell de dashboard com sidebar e barra de métricas;
- componentes utilitários genéricos de Tailwind/shadcn;
- feed inspirado em Twitter/Reddit;
- navegação e cards inspirados em GitHub;
- páginas escuras com tratamento visual industrial;
- carrosséis e reels inspirados em streaming e redes sociais.

O resultado é uma plataforma que comunica "software para operar" em vez de
"lugar para aprender". Conteúdo, progresso e comunidade recebem o mesmo peso
visual, quase sempre dentro de caixas equivalentes.

Evidências objetivas do estado inicial:

- `static/css/style.css`: 9.048 linhas, aproximadamente 1.241 regras;
- 26 templates dependem de classes utilitárias do Tailwind;
- 12 templates possuem CSS ou estilos inline;
- Tailwind é carregado por CDN ao mesmo tempo que o CSS proprietário;
- a Home é um feed social e possui composer de publicação como ação central;
- o tema escuro é ativado por padrão;
- o carrossel principal do Explorar vem de um array hardcoded no JavaScript;
- o chatbot Salomão simula resposta e admite não estar ligado a uma API;
- algumas ações exibem sucesso mesmo quando a persistência falha.

## 2. Princípios da nova Mundu

### Produto

1. **Aprendizado primeiro.** A próxima ação útil de estudo deve ser a decisão
   mais fácil da tela.
2. **Progresso como narrativa.** XP, sequência e conquistas aparecem como
   evidência de evolução, não como um painel de indicadores.
3. **Conteúdo com presença editorial.** Imagem, professor, contexto, duração e
   objetivo substituem grades de cards indistinguíveis.
4. **Comunidade com intenção.** Comunidades e discussões são destinos, não um
   feed infinito misturado à entrada do produto.
5. **Captura sem fricção.** O My Brain permanece acessível globalmente e só
   confirma uma nota depois de persistir.
6. **Menos interface.** Bordas são reservadas a controles, separação necessária
   e estados de foco; espaço e tipografia fazem a maior parte da hierarquia.

### Linguagem visual

- tema claro como padrão;
- Inter como família tipográfica;
- paleta principal do briefing: `#F8F9F7`, `#F4F5F3`, `#E8ECE7`,
  `#16A34A`, `#15803D`, `#151515`, `#6B7280`;
- superfícies levemente quebradas para evitar branco puro;
- assinatura Mundu baseada em órbitas, caminhos e pontos de progresso;
- motion entre 150 e 250 ms, `ease-out`, respeitando
  `prefers-reduced-motion`;
- foco visível, alvos mínimos de toque, HTML semântico e contraste WCAG AA.

## 3. Decisão por experiência

| Experiência | Problema atual e por que é ruim | Solução aprovada para implementação | Contrato funcional preservado |
| --- | --- | --- | --- |
| Shell global | Sidebar, header de XP, bottom nav e FAB competem o tempo todo; a plataforma parece um painel administrativo. | Header horizontal calmo, navegação pelos cinco destinos principais, captura rápida contextual, menu móvel reorganizado e perfil/XP discretos. | Mesmas URLs, notificações reais, alternância de tema, perfil, área do professor e Quick Note. |
| Home | É um feed com stories, composer, ordenação e sidebar social; não funciona como lobby. | Lobby personalizado: saudação, retomada de aprendizado dominante, ritual do dia, evolução, cursos, comunidades, Library e conquista recente. Sem feed infinito. | Dados derivados de módulos, progresso, desafios, comunidades, frameworks e conquistas reais. |
| Explorar | Hero hardcoded, CTAs sem destino e cinco carrosséis visualmente iguais. | Descoberta editorial com destaque vindo do banco, coleções com ritmos diferentes e entradas claras para cursos, collabs, casos, Library e Guild. | `FeaturedContent`, progresso, desafios, frameworks e threads continuam como fontes. |
| Cursos | Módulos parecem registros administrativos em accordions repetidos. | Catálogo cinematográfico com um curso em foco, capas dominantes, metadados essenciais e currículos progressivamente revelados. | `/conteudos`, módulos, aulas, quiz, progresso, XP e certificado. |
| Trilhas | Filtros decorativos e cards densos escondem a sequência de domínio. | Jornadas editoriais com mapa de marcos, progresso longitudinal e estados concluído/em curso/bloqueado inequívocos. | Dados de `Trilha`, `TrilhaModulo` e `ProgressoModulo`. |
| Player | O vídeo está cercado por UI utilitária e a ação de conclusão não persiste progresso. | Sala de foco: vídeo como protagonista, overlays Mundu preservados, trilha lateral leve e captura de insight próxima ao conteúdo. | URL `/watch/<modulo_slug>/<ordem>/`, controles de vídeo, auto-hide em 4 s, seek/timestamp e endpoint de progresso. |
| Quiz e resultado | Formulário e resultado parecem páginas genéricas, sem sensação de etapa de aprendizagem. | Sessão focada, uma hierarquia de pergunta por vez/por bloco e resultado narrado como domínio, com revisão clara. | Tentativas, respostas, aprovação, XP e redirect existentes. |
| Ao vivo | Layout comprime vídeo, chat, enquete e agenda em vários painéis concorrentes; envio do chat aparenta funcionar sem fluxo real. | Palco para a transmissão, agenda editorial e replays; chat só permanece como ação quando existir persistência real. | `LiveStream`, agenda, replays, mensagens e enquete continuam visíveis conforme dados reais. |
| Guild | Copia fóruns/Reddit: votos, cards, sidebar e nomenclatura `r/` dominam a experiência. | Praça de comunidades: identidade visual por comunidade, eventos/atividade, discussões curadas, membros ativos e ranking. | Comunidades, membership, criação, edição, threads, votos e links atuais. |
| Comunidade | Cabeçalho e lista de posts repetem Reddit; muitas ações pequenas competem. | Página de clube com manifesto, atividade, discussões em destaque, regras e pessoas integradas à narrativa. | Entrar/sair, criar post, votar, compartilhar, moderar e URLs atuais. |
| Thread | Coluna de votos, metadados e ações decorativas fragmentam leitura; há botões sem implementação. | Leitura longa, autor/contexto primeiro, respostas como conversa e apenas ações reais. | Voto, comentário, resposta, seguir e Quick Note. |
| Networking | Replica um feed social genérico e oferece ações sem contexto de thread. | Diretório de pessoas e conversas úteis, com aproximações por tema e link para a discussão de origem. | Perfis, Follow, threads e tendências reais. |
| Library | Frameworks parecem repositórios e summaries parecem cards de catálogo. | Biblioteca premium: coleções editoriais, objetos de conhecimento com preview, aplicação, autoria e prova social. | `Summary`, `Framework`, fork, reviews e detalhe. |
| Framework | Densidade de metadados e sidebar lembram GitHub; há inconsistências de contexto/HTML e endpoint de review. | Página de produto de conhecimento: promessa, como aplicar, versão, prova social, fork e review com estados honestos. | Mesmo slug/ID e APIs, após correção do contrato quebrado. |
| My Brain | Notas, salvos, forks e seguidores são caixas equivalentes; a captura não é dominante. | Workspace de pensamento: captura instantânea, stream de notas valiosas, coleções/forks como contexto e privacidade explícita. | Notas, visibilidade, salvos, streak, forks e seguidores persistidos. |
| Insumos | Busca e tabs são decorativas; grade genérica trata todos os recursos como iguais. | Estante de ferramentas com busca/filtros funcionais no cliente e agrupamento por formato/aplicação. | Categorias e `Resource` reais; links públicos preservados. |
| Perfil próprio | É um dashboard de métricas e mini-cards, com cores utilitárias concorrentes. | Retrato de evolução: identidade, trajetória, domínio, conquistas, certificados e relações em narrativa vertical. | Perfil, XP, nível, streak, skills, certificados, conexões e leaderboard. |
| Perfil público | Imita perfil de rede social e contém estado “em breve”. | Página de membro centrada em contribuição, experiência, discussões e relação com a comunidade. | `/u/<handle>`, posts, comentários, Follow e estados próprio/terceiro. |
| Desafios | Gamificação aparece como grade colorida e painel de contadores. | Ritual de progresso sóbrio: missão atual dominante, sequência, próximas metas e conquistas como marcos. | Desafios, progresso, XP, achievements e unlockables existentes. |
| Configurações | Estrutura de formulário inválida, campos omitidos e excesso de painéis. | Formulário editorial em seções curtas, preview de identidade e feedback de erro/sucesso acessível. | `PerfilModelForm`, POST e redirect atuais; todos os campos reais renderizados. |
| Professor | Dashboard administrativo genérico, porém é uma superfície de trabalho legítima. | Studio separado do consumo: navegação compacta, tabelas legíveis, formulários robustos e densidade controlada. | CRUDs, permissões, busca, paginação, reordenação, quiz builder e certificados. |
| Autenticação | Login industrial dark e registro Tailwind roxo parecem produtos diferentes. | Entrada serena e única, light-first, com narrativa de benefício e formulários consistentes. | Login, registro, CSRF, mensagens e alteração de senha. |
| Certificado/404 | Páginas utilitárias sem continuidade de marca. | Certificado como artefato premium e 404 como recuperação simples com caminhos reais. | Verificação/download do certificado e códigos HTTP/rotas existentes. |

## 4. Problemas funcionais descobertos durante a auditoria

O redesign não deve mascarar controles quebrados. Os seguintes pontos precisam
ser corrigidos junto com a experiência correspondente:

1. o player não chama `/api/progresso`;
2. a rota de concluir desafio inclui `desafio_id`, mas a view correspondente
   não recebe esse argumento;
3. criação de review de framework usa campos que não existem em
   `FrameworkReview`;
4. o detalhe de framework recebe `related_frameworks`, mas o template procura
   `related`;
5. Config possui fechamento de `form` fora de ordem e omite campos reais;
6. ações públicas que exigem usuário precisam redirecionar para login ou ser
   exibidas apenas quando autenticado;
7. sucessos otimistas não podem ser mostrados quando a resposta da API falhar;
8. controles sem fluxo (chat fake, salvar/mais sem implementação, filtros
   decorativos) devem ser removidos, desabilitados explicitamente ou ligados a
   uma ação real.

## 5. Arquitetura de frontend

O frontend será separado por responsabilidade, sem framework visual genérico:

- `static/css/style.css`: foundations, tokens, reset, acessibilidade, shell e
  primitives compartilhadas;
- `static/css/pages/lobby.css`: Home e Explorar;
- `static/css/pages/learning.css`: cursos, trilhas, player, quiz e lives;
- `static/css/pages/community.css`: Guild, comunidades, threads e networking;
- `static/css/pages/knowledge.css`: Library, Framework, My Brain e insumos;
- `static/css/pages/growth.css`: perfil, desafios e configurações;
- `static/css/pages/studio.css`: área do professor;
- `static/css/pages/auth.css`: autenticação, certificado e estados de sistema;
- `static/js/app.js`: comportamento global real, sem conteúdo hardcoded nem
  respostas simuladas.

As páginas continuam em Jinja2 e consomem os mesmos contextos Django. O redesign
é visual e de organização; mudanças de backend serão somente aditivas para
expor dados reais, completar ações existentes ou corrigir contratos quebrados.
