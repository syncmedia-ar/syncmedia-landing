/* =========================================================
   SYNC MEDIA — Funciones de toda la web
   El WhatsApp y la frase de la pestaña se cambian en contenido.json
   (o desde el panel). Acá solo quedan las conexiones técnicas.
   ========================================================= */

const CONFIG = {
  // Número de WhatsApp: se toma de contenido.json
  WHATSAPP: document.body.dataset.wa || '5491162338685',

  // Dirección del script de Google que guarda los leads en el Sheet
  SHEET_URL: 'https://script.google.com/macros/s/AKfycbxj69VHBsMNXggxE5LIwtAAAxvOSHmw11eE6x6OfSGcxcaiXtqpXc4oGq6FkQG1pH08/exec',

  // Make (avisos automáticos). Vacío = apagado.
  // Para activarlo, pegá entre las comillas la URL del webhook de Make.
  // La que usabas antes era: https://hook.us2.make.com/fqmowoflnlqk6kx54ez3jjov5q6xk46g
  MAKE_WEBHOOK_URL: '',
};

// Nombres "lindos" de cada servicio (se guardan así en el Sheet)
const SERVICIOS = {
  'auditoria': 'Auditoría gratis de Meta Ads',
  'meta-ads': 'Gestión de Meta Ads',
  'marca-lista': 'Marca Lista',
  'tienda-lista': 'Tienda Lista',
  'no-se': 'No sé, quiero que me asesoren',
};

window.dataLayer = window.dataLayer || [];

/* ── Links de WhatsApp ──
   Cualquier link con data-wa="mensaje" se convierte en un link a WhatsApp
   con ese mensaje ya escrito. */
function waLink(msg) {
  // WhatsApp muestra un rombo con signo de pregunta con algunos emojis que llegan por link
  // desde la compu, así que se quitan antes de armar el mensaje.
  const limpio = String(msg)
    .replace(/[\u{1F000}-\u{1FAFF}\u{2600}-\u{27BF}\u{2B00}-\u{2BFF}\u{FE0F}\u{200D}]/gu, '')
    .replace(/\s+/g, ' ')
    .trim();
  return 'https://wa.me/' + CONFIG.WHATSAPP + '?text=' + encodeURIComponent(limpio);
}
document.querySelectorAll('[data-wa]').forEach(function (a) {
  a.href = waLink(a.dataset.wa);
  a.target = '_blank';
  a.rel = 'noopener';
  a.addEventListener('click', function () {
    window.dataLayer.push({ event: 'whatsapp_click', wa_mensaje: a.dataset.wa, pagina: location.pathname });
  });
});

/* ── Botones de pago: aviso para el Píxel (inicio de compra) ── */
document.querySelectorAll('[data-pago]').forEach(function (a) {
  a.addEventListener('click', function () {
    window.dataLayer.push({ event: 'begin_checkout', servicio: a.dataset.pago });
  });
});

/* ── Selector de forma de pago ── */
document.querySelectorAll('[data-pay]').forEach(function (box) {
  const panels = box.querySelectorAll('[data-panel]');
  box.querySelectorAll('input[type="radio"]').forEach(function (r) {
    r.addEventListener('change', function () {
      panels.forEach(function (p) { p.hidden = p.dataset.panel !== r.value; });
    });
  });
});

/* ── Botón Copiar del alias ── */
document.querySelectorAll('[data-copy]').forEach(function (btn) {
  btn.addEventListener('click', function () {
    const texto = btn.dataset.copy;
    function listo() {
      btn.textContent = '¡Copiado!';
      btn.classList.add('copied');
      setTimeout(function () { btn.textContent = 'Copiar'; btn.classList.remove('copied'); }, 2000);
    }
    function respaldo() {
      // Si el navegador no deja copiar, se selecciona el alias para copiarlo a mano
      const code = btn.parentElement.querySelector('.alias-value');
      const sel = window.getSelection();
      const range = document.createRange();
      range.selectNodeContents(code);
      sel.removeAllRanges();
      sel.addRange(range);
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(texto).then(listo, respaldo);
    } else {
      respaldo();
    }
    window.dataLayer.push({ event: 'alias_copiado', pagina: location.pathname });
  });
});

