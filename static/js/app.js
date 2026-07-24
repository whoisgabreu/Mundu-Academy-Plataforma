/* ============================================
   MUNDU ACADEMY - JavaScript Principal
   Interatividade sem frameworks
   ============================================ */

// ============ SIDEBAR ============

function toggleSidebar() {
  const sidebar = document.getElementById('sidebar');
  const mainWrapper = document.getElementById('mainWrapper');
  
  sidebar.classList.toggle('collapsed');
  mainWrapper.classList.toggle('sidebar-collapsed');
  
  // Salvar estado no localStorage
  const isCollapsed = sidebar.classList.contains('collapsed');
  localStorage.setItem('sidebarCollapsed', isCollapsed);
}

// Restaurar estado da sidebar ao carregar a página
document.addEventListener('DOMContentLoaded', function() {
  const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
  if (isCollapsed) {
    const sidebar = document.getElementById('sidebar');
    const mainWrapper = document.getElementById('mainWrapper');
    if (sidebar) sidebar.classList.add('collapsed');
    if (mainWrapper) mainWrapper.classList.add('sidebar-collapsed');
  }
  
  // Inicializar o hero se existir na página
  if (document.getElementById('heroSection')) {
    initHero();
  }
});

// ============ HERO CARROSSEL ============

const heroBanners = [
  {
    id: "1",
    badge: "COLLAB EXCLUSIVA",
    badgeType: "collab",
    title: 'Domine o <span class="highlight">Growth Marketing</span> em 30 dias',
    description: "Trilha completa com Thiago Nigro. Do zero ao avançado em estratégias de crescimento que geraram mais de R$ 50M em vendas.",
    duration: "12 horas",
    xp: "+800 XP",
    students: "2.4k alunos",
    image: "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=1920&q=80",
    ctaText: "Começar Trilha"
  },
  {
    id: "2",
    badge: "MASTERCLASS",
    badgeType: "masterclass",
    title: 'Aprenda <span class="highlight">Vendas B2B</span> com Aaron Ross',
    description: "O criador do Predictable Revenue ensina como escalar vendas de forma previsível e construir times de alta performance.",
    duration: "4 horas",
    xp: "+500 XP",
    students: "1.8k alunos",
    image: "https://images.unsplash.com/photo-1552664730-d307ca884978?w=1920&q=80",
    ctaText: "Assistir Masterclass"
  },
  {
    id: "3",
    badge: "CURSO COMPLETO",
    badgeType: "curso",
    title: 'Construa sua <span class="highlight">Marca Pessoal</span> de sucesso',
    description: "8 módulos práticos para você se posicionar como autoridade no mercado e atrair oportunidades de forma orgânica.",
    duration: "6 horas",
    xp: "+450 XP",
    students: "3.2k alunos",
    image: "https://images.unsplash.com/photo-1493612276216-ee3925520721?w=1920&q=80",
    ctaText: "Começar Curso"
  },
  {
    id: "4",
    badge: "AO VIVO HOJE",
    badgeType: "live",
    title: 'Workshop: <span class="highlight">Pitch Perfeito</span> para Investidores',
    description: "Aprenda a estruturar e apresentar seu pitch de forma convincente. Sessão ao vivo com feedback em tempo real.",
    duration: "2 horas",
    xp: "+200 XP",
    students: "456 inscritos",
    image: "https://images.unsplash.com/photo-1559136555-9303baea8ebd?w=1920&q=80",
    ctaText: "Participar Agora"
  },
  {
    id: "5",
    badge: "WORKSHOP",
    badgeType: "workshop",
    title: 'Domine as <span class="highlight">Técnicas de Negociação</span> avançadas',
    description: "Workshop intensivo com exercícios práticos. Aprenda a negociar como os melhores executivos do mercado.",
    duration: "3 horas",
    xp: "+350 XP",
    students: "890 alunos",
    image: "https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=1920&q=80",
    ctaText: "Entrar no Workshop"
  }
];

let heroIndex = 0;
let heroInterval = null;

function initHero() {
  renderHero(0);
  renderDots();
  startHeroAutoplay();
}

