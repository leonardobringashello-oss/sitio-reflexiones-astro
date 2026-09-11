const LIBROS_CANONICOS = [
  'Génesis', 'Éxodo', 'Levítico', 'Números', 'Deuteronomio',
  'Josué', 'Jueces', 'Rut',
  '1 Samuel', '2 Samuel', '1 Reyes', '2 Reyes',
  '1 Crónicas', '2 Crónicas', 'Esdras', 'Nehemías', 'Ester',
  'Job', 'Salmos', 'Salmo', 'Proverbios', 'Eclesiastés', 'Cantares',
  'Isaías', 'Jeremías', 'Lamentaciones', 'Ezequiel', 'Daniel',
  'Oseas', 'Joel', 'Amós', 'Abdías', 'Jonás', 'Miqueas', 'Nahum',
  'Habacuc', 'Sofonías', 'Hageo', 'Zacarías', 'Malaquías',
  'Mateo', 'Marcos', 'Lucas', 'Juan', 'Hechos', 'Romanos',
  '1 Corintios', '2 Corintios', 'Gálatas', 'Efesios', 'Filipenses',
  'Colosenses', '1 Tesalonicenses', '2 Tesalonicenses',
  '1 Timoteo', '2 Timoteo', 'Tito', 'Filemón', 'Hebreos',
  'Santiago', '1 Pedro', '2 Pedro', '1 Juan', '2 Juan', '3 Juan',
  'Judas', 'Apocalipsis',
];

function stripAccents(s) {
  return s.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
}

// Mapa: nombre normalizado (minúsculas, sin tildes, espacios colapsados) -> canónico
const CANONICO_POR_NORM = new Map(
  LIBROS_CANONICOS.map((c) => [stripAccents(c).toLowerCase().replace(/\s+/g, ' '), c]),
);

// Alternancia ordenada por longitud desc para que "1 corintios" gane a "corintios"
const ALTERNANCIA = [...CANONICO_POR_NORM.keys()]
  .sort((a, b) => b.length - a.length)
  .map((k) => k.replace(/[.*+?^${}()|[\]\\]/g, '\\$&').replace(/ /g, '\\s+'))
  .join('|');

// Requiere SIEMPRE capítulo:versículo -> nunca devuelve "Éxodo" sin número
// y nunca captura palabras comunes ("en 4:2") porque el libro debe estar en la whitelist.
const VERSE_RE = new RegExp(`(^|[^\\p{L}\\p{N}_])(${ALTERNANCIA})\\s+(\\d+:\\d+(?:-\\d+)?)`, 'giu');

/**
 * Extrae hasta 3 versículos tipo "Éxodo 3:6" o "Juan 14:5-6" del contenido.
 * Solo devuelve libros canónicos con capítulo:versículo. No inventa nada.
 * @param {string} contenido
 * @returns {string[]}
 */
export function extractVerses(contenido) {
  if (!contenido) return [];
  const versiculos = [];
  const vistos = new Set();
  // Normalizamos tildes para que "Éxodo" matchee "exodo" sin perder la primera letra.
  // Los números no se ven afectados, y el display usa el nombre canónico con tilde.
  const texto = stripAccents(contenido);
  VERSE_RE.lastIndex = 0;
  let m;
  while ((m = VERSE_RE.exec(texto)) !== null) {
    const normLibro = m[2].replace(/\s+/g, ' ').trim().toLowerCase();
    // m[2] ya viene sin tildes si el texto las tenía? No: el match es sobre
    // el texto original con flag i, así que normalizamos para buscar el canónico.
    const clave = stripAccents(normLibro).replace(/\s+/g, ' ');
    const canonico = CANONICO_POR_NORM.get(clave);
    if (!canonico) continue;
    const valor = `${canonico} ${m[3]}`.slice(0, 50);
    const dedup = valor.toLowerCase();
    if (vistos.has(dedup)) continue;
    vistos.add(dedup);
    versiculos.push(valor);
    if (versiculos.length >= 3) break;
  }
  return versiculos;
}

/**
 * Normaliza para scoring (libro + capítulo).
 * Ej: "Éxodo 3:6" -> "éxodo 3" (insensible a tildes en comparación: usá stripAccents al comparar).
 */
export function normalizeVerseBookChapter(verse) {
  if (!verse) return '';
  const m = stripAccents(verse).match(/^\s*(.+?)\s+(\d+):/);
  if (!m) return stripAccents(verse).toLowerCase().trim();
  return `${m[1].replace(/\s+/g, ' ').trim().toLowerCase()} ${m[2]}`;
}