/* ── Checklist "Para empezar necesitamos" ── */
document.querySelectorAll('[data-checklist]').forEach(function (box) {
  const clave = 'sync_ck_' + box.dataset.checklist;
  const checks = box.querySelectorAll('input[data-ck]');
  const total = checks.length;
  const contador = box.querySelector('[data-ck-done]');
  const barra = box.querySelector('.ck-bar');
  const listo = box.querySelector('.ck-done');
  let guardado = [];
  try { guardado = JSON.parse(localStorage.getItem(clave) || '[]'); } catch (e) {}
  checks.forEach(function (c) { c.checked = guardado.indexOf(c.dataset.ck) !== -1; });

  function actualizar(guardar) {
    const marcados = Array.prototype.filter.call(checks, function (c) { return c.checked; });
    contador.textContent = marcados.length;
    barra.style.width = (marcados.length / total * 100) + '%';
    listo.hidden = marcados.length !== total;
    if (guardar) {
      try { localStorage.setItem(clave, JSON.stringify(marcados.map(function (c) { return c.dataset.ck; }))); } catch (e) {}
    }
  }
  checks.forEach(function (c) {
    c.addEventListener('change', function () {
      actualizar(true);
      if (!listo.hidden) window.dataLayer.push({ event: 'checklist_completa', pagina: location.pathname });
    });
  });
  actualizar(false);
});

/* ── Menú ── */
const nav = document.querySelector('.nav');
const burger = document.getElementById('nav-hamburger');
const mobileMenu = document.getElementById('nav-mobile-menu');

function setMenu(open) {
  mobileMenu.classList.toggle('open', open);
  burger.classList.toggle('open', open);
  burger.setAttribute('aria-expanded', open ? 'true' : 'false');
  document.body.style.overflow = open ? 'hidden' : '';
  document.body.classList.toggle('menu-open', open);
}
if (burger && mobileMenu) {
  burger.addEventListener('click', function () { setMenu(!mobileMenu.classList.contains('open')); });
  mobileMenu.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });
}
if (nav) {
  const onScroll = function () { nav.classList.toggle('scrolled', window.scrollY > 30); };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
}

/* ── Barra fija de celular ──
   Aparece cuando el usuario empieza a bajar y se oculta cuando el formulario está a la vista. */
const sticky = document.getElementById('sticky-cta');
if (sticky) {
  const contacto = document.getElementById('contacto');
  let formVisible = false;
  function refrescarBarra() {
    const mostrar = window.scrollY > window.innerHeight * 0.6 && !formVisible;
    sticky.classList.toggle('show', mostrar);
    document.body.classList.toggle('sticky-on', mostrar);
  }
  if (contacto && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      formVisible = entries[0].isIntersecting;
      refrescarBarra();
    }, { threshold: 0.15 }).observe(contacto);
  }
  window.addEventListener('scroll', refrescarBarra, { passive: true });
  refrescarBarra();
}

/* ── Mensaje en la pestaña cuando el usuario se va ── */
(function () {
  const MENSAJE_PESTANA = document.body.dataset.tab || 'Volvé, tu marca te espera 💜';
  const original = document.title;
  document.addEventListener('visibilitychange', function () {
    document.title = document.hidden ? MENSAJE_PESTANA : original;
  });
})();