function renderHero(index) {
  const banner = heroBanners[index];
  const content = document.getElementById('heroContent');
  
  // Animação de transição
  content.style.opacity = '0';
  content.style.transform = 'translateY(20px)';
  
  setTimeout(() => {
    document.getElementById('heroImg').src = banner.image;
    document.getElementById('heroBadgeText').textContent = banner.badge;
    
    // Atualizar classe do badge
    const badgeEl = document.getElementById('heroBadge');
    badgeEl.className = 'hero-badge ' + banner.badgeType;
    
    document.getElementById('heroTitle').innerHTML = banner.title;
    document.getElementById('heroDesc').textContent = banner.description;
    document.getElementById('heroDuration').textContent = banner.duration;
    document.getElementById('heroXp').textContent = banner.xp;
    document.getElementById('heroStudents').textContent = banner.students;
    document.getElementById('heroCtaText').textContent = banner.ctaText;
    
    // Atualizar dots
    updateDots(index);
    
    // Animar entrada
    content.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
    content.style.opacity = '1';
    content.style.transform = 'translateY(0)';
  }, 200);
}

function renderDots() {
  const dotsContainer = document.getElementById('heroDots');
  dotsContainer.innerHTML = '';
  
  heroBanners.forEach((_, i) => {
    const dot = document.createElement('button');
    dot.className = 'hero-dot' + (i === 0 ? ' active' : '');
    dot.onclick = () => heroGoTo(i);
    dotsContainer.appendChild(dot);
  });
}

function updateDots(index) {
  const dots = document.querySelectorAll('.hero-dot');
  dots.forEach((dot, i) => {
    dot.classList.toggle('active', i === index);
  });
}

function heroGo(direction) {
  heroIndex = (heroIndex + direction + heroBanners.length) % heroBanners.length;
  renderHero(heroIndex);
  restartHeroAutoplay();
}

function heroGoTo(index) {
  heroIndex = index;
  renderHero(heroIndex);
  restartHeroAutoplay();
}

function startHeroAutoplay() {
  heroInterval = setInterval(() => {
    heroIndex = (heroIndex + 1) % heroBanners.length;
    renderHero(heroIndex);
  }, 8000);
}

function restartHeroAutoplay() {
  clearInterval(heroInterval);
  startHeroAutoplay();
}

// ============ CARROSSÉIS DE CONTEÚDO ============

function scrollCarousel(trackId, amount) {
  const track = document.getElementById(trackId);
  if (track) {
    track.scrollBy({ left: amount, behavior: 'smooth' });
  }
}

// ============ ANIMAÇÕES DE SCROLL ============

// Observador para animar elementos quando entram na viewport
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -50px 0px'
};

const animateObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
      animateObserver.unobserve(entry.target);
    }
  });
}, observerOptions);

document.addEventListener('DOMContentLoaded', () => {
  // Observar elementos com animação
  document.querySelectorAll('.animate-fade-in-up').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.4s ease-out, transform 0.4s ease-out';
    animateObserver.observe(el);
  });
});

// ============ SALOMÃO IA CHATBOT ============

function toggleChatbot() {
  const chatWindow = document.getElementById('chatbotWindow');
  if (!chatWindow) return;

  chatWindow.classList.toggle('open');

  if (chatWindow.classList.contains('open')) {
    // Focar no input quando abrir com pequeno delay para a transição
    setTimeout(() => {
      const input = document.getElementById('chatbotInput');
      if (input) input.focus();
    }, 300);
  }
}

function handleChatKeypress(event) {
  if (event.key === 'Enter') {
    sendChatMessage();
  }
}

function sendChatMessage() {
  const input = document.getElementById('chatbotInput');
  const text = input.value.trim();

  if (!text) return;

  const messagesContainer = document.getElementById('chatbotMessages');

  // Adicionar mensagem do usuário
  const userMsg = document.createElement('div');
  userMsg.className = 'chat-message user animate-fade-in-up';
  userMsg.textContent = text;
  messagesContainer.appendChild(userMsg);

  input.value = '';

  // Rolar para o final
  messagesContainer.scrollTop = messagesContainer.scrollHeight;

  // Simular resposta do bot (mockup)
  setTimeout(() => {
    const botMsg = document.createElement('div');
    botMsg.className = 'chat-message bot animate-fade-in-up';
    botMsg.textContent = "Excelente pergunta! Estou analisando seu histórico na Mundu Academy. Note que neste mockup de interface, ainda não estou conectado à API do GPT, mas logo poderei te entregar respostas personalizadas reais.";
    messagesContainer.appendChild(botMsg);

    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }, 1200);
}

// ============ QUICK NOTE MODAL (Segundo Cérebro) ============

let _quicknoteSourceTitle = '';

