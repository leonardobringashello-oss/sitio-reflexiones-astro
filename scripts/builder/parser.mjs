// scripts/builder/parser.mjs — Module ContentParser (deep module)
// Interface: parseMd(filePath, {fs, taxonomy, verses}) -> Item
// Accept dependencies, don't create them. Return results, don't produce side effects.

import fs from 'fs';
import path from 'path';
import { categoriaPorFecha } from './taxonomy.mjs';
import { extractVerses } from './verses.mjs';

export function parseMd(filePath, deps = {}) {
  const _fs = deps.fs || fs;
  const raw = _fs.readFileSync(filePath, 'utf-8');

  const titleMatch = raw.match(/-\s*Titulo:\s*(.+)/);
  const fechaMatch = raw.match(/-\s*Fecha:\s*(.+)/);
  const urlMatch = raw.match(/-\s*URL ORIGEN:\s*(.+)/);
  const imgMatch = raw.match(/-\s*Imagen:\s*(.+)/);
  const audioMatch = raw.match(/-\s*Audio Local:\s*(.+)/);

  let titulo = titleMatch ? titleMatch[1].trim() : path.basename(filePath, '.md');
  titulo = titulo.replace(/^["'“”]+|["'“”]+$/g, '').trim();

  const fechaStr = fechaMatch ? fechaMatch[1].trim() : '';
  const urlOrigen = urlMatch ? urlMatch[1].trim() : '';
  const imagenRaw = imgMatch ? imgMatch[1].trim() : 'Ninguna';
  const audioRaw = audioMatch ? audioMatch[1].trim() : 'Ninguno';

  const contenidoIdx = raw.indexOf('Contenido:');
  let contenido = contenidoIdx !== -1 ? raw.slice(contenidoIdx + 'Contenido:'.length) : raw;
  contenido = contenido.replace(/\n-{3,}[\s\S]*?$/, '').trim();
  contenido = contenido.replace(/Comparte esto:[\s\S]*$/i, '').trim();
  contenido = contenido.replace(/Relacionado[\s\S]*$/i, '').trim();
  // Labels sueltos de botones al final (X, Facebook, Me gusta, Cargando...) — red de seguridad
  contenido = contenido.replace(/(\n*(?:^(?:X|Facebook|Me gusta[^\n]*|Cargando\.*|Compartir[^\n]{0,60}|Comparte[^\n]{0,60}|Seguir[^\n]{0,60}|Suscribir[^\n]{0,60})\s*$))+$/gim, '').trim();
  contenido = contenido.split('\n').map((l) => l.trim()).filter(Boolean).join('\n\n');

  const plain = contenido.replace(/\n/g, ' ').replace(/\s+/g, ' ').trim();
  const excerpt = plain.slice(0, 220) + (plain.length > 220 ? '…' : '');

  let fechaISO = null;
  let ts = 0;
  if (fechaStr) {
    const [d, m, y] = fechaStr.split('/').map(Number);
    if (d && m && y) {
      const dt = new Date(y, m - 1, d);
      fechaISO = dt.toISOString().slice(0, 10);
      ts = dt.getTime();
    }
  }

  const slug = path.basename(filePath, '.md');
  const imagen = imagenRaw && imagenRaw !== 'Ninguna' && imagenRaw !== 'Ninguno' ? imagenRaw : null;
  const audio = audioRaw && audioRaw !== 'Ninguna' && audioRaw !== 'Ninguno' ? audioRaw : null;

  const categoria = categoriaPorFecha(fechaISO);
  const versiculos = extractVerses(contenido);

  const words = contenido.split(/\s+/).length;
  const lecturaMin = Math.max(2, Math.ceil(words / 180));

  return {
    slug,
    titulo,
    fecha: fechaStr,
    fechaISO,
    ts,
    urlOrigen,
    imagen,
    imagenPath: imagen ? `imagenes/${imagen}` : null,
    audio,
    audioPath: audio ? `audios/${audio}` : null,
    excerpt,
    contenido: contenido.slice(0, 8000),
    contenidoFull: contenido.length,
    categoria,
    versiculos,
    lecturaMin,
    palabras: words,
  };
}
