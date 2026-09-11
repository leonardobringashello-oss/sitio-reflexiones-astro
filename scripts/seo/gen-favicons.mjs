#!/usr/bin/env node
// scripts/seo/gen-favicons.mjs — genera el set favicon desde el logo versionado.
// Fuente: content/imagenes/logos/logo-we.webp (192x192, fuente de verdad).
// Salida: public/favicon.{ico,svg}, favicon-16/32.png, apple-touch-icon.png,
//   android-chrome 192/512, site.webmanifest. Estilo sencillo.
// Uso: node scripts/seo/gen-favicons.mjs

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, '..', '..');
const SRC = path.join(root, 'content', 'imagenes', 'logos', 'logo-we.webp');
const PUB = path.join(root, 'public');

const ACCENT = '#000000';
const BG = '#f5f5f5';

// SVG sencillo: pastilla redondeada color acento + iniciales WE (mismo
// fallback que usa el brand en index.astro cuando el logo no carga).
const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="${ACCENT}"/><text x="32" y="42" font-family="Georgia, serif" font-size="28" font-weight="bold" fill="${BG}" text-anchor="middle">WE</text></svg>\n`;

const ICO_SIDES = [16, 32, 48];

// ICO con entradas PNG comprimidas (válido Vista+): cabecera + dir + datos.
function pngsToIco(pngBuffers) {
  const count = pngBuffers.length;
  const header = Buffer.alloc(6);
  header.writeUInt16LE(0, 0);
  header.writeUInt16LE(1, 2);
  header.writeUInt16LE(count, 4);
  let off = 6 + 16 * count;
  const entries = pngBuffers.map((buf, i) => {
    const side = ICO_SIDES[i];
    const e = Buffer.alloc(16);
    e.writeUInt8(side >= 256 ? 0 : side, 0);
    e.writeUInt8(side >= 256 ? 0 : side, 1);
    e.writeUInt8(0, 2);
    e.writeUInt8(0, 3);
    e.writeUInt16LE(1, 4);
    e.writeUInt16LE(32, 6);
    e.writeUInt32LE(buf.length, 8);
    e.writeUInt32LE(off, 12);
    off += buf.length;
    return e;
  });
  return Buffer.concat([header, ...entries, ...pngBuffers]);
}

const src = sharp(SRC);
const meta = await src.metadata();
console.log(`Fuente: ${SRC} (${meta.width}x${meta.height} ${meta.format})`);

fs.writeFileSync(path.join(PUB, 'favicon.svg'), svg);
console.log('✓ public/favicon.svg (WE sencillo, fondo negro)');

const pngs = {};
for (const side of [16, 32, 48, 180, 192, 512]) {
  pngs[side] = await sharp(SRC).resize(side, side, { fit: 'cover' }).png().toBuffer();
}
fs.writeFileSync(path.join(PUB, 'favicon-16x16.png'), pngs[16]);
fs.writeFileSync(path.join(PUB, 'favicon-32x32.png'), pngs[32]);
fs.writeFileSync(path.join(PUB, 'apple-touch-icon.png'), pngs[180]);
fs.writeFileSync(path.join(PUB, 'android-chrome-192x192.png'), pngs[192]);
fs.writeFileSync(path.join(PUB, 'android-chrome-512x512.png'), pngs[512]);
fs.writeFileSync(path.join(PUB, 'favicon.ico'), pngsToIco([pngs[16], pngs[32], pngs[48]]));
console.log('✓ PNGs 16/32/180/192/512 + favicon.ico (16+32+48)');

const manifest = {
  name: 'Reflexiones diarias — Pr. Walter Escalante',
  short_name: 'Reflexiones',
  start_url: '/',
  display: 'standalone',
  background_color: '#000000',
  theme_color: '#000000',
  icons: [
    { src: '/android-chrome-192x192.png', sizes: '192x192', type: 'image/png' },
    { src: '/android-chrome-512x512.png', sizes: '512x512', type: 'image/png' },
  ],
};
fs.writeFileSync(path.join(PUB, 'site.webmanifest'), JSON.stringify(manifest, null, 2) + '\n');
console.log('✓ public/site.webmanifest');