/* ── Aparición suave al hacer scroll ── */
(function () {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce || !('IntersectionObserver' in window)) return;

  const selector = [
    '.section-head', '.services-grid > *', '.path-block', '.proceso-step', '.why-item',
    '.value-circles > li', '.faq', '.include-card', '.plan', '.step', '.fact', '.cta-band',
    '.two-col > div', '.contact-left', '.form-card', '.price-box'
  ].join(',');
  const items = Array.prototype.slice.call(document.querySelectorAll(selector));
  const alto = window.innerHeight;

  items.forEach(function (el) {
    // Los elementos que ya se ven al abrir la página no se animan
    if (el.getBoundingClientRect().top < alto * 0.95) return;
    // Pequeño escalonado entre tarjetas hermanas
    const hermanos = Array.prototype.filter.call(el.parentElement.children, function (c) { return c.matches(selector); });
    el.style.setProperty('--i', Math.min(hermanos.indexOf(el), 4));
    el.classList.add('reveal');
  });
  document.documentElement.classList.add('reveal-on');

  const obs = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      const el = entry.target;
      el.classList.add('is-visible');
      obs.unobserve(el);
      // Al terminar, se limpia para no interferir con los efectos del mouse
      setTimeout(function () {
        el.classList.remove('reveal', 'is-visible');
        el.style.removeProperty('--i');
      }, 1200);
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

  document.querySelectorAll('.reveal').forEach(function (el) { obs.observe(el); });
})();

/* ── Luz que sigue al cursor (cabecera y tarjetas, solo en compu) ── */
(function () {
  const conMouse = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!conMouse || reduce) return;

  const zona = document.querySelector('.hero-zone');
  let ultimo = null;
  let esperando = false;

  document.addEventListener('pointermove', function (e) {
    ultimo = e;
    if (esperando) return; // como máximo una actualización por cuadro
    esperando = true;
    requestAnimationFrame(function () {
      esperando = false;
      const ev = ultimo;
      // Cabecera
      if (zona) {
        const r = zona.getBoundingClientRect();
        const dentro = ev.clientY >= r.top && ev.clientY <= r.bottom;
        zona.classList.toggle('lit', dentro);
        if (dentro) {
          zona.style.setProperty('--mx', (ev.clientX - r.left) + 'px');
          zona.style.setProperty('--my', (ev.clientY - r.top) + 'px');
        }
      }
      // Tarjetas
      const card = ev.target.closest && ev.target.closest('.glow-card');
      if (card) {
        const c = card.getBoundingClientRect();
        card.style.setProperty('--gx', (ev.clientX - c.left) + 'px');
        card.style.setProperty('--gy', (ev.clientY - c.top) + 'px');
      }
    });
  }, { passive: true });
})();

/* ── Círculos de valores: pulso al tocar ── */
document.querySelectorAll('.vcircle').forEach(function (c) {
  c.addEventListener('click', function () {
    // En celular, el toque deja el círculo iluminado
    document.querySelectorAll('.vcircle').forEach(function (o) { if (o !== c) o.classList.remove('is-on'); });
    c.classList.toggle('is-on');
    c.classList.remove('pulse');
    void c.offsetWidth; // reinicia la animación
    c.classList.add('pulse');
  });
  c.addEventListener('animationend', function () { c.classList.remove('pulse'); });
});

/* ── Año del footer ── */
document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

/* ── Aviso de cookies ── */
(function () {
  const banner = document.getElementById('cookie-banner');
  if (!banner) return;
  let ok = false;
  try { ok = localStorage.getItem('sync_cookies_ok') === '1'; } catch (e) {}
  if (ok) return;
  banner.hidden = false;
  banner.querySelector('button').addEventListener('click', function () {
    try { localStorage.setItem('sync_cookies_ok', '1'); } catch (e) {}
    banner.hidden = true;
  });
})();