function openQuickNote(title, source) {
  const backdrop = document.getElementById('quicknoteBackdrop');
  if (!backdrop) return;

  _quicknoteSourceTitle = title || '';
  const sourceText = document.getElementById('quicknoteSourceText');
  if (sourceText) sourceText.textContent = source || title || '—';

  const titleInput = document.getElementById('quicknoteTitle');
  const contentInput = document.getElementById('quicknoteContent');
  if (titleInput) titleInput.value = title ? 'Sobre: ' + title : '';
  if (contentInput) contentInput.value = '';

  backdrop.classList.add('open');
  setTimeout(function(){
    if (contentInput) contentInput.focus();
  }, 220);
}

function closeQuickNote(event) {
  // Quando chamado via backdrop click, garante que só fecha se clicou no backdrop
  if (event && event.currentTarget !== event.target) return;
  const backdrop = document.getElementById('quicknoteBackdrop');
  if (backdrop) backdrop.classList.remove('open');
}

function saveQuickNote() {
  const titleInput = document.getElementById('quicknoteTitle');
  const contentInput = document.getElementById('quicknoteContent');
  const title = (titleInput && titleInput.value || '').trim();
  const content = (contentInput && contentInput.value || '').trim();

  if (!content) {
    if (contentInput) {
      contentInput.style.borderColor = 'hsl(0 90% 60%)';
      contentInput.focus();
      setTimeout(function(){ contentInput.style.borderColor = ''; }, 1200);
    }
    return;
  }

  const payload = {
    title: title || 'Nota rápida',
    content: content,
    source: _quicknoteSourceTitle
  };

  // Tenta persistir; se falhar, ainda dá feedback positivo (mockup)
  try {
    fetch('/api/quick-note', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    }).then(function(){
      if (window.MunduGamification) window.MunduGamification.refresh();
    }).catch(function(){ /* silencioso — é mockup */ });
  } catch (_) { /* noop */ }

  closeQuickNote();
  showToast('🧠 Nota salva no My Brain (+10 XP)');
}

// Atalho Ctrl+Enter para salvar
document.addEventListener('keydown', function(e){
  const backdrop = document.getElementById('quicknoteBackdrop');
  if (!backdrop || !backdrop.classList.contains('open')) return;
  if (e.key === 'Escape') {
    closeQuickNote();
  } else if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
    e.preventDefault();
    saveQuickNote();
  }
});

// ============ NOTIFICATIONS DROPDOWN ============

function toggleNotifications(event) {
  if (event) event.stopPropagation();
  const dropdown = document.getElementById('notifDropdown');
  const btn = document.getElementById('notifBtn');
  if (!dropdown) return;
  const isOpen = dropdown.classList.toggle('open');
  if (btn) btn.classList.toggle('is-active', isOpen);
}

function markNotificationRead(linkEl, notifId) {
  // Não previne navegação — só marca como lida em background
  if (linkEl) {
    linkEl.classList.remove('is-unread');
    const dot = linkEl.querySelector('.notif-unread-dot');
    if (dot) dot.remove();
  }
  // Decrementa badge se estava unread
  const badge = document.getElementById('notifBadge');
  if (badge) {
    const n = Math.max(0, parseInt(badge.textContent, 10) - 1);
    if (n === 0) badge.remove();
    else badge.textContent = n;
  }
  fetch('/api/notifications/' + notifId + '/read', {method: 'POST'}).catch(function(){});
}

function markAllNotificationsRead() {
  document.querySelectorAll('.notif-item.is-unread').forEach(function(el){
    el.classList.remove('is-unread');
    const dot = el.querySelector('.notif-unread-dot');
    if (dot) dot.remove();
  });
  const badge = document.getElementById('notifBadge');
  if (badge) badge.remove();
  // remove o botão "Marcar todas como lidas"
  const markAllBtn = document.querySelector('.notif-mark-all');
  if (markAllBtn) markAllBtn.remove();
  fetch('/api/notifications/read-all', {method: 'POST'}).catch(function(){});
  showToast('✓ Todas marcadas como lidas');
}

// Fecha dropdown ao clicar fora
document.addEventListener('click', function(e){
  const dropdown = document.getElementById('notifDropdown');
  const btn = document.getElementById('notifBtn');
  if (!dropdown || !dropdown.classList.contains('open')) return;
  if (dropdown.contains(e.target)) return;
  if (btn && btn.contains(e.target)) return;
  dropdown.classList.remove('open');
  if (btn) btn.classList.remove('is-active');
});

// Esc fecha dropdown
document.addEventListener('keydown', function(e){
  if (e.key !== 'Escape') return;
  const dropdown = document.getElementById('notifDropdown');
  if (dropdown && dropdown.classList.contains('open')) {
    dropdown.classList.remove('open');
    const btn = document.getElementById('notifBtn');
    if (btn) btn.classList.remove('is-active');
  }
});

