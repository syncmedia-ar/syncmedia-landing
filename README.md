# syncmedia.ar — Web de Sync Media

Web oficial de Sync Media: Marca Lista, Tienda Lista y Meta Ads.
Se publica gratis con **GitHub Pages** en el dominio **syncmedia.ar**.

## Qué hay en cada archivo

| Archivo | Para qué sirve |
| --- | --- |
| `contenido.json` | **Lo que se edita desde el panel:** banner, precios, links de pago, formularios, WhatsApp |
| `scripts/build.py` | Arma todas las páginas `.html` a partir de `contenido.json`. Los textos fijos de cada página están acá |
| `.pages.yml` | Configuración del panel (qué campos se ven) |
| `.github/workflows/generar-web.yml` | Automatización que regenera la web al guardar desde el panel |
| `index.html` | Inicio (servicios, proceso, equipo, preguntas y formulario) |
| `marca-lista.html` | Página de Marca Lista |
| `tienda-lista.html` | Página de Tienda Lista |
| `meta-ads.html` | Página de Meta Ads (planes con "Consultá") |
| `gracias.html` | Página que ve el cliente después de enviar el formulario |
| `privacidad.html` / `terminos.html` | Legales |
| `404.html` | Página de error si alguien entra a un link que no existe |
| `assets/css/styles.css` | Colores, tipografías y diseño de toda la web |
| `assets/js/main.js` | Menú, formulario, efectos y cookies. Arriba está la conexión con el Sheet y Make |
| `assets/img/og-image.png` | Imagen que aparece al compartir el link en WhatsApp o redes |
| `apps-script/Codigo.gs` | Código del Google Sheet (no se sube a la web, se pega en Google) |
| `CNAME` | Le dice a GitHub que la web va en syncmedia.ar. **No borrar** |

## Panel de control (Pages CMS)

Desde el panel se cambian **sin programar**: banner de inicio y cartelitos, precios y cuotas, plazos, links de pago, links de formularios, WhatsApp y la frase de la pestaña.

**Primera vez (solo una):** entrá a **app.pagescms.org**, iniciá sesión con GitHub y cuando te lo pida **instalá la app de Pages CMS** en la organización `syncmedia-ar` (solo en el repositorio `syncmedia-landing`).

**Después:** entrá a app.pagescms.org → elegí `syncmedia-landing` → **Contenido de la web** → cambiá lo que necesites → **Save**. En 1 o 2 minutos la web se actualiza sola (podés ver el avance en la pestaña **Actions** del repositorio).

**Quién puede entrar:** solo quienes tengan permiso de escritura en el repositorio. Para sumar a Cami: repositorio → **Settings → Collaborators and teams → Add people** → rol **Write**.

**Botones automáticos:**
En Marca Lista y Tienda Lista, la caja de precio tiene un selector **"¿Cómo querés pagar?"**:
- **Transferencia** (siempre visible, al precio de contado): muestra el **alias** con botón *Copiar* y el botón *Enviar comprobante por WhatsApp*. Si el alias está vacío, aparece *Pedir datos para transferir*.
- **3 cuotas sin interés**: aparece solo si cargás el **link de pago en 3 cuotas**. El total se calcula solo (valor de la cuota x 3).
- Si cargás un **link de formulario**, aparece *"Después de pagar, completá el formulario de inicio"* debajo del botón, y también en el paso 1 de "Cómo trabajamos".

**Cómo crear el link de pago en cuotas (Mercado Pago):** Link de pago → monto = total en cuotas (ej. $183.600) → activá **3 cuotas sin interés** → copiá el link y pegalo en el panel.

## Reglas importantes

- **No edites los `.html` de la raíz a mano:** se vuelven a generar solos y perderías el cambio.
  - Precios, links y banner → panel o `contenido.json`.
  - Textos fijos de las páginas → `scripts/build.py`.
  - Colores y diseño → `assets/css/styles.css` (al principio, en `:root`).
- Si cambiás algo en tu compu, generá las páginas antes de probar: en la terminal de VS Code escribí `python scripts/build.py`.

## Subir cambios a la web

1. Abrí la carpeta en VS Code y hacé tus cambios (si tocaste `contenido.json` o `scripts/build.py`, corré `python scripts/build.py`).
2. Probala en tu compu con la extensión **Live Server** (clic derecho en `index.html` → *Open with Live Server*).
3. En la barra lateral, ícono de **Control de código fuente** → escribí un mensaje → **Commit** → **Sync / Push**.
4. En 1 o 2 minutos se ve en syncmedia.ar.

## Integraciones

### Formulario → Google Sheet
La web manda cada consulta a tu Sheet de leads. Como ahora hay una pregunta nueva (*¿Qué servicio te interesa?*), hay que actualizar el script de Google **una sola vez**:

1. Abrí el Sheet → **Extensiones → Apps Script**.
2. Borrá el código y pegá todo el contenido de `apps-script/Codigo.gs`. Guardá.
3. **Implementar → Gestionar implementaciones** → lápiz de la implementación actual → Versión: **Nueva versión** → **Implementar**.
   (Así la dirección no cambia y no hay que tocar la web.)
4. Probalo: completá el formulario de la web y fijate que aparezca la fila con la columna *Servicio*.

### Make (avisos automáticos)
Está **apagado**. Cuando retomes el escenario, pegá la URL del webhook en `assets/js/main.js`, en `MAKE_WEBHOOK_URL`. La web le manda los mismos datos que al Sheet.

### Google Tag Manager (GTM-WQXNB7L3)
Ya está instalado en todas las páginas. Desde Tag Manager se configuran el Píxel de Meta y Google Analytics, sin tocar la web. La web avisa estos eventos:

| Evento | Cuándo pasa | Uso sugerido |
| --- | --- | --- |
| `generate_lead` | Alguien envía el formulario (incluye `servicio` y `rubro`) | Evento **Lead** del Píxel y conversión en Analytics |
| `whatsapp_click` | Alguien toca un botón de WhatsApp | Evento **Contact** del Píxel |
| `begin_checkout` | Alguien toca *Pagar 3 x $…* (incluye `servicio`) | Evento **InitiateCheckout** del Píxel |
| `alias_copiado` | Alguien copia el alias para transferir | Evento **InitiateCheckout** (pago por transferencia) |
| Vista de `gracias.html` | Después de enviar el formulario | Alternativa para medir Leads |

### Google Search Console
Para aparecer en Google: entrá a search.google.com/search-console, agregá `syncmedia.ar` y cargá el mapa del sitio `https://syncmedia.ar/sitemap.xml`.
