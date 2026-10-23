"""
Genera las páginas de syncmedia.ar a partir de contenido.json.

NO edites los .html de la raíz a mano: se vuelven a generar solos.
- Precios, links de pago, banner, etc. → contenido.json (o el panel Pages CMS)
- Textos fijos y estructura de las páginas → este archivo
Para regenerar en tu compu:  python scripts/build.py
"""
import html, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT
C = json.loads((ROOT / "contenido.json").read_text(encoding="utf-8"))
G, I, M, T = C["general"], C["inicio"], C["marca_lista"], C["tienda_lista"]
E = lambda s: html.escape(str(s or "").strip())
SITE = "https://syncmedia.ar"
GTM = "GTM-WQXNB7L3"

LOGO_BARS = """<svg viewBox="0 0 32 32" fill="none" aria-hidden="true">
      <rect x="2" y="18" width="7" height="14" rx="3.5" fill="url(#{p}1)"/>
      <rect x="12" y="10" width="7" height="22" rx="3.5" fill="url(#{p}2)"/>
      <rect x="22" y="4" width="7" height="28" rx="3.5" fill="url(#{p}3)"/>
      <defs>
        <linearGradient id="{p}1" x1="5.5" y1="18" x2="5.5" y2="32" gradientUnits="userSpaceOnUse"><stop stop-color="#a855f7"/><stop offset="1" stop-color="#7c3aed"/></linearGradient>
        <linearGradient id="{p}2" x1="15.5" y1="10" x2="15.5" y2="32" gradientUnits="userSpaceOnUse"><stop stop-color="#c084fc"/><stop offset="1" stop-color="#a855f7"/></linearGradient>
        <linearGradient id="{p}3" x1="25.5" y1="4" x2="25.5" y2="32" gradientUnits="userSpaceOnUse"><stop stop-color="#e9d5ff"/><stop offset="1" stop-color="#c084fc"/></linearGradient>
      </defs>
    </svg>"""

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="7" y1="17" x2="17" y2="7"/><polyline points="7 7 17 7 17 17"/></svg>'
CHECK = '<span class="check-icon"><svg viewBox="0 0 24 24" aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg></span>'

CUR = ' aria-current="page"'
NAV_ITEMS = [
    ("index.html", "Inicio"),
    ("marca-lista.html", "Marca Lista"),
    ("tienda-lista.html", "Tienda Lista"),
    ("meta-ads.html", "Meta Ads"),
    ("index.html#contacto", "Contacto"),
]


def head(title, desc, path, noindex=False):
    url = SITE + "/" + ("" if path == "index.html" else path)
    robots = '\n  <meta name="robots" content="noindex">' if noindex else ""
    return f"""<!DOCTYPE html>
<html lang="es-AR">
<head>
  <!-- Google Tag Manager -->
  <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
  new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  }})(window,document,'script','dataLayer','{GTM}');</script>
  <!-- End Google Tag Manager -->
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>{title}</title>
  <meta name="description" content="{desc}">{robots}
  <link rel="canonical" href="{url}">
  <meta name="theme-color" content="#120820">
  <link rel="icon" href="favicon.svg" type="image/svg+xml">

  <!-- Cómo se ve el link al compartirlo en WhatsApp / redes -->
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/assets/img/og-image.png">
  <meta property="og:locale" content="es_AR">
  <meta name="twitter:card" content="summary_large_image">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@800;900&family=Figtree:wght@400;500;600;700;800&family=Alice&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/css/styles.css">
</head>
<body data-wa="{E(G['whatsapp'])}" data-tab="{E(G['mensaje_pestana'])}">
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM}" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
"""


def nav(active):
    links = "\n".join(
        f'        <li><a href="{h}"{CUR if h == active else ""}>{t}</a></li>'
        for h, t in NAV_ITEMS
    )
    mobile = "\n".join(f'  <a href="{h}">{t}</a>' for h, t in NAV_ITEMS)
    return f"""
<header class="nav">
  <div class="wrap nav-inner">
    <a href="index.html" class="logo" aria-label="Sync, ir al inicio">
    {LOGO_BARS.format(p='lg')}
      sync
    </a>
    <nav aria-label="Principal">
      <ul class="nav-links">
{links}
      </ul>
    </nav>
    <a href="index.html#contacto" class="btn btn-primary btn-desktop">Auditoría gratis →</a>
    <button class="nav-hamburger" id="nav-hamburger" aria-label="Abrir menú" aria-expanded="false" aria-controls="nav-mobile-menu">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>

<div class="nav-mobile-menu" id="nav-mobile-menu">
{mobile}
  <a href="index.html#contacto" class="btn btn-primary">Quiero mi auditoría gratis →</a>
  <p class="nav-mobile-badge">Sin costo · Sin contrato · Sin compromiso</p>
</div>
"""


def footer(sticky_text, sticky_href, sticky_wa=None):
    sticky_attr = f'data-wa="{sticky_wa}" href="#"' if sticky_wa else f'href="{sticky_href}"'
    return f"""
<footer class="footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a href="index.html" class="logo" aria-label="Sync, ir al inicio">
        {LOGO_BARS.format(p='lf')}
          sync
        </a>
        <p class="footer-claim">Estrategia y creatividad en perfecta sincronía.</p>
      </div>
      <div>
        <h2>Servicios</h2>
        <ul>
          <li><a href="marca-lista.html">Marca Lista</a></li>
          <li><a href="tienda-lista.html">Tienda Lista</a></li>
          <li><a href="meta-ads.html">Meta Ads</a></li>
        </ul>
      </div>
      <div>
        <h2>Contacto</h2>
        <ul>
          <li><a href="#" data-wa="Hola, quiero saber más sobre sus servicios 🚀">WhatsApp: {E(G['whatsapp_visible'])}</a></li>
          <li><a href="index.html#contacto">Pedir auditoría gratis</a></li>
        </ul>
      </div>
      <div>
        <h2>Legales</h2>
        <ul>
          <li><a href="privacidad.html">Política de privacidad</a></li>
          <li><a href="terminos.html">Términos y condiciones</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span data-year>2026</span> Sync Media · Buenos Aires, Argentina</span>
      <span>Precios en pesos argentinos (ARS).</span>
    </div>
  </div>
</footer>

<div class="sticky-cta-bar" id="sticky-cta">
  <a {sticky_attr} class="btn btn-primary">{sticky_text}</a>
</div>

<a href="#" data-wa="Hola, quiero saber más sobre sus servicios 🚀" class="whatsapp-fab" aria-label="Escribinos por WhatsApp">
  <svg viewBox="0 0 60 60" aria-hidden="true">
    <circle cx="30" cy="30" r="30" fill="#25D366"/>
    <path d="M30 14C21.163 14 14 21.163 14 30c0 2.84.752 5.504 2.063 7.808L14 46l8.428-2.035A15.93 15.93 0 0030 46c8.837 0 16-7.163 16-16S38.837 14 30 14zm8.295 21.728c-.352.988-2.06 1.892-2.836 2.012-.726.112-1.64.16-2.647-.167-.609-.197-1.392-.46-2.39-.902-4.208-1.816-6.957-6.072-7.168-6.353-.21-.28-1.72-2.287-1.72-4.363s1.088-3.093 1.475-3.515c.387-.422.845-.527 1.127-.527.282 0 .563.003.81.014.26.012.608-.098.952.727.352.843 1.196 2.918 1.302 3.129.105.211.176.456.035.737-.14.28-.21.457-.42.703-.21.246-.44.55-.633.739-.21.21-.43.436-.185.854.246.42 1.093 1.8 2.347 2.918 1.612 1.437 2.97 1.883 3.39 2.094.42.21.667.176.912-.106.246-.28 1.053-1.23 1.335-1.65.28-.422.56-.352.946-.211.386.14 2.45 1.156 2.87 1.365.422.21.703.316.808.493.104.175.104 1.01-.248 1.998z" fill="#fff"/>
  </svg>
</a>

<div class="cookie-banner" id="cookie-banner" role="region" aria-label="Aviso de cookies" hidden>
  <p>Usamos cookies para medir las visitas y mejorar nuestros anuncios. Más info en la <a href="privacidad.html">política de privacidad</a>.</p>
  <button type="button" class="btn btn-primary">Entendido</button>
</div>

<script src="assets/js/main.js" defer></script>
</body>
</html>
"""


