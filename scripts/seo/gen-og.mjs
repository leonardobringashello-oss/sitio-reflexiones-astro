#!/usr/bin/env node
// scripts/seo/gen-og.mjs — genera la imagen Open Graph del sitio (1200x630).
// Estilo sencillo con los colores del sitio. Salida: public/og-image.png
// (en raíz de public/ para que NO la ignore .gitignore como public/imagenes).
// Uso: node scripts/seo/gen-og.mjs

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, '..', '..');
const OUT = path.join(root, 'public', 'og-image.png');

const W = 1200;
const H = 630;

const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
  <rect width="${W}" height="${H}" fill="#000000"/>
  <rect x="0" y="0" width="28" height="${H}" fill="#f5f5f5"/>
  <rect x="28" y="0" width="6" height="${H}" fill="#3d3d3d"/>
  <circle cx="170" cy="315" r="86" fill="#f5f5f5"/>
  <text x="170" y="343" font-family="Georgia, 'Times New Roman', serif" font-size="64" font-weight="bold" fill="#000000" text-anchor="middle">WE</text>
  <text x="300" y="290" font-family="Georgia, 'Times New Roman', serif" font-size="84" font-weight="bold" fill="#f5f5f5">Reflexiones diarias</text>
  <text x="302" y="360" font-family="Georgia, 'Times New Roman', serif" font-size="44" fill="#b3b3b3">por Walter Escalante</text>
  <rect x="302" y="400" width="120" height="5" fill="#f5f5f5"/>
  <text x="302" y="450" font-family="Verdana, sans-serif" font-size="30" fill="#8a8a8a">Biblioteca · Lectura y audio</text>
</svg>`;

await sharp(Buffer.from(svg)).png().toFile(OUT);
const kb = (fs.statSync(OUT).size / 1024).toFixed(1);
console.log(`✓ public/og-image.png (${W}x${H}, ${kb} KB)`);