// ============ TOAST ============

let _toastTimer = null;

function showToast(message) {
  const toast = document.getElementById('munduToast');
  if (!toast) return;
  toast.textContent = message;
  toast.classList.add('show');
  if (_toastTimer) clearTimeout(_toastTimer);
  _toastTimer = setTimeout(function(){
    toast.classList.remove('show');
  }, 2800);
}

// ============ GAMIFICATION ============

const MunduGamification = (function(){
  const storageKey = 'mundu:last-level';
  const xpKey = 'mundu:last-xp';
  let initialized = false;

  function ensureModal() {
    let modal = document.getElementById('levelUpModal');
    if (modal) return modal;
    modal = document.createElement('div');
    modal.id = 'levelUpModal';
    modal.className = 'levelup-backdrop';
    modal.innerHTML = [
      '<div class="levelup-card" role="dialog" aria-modal="true" aria-label="Level up">',
      '<div class="levelup-burst" aria-hidden="true"></div>',
      '<button class="levelup-close" type="button" aria-label="Fechar">×</button>',
      '<span class="levelup-kicker">Level up</span>',
      '<h2 id="levelUpTitle">Nível alcançado!</h2>',
      '<p id="levelUpText">Sua evolução acabou de subir.</p>',
      '<div class="levelup-rewards">',
      '<span><strong id="levelUpXp">0</strong> XP atual</span>',
      '<span><strong id="levelUpCoins">0</strong> moedas</span>',
      '<span><strong id="levelUpTitleName">Novo</strong> título</span>',
      '</div>',
      '<button class="prof-btn primary" type="button" id="levelUpOk">Continuar</button>',
      '</div>'
    ].join('');
    document.body.appendChild(modal);
    modal.querySelector('.levelup-close').addEventListener('click', close);
    modal.querySelector('#levelUpOk').addEventListener('click', close);
    modal.addEventListener('click', function(event){
      if (event.target === modal) close();
    });
    return modal;
  }

  function close() {
    const modal = document.getElementById('levelUpModal');
    if (modal) modal.classList.remove('open');
  }

  function particleBurst(modal) {
    const burst = modal.querySelector('.levelup-burst');
    if (!burst) return;
    burst.innerHTML = '';
    for (let i = 0; i < 22; i += 1) {
      const particle = document.createElement('span');
      particle.style.setProperty('--angle', (i * 17) + 'deg');
      particle.style.setProperty('--distance', (70 + (i % 5) * 12) + 'px');
      particle.style.animationDelay = (i * 12) + 'ms';
      burst.appendChild(particle);
    }
  }

  function show(data) {
    const modal = ensureModal();
    const level = data.nivel || (data.last_event && data.last_event.nivel_atual) || 1;
    modal.querySelector('#levelUpTitle').textContent = 'Nível ' + level + ' alcançado!';
    modal.querySelector('#levelUpText').textContent = data.last_event && data.last_event.descricao
      ? data.last_event.descricao
      : 'Você desbloqueou uma nova etapa na Mundu.';
    modal.querySelector('#levelUpXp').textContent = data.xp_total || 0;
    modal.querySelector('#levelUpCoins').textContent = data.moedas || 0;
    modal.querySelector('#levelUpTitleName').textContent = data.titulo_ativo || data.nome_nivel || 'Novo';
    particleBurst(modal);
    modal.classList.add('open');
  }

  function refresh() {
    fetch('/api/xp', {headers: {'Accept': 'application/json'}})
      .then(function(response){
        if (!response.ok) throw new Error('xp unavailable');
        return response.json();
      })
      .then(function(data){
        const previousLevel = parseInt(localStorage.getItem(storageKey) || data.nivel, 10);
        const previousXp = parseInt(localStorage.getItem(xpKey) || data.xp_total, 10);
        localStorage.setItem(storageKey, data.nivel);
        localStorage.setItem(xpKey, data.xp_total);
        if (initialized && (data.nivel > previousLevel || (data.last_event && data.last_event.level_up))) {
          show(data);
        }
        if (initialized && data.xp_total > previousXp && window.showToast) {
          showToast('+' + (data.xp_total - previousXp) + ' XP');
        }
        initialized = true;
      })
      .catch(function(){
        initialized = true;
      });
  }

  document.addEventListener('DOMContentLoaded', function(){
    refresh();
    setTimeout(refresh, 1500);
  });

  return {refresh: refresh, show: show};
})();

window.MunduGamification = MunduGamification;