def page(path, title, desc, body, sticky=("Quiero mi auditoría gratis →", "index.html#contacto", None), active=None, noindex=False):
    html = head(title, desc, path, noindex) + nav(active or path) + "\n<main>\n" + body + "\n</main>\n" + footer(*sticky)
    (OUT / path).write_text(html, encoding="utf-8")


def cta_band(title, text, wa_msg, form_service, wa_label="Escribinos por WhatsApp"):
    return f"""
  <section class="section">
    <div class="wrap">
      <div class="cta-band">
        <div>
          <h2>{title}</h2>
          <p>{text}</p>
        </div>
        <div class="btn-row">
          <a href="#" data-wa="{wa_msg}" class="btn btn-primary">{wa_label}</a>
          <a href="index.html?servicio={form_service}#contacto" class="btn btn-ghost">Completar formulario</a>
        </div>
      </div>
    </div>
  </section>"""


# ───────────────────────── INICIO ─────────────────────────
TAG_COLORS = ["t-white", "t-lime", "t-lilac", "t-dark"]
TAGS = "\n".join(
    f'      <span class="htag {TAG_COLORS[i % 4]}">{E(t)}</span>'
    for i, t in enumerate([t for t in I.get("cartelitos", []) if str(t).strip()][:7])
)


def money(v):
    """Convierte '61.200' en 61200."""
    digits = "".join(ch for ch in str(v) if ch.isdigit())
    return int(digits) if digits else 0


def fmt(n):
    """Convierte 183600 en '183.600'."""
    return f"{n:,}".replace(",", ".")


def pay_block(d, servicio, nombre):
    """Selector de forma de pago: transferencia o 3 cuotas."""
    precio = E(d["precio"])
    cuota = E(d["cuota"])
    total = fmt(money(d["cuota"]) * 3)
    alias = E(G.get("alias_transferencia"))
    link_cuotas = str(d.get("link_pago_cuotas") or "").strip()
    link_form = str(d.get("link_formulario") or "").strip()
    medio = E(G["medio_de_pago"])
    grupo = f"pago-{servicio}"

    if alias:
        transferencia = f"""
            <div class="alias">
              <span class="alias-label">Alias</span>
              <code class="alias-value">{alias}</code>
              <button type="button" class="alias-copy" data-copy="{alias}">Copiar</button>
            </div>
            <a href="#" data-wa="Hola, te envío el comprobante de transferencia por {nombre} (${precio})" class="btn btn-primary">Enviar comprobante por WhatsApp</a>"""
    else:
        transferencia = f"""
            <a href="#" data-wa="Hola, quiero pagar {nombre} por transferencia" class="btn btn-primary">Pedir datos para transferir</a>"""

    cuotas_opt = cuotas_panel = ""
    if link_cuotas.startswith("http"):
        cuotas_opt = f"""
          <label class="pay-opt">
            <input type="radio" name="{grupo}" value="cuotas">
            <span class="pay-opt-body">
              <span class="pay-opt-name">3 cuotas sin interés</span>
              <span class="pay-opt-price">3 x ${cuota}</span>
              <small>Total ${total} con {medio}</small>
            </span>
          </label>"""
        cuotas_panel = f"""
          <div class="pay-panel" data-panel="cuotas" hidden>
            <a href="{E(link_cuotas)}" target="_blank" rel="noopener" class="btn btn-primary" data-pago="{servicio}">Pagar 3 x ${cuota}</a>
          </div>"""

    despues = ""
    if link_form.startswith("http"):
        despues = f"""
          <p class="pay-after">Después de pagar, <a href="{E(link_form)}" target="_blank" rel="noopener">completá el formulario de inicio →</a></p>"""

    return f"""
        <div class="pay" data-pay>
          <p class="pay-title">¿Cómo querés pagar?</p>
          <div class="pay-options" role="radiogroup" aria-label="Forma de pago">
          <label class="pay-opt">
            <input type="radio" name="{grupo}" value="transferencia" checked>
            <span class="pay-opt-body">
              <span class="pay-opt-name">Transferencia</span>
              <span class="pay-opt-price">${precio}</span>
              <small>Precio por pago al contado</small>
            </span>
          </label>{cuotas_opt}
          </div>
          <div class="pay-panel" data-panel="transferencia">{transferencia}
          </div>{cuotas_panel}{despues}
        </div>"""


def form_link(d):
    """Botón al formulario de inicio (solo si hay link cargado)."""
    link = str(d.get("link_formulario") or "").strip()
    if not link.startswith("http"):
        return ""
    return f' <a href="{E(link)}" target="_blank" rel="noopener" class="step-link">Completar formulario de inicio →</a>'

