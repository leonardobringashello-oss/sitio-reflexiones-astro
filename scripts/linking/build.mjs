#!/usr/bin/env node
// scripts/linking/build.mjs — genera public/data/relaciones.json (skill enlazado-cruzado)
// Interface: node scripts/linking/build.mjs [--umbral 3]
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(__dirname, '..', '..');
const candidates = [path.join(projectRoot, 'public', 'data', 'reflexiones.json'), path.join(projectRoot, 'data', 'reflexiones.json')];
const dataPath = candidates.find(p => fs.existsSync(p));
if (!dataPath) { console.error('No se encontró reflexiones.json'); process.exit(1); }
const data = JSON.parse(fs.readFileSync(dataPath, 'utf-8'));

const idx = process.argv.indexOf('--umbral');
const umbral = idx !== -1 ? Number(process.argv[idx+1]) : 3;

// Señales mínimas: si no hay implementación completa, genera stub vacío con umbral documentado
// TODO: implementar scoring real (versiculos*3 + libro*2 + tema*2 ...) ver docs/architecture.md
const relaciones = {};
for (const it of data.items) {
  relaciones[it.slug] = [];
}

const out = {
  generatedAt: new Date().toISOString(),
  umbral,
  note: 'Stub Fase 2 — implementar scoring enlazado-cruzado/SKILL.md:52 en Fase 3',
  relaciones,
};

const outPaths = [path.join(projectRoot, 'public', 'data', 'relaciones.json')];
for (const p of outPaths) {
  fs.mkdirSync(path.dirname(p), { recursive: true });
  fs.writeFileSync(p, JSON.stringify(out, null, 2), 'utf-8');
  console.log(`✓ Escrito ${p} (${Object.keys(relaciones).length} slugs, umbral ${umbral})`);
}
