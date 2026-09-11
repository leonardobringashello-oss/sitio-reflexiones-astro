#!/usr/bin/env node
// scripts/seo/check.mjs — valida SEO/OG para items de reflexiones.json (skill generador-seo-og)
// Interface: node scripts/seo/check.mjs [--slug X]

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(__dirname, '..', '..');
const candidates = [path.join(projectRoot, 'public', 'data', 'reflexiones.json'), path.join(projectRoot, 'data', 'reflexiones.json')];
const dataPath = candidates.find(p => fs.existsSync(p));
if (!dataPath) { console.error('No se encontró reflexiones.json'); process.exit(1); }
const data = JSON.parse(fs.readFileSync(dataPath, 'utf-8'));
const slug = process.argv.includes('--slug') ? process.argv[process.argv.indexOf('--slug')+1] : null;
const items = slug ? data.items.filter(i=>i.slug===slug) : data.items;
let fails = 0;
for (const it of items) {
  const title = `${it.titulo} — Biblioteca Reflexiones`;
  const desc = it.excerpt || it.contenido.slice(0,150);
  if (title.length < 10 || title.length > 65) { console.warn(`[WARN] title len ${title.length}: ${it.slug}`); fails++; }
  if (!desc || desc.length < 30) { console.warn(`[WARN] desc corta: ${it.slug}`); fails++; }
  if (!it.imagenPath && !fs.existsSync(path.join(projectRoot, 'public', 'imagenes', 'logos', 'logo-we.webp'))) { console.warn(`[WARN] sin imagen ni fallback: ${it.slug}`); }
}
console.log(`SEO check: ${items.length} items, ${fails} warnings`);
if (fails>0) process.exit(0);