FORM = f"""
  <section class="section alt" id="contacto">
    <div class="wrap contact">
      <div class="contact-left violet">
        <div class="section-label">Empezá hoy</div>
        <h2>Llevamos tu negocio al <span class="lime">siguiente nivel</span></h2>
        <p>Contanos qué necesitás y te escribimos por WhatsApp en menos de 24 h. Si querés contratar la gestión de Meta Ads, empezamos con una auditoría gratis de tu cuenta:</p>
        <ul class="checks">
          <li>{CHECK} Análisis de tu cuenta de Meta Ads</li>
          <li>{CHECK} Revisión de la competencia en tu rubro</li>
          <li>{CHECK} Propuesta de estrategia personalizada</li>
          <li>{CHECK} Sin costo, sin contrato, sin compromiso</li>
        </ul>
      </div>

      <form class="form-card" id="lead-form" novalidate>
        <h3>Pedí tu auditoría <span class="lime">gratis</span></h3>
        <p class="form-subtitle">La auditoría gratis es para negocios interesados en contratar nuestro servicio de <strong>Meta Ads</strong>. ¿Te interesa Marca Lista o Tienda Lista? Elegilo abajo y te contactamos.</p>

        <div class="form-row">
          <div class="form-group" id="g-nombre">
            <label for="f-nombre">Nombre</label>
            <input type="text" id="f-nombre" name="nombre" placeholder="Tu nombre" autocomplete="name">
            <span class="field-error" role="alert"></span>
          </div>
          <div class="form-group" id="g-wp">
            <label for="f-wp">WhatsApp</label>
            <input type="tel" id="f-wp" name="whatsapp" placeholder="+54 9 11..." autocomplete="tel" inputmode="tel">
            <span class="field-error" role="alert"></span>
          </div>
        </div>

        <div class="form-group" id="g-web">
          <label for="f-web">Instagram o sitio web</label>
          <input type="text" id="f-web" name="web" placeholder="@tuempresa o www.tuempresa.com">
          <span class="field-error" role="alert"></span>
        </div>

        <div class="form-group" id="g-servicio">
          <label for="f-servicio">¿Qué servicio te interesa?</label>
          <div class="select-wrap">
            <select id="f-servicio" name="servicio" required>
              <option value="" disabled selected hidden>Elegí una opción</option>
              <option value="auditoria">Auditoría gratis de Meta Ads</option>
              <option value="meta-ads">Gestión de Meta Ads</option>
              <option value="marca-lista">Marca Lista</option>
              <option value="tienda-lista">Tienda Lista</option>
              <option value="no-se">No sé, quiero que me asesoren</option>
            </select>
          </div>
          <span class="field-error" role="alert"></span>
        </div>

        <div class="form-group" id="g-rubro">
          <label for="f-rubro">¿En qué rubro estás?</label>
          <div class="select-wrap">
            <select id="f-rubro" name="rubro">
              <option value="" selected hidden>Seleccioná tu rubro</option>
              <option>E-commerce / Tienda online</option>
              <option>Moda, belleza o cosmética</option>
              <option>Salud, clínicas o bienestar</option>
              <option>Servicios profesionales</option>
              <option>Infoproductos / Cursos online</option>
              <option>Servicios locales</option>
              <option>Inmobiliaria</option>
              <option>Otro</option>
            </select>
          </div>
          <span class="field-error" role="alert"></span>
        </div>

        <div class="form-group" id="g-budget" hidden>
          <label for="f-budget">¿Cuánto invertís por mes en ads?</label>
          <div class="select-wrap">
            <select id="f-budget" name="presupuesto">
              <option value="" selected hidden>Presupuesto mensual aprox.</option>
              <option>Aún no invierto en ads</option>
              <option>Menos de USD 200/mes</option>
              <option>USD 200 – 1.000/mes</option>
              <option>USD 1.000 – 2.000/mes</option>
              <option>Más de USD 2.000/mes</option>
            </select>
          </div>
          <span class="field-error" role="alert"></span>
        </div>

        <button type="submit" class="btn btn-primary btn-submit" id="btn-submit">Enviar consulta →</button>
        <p class="form-status" id="form-status" role="status"></p>
        <p class="form-note">Tu información es confidencial. Ver <a href="privacidad.html">política de privacidad</a>.</p>
      </form>
    </div>
  </section>"""

INDEX = f"""
  <div class="hero-zone">
  <section class="wrap hero">
    <div class="hero-left">
      <span class="hero-badge">{E(I['etiqueta'])}</span>
      <h1>{E(I['titulo_linea_1'])}<br>{E(I['titulo_linea_2'])}<br><span class="lime">{E(I['titulo_linea_3'])}</span></h1>
      <p class="hero-lead">{E(I['texto'])} <strong>{E(I['texto_destacado'])}</strong></p>
      <div class="btn-row">
        <a href="#contacto" class="btn btn-primary">Quiero mi auditoría gratis <span class="arrow-circle">{ARROW}</span></a>
        <a href="#servicios" class="btn btn-ghost">Ver servicios</a>
      </div>
    </div>

    <div class="hero-visual" aria-hidden="true">
      <div class="hero-visual-core">
        {LOGO_BARS.format(p='hv')}
        <span>sync</span>
      </div>
{TAGS}
    </div>
  </section>
  </div>

  <section class="section alt" id="servicios">
    <div class="wrap">
      <div class="section-head">
        <div class="section-label">Servicios</div>
        <h2>Tres servicios, un mismo objetivo: que vendas más</h2>
        <p>Podés contratar cada uno por separado o ir sumándolos a medida que crece tu negocio.</p>
      </div>
      <div class="services-grid">
        <article class="service-card glow-card">
          <span class="tag">Imagen profesional</span>
          <h3>Marca Lista</h3>
          <p class="hook">Tenés un buen producto. El problema es que tu marca no lo refleja.</p>
          <ul>
            <li>Ajuste de logo y destacadas</li>
            <li>Plantillas e infografías para redes</li>
            <li>Bio, textos y Google Maps optimizado</li>
          </ul>
          <div class="price-line">
            <span class="price">${E(M['precio'])} <small>pago único</small></span>
            <a href="marca-lista.html">Ver más →</a>
          </div>
        </article>
        <article class="service-card glow-card">
          <span class="tag">Venta online</span>
          <h3>Tienda Lista</h3>
          <p class="hook">Tu negocio vende mientras dormís.</p>
          <ul>
            <li>Tienda en Empretienda con tu identidad</li>
            <li>Hasta {E(T['productos_incluidos'])} productos cargados</li>
            <li>Pagos, envíos y promociones configurados</li>
          </ul>
          <div class="price-line">
            <span class="price">${E(T['precio'])} <small>pago único</small></span>
            <a href="tienda-lista.html">Ver más →</a>
          </div>
        </article>
        <article class="service-card glow-card">
          <span class="tag">Publicidad</span>
          <h3>Meta Ads</h3>
          <p class="hook">No vendemos anuncios. Vendemos resultados medibles.</p>
          <ul>
            <li>Campañas en Facebook e Instagram</li>
            <li>Creativos diseñados para convertir</li>
            <li>Reporte mensual con números reales</li>
          </ul>
          <div class="price-line">
            <span class="price">Consultá <small>plan mensual</small></span>
            <a href="meta-ads.html">Ver planes →</a>
          </div>
        </article>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section-head">
        <div class="section-label">¿Por dónde empiezo?</div>
        <h2>Elegí según dónde está hoy tu negocio</h2>
      </div>
      <div class="violet path-block">
      <div class="path-list">
        <a href="marca-lista.html" class="path-item">
          <span class="path-situation">Tu producto es bueno, pero tus redes no generan confianza.</span>
          <span class="path-answer"><strong>Marca Lista</strong>Imagen profesional en {E(M['plazo_dias_habiles'])} días hábiles.</span>
          <span class="path-go">{ARROW}</span>
        </a>
        <a href="tienda-lista.html" class="path-item">
          <span class="path-situation">Vendés por Instagram o WhatsApp y respondés mensajes todo el día.</span>
          <span class="path-answer"><strong>Tienda Lista</strong>Tu tienda online cobrando las 24 horas.</span>
          <span class="path-go">{ARROW}</span>
        </a>
        <a href="meta-ads.html" class="path-item">
          <span class="path-situation">Ya vendés y querés llegar a muchos más clientes.</span>
          <span class="path-answer"><strong>Meta Ads</strong>Anuncios con estrategia y creativos que convierten.</span>
          <span class="path-go">{ARROW}</span>
        </a>
      </div>
      </div>
    </div>
  </section>

  <section class="section alt" id="proceso">
    <div class="wrap">
      <div class="section-head">
        <div class="section-label">El proceso</div>
        <h2>Así es trabajar con sync</h2>
        <p>Un proceso claro, estratégico y enfocado en resultados.</p>
      </div>
      <div class="proceso-grid">
        <div class="proceso-step">
          <div class="paso-icon-wrap"><svg viewBox="0 0 24 24"><circle cx="10.5" cy="10.5" r="7"/><line x1="16.5" y1="16.5" x2="23" y2="23"/></svg></div>
          <div class="proceso-text"><h3>Diagnóstico</h3><p>Analizamos tu negocio, tu competencia y cómo te ven hoy tus clientes.</p></div>
        </div>
        <div class="proceso-step">
          <div class="paso-icon-wrap"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg></div>
          <div class="proceso-text"><h3>Estrategia</h3><p>Definimos qué mostrar, cómo decirlo y a quién, según tu objetivo y presupuesto.</p></div>
        </div>
        <div class="proceso-step">
          <div class="paso-icon-wrap"><svg viewBox="0 0 24 24"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/></svg></div>
          <div class="proceso-text"><h3>Lanzamiento</h3><p>Diseñamos las piezas, armamos tu tienda o lanzamos tus campañas bien configuradas.</p></div>
        </div>
        <div class="proceso-step">
          <div class="paso-icon-wrap"><svg viewBox="0 0 24 24"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg></div>
          <div class="proceso-text"><h3>Análisis</h3><p>Medimos, ajustamos y te contamos con números reales qué pasa con tu plata.</p></div>
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section-head">
        <div class="section-label">Por qué sync</div>
        <h2>La creatividad y la estrategia van de la mano</h2>
      </div>
      <div class="why-grid">
        <div class="why-item">
          <span class="why-icon"><svg viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg></span>
          <div><h3>Diseño y pauta en un mismo equipo</h3><p>No tenés que coordinar con un diseñador por un lado y una agencia por el otro.</p></div>
        </div>
        <div class="why-item">
          <span class="why-icon"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg></span>
          <div><h3>Cada pieza tiene una razón</h3><p>Diseñamos pensando en cómo decide tu cliente: qué lo frena en el scroll y qué lo lleva a comprar.</p></div>
        </div>
        <div class="why-item">
          <span class="why-icon"><svg viewBox="0 0 24 24"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg></span>
          <div><h3>Números claros</h3><p>Recibís un reporte mensual simple: cuánto invertiste, qué funcionó y qué hacemos el mes que viene.</p></div>
        </div>
        <div class="why-item">
          <span class="why-icon"><svg viewBox="0 0 24 24"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg></span>
          <div><h3>Seguimiento cercano</h3><p>Hablamos por WhatsApp, te mantenemos al tanto y respondemos tus dudas sin vueltas.</p></div>
        </div>
      </div>
    </div>
  </section>

  <section class="section alt">
    <div class="wrap">
      <div class="section-head">
        <h2>Hablás directo con quienes hacen el trabajo.</h2>
        <p>Somos un equipo chico a propósito.</p>
      </div>
      <ul class="value-circles">
        <li><button type="button" class="vcircle"><span class="vword">Profesionalismo</span><span class="vphrase">Entregas en fecha y procesos claros, sin vueltas.</span></button></li>
        <li><button type="button" class="vcircle"><span class="vword">Transparencia</span><span class="vphrase">Sabés qué pasa con cada peso que invertís.</span></button></li>
        <li><button type="button" class="vcircle"><span class="vword">Creatividad con estrategia</span><span class="vphrase">Cada pieza tiene una razón para existir.</span></button></li>
        <li><button type="button" class="vcircle"><span class="vword">Cercanía</span><span class="vphrase">Una estrategia pensada para tu negocio, no una plantilla.</span></button></li>
      </ul>
    </div>
  </section>

  <section class="section" id="preguntas">
    <div class="wrap">
      <div class="section-head">
        <div class="section-label">Preguntas frecuentes</div>
        <h2>Lo que más nos preguntan</h2>
      </div>
      <div class="faq">
        <details>
          <summary>¿Puedo contratar un solo servicio?</summary>
          <p class="answer">Sí. Marca Lista, Tienda Lista y Meta Ads se contratan por separado. Muchos clientes empiezan por uno y después suman el siguiente.</p>
        </details>
        <details>
          <summary>¿Cómo se paga?</summary>
          <p class="answer">Marca Lista y Tienda Lista se pagan por adelantado, por transferencia o en 3 cuotas sin interés con {E(G['medio_de_pago'])}. Meta Ads es un plan mensual que se abona al inicio de cada mes.</p>
        </details>
        <details>
          <summary>¿Hacen videos o Reels?</summary>
          <p class="answer">No producimos ni editamos video. Trabajamos con piezas estáticas, carruseles, GIFs y animaciones simples. Si tenés material de video propio, te orientamos sobre cómo usarlo en tus anuncios.</p>
        </details>
        <details>
          <summary>¿Qué pasa si no me gusta un diseño?</summary>
          <p class="answer">Cada pieza incluye 2 rondas de ajustes. Tenés 48 horas hábiles para darnos tu opinión.</p>
        </details>
        <details>
          <summary>¿La publicidad en Meta está incluida en el precio?</summary>
          <p class="answer">No. El presupuesto de los anuncios lo pagás directo a Meta con tu tarjeta. Así vos tenés siempre el control de tu plata y podés pausar cuando quieras.</p>
        </details>
        <details>
          <summary>¿Garantizan resultados?</summary>
          <p class="answer">Ninguna agencia seria puede garantizar ventas, porque influyen cosas que no controlamos, como el mercado o la temporada. Lo que sí garantizamos es el trabajo: entregas en fecha, reportes claros y la mejor estrategia para cada peso que invertís.</p>
        </details>
      </div>
    </div>
  </section>
""" + FORM

