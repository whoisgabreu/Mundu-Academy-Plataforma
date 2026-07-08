# Player personalizado com YouTube Iframe API

## O que precisa de ser feito

Substituir o conteúdo de `templates/streaming/player.html` pelo código abaixo.

A alteração substitui o **iframe estático** por um **player controlado pela YouTube Iframe API** com controlos personalizados (apenas play, pause e voltar 10s).

---

## Código final de `templates/streaming/player.html`

```html
{% extends "base.html" %}

{% block title %}{{ aula.titulo }} — Mundu Academy{% endblock %}
{% block page_title %}Player{% endblock %}

{% block content %}
<div class="max-w-5xl mx-auto px-4 py-6">
  <!-- Cabeçalho da Aula -->
  <div class="mb-4">
    <a href="/conteudos" class="inline-flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors mb-3">
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 19-7-7 7-7"/><path d="M19 12H5"/></svg>
      Voltar aos cursos
    </a>
    <h1 class="text-2xl font-bold text-foreground">{{ aula.titulo }}</h1>
    {% if aula.descricao %}
    <p class="text-muted-foreground mt-1">{{ aula.descricao }}</p>
    {% endif %}
    <div class="flex items-center gap-3 mt-2">
      <span class="inline-flex items-center gap-1 text-sm text-muted-foreground">
        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H19a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H6.5a2.5 2.5 0 0 1 0-5H20"/></svg>
        {{ aula.modulo.titulo }}
      </span>
      {% if aula.duracao %}
      <span class="inline-flex items-center gap-1 text-sm text-muted-foreground">
        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 14 16"/></svg>
        {{ aula.duracao }}
      </span>
      {% endif %}
    </div>
  </div>

  <!-- Player YouTube com controlos personalizados -->
  {% set video = get_embed_video(aula.url_video) %}
  <div class="relative bg-black rounded-xl overflow-hidden shadow-2xl" style="aspect-ratio: 16/9;">
    {% if video %}
    <div id="player" class="w-full h-full"></div>

    <div id="controls-overlay" class="absolute inset-0 flex flex-col justify-between pointer-events-none transition-opacity duration-300">
      <!-- Botão Play central -->
      <div id="big-play-btn" class="absolute inset-0 flex items-center justify-center pointer-events-auto">
        <button onclick="togglePlay()" class="w-16 h-16 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center hover:bg-white/30 hover:scale-105 transition-all cursor-pointer">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="white"><polygon points="8 5 19 12 8 19 8 5"/></svg>
        </button>
      </div>

      <!-- Barra inferior de controlos -->
      <div id="bottom-controls" class="bg-gradient-to-t from-black/80 via-black/30 to-transparent pt-12 pb-4 px-4 pointer-events-auto">
        <div class="flex items-center justify-center gap-6">
          <button onclick="rewind()" class="text-white/80 hover:text-white transition-colors cursor-pointer" title="Voltar 10s">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="1 4 1 10 7 10"/>
              <path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/>
            </svg>
          </button>
          <button onclick="togglePlay()" class="text-white hover:text-white transition-colors cursor-pointer" title="Play / Pause">
            <span id="play-icon">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor"><polygon points="8 5 19 12 8 19 8 5"/></svg>
            </span>
            <span id="pause-icon" class="hidden">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg>
            </span>
          </button>
        </div>
      </div>
    </div>
    {% else %}
    <div class="w-full h-full flex items-center justify-center bg-gray-900 text-white/60 text-sm">
      URL de vídeo inválida ou não reconhecida.
    </div>
    {% endif %}
  </div>

  <!-- Ações da Aula -->
  <div class="mt-6 flex flex-wrap items-center justify-between gap-4">
    <div class="flex items-center gap-3">
      <button onclick="openQuickNote('{{ aula.titulo|e }}', '{{ aula.modulo.titulo|e }}')" class="btn-outline inline-flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>
        Quick Note (+10 XP)
      </button>
    </div>

    <a href="/conteudos" class="btn-primary inline-flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium">
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.29 1.51 4.04 3 5.5l7 7Z"/></svg>
      Marcar como concluída
    </a>
  </div>
</div>
{% endblock %}

{% block scripts %}
<script src="https://www.youtube.com/iframe_api"></script>
<script>
var player;
var controlsTimer;

function onYouTubeIframeAPIReady() {
    player = new YT.Player('player', {
        videoId: '{{ video.code }}',
        playerVars: {
            controls: 0,
            modestbranding: 1,
            rel: 0,
            fs: 0,
            iv_load_policy: 3,
            playsinline: 1,
        },
        events: {
            onReady: onPlayerReady,
            onStateChange: onPlayerStateChange,
        }
    });
}

function onPlayerReady() {
    showBigPlay();
    showControls();
    var container = document.querySelector('.relative.bg-black');
    container.addEventListener('mousemove', function() {
        if (player.getPlayerState() === YT.PlayerState.PLAYING) {
            showControls();
            startHideTimer();
        }
    });
    container.addEventListener('mouseleave', function() {
        if (player.getPlayerState() === YT.PlayerState.PLAYING) {
            startHideTimer();
        }
    });
    container.addEventListener('contextmenu', function(e) {
        e.preventDefault();
    });
}

function onPlayerStateChange(event) {
    updatePlayButton();
    if (event.data === YT.PlayerState.PLAYING) {
        hideBigPlay();
        startHideTimer();
    } else if (event.data === YT.PlayerState.PAUSED) {
        showBigPlay();
        showControls();
        clearTimeout(controlsTimer);
    }
}

function togglePlay() {
    if (!player) return;
    if (player.getPlayerState() === YT.PlayerState.PLAYING) {
        player.pauseVideo();
    } else {
        player.playVideo();
    }
}

function rewind() {
    if (!player) return;
    player.seekTo(player.getCurrentTime() - 10, true);
}

function updatePlayButton() {
    if (!player) return;
    var playing = player.getPlayerState() === YT.PlayerState.PLAYING;
    document.getElementById('play-icon').classList.toggle('hidden', playing);
    document.getElementById('pause-icon').classList.toggle('hidden', !playing);
}

function showControls() {
    clearTimeout(controlsTimer);
    var overlay = document.getElementById('controls-overlay');
    overlay.classList.remove('opacity-0');
}

function hideControls() {
    var overlay = document.getElementById('controls-overlay');
    if (player.getPlayerState() !== YT.PlayerState.PAUSED) {
        overlay.classList.add('opacity-0');
    }
}

function startHideTimer() {
    clearTimeout(controlsTimer);
    controlsTimer = setTimeout(hideControls, 3000);
}

function showBigPlay() {
    document.getElementById('big-play-btn').classList.remove('hidden');
}

function hideBigPlay() {
    document.getElementById('big-play-btn').classList.add('hidden');
}
</script>
{% endblock %}
```

---

## Como aplicar

1. Abrir `templates/streaming/player.html`
2. Substituir TODO o conteúdo pelo código acima
3. Guardar o ficheiro
4. Testar a página /watch/{id}/