/* ── Formulario de contacto ── */
(function () {
  const form = document.getElementById('lead-form');
  if (!form) return;

  const servicio = form.querySelector('#f-servicio');
  const budgetGroup = form.querySelector('#g-budget');
  const btn = form.querySelector('#btn-submit');
  const status = form.querySelector('#form-status');
  const btnText = btn.innerHTML;

  // Si alguien llega con ?servicio=tienda-lista, se elige solo
  const desde = new URLSearchParams(location.search).get('servicio');
  if (desde && SERVICIOS[desde]) servicio.value = desde;

  // La pregunta de presupuesto en ads solo aparece si le interesa Meta Ads
  function toggleBudget() {
    const v = servicio.value;
    budgetGroup.hidden = !(v === 'auditoria' || v === 'meta-ads' || v === 'no-se');
  }
  servicio.addEventListener('change', toggleBudget);
  toggleBudget();

  function setError(id, msg) {
    const group = form.querySelector('#g-' + id);
    group.classList.toggle('has-error', !!msg);
    group.querySelector('.field-error').textContent = msg || '';
  }

  form.addEventListener('submit', async function (e) {
    e.preventDefault();
    status.textContent = '';

    const data = {
      nombre: form.querySelector('#f-nombre').value.trim(),
      whatsapp: form.querySelector('#f-wp').value.trim(),
      web: form.querySelector('#f-web').value.trim(),
      servicio: SERVICIOS[servicio.value] || '',
      rubro: form.querySelector('#f-rubro').value,
      presupuesto: budgetGroup.hidden ? '' : form.querySelector('#f-budget').value,
      origen: location.pathname,
    };

    // Validaciones
    let ok = true;
    setError('nombre', data.nombre ? '' : 'Contanos tu nombre.');
    if (!data.nombre) ok = false;

    const soloNumeros = data.whatsapp.replace(/[\s\-\(\)]/g, '');
    const wpOk = /^\+?[0-9]{8,15}$/.test(soloNumeros);
    setError('wp', wpOk ? '' : 'Revisá el número. Ejemplo: +54 9 11 1234-5678');
    if (!wpOk) ok = false;

    setError('servicio', data.servicio ? '' : 'Elegí una opción.');
    if (!data.servicio) ok = false;

    if (!ok) {
      const firstError = form.querySelector('.has-error input, .has-error select');
      if (firstError) firstError.focus();
      return;
    }

    btn.innerHTML = '<span class="btn-spinner" aria-hidden="true"></span> Enviando...';
    btn.disabled = true;

    const payload = JSON.stringify(data);
    let guardado = false;

    // 1) Google Sheet
    try {
      await fetch(CONFIG.SHEET_URL, {
        method: 'POST',
        mode: 'no-cors',
        headers: { 'Content-Type': 'text/plain;charset=utf-8' },
        body: payload,
      });
      guardado = true;
    } catch (err) {
      console.warn('Error al guardar en Sheets:', err);
    }

    // 2) Make (solo si está configurado)
    if (CONFIG.MAKE_WEBHOOK_URL) {
      try {
        await fetch(CONFIG.MAKE_WEBHOOK_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: payload,
        });
        guardado = true;
      } catch (err) {
        console.warn('Error al enviar a Make:', err);
      }
    }

    if (!guardado) {
      btn.innerHTML = btnText;
      btn.disabled = false;
      status.innerHTML = 'No pudimos enviar el formulario. Probá de nuevo o <a href="' + waLink('Hola, quiero consultar por ' + data.servicio) + '" target="_blank" rel="noopener">escribinos por WhatsApp</a>.';
      return;
    }

    // Evento para Google Tag Manager (Píxel de Meta / Analytics)
    window.dataLayer.push({ event: 'generate_lead', servicio: data.servicio, rubro: data.rubro });

    location.href = 'gracias.html?servicio=' + encodeURIComponent(servicio.value);
  });
})();

/* ── Página de gracias: adapta el texto al servicio elegido ── */
(function () {
  const el = document.getElementById('ty-servicio');
  if (!el) return;
  const key = new URLSearchParams(location.search).get('servicio');
  const nombre = SERVICIOS[key];
  if (nombre) el.textContent = nombre;
  const wa = document.getElementById('ty-wa');
  if (wa && nombre) wa.href = waLink('Hola, acabo de completar el formulario por ' + nombre + ' 🚀');
})();