page("index.html",
     "Sync — Marca, tienda online y Meta Ads en Argentina",
     "Ordenamos la imagen de tu marca, armamos tu tienda online en Empretienda y gestionamos tus anuncios en Facebook e Instagram. Auditoría gratis de Meta Ads.",
     INDEX)

# ───────────────────────── MARCA LISTA ─────────────────────────
MARCA = f"""
  <section class="wrap page-hero">
    <div class="page-hero-grid">
      <div>
        <div class="section-label">Marca Lista</div>
        <h1>Tu marca lista para <span class="lime">vender</span></h1>
        <p class="hook">Tenés un buen producto. El problema es que tu marca no lo refleja.</p>
        <p class="lead">Dejamos tu negocio con una imagen profesional, redes ordenadas y un perfil de Google Maps optimizado para atraer clientes desde el primer día.</p>
        <div class="btn-row">
          <a href="#" data-wa="Hola, quiero Marca Lista para mi negocio 🚀" class="btn btn-primary">Quiero Marca Lista <span class="arrow-circle">{ARROW}</span></a>
          <a href="#incluye" class="btn btn-ghost">Qué incluye</a>
        </div>
      </div>
      <aside class="price-box violet" aria-label="Precio">
        <span class="label">Inversión</span>
        <span class="big">${E(M['precio'])}<small>por transferencia</small></span>
        <dl class="price-meta">
          <div><dt>Entrega</dt><dd>{E(M['plazo_dias_habiles'])} días hábiles</dd></div>
          <div><dt>Ajustes incluidos</dt><dd>2 rondas</dd></div>
        </dl>{pay_block(M, 'marca-lista', 'Marca Lista')}
      </aside>
    </div>
  </section>

  <section class="section alt" id="incluye">
    <div class="wrap">
      <div class="section-head">
        <div class="section-label">Qué incluye</div>
        <h2>Todo lo que tu marca necesita para dar confianza</h2>
      </div>
      <div class="include-grid">
        <div class="include-card glow-card">
          <h3>Identidad visual express</h3>
          <p class="sub">Que te reconozcan a primera vista.</p>
          <ul>
            <li><span><strong>Ajuste de logo:</strong> optimizamos tu logo actual para que se vea bien en digital (hasta 2 revisiones).</span></li>
            <li><span><strong>Historias destacadas:</strong> íconos y portadas con los colores y el estilo de tu marca.</span></li>
          </ul>
        </div>
        <div class="include-card glow-card">
          <h3>Diseño y contenido para redes</h3>
          <p class="sub">Publicá con coherencia sin empezar de cero cada vez.</p>
          <ul>
            <li><span><strong>4 a 6 infografías</strong> para presentar tus productos o servicios, listas para WhatsApp e Instagram.</span></li>
            <li><span><strong>4 a 6 plantillas de feed</strong> editables para tus publicaciones.</span></li>
            <li><span><strong>4 a 6 plantillas de historias</strong> y estados en formato vertical.</span></li>
          </ul>
        </div>
        <div class="include-card glow-card">
          <h3>Textos de tu marca</h3>
          <p class="sub">Palabras que generan confianza y ganas de comprar.</p>
          <ul>
            <li><span><strong>Bio y perfil:</strong> descripciones estratégicas para tus redes con la información clave de tu negocio.</span></li>
            <li><span><strong>Textos listos para usar:</strong> publicaciones, mensajes de presentación y respuestas a reseñas.</span></li>
          </ul>
        </div>
        <div class="include-card glow-card">
          <h3>Google Maps (Perfil de empresa)</h3>
          <p class="sub">Que te encuentren cuando buscan lo que ofrecés en tu zona.</p>
          <ul>
            <li><span><strong>Configuración completa:</strong> categorías, horarios y datos de contacto.</span></li>
            <li><span><strong>Enlaces:</strong> tu web, Instagram y WhatsApp o agenda de turnos.</span></li>
            <li><span><strong>Reseñas:</strong> plantillas para responder rápido reseñas positivas y negativas.</span></li>
            <li><span><strong>Descripción optimizada</strong> con palabras clave de tu zona para aparecer más en búsquedas.</span></li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section-head">
        <div class="section-label">Cómo trabajamos</div>
        <h2>De tu marca actual a tu marca lista</h2>
      </div>
      <div class="steps">
        <div class="step"><h3>Pago y formulario</h3><p>Confirmás el pago y completás un breve formulario sobre tu negocio.{form_link(M)}</p></div>
        <div class="step"><h3>Diagnóstico</h3><p>Revisamos tu logo, tus redes y tu perfil de Google.</p></div>
        <div class="step"><h3>Diseño</h3><p>Creamos las piezas y los textos. Tenés 2 rondas de ajustes.</p></div>
        <div class="step"><h3>Entrega</h3><p>En {E(M['plazo_dias_habiles'])} días hábiles recibís todo listo para usar.</p></div>
      </div>
    </div>
  </section>

  <section class="section alt">
    <div class="wrap two-col">
      <div>
        <h2 class="list-title"><span class="dot off"></span>Qué no incluye</h2>
        <ul class="plain-list">
          <li>Diseño de un logo desde cero.</li>
          <li>Manual de marca corporativo.</li>
          <li>Sesiones de fotos o producción de video.</li>
          <li>Manejo diario de tus redes (publicar, responder comentarios y mensajes).</li>
        </ul>
      </div>
      <div>
        <h2 class="list-title"><span class="dot"></span>Después de Marca Lista</h2>
        <ul class="plain-list">
          <li><strong>Vender online:</strong> sumá <a href="tienda-lista.html">Tienda Lista</a> y ofrecé pago con tarjeta y cuotas, con la misma identidad visual.</li>
          <li><strong>Llegar a más clientes:</strong> con tu marca lista, <a href="meta-ads.html">Meta Ads</a> pone tu negocio frente a miles de compradores de tu zona.</li>
          <li><strong>Materiales de venta:</strong> catálogos, menús, guías en PDF o presentaciones a medida. Consultanos.</li>
        </ul>
      </div>
    </div>
  </section>
""" + cta_band("¿Arrancamos con tu marca?", "Escribinos y en el día te contamos cómo seguimos.", "Hola, quiero Marca Lista para mi negocio 🚀", "marca-lista")

