#!/usr/bin/env node
// Orquestador delgado — Fase 2: delega a módulos profundos (taxonomy/parser/verses)
// Mantiene compatibilidad con build-data.js legacy.

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { MESES } from './taxonomy.mjs';
import { parseMd } from './parser.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(__dirname, '..', '..');
// Dual-path: prioriza content/articulos (canónico), fallback a articulos_completos
const candidates = [
  path.join(projectRoot, 'content', 'articulos'),
  path.join(projectRoot, 'articulos_completos'),
];
const srcDir = candidates.find(p => fs.existsSync(p)) || candidates[0];
const outDirs = [
  path.join(projectRoot, 'public', 'data'),
  // Fase 3 limpio: ya no escribe a data/ raíz (ver explorer limpio). Descomentar si necesitás compatibilidad temporal:
  // path.join(projectRoot, 'data'),
];
const outFiles = outDirs.map(d => path.join(d, 'reflexiones.json'));

const files = fs.readdirSync(srcDir).filter(f=> f.endsWith('.md'));
const items = files.map(f => parseMd(path.join(srcDir, f)));

// ordenar por fecha desc
items.sort((a,b)=> b.ts - a.ts);

// stats por mes
const byCat = {};
MESES.forEach(c=> byCat[c.id]=0);
items.forEach(i=> byCat[i.categoria]++);

console.log(`Total: ${items.length}`);
console.log('Por mes:', byCat);
console.log('Ejemplo:', items[0]);

const payload = JSON.stringify({
  generatedAt: new Date().toISOString(),
  total: items.length,
  categories: MESES.map(c=> ({ ...c, count: byCat[c.id] })),
  items
}, null, 2);

for (const outFile of outFiles) {
  fs.mkdirSync(path.dirname(outFile), { recursive: true });
  fs.writeFileSync(outFile, payload, 'utf-8');
  console.log(`✓ Escrito ${outFile} (${(fs.statSync(outFile).size/1024).toFixed(1)} KB)`);
}
console.log(`  srcDir: ${srcDir}`);

// Activos: content/ es fuente de verdad, public/ es derivado servido.
// Copia (no symlink: Windows) para no sincronizar a mano.
for (const dir of ['imagenes', 'audios']) {
  const from = path.join(projectRoot, 'content', dir);
  const to = path.join(projectRoot, 'public', dir);
  if (!fs.existsSync(from)) {
    console.log(`  (sin ${from}, se omite copia de ${dir})`);
    continue;
  }
  fs.mkdirSync(to, { recursive: true });
  fs.cpSync(from, to, { recursive: true });
  const count = fs.readdirSync(to).length;
  console.log(`✓ Copiado ${dir}: ${from} → ${to} (${count} entradas)`);
}
