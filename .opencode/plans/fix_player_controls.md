# Fix: posição da barra inferior + cor do botão play

## 1. Barra inferior de controlos

**Problema:** A `#bottom-controls` está no topo do vídeo porque:
- `#big-play-btn` é `absolute` → sai do fluxo flex
- `#bottom-controls` é o único filho flex → `justify-between` coloca-o no início

**Correção:** Substituir `flex flex-col justify-between` por posicionamento absoluto.

**Linha 38 — antes:**
```html
<div id="controls-overlay" class="absolute inset-0 flex flex-col justify-between pointer-events-none transition-opacity duration-300">
```

**Linha 38 — depois:**
```html
<div id="controls-overlay" class="absolute inset-0 pointer-events-none transition-opacity duration-300">
```

**Linha 47 — antes:**
```html
<div id="bottom-controls" class="bg-gradient-to-t from-black/80 via-black/30 to-transparent pt-12 pb-4 px-4 pointer-events-auto">
```

**Linha 47 — depois:**
```html
<div id="bottom-controls" class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 via-black/30 to-transparent pt-12 pb-4 px-4 pointer-events-auto">
```

## 2. Botão play central verde (Mundu)

**Problema:** Botão play usa `bg-white/20 backdrop-blur-sm`, que não combina com a marca.

**Correção:** Usar `bg-primary` (verde Mundu: `hsl(145, 90%, 32%)`) com glow.

**Linha 41 — antes:**
```html
<button onclick="togglePlay()" class="w-16 h-16 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center hover:bg-white/30 hover:scale-105 transition-all cursor-pointer">
```

**Linha 41 — depois:**
```html
<button onclick="togglePlay()" class="w-16 h-16 rounded-full bg-primary shadow-lg shadow-primary/40 flex items-center justify-center hover:scale-105 transition-all cursor-pointer">
```

---

## Ficheiro a editar

`templates/streaming/player.html` — 3 linhas alteradas (38, 41, 47)