page("marca-lista.html",
     "Marca Lista — Imagen profesional para tu negocio | Sync",
     "Logo optimizado, plantillas para redes, infografías, textos y Google Maps optimizado. ${E(M['precio'])} pago único, entrega en {E(M['plazo_dias_habiles'])} días hábiles.",
     MARCA, sticky=("Quiero Marca Lista →", None, "Hola, quiero Marca Lista para mi negocio 🚀"))

# ───────────────────────── TIENDA LISTA ─────────────────────────
TIENDA = f"""
  <section class="wrap page-hero">
    <div class="page-hero-grid">
      <div>
        <div class="section-label">Tienda Lista</div>
        <h1>Tu tienda online, <span class="lime">lista para vender</span></h1>
        <p class="hook">Tu negocio vende mientras dormís.</p>
        <p class="lead">Armamos tu tienda en Empretienda con la identidad de tu marca, tus productos cargados y todo configurado para cobrar y enviar. Vos solo despachás.</p>
        <div class="btn-row">
          <a href="#" data-wa="Hola, quiero Tienda Lista para mi negocio 🛍️" class="btn btn-primary">Quiero mi tienda <span class="arrow-circle">{ARROW}</span></a>
          <a href="#incluye" class="btn btn-ghost">Qué incluye</a>
        </div>
      </div>
      <aside class="price-box violet" aria-label="Precio">
        <span class="label">Inversión</span>
        <span class="big">${E(T['precio'])}<small>por transferencia</small></span>
        <dl class="price-meta">
          <div><dt>Entrega</dt><dd>{E(T['plazo_dias_habiles'])} días hábiles</dd></div>
          <div><dt>Productos incluidos</dt><dd>Hasta {E(T['productos_incluidos'])}</dd></div>
          <div><dt>Productos adicionales</dt><dd>${E(T['precio_10_productos_extra'])} cada 10</dd></div>
        </dl>{pay_block(T, 'tienda-lista', 'Tienda Lista')}
      </aside>
    </div>
  </section>

  <section class="section alt">
    <div class="wrap">
      <div class="section-head">
        <div class="section-label">¿Por qué Empretienda?</div>
        <h2>Cada peso que vendés queda en tu bolsillo</h2>
        <p>Empretienda es una plataforma argentina para tiendas online, simple de manejar desde el celular.</p>
      </div>
      <div class="fact-row">
        <div class="fact"><strong>0%</strong><span>de comisión por venta, a diferencia de otras plataformas.</span></div>
        <div class="fact"><strong>${E(T['abono_empretienda'])}</strong><span>por mes de abono. Menos que un café por día.</span></div>
        <div class="fact"><strong>15 días</strong><span>de prueba gratis de la plataforma.</span></div>
        <div class="fact"><strong>24/7</strong><span>tus clientes compran sin esperar tu respuesta.</span></div>
      </div>
      <p class="fine">Datos de la plataforma según empretienda.com en octubre de 2026. El abono lo pagás directo a Empretienda y puede cambiar.</p>
    </div>
  </section>

  <section class="section" id="incluye">
    <div class="wrap">
      <div class="section-head">
        <div class="section-label">Qué incluye</div>
        <h2>Nosotras la armamos, vos la manejás fácil</h2>
      </div>
      <div class="include-grid">
        <div class="include-card glow-card">
          <h3>Configuración de la tienda</h3>
          <ul>
            <li><span><strong>Alta y configuración</strong> inicial de tu cuenta.</span></li>
            <li><span><strong>Medios de pago:</strong> Mercado Pago, Ualá Bis, transferencia y efectivo.</span></li>
            <li><span><strong>Envíos:</strong> Correo Argentino, Andreani, OCA, E-Pick, puntos de retiro o envíos propios.</span></li>
            <li><span><strong>Dominio gratuito:</strong> tumarca.empretienda.com.ar</span></li>
          </ul>
        </div>
        <div class="include-card glow-card">
          <h3>Diseño con tu identidad</h3>
          <ul>
            <li><span><strong>Plantilla personalizada</strong> con tus colores, tipografías y logo.</span></li>
            <li><span><strong>Banners</strong> de portada y de categorías.</span></li>
            <li><span><strong>Fotos optimizadas:</strong> trabajamos con las tuyas y, si hace falta, generamos imágenes con IA.</span></li>
          </ul>
        </div>
        <div class="include-card glow-card">
          <h3>Catálogo y textos</h3>
          <ul>
            <li><span><strong>Carga de hasta {E(T['productos_incluidos'])} productos</strong> organizados por categorías.</span></li>
            <li><span><strong>Descripciones</strong> persuasivas de tus productos.</span></li>
            <li><span><strong>Páginas institucionales:</strong> Quiénes somos, Preguntas frecuentes y Políticas de cambio y envío.</span></li>
          </ul>
        </div>
        <div class="include-card glow-card">
          <h3>Herramientas de venta</h3>
          <ul>
            <li><span><strong>Cupones y promociones</strong> iniciales: 2x1, descuentos o envío gratis.</span></li>
            <li><span><strong>Botón de WhatsApp</strong> para consultas directas.</span></li>
            <li><span><strong>Tus redes vinculadas:</strong> Instagram, Facebook, TikTok y más.</span></li>
            <li><span><strong>Formulario de contacto</strong> para recibir consultas.</span></li>
            <li><span><strong>Opcional:</strong> Píxel de Meta y Google Analytics instalados, para dejarla lista para publicitar.</span></li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <section class="section alt">
    <div class="wrap two-col">
      <div>
        <h2 class="list-title"><span class="dot"></span>Para empezar necesitamos</h2>
        <ul class="plain-list">
          <li><strong>Tu logo</strong> en PNG con fondo transparente (o PDF).</li>
          <li><strong>Info de tu marca:</strong> quiénes son, qué venden y cómo manejan cambios, envíos y devoluciones.</li>
          <li><strong>Fotos de tus productos:</strong> mínimo 10 para arrancar.</li>
          <li><strong>Datos de cada producto:</strong> nombre, precio, talles o colores y stock.</li>
          <li><strong>Peso y medidas</strong> de los productos empaquetados, para calcular el envío solo.</li>
          <li><strong>Cómo cobrás y enviás:</strong> tu cuenta de Mercado Pago o Ualá Bis y tus opciones de envío.</li>
          <li><strong>Contacto y redes:</strong> email, WhatsApp, dirección y horarios si tenés local.</li>
        </ul>
        <p class="fine">¿No tenés las categorías definidas? Te ayudamos a armarlas.</p>
      </div>
      <div>
        <h2 class="list-title"><span class="dot off"></span>Qué no incluye</h2>
        <ul class="plain-list">
          <li><strong>Abono de Empretienda:</strong> lo pagás directo a la plataforma.</li>
          <li><strong>Dominio propio</strong> (.com o .com.ar) y su renovación anual.</li>
          <li><strong>Sesiones de fotos</strong> o retoque avanzado.</li>
          <li><strong>Cambios en el código</strong> de la plataforma: usamos sus herramientas y plantillas.</li>
          <li><strong>Creación de cuentas de redes</strong> o catálogos de Instagram y WhatsApp.</li>
          <li><strong>Gestión diaria:</strong> carga de productos nuevos después de la entrega, pedidos y atención al cliente se cotizan aparte.</li>
        </ul>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section-head">
        <div class="section-label">Cómo trabajamos</div>
        <h2>De vender por mensajes a tener tu propia tienda</h2>
      </div>
      <div class="steps">
        <div class="step"><h3>Pago y materiales</h3><p>Confirmás el pago y nos mandás fotos, datos y logo.{form_link(T)}</p></div>
        <div class="step"><h3>Configuración</h3><p>Damos de alta la tienda, pagos, envíos y dominio.</p></div>
        <div class="step"><h3>Diseño y carga</h3><p>Personalizamos el diseño y cargamos tus productos. Tenés 2 rondas de ajustes.</p></div>
        <div class="step"><h3>Entrega</h3><p>En {E(T['plazo_dias_habiles'])} días hábiles tu tienda queda online y te mostramos cómo manejarla.</p></div>
      </div>
      <p class="fine">El plazo corre desde que confirmás el pago y nos enviás todos los materiales.</p>
    </div>
  </section>
""" + cta_band("¿Querés empezar a vender online?", "Escribinos y te contamos cómo sería tu tienda.", "Hola, quiero Tienda Lista para mi negocio 🛍️", "tienda-lista")

