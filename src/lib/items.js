// src/lib/items.js — Loader Astro que reutiliza los deep modules existentes.
// No duplica lógica: importa parser/taxonomy/verses de scripts/builder.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseMd } from '../../scripts/builder/parser.mjs';
import { MESES } from '../../scripts/builder/taxonomy.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(__dirname, '..', '..');

function resolveArticulosDir() {
  const candidates = [
    path.join(projectRoot, 'content', 'articulos'),
    path.join(projectRoot, 'articulos_completos'),
  ];
  return candidates.find((p) => fs.existsSync(p)) ?? candidates[0];
}

let _cache = null;

/** Carga todos los items ordenados por fecha desc (misma semántica que build-data.mjs). */
export function loadItems() {
  if (_cache) return _cache;
  const srcDir = resolveArticulosDir();
  const files = fs.readdirSync(srcDir).filter((f) => f.endsWith('.md'));
  const items = files.map((f) => parseMd(path.join(srcDir, f)));
  items.sort((a, b) => b.ts - a.ts);
  const byCat = {};
  MESES.forEach((c) => (byCat[c.id] = 0));
  items.forEach((i) => {
    if (byCat[i.categoria] !== undefined) byCat[i.categoria] += 1;
  });
  const categories = MESES.map((c) => ({ ...c, count: byCat[c.id] ?? 0 }));
  _cache = { items, categories, total: items.length };
  return _cache;
}

export { MESES };
