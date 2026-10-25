/**
 * SYNC MEDIA — Script que guarda los leads de la web en el Google Sheet.
 *
 * Cómo instalarlo (una sola vez):
 * 1. Abrí tu Google Sheet de leads → menú Extensiones → Apps Script.
 * 2. Borrá todo el código que hay y pegá este archivo completo. Guardá (ícono de disquete).
 * 3. Arriba a la derecha: Implementar → Gestionar implementaciones.
 * 4. Tocá el lápiz (editar) de la implementación que ya existe.
 * 5. En "Versión" elegí "Nueva versión" → Implementar.
 *    Así la dirección (URL) no cambia y la web sigue funcionando.
 *
 * Qué hace: cada vez que alguien completa el formulario, agrega una fila.
 * Si falta alguna columna (por ejemplo "Servicio"), la crea sola al final.
 */

// Nombre de la pestaña donde se guardan los leads.
// Si lo dejás vacío, usa la primera pestaña del archivo.
const NOMBRE_PESTANA = '';

// Columnas: [nombre que se ve en el Sheet, dato que manda la web]
// (al comparar se ignoran mayúsculas y espacios: "Instagram / Web" = "Instagram/Web")
const COLUMNAS = [
  ['Fecha', 'fecha'],
  ['Nombre', 'nombre'],
  ['WhatsApp', 'whatsapp'],
  ['Instagram/Web', 'web'],
  ['Servicio', 'servicio'],
  ['Rubro', 'rubro'],
  ['Presupuesto', 'presupuesto'],
  ['Página', 'origen'],
];

function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const datos = JSON.parse(e.postData.contents || '{}');
    datos.fecha = new Date();

    const libro = SpreadsheetApp.getActiveSpreadsheet();
    const hoja = NOMBRE_PESTANA ? libro.getSheetByName(NOMBRE_PESTANA) : libro.getSheets()[0];

    // Leer los títulos actuales (fila 1)
    let titulos = [];
    if (hoja.getLastColumn() > 0) {
      titulos = hoja.getRange(1, 1, 1, hoja.getLastColumn()).getValues()[0]
        .map(function (t) { return String(t).trim(); });
    }
    function igual(a, b) {
      return String(a).toLowerCase().replace(/\s+/g, '') === String(b).toLowerCase().replace(/\s+/g, '');
    }

    // Crear las columnas que falten
    COLUMNAS.forEach(function (col) {
      const titulo = col[0];
      const existe = titulos.some(function (t) { return igual(t, titulo); });
      if (!existe) {
        titulos.push(titulo);
        hoja.getRange(1, titulos.length).setValue(titulo).setFontWeight('bold');
      }
    });

    // Armar la fila respetando el orden de las columnas del Sheet
    const fila = titulos.map(function (t) {
      const col = COLUMNAS.find(function (c) { return igual(c[0], t); });
      return col ? (datos[col[1]] !== undefined ? datos[col[1]] : '') : '';
    });

    hoja.appendRow(fila);

    return ContentService.createTextOutput(JSON.stringify({ ok: true }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({ ok: false, error: String(err) }))
      .setMimeType(ContentService.MimeType.JSON);
  } finally {
    lock.releaseLock();
  }
}

// Para probar desde el editor: elegí "probar" arriba y tocá Ejecutar.
// Tiene que aparecer una fila de prueba en el Sheet (después borrala).
function probar() {
  doPost({ postData: { contents: JSON.stringify({
    nombre: 'Prueba', whatsapp: '+5491100000000', web: '@prueba',
    servicio: 'Tienda Lista', rubro: 'Otro', presupuesto: '', origen: '/index.html'
  }) } });
}