page("tienda-lista.html",
     "Tienda Lista — Tu tienda online en Empretienda | Sync",
     "Armamos tu tienda online en Empretienda con tu identidad, hasta {E(T['productos_incluidos'])} productos cargados, pagos y envíos configurados. ${E(T['precio'])} pago único, entrega en {E(T['plazo_dias_habiles'])} días hábiles.",
     TIENDA, sticky=("Quiero mi tienda →", None, "Hola, quiero Tienda Lista para mi negocio 🛍️"))

# ───────────────────────── META ADS ─────────────────────────
def plan(name, forwho, rows, msg, featured=False):
    dl = "\n".join(f"            <div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in rows)
    rib = '<span class="ribbon">Más elegido</span>' if featured else ""
    cls = "plan glow-card featured" if featured else "plan glow-card"
    btn = "btn btn-primary" if featured else "btn btn-ghost"
    return f"""
        <article class="{cls}">
          {rib}
          <h3>{name}</h3>
          <p class="for">{forwho}</p>
          <span class="consult">Consultá el precio</span>
          <dl>
{dl}
          </dl>
          <a href="#" data-wa="{msg}" class="{btn}">Consultar por WhatsApp</a>
        </article>"""

META = f"""
  <section class="wrap page-hero">
    <div class="page-hero-grid">
      <div>
        <div class="section-label">Meta Ads</div>
        <h1>Estrategia<br>Anuncios<br><span class="lime">Resultados</span></h1>
        <p class="hook">No vendemos anuncios. Vendemos resultados medibles con una estrategia detrás.</p>
        <p class="lead">Gestionamos tus campañas en Facebook e Instagram y diseñamos creativos pensados para frenar el scroll y generar consultas y ventas.</p>
        <div class="btn-row">
          <a href="index.html?servicio=auditoria#contacto" class="btn btn-primary">Quiero mi auditoría gratis <span class="arrow-circle">{ARROW}</span></a>
          <a href="#planes" class="btn btn-ghost">Ver planes</a>
        </div>
      </div>
      <aside class="price-box violet" aria-label="Auditoría gratis">
        <span class="label">Primer paso</span>
        <span class="big" style="font-size:clamp(2rem,3.4vw,2.6rem)">Auditoría <span class="lime">gratis</span></span>
        <dl class="price-meta">
          <div><dt>Análisis de tu cuenta</dt><dd>Incluido</dd></div>
          <div><dt>Revisión de tu competencia</dt><dd>Incluido</dd></div>
          <div><dt>Propuesta de estrategia</dt><dd>Incluido</dd></div>
          <div><dt>Costo</dt><dd>$0, sin compromiso</dd></div>
        </dl>
      </aside>
    </div>
  </section>

  <section class="section alt" id="planes">
    <div class="wrap">
      <div class="section-head">
        <div class="section-label">Planes mensuales</div>
        <h2>Elegí el plan según cuánto invertís en anuncios</h2>
        <p>El precio de cada plan lo vemos juntos después de la auditoría, según tu negocio y tu objetivo.</p>
      </div>
      <div class="plans" style="grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));max-width:880px">
        {plan("Plan Base", "Para empezar a medir resultados con una estructura simple.", [
            ("Inversión en anuncios", "Hasta USD 1.000/mes"),
            ("Creativos por mes", "4 piezas"),
            ("Estrategia", "1 campaña + retargeting"),
            ("Reporte", "Mensual"),
            ("Ajustes por pieza", "2 rondas"),
        ], "Hola, quiero consultar por el Plan Base de Meta Ads")}
        {plan("Plan Pro", "Para negocios que quieren escalar con un embudo completo.", [
            ("Inversión en anuncios", "Hasta USD 2.000/mes"),
            ("Creativos por mes", "8 a 10 piezas"),
            ("Estrategia", "Embudo completo"),
            ("Reporte", "Mensual"),
            ("Ajustes por pieza", "2 rondas"),
        ], "Hola, quiero consultar por el Plan Pro de Meta Ads", featured=True)}
      </div>
      <p class="fine">¿Invertís más de USD 2.000 por mes? <a href="#" data-wa="Hola, invierto más de USD 2.000 por mes en anuncios y quiero un plan a medida" style="color:var(--lime)">Escribinos y armamos un plan a medida</a>.</p>
    </div>
  </section>

  <section class="section" id="incluye">
    <div class="wrap">
      <div class="section-head">
        <div class="section-label">Qué incluye</div>
        <h2>Nosotras manejamos el auto. Vos ponés el combustible.</h2>
        <p>Vos ponés el presupuesto de Meta; nosotras hacemos que rinda lo más posible sin desperdiciar nada.</p>
      </div>
      <div class="include-grid">
        <div class="include-card glow-card">
          <h3>Puesta en marcha</h3>
          <p class="sub">Se hace una sola vez, en 7 a 15 días.</p>
          <ul>
            <li><span><strong>Diagnóstico</strong> de tu cuenta actual, si ya tenés una.</span></li>
            <li><span><strong>Configuración</strong> del Business Manager y la cuenta publicitaria.</span></li>
            <li><span><strong>Píxel de Meta y API de conversiones</strong> instalados y verificados.</span></li>
            <li><span><strong>Eventos de conversión</strong> (visitas, carrito, compras) y verificación del dominio.</span></li>
            <li><span><strong>Públicos base</strong> para remarketing y audiencias similares.</span></li>
            <li><span><strong>Creativos y textos iniciales</strong> para lanzar.</span></li>
          </ul>
        </div>
        <div class="include-card glow-card">
          <h3>Gestión mensual</h3>
          <p class="sub">El trabajo continuo, mes a mes.</p>
          <ul>
            <li><span><strong>Estrategia de campañas</strong> para público frío, tibio y retargeting.</span></li>
            <li><span><strong>Optimización</strong> de presupuesto cada 2 o 3 días.</span></li>
            <li><span><strong>Textos persuasivos</strong> y variaciones para probar qué funciona.</span></li>
            <li><span><strong>Rotación de creativos</strong> cuando el público se cansa de verlos.</span></li>
            <li><span><strong>Reporte mensual</strong> con resultados, aprendizajes y próximos pasos.</span></li>
            <li><span><strong>Novedades por WhatsApp</strong> cada semana y una reunión mensual opcional.</span></li>
          </ul>
        </div>
        <div class="include-card glow-card">
          <h3>Creativos que convierten</h3>
          <p class="sub">Cada pieza tiene una razón estratégica para existir.</p>
          <ul>
            <li><span><strong>Piezas estáticas, carruseles, GIFs</strong> y animaciones simples para feed y stories.</span></li>
            <li><span><strong>Usamos tu material</strong> y lo optimizamos. Si no tenés fotos, las generamos con IA.</span></li>
            <li><span><strong>Versiones para comparar:</strong> con y sin precio, distintos llamados a la acción y públicos.</span></li>
          </ul>
        </div>
        <div class="include-card glow-card">
          <h3>Vos tenés el control</h3>
          <p class="sub">Tu plata, tu cuenta, tus decisiones.</p>
          <ul>
            <li><span><strong>El presupuesto de anuncios</strong> lo pagás directo a Meta con tu tarjeta.</span></li>
            <li><span><strong>Podés pausar</strong> los anuncios con un clic cuando quieras.</span></li>
            <li><span><strong>Siempre sabés</strong> cuánto se invirtió y qué resultados dio.</span></li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <section class="section alt">
    <div class="wrap two-col">
      <div>
        <h2 class="list-title"><span class="dot off"></span>Qué no incluye</h2>
        <ul class="plain-list">
          <li><strong>El presupuesto de anuncios:</strong> lo pagás directo a Meta, junto con los impuestos que cobra tu banco.</li>
          <li><strong>Otras plataformas</strong> como Google Ads o TikTok Ads.</li>
          <li><strong>Producción o edición de video</strong> y Reels.</li>
          <li><strong>Cambios en tu web:</strong> si detectamos problemas en tu página te los marcamos, pero no la programamos.</li>
          <li><strong>Manejo diario de redes</strong> (comentarios y mensajes).</li>
        </ul>
      </div>
      <div>
        <h2 class="list-title"><span class="dot"></span>Condiciones</h2>
        <ul class="plain-list">
          <li><strong>Permanencia mínima de 2 meses.</strong> Es el tiempo que necesita una campaña para aprender y mostrar resultados.</li>
          <li><strong>Pago por adelantado:</strong> la puesta en marcha se abona junto con el primer mes.</li>
          <li><strong>Desde el tercer mes,</strong> el plan se renueva mes a mes y podés darlo de baja avisando antes del vencimiento.</li>
          <li><strong>Ideal si ya vendés</strong> por algún canal (tienda online, local o redes) y querés escalar.</li>
        </ul>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section-head">
        <div class="section-label">Preguntas frecuentes</div>
        <h2>Antes de empezar</h2>
      </div>
      <div class="faq">
        <details>
          <summary>¿Cuánto tengo que invertir en anuncios?</summary>
          <p class="answer">Depende de tu rubro y tu objetivo. En la auditoría gratis te recomendamos un presupuesto realista para tu negocio.</p>
        </details>
        <details>
          <summary>¿Garantizan resultados?</summary>
          <p class="answer">Ninguna agencia seria puede garantizar ventas, porque influyen cosas que no controlamos, como el mercado o la temporada. Lo que sí garantizamos es el trabajo: entregas en fecha, reportes claros y la mejor estrategia para cada peso que invertís.</p>
        </details>
        <details>
          <summary>¿Por qué no se puede negociar el precio?</summary>
          <p class="answer">Nuestros precios están calculados para hacer el trabajo bien. Si el presupuesto es una limitación, el Plan Base es una buena forma de empezar a medir resultados.</p>
        </details>
        <details>
          <summary>No tengo tienda online, ¿puedo pautar igual?</summary>
          <p class="answer">Sí, podés recibir consultas por WhatsApp o Instagram. Si querés vender directo desde los anuncios, te conviene sumar <a href="tienda-lista.html" style="color:var(--lime)">Tienda Lista</a>: la dejamos con el Píxel instalado, lista para pautar.</p>
        </details>
      </div>
    </div>
  </section>
""" + cta_band("Empezá con una auditoría gratis", "Analizamos tu cuenta y tu competencia y te proponemos una estrategia. Sin costo y sin compromiso.", "Hola, quiero mi auditoría gratis de Meta Ads 🚀", "auditoria", wa_label="Pedir por WhatsApp")

page("meta-ads.html",
     "Meta Ads — Gestión de anuncios en Facebook e Instagram | Sync",
     "Gestión profesional de campañas en Facebook e Instagram con creativos diseñados para convertir. Pedí tu auditoría gratis, sin compromiso.",
     META, sticky=("Quiero mi auditoría gratis →", "index.html?servicio=auditoria#contacto", None))

# ───────────────────────── GRACIAS ─────────────────────────
GRACIAS = """
  <section class="wrap center-page">
    <div class="ty-check"><svg viewBox="0 0 24 24" aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg></div>
    <h1>¡Solicitud enviada con <span class="lime">éxito!</span></h1>
    <p>Gracias por confiar en sync. Recibimos tu consulta por <strong id="ty-servicio">nuestros servicios</strong> y te escribimos por WhatsApp a la brevedad.</p>
    <div class="ty-cards">
      <div class="ty-card"><h2>Revisamos tu negocio</h2><p>Miramos tus redes, tu cuenta y tu rubro para detectar oportunidades reales.</p></div>
      <div class="ty-card"><h2>Te contactamos</h2><p>Recibís un WhatsApp con los próximos pasos en menos de 24 h hábiles.</p></div>
      <div class="ty-card"><h2>Preparate para crecer</h2><p>Te proponemos un plan claro y accionable para tu negocio.</p></div>
    </div>
    <div class="btn-row" style="justify-content:center">
      <a href="#" id="ty-wa" data-wa="Hola, acabo de completar el formulario 🚀" class="btn btn-primary">Escribinos por WhatsApp</a>
      <a href="index.html" class="btn btn-ghost">Volver al inicio</a>
    </div>
  </section>
"""
page("gracias.html", "¡Gracias! — Sync", "Recibimos tu consulta.", GRACIAS, active="", noindex=True)

# ───────────────────────── 404 ─────────────────────────
NOTFOUND = """
  <section class="wrap center-page">
    <h1>Esta página <span class="lime">no existe</span></h1>
    <p>Puede que el link esté mal escrito o que la página se haya movido.</p>
    <div class="btn-row" style="justify-content:center">
      <a href="index.html" class="btn btn-primary">Ir al inicio</a>
      <a href="#" data-wa="Hola, quiero saber más sobre sus servicios 🚀" class="btn btn-ghost">Escribinos</a>
    </div>
  </section>
"""
page("404.html", "Página no encontrada — Sync", "La página que buscás no existe.", NOTFOUND, active="", noindex=True)

# ───────────────────────── LEGALES ─────────────────────────
PRIV = f"""
  <article class="wrap legal">
    <h1>Política de privacidad</h1>
    <p class="updated">Última actualización: octubre de 2026</p>

    <h2>Quiénes somos</h2>
    <p>Sync Media es una agencia de marketing digital de Buenos Aires, Argentina. Podés contactarnos por WhatsApp al {E(G['whatsapp_visible'])}.</p>

    <h2>Qué datos recopilamos</h2>
    <p>Cuando completás el formulario de contacto guardamos:</p>
    <ul>
      <li>Tu nombre y número de WhatsApp.</li>
      <li>Tu Instagram o sitio web, si lo cargás.</li>
      <li>El servicio que te interesa, tu rubro y tu presupuesto aproximado en publicidad.</li>
    </ul>

    <h2>Para qué los usamos</h2>
    <p>Solo para responder tu consulta, preparar tu auditoría o propuesta y comunicarnos con vos sobre nuestros servicios. No vendemos ni compartimos tus datos con terceros para fines comerciales.</p>

    <h2>Dónde se guardan</h2>
    <p>Los datos del formulario se guardan en una planilla privada de Google a la que solo accede nuestro equipo.</p>

    <h2>Cookies y medición</h2>
    <p>Usamos Google Tag Manager, Google Analytics y el Píxel de Meta para saber cuántas personas visitan la web, de dónde llegan y si completan el formulario. Esto nos ayuda a mejorar la web y nuestros anuncios. Podés bloquear o borrar las cookies desde la configuración de tu navegador.</p>

    <h2>Tus derechos</h2>
    <p>Podés pedirnos en cualquier momento ver, corregir o borrar tus datos escribiéndonos por WhatsApp. Respondemos dentro de los 10 días hábiles, como indica la Ley 25.326 de Protección de Datos Personales. La Agencia de Acceso a la Información Pública es el organismo de control en Argentina y recibe denuncias o reclamos relacionados con el uso de datos personales.</p>
  </article>
"""
page("privacidad.html", "Política de privacidad — Sync", "Cómo usamos los datos que nos dejás en el formulario de contacto de Sync Media.", PRIV, active="")

TERM = f"""
  <article class="wrap legal">
    <h1>Términos y condiciones</h1>
    <p class="updated">Última actualización: octubre de 2026</p>

    <h2>Precios</h2>
    <ul>
      <li>Todos los precios están en pesos argentinos (ARS) y pueden actualizarse. Los clientes activos reciben aviso con 30 días de anticipación.</li>
      <li>Marca Lista y Tienda Lista se pagan 100% por adelantado, por transferencia o en 3 cuotas sin interés con {E(G['medio_de_pago'])}.</li>
      <li>Los planes de Meta Ads se pagan al inicio de cada mes. La puesta en marcha se abona junto con el primer mes.</li>
    </ul>

    <h2>Plazos</h2>
    <ul>
      <li>Marca Lista: {E(M['plazo_dias_habiles'])} días hábiles desde la aprobación del formulario inicial.</li>
      <li>Tienda Lista: {E(T['plazo_dias_habiles'])} días hábiles desde la confirmación del pago y la entrega de todos los materiales.</li>
      <li>Meta Ads: las campañas se lanzan dentro de los 3 días hábiles desde que aprobás los creativos.</li>
    </ul>

    <h2>Revisiones</h2>
    <ul>
      <li>Cada pieza incluye 2 rondas de ajustes sin costo.</li>
      <li>Tenés 48 horas hábiles para darnos tu opinión. Si no recibimos respuesta, la pieza se considera aprobada.</li>
      <li>Las rondas adicionales tienen un costo extra que te confirmamos por escrito antes de hacerlas.</li>
    </ul>

    <h2>Meta Ads</h2>
    <ul>
      <li>Permanencia mínima de 2 meses. Desde el tercer mes el plan se renueva mes a mes.</li>
      <li>Para dar de baja el servicio, avisanos por escrito antes del vencimiento del mes en curso. No se devuelven meses ya pagados.</li>
      <li>El presupuesto de anuncios lo paga el cliente directamente a Meta y no está incluido en nuestros honorarios.</li>
      <li>No garantizamos resultados de venta, porque dependen de factores externos. Sí garantizamos el trabajo acordado, en tiempo y forma.</li>
    </ul>

    <h2>Propiedad de los diseños</h2>
    <p>Los archivos finales son tuyos una vez abonado el servicio o el mes correspondiente. Los archivos editables y la metodología de trabajo de la agencia no se entregan, salvo acuerdo por escrito.</p>

    <h2>Servicios de terceros</h2>
    <p>Plataformas como Empretienda, Meta, Google o Mercado Pago tienen sus propios costos y condiciones, que no dependen de nosotras.</p>
  </article>
"""
page("terminos.html", "Términos y condiciones — Sync", "Condiciones de contratación de los servicios de Sync Media.", TERM, active="")

print("Páginas generadas en", OUT)
