/* Mundu Academy — shared product behavior, no framework and no mock content. */
(function () {
  'use strict';

  var lastFocusedElement = null;
  var toastTimer = null;
  var quicknoteSourceTitle = '';

  function clampPercentage(value) {
    var number = Number(value);
    if (!Number.isFinite(number)) return 0;
    return Math.min(100, Math.max(0, number));
  }

  function refreshIcons() {
    if (window.lucide && typeof window.lucide.createIcons === 'function') {
      window.lucide.createIcons();
    }
  }

  function applyProgressValues(root) {
    var scope = root || document;
    scope.querySelectorAll('[data-progress], [data-pct], [data-progress-ring]').forEach(function (element) {
      var raw = element.dataset.progress;
      if (raw === undefined) raw = element.dataset.pct;
      if (raw === undefined) raw = element.dataset.progressRing;
      var value = clampPercentage(raw);
      element.style.setProperty('--m-progress', value + '%');
      if (element.hasAttribute('role') && element.getAttribute('role') === 'progressbar') {
        element.setAttribute('aria-valuenow', String(Math.round(value)));
      }
    });
  }

  function setTheme(theme) {
    var nextTheme = theme === 'dark' ? 'dark' : 'light';
    document.documentElement.dataset.theme = nextTheme;
    localStorage.setItem('mundu:theme', nextTheme);
    document.querySelectorAll('[data-theme-label]').forEach(function (label) {
      label.textContent = nextTheme === 'dark' ? 'Tema claro' : 'Tema escuro';
    });
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.content = nextTheme === 'dark' ? '#111411' : '#F8F9F7';
    refreshIcons();
  }

  function toggleTheme() {
    setTheme(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark');
  }

  function initTheme() {
    setTheme(document.documentElement.dataset.theme || 'light');
    document.querySelectorAll('[data-theme-toggle]').forEach(function (button) {
      button.addEventListener('click', toggleTheme);
    });
  }

  function openMobileNav() {
    var nav = document.getElementById('mobileNav');
    var trigger = document.getElementById('mobileNavTrigger');
    if (!nav || !trigger) return;
    lastFocusedElement = document.activeElement;
    nav.hidden = false;
    document.body.classList.add('m-nav-open');
    trigger.setAttribute('aria-expanded', 'true');
    var firstControl = nav.querySelector('button, a');
    if (firstControl) firstControl.focus();
  }

  function closeMobileNav() {
    var nav = document.getElementById('mobileNav');
    var trigger = document.getElementById('mobileNavTrigger');
    if (!nav || nav.hidden) return;
    nav.hidden = true;
    document.body.classList.remove('m-nav-open');
    if (trigger) trigger.setAttribute('aria-expanded', 'false');
    if (lastFocusedElement && typeof lastFocusedElement.focus === 'function') {
      lastFocusedElement.focus();
    }
  }

  function initMobileNav() {
    var trigger = document.getElementById('mobileNavTrigger');
    if (trigger) trigger.addEventListener('click', openMobileNav);
    document.querySelectorAll('[data-close-mobile-nav]').forEach(function (button) {
      button.addEventListener('click', closeMobileNav);
    });
  }

  function closeOpenMenus(event) {
    document.querySelectorAll('details.m-menu[open]').forEach(function (menu) {
      if (!event || !menu.contains(event.target)) menu.removeAttribute('open');
    });
  }

  function showToast(message, tone) {
    var toast = document.getElementById('munduToast');
    if (!toast) return;
    toast.textContent = message;
    if (tone) toast.dataset.tone = tone;
    else toast.removeAttribute('data-tone');
    toast.classList.add('is-visible');
    if (toastTimer) window.clearTimeout(toastTimer);
    toastTimer = window.setTimeout(function () {
      toast.classList.remove('is-visible');
    }, 3200);
  }

  function openQuickNote(title, source) {
    var backdrop = document.getElementById('quicknoteBackdrop');
    if (!backdrop) {
      var next = encodeURIComponent(window.location.pathname + window.location.search);
      window.location.href = '/login?next=' + next;
      return;
    }

    lastFocusedElement = document.activeElement;
    quicknoteSourceTitle = title || '';
    var titleInput = document.getElementById('quicknoteTitle');
    var contentInput = document.getElementById('quicknoteContent');
    var sourceCopy = document.getElementById('quicknoteSource');
    var error = document.getElementById('quicknoteError');

    if (titleInput) titleInput.value = title ? 'Sobre: ' + title : '';
    if (contentInput) contentInput.value = '';
    if (sourceCopy) {
      sourceCopy.textContent = source
        ? 'Captura a partir de ' + source + '.'
        : 'Uma nota curta agora pode virar uma decisão melhor depois.';
    }
    if (error) error.textContent = '';

    backdrop.classList.add('is-open');
    backdrop.setAttribute('aria-hidden', 'false');
    document.body.classList.add('m-nav-open');
    window.setTimeout(function () {
      if (contentInput) contentInput.focus();
    }, 80);
  }

  function closeQuickNote() {
    var backdrop = document.getElementById('quicknoteBackdrop');
    if (!backdrop || !backdrop.classList.contains('is-open')) return;
    backdrop.classList.remove('is-open');
    backdrop.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('m-nav-open');
    if (lastFocusedElement && typeof lastFocusedElement.focus === 'function') {
      lastFocusedElement.focus();
    }
  }

  async function submitQuickNote(event) {
    event.preventDefault();
    var titleInput = document.getElementById('quicknoteTitle');
    var contentInput = document.getElementById('quicknoteContent');
    var submitButton = document.getElementById('quicknoteSubmit');
    var error = document.getElementById('quicknoteError');
    var title = titleInput ? titleInput.value.trim() : '';
    var content = contentInput ? contentInput.value.trim() : '';

    if (!content) {
      if (error) error.textContent = 'Escreva a ideia que deseja guardar.';
      if (contentInput) contentInput.focus();
      return;
    }

    if (error) error.textContent = '';
    if (submitButton) {
      submitButton.disabled = true;
      submitButton.setAttribute('aria-busy', 'true');
    }

    try {
      var response = await fetch('/api/quick-note', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          title: title || 'Nota rápida',
          content: content,
          source: quicknoteSourceTitle
        })
      });
      var payload = await response.json().catch(function () { return {}; });
      if (!response.ok || payload.ok === false) {
        throw new Error(payload.erro || payload.error || 'Não foi possível salvar a nota.');
      }
      closeQuickNote();
      showToast('Nota salva no My Brain · +10 XP');
      if (window.MunduGamification) window.MunduGamification.refresh();
    } catch (requestError) {
      if (error) error.textContent = requestError.message || 'Não foi possível salvar. Tente novamente.';
    } finally {
      if (submitButton) {
        submitButton.disabled = false;
        submitButton.removeAttribute('aria-busy');
      }
    }
  }

  function initQuickNote() {
    document.querySelectorAll('[data-open-quicknote]').forEach(function (button) {
      button.addEventListener('click', function () {
        openQuickNote(button.dataset.noteTitle || '', button.dataset.noteSource || '');
      });
    });
    document.querySelectorAll('[data-close-quicknote]').forEach(function (button) {
      button.addEventListener('click', closeQuickNote);
    });
    var form = document.getElementById('quicknoteForm');
    if (form) form.addEventListener('submit', submitQuickNote);
    var backdrop = document.getElementById('quicknoteBackdrop');
    if (backdrop) {
      backdrop.addEventListener('click', function (event) {
        if (event.target === backdrop) closeQuickNote();
      });
    }
  }

  function markNotificationRead(link, notificationId) {
    if (!link || !link.classList.contains('is-unread')) return;
    fetch('/api/notifications/' + notificationId + '/read', {
      method: 'POST',
      headers: {'Accept': 'application/json'},
      keepalive: true
    }).then(function (response) {
      if (!response.ok) return;
      link.classList.remove('is-unread');
      var badge = document.getElementById('notifBadge');
      if (!badge) return;
      var remaining = Math.max(0, Number.parseInt(badge.textContent, 10) - 1);
      if (remaining === 0) badge.remove();
      else badge.textContent = String(remaining);
    }).catch(function () {
      /* Navigation may cancel this background request; do not show false state. */
    });
  }

  async function markAllNotificationsRead() {
    var button = document.querySelector('[data-mark-all-notifications]');
    if (button) button.disabled = true;
    try {
      var response = await fetch('/api/notifications/read-all', {
        method: 'POST',
        headers: {'Accept': 'application/json'}
      });
      if (!response.ok) throw new Error();
      document.querySelectorAll('.m-notification.is-unread').forEach(function (item) {
        item.classList.remove('is-unread');
      });
      var badge = document.getElementById('notifBadge');
      if (badge) badge.remove();
      if (button) button.remove();
      showToast('Notificações marcadas como lidas');
    } catch (error) {
      showToast('Não foi possível atualizar as notificações', 'danger');
      if (button) button.disabled = false;
    }
  }

  function initNotifications() {
    document.querySelectorAll('[data-notification-id]').forEach(function (link) {
      link.addEventListener('click', function () {
        markNotificationRead(link, link.dataset.notificationId);
      });
    });
    var markAllButton = document.querySelector('[data-mark-all-notifications]');
    if (markAllButton) markAllButton.addEventListener('click', markAllNotificationsRead);
  }

  function scrollRail(trackId, direction) {
    var track = document.getElementById(trackId);
    if (!track) return;
    var amount = Math.max(280, track.clientWidth * 0.82);
    track.scrollBy({left: amount * direction, behavior: 'smooth'});
  }

  function initTabs(root) {
    var scope = root || document;
    scope.querySelectorAll('[data-tabs]').forEach(function (tabs) {
      var buttons = Array.from(tabs.querySelectorAll('[role="tab"][data-tab]'));
      var containerId = tabs.dataset.tabs;
      var panelScope = containerId ? document.getElementById(containerId) : tabs.parentElement;
      if (!panelScope || !buttons.length) return;
      var panels = Array.from(panelScope.querySelectorAll('[role="tabpanel"][data-tab-panel]'));

      function activate(button, moveFocus) {
        var key = button.dataset.tab;
        buttons.forEach(function (item) {
          var selected = item === button;
          item.setAttribute('aria-selected', selected ? 'true' : 'false');
          item.tabIndex = selected ? 0 : -1;
        });
        panels.forEach(function (panel) {
          panel.hidden = panel.dataset.tabPanel !== key;
        });
        if (moveFocus) button.focus();
      }

      buttons.forEach(function (button, index) {
        button.addEventListener('click', function () { activate(button, false); });
        button.addEventListener('keydown', function (event) {
          if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
          event.preventDefault();
          var offset = event.key === 'ArrowRight' ? 1 : -1;
          var next = buttons[(index + offset + buttons.length) % buttons.length];
          activate(next, true);
        });
      });
    });
  }

  function initDisclosures(root) {
    var scope = root || document;
    scope.querySelectorAll('[data-disclosure]').forEach(function (button) {
      var panel = document.getElementById(button.dataset.disclosure);
      if (!panel) return;
      button.addEventListener('click', function () {
        var expanded = button.getAttribute('aria-expanded') === 'true';
        button.setAttribute('aria-expanded', expanded ? 'false' : 'true');
        panel.hidden = expanded;
      });
    });
  }

  function initConfirmations() {
    document.querySelectorAll('form[data-confirm]').forEach(function (form) {
      form.addEventListener('submit', function (event) {
        var message = form.dataset.confirm || 'Confirmar esta a\u00e7\u00e3o?';
        if (!window.confirm(message)) event.preventDefault();
      });
    });
  }

  function initReveal() {
    var elements = document.querySelectorAll('.m-reveal');
    if (!elements.length) return;
    if (!('IntersectionObserver' in window) || window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      elements.forEach(function (element) { element.classList.add('is-visible'); });
      return;
    }
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      });
    }, {threshold: 0.08, rootMargin: '0px 0px -30px'});
    elements.forEach(function (element) { observer.observe(element); });
  }

  function createLevelDialog() {
    var backdrop = document.createElement('div');
    backdrop.id = 'levelUpModal';
    backdrop.className = 'm-dialog-backdrop';
    backdrop.setAttribute('aria-hidden', 'true');
    backdrop.innerHTML = [
      '<section class="m-dialog" role="dialog" aria-modal="true" aria-labelledby="levelUpTitle">',
      '  <div class="m-dialog__body m-level-dialog__body">',
      '    <div class="m-level-dialog__visual" id="levelUpNumber">2</div>',
      '    <span class="m-eyebrow">Novo marco</span>',
      '    <h2 id="levelUpTitle" class="m-section-title">Você avançou de nível</h2>',
      '    <p id="levelUpText" class="m-section-description">Sua constância abriu uma nova etapa.</p>',
      '    <button class="m-button m-button--primary m-level-dialog__action" id="levelUpClose" type="button">Continuar aprendendo</button>',
      '  </div>',
      '</section>'
    ].join('');
    document.body.appendChild(backdrop);
    backdrop.querySelector('#levelUpClose').addEventListener('click', function () {
      backdrop.classList.remove('is-open');
      backdrop.setAttribute('aria-hidden', 'true');
    });
    return backdrop;
  }

  var MunduGamification = (function () {
    var initialized = false;
    var levelKey = 'mundu:last-level';
    var xpKey = 'mundu:last-xp';

    function show(data) {
      var modal = document.getElementById('levelUpModal') || createLevelDialog();
      var level = data.nivel || 1;
      modal.querySelector('#levelUpNumber').textContent = String(level);
      modal.querySelector('#levelUpTitle').textContent = 'Nível ' + level + ' alcançado';
      modal.querySelector('#levelUpText').textContent = data.last_event && data.last_event.descricao
        ? data.last_event.descricao
        : 'Sua constância abriu uma nova etapa na Mundu.';
      modal.classList.add('is-open');
      modal.setAttribute('aria-hidden', 'false');
      modal.querySelector('#levelUpClose').focus();
    }

    async function refresh() {
      if (!document.querySelector('.m-xp-orbit')) return;
      try {
        var response = await fetch('/api/xp', {headers: {'Accept': 'application/json'}});
        if (!response.ok) throw new Error();
        var data = await response.json();
        var previousLevel = Number.parseInt(localStorage.getItem(levelKey) || String(data.nivel), 10);
        var previousXp = Number.parseInt(localStorage.getItem(xpKey) || String(data.xp_total), 10);
        localStorage.setItem(levelKey, String(data.nivel));
        localStorage.setItem(xpKey, String(data.xp_total));
        if (initialized && (data.nivel > previousLevel || (data.last_event && data.last_event.level_up))) {
          show(data);
        } else if (initialized && data.xp_total > previousXp) {
          showToast('+' + (data.xp_total - previousXp) + ' XP');
        }
      } catch (error) {
        /* XP is supplemental UI; the page remains usable if unavailable. */
      } finally {
        initialized = true;
      }
    }

    return {refresh: refresh, show: show};
  }());

  function handleEscape(event) {
    if (event.key !== 'Escape') return;
    closeMobileNav();
    closeQuickNote();
    closeOpenMenus();
  }

  function initialize() {
    initTheme();
    initMobileNav();
    initQuickNote();
    initNotifications();
    initTabs();
    initDisclosures();
    initConfirmations();
    initReveal();
    applyProgressValues();
    refreshIcons();

    document.addEventListener('click', closeOpenMenus);
    document.addEventListener('keydown', handleEscape);
    document.addEventListener('keydown', function (event) {
      var backdrop = document.getElementById('quicknoteBackdrop');
      if (!backdrop || !backdrop.classList.contains('is-open')) return;
      if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
        event.preventDefault();
        var form = document.getElementById('quicknoteForm');
        if (form) form.requestSubmit();
      }
    });

    MunduGamification.refresh();
  }

  window.Mundu = {
    applyProgressValues: applyProgressValues,
    refreshIcons: refreshIcons,
    initTabs: initTabs,
    initDisclosures: initDisclosures,
    scrollRail: scrollRail
  };
  window.MunduGamification = MunduGamification;
  window.openQuickNote = openQuickNote;
  window.closeQuickNote = closeQuickNote;
  window.showToast = showToast;
  window.markNotificationRead = markNotificationRead;
  window.markAllNotificationsRead = markAllNotificationsRead;
  window.scrollRail = scrollRail;
  window.scrollCarousel = function (trackId, amount) {
    scrollRail(trackId, amount < 0 ? -1 : 1);
  };
  window.toggleTheme = toggleTheme;

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialize);
  } else {
    initialize();
  }
}());
