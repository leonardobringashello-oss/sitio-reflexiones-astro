import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// Migración in-place Fase Astro: estático puro, sin adapter.
// Publish dir agnóstico: dist/ (Netlify / Cloudflare Pages / Vercel static).
// Sitio canónico: env SITE en CI/deploy, fallback demo para builds locales.
// Definir SITE=https://tudominio.com en Netlify/Vercel/Cloudflare para
// sitemap, RSS y canonical absolutos. Sin SITE el build igual funciona,
// pero el SEO sale relativo (solo válido para demo local).
const SITE = (process.env.SITE || 'https://reflexiones-demo.leobringasatlife.site').replace(/\/$/, '');
// Base-path para GitHub Pages (project pages sirven en subruta).
// Local: PAGES_BASE no definido -> '/' (sin cambios). CI: PAGES_BASE=/sitio-reflexiones-astro.
const BASE_RAW = (process.env.PAGES_BASE || '/').trim();
const BASE = BASE_RAW === '/' ? '/' : `/${BASE_RAW.replace(/^\/+|\/+$/g, '')}`;
export default defineConfig({
  site: SITE,
  base: BASE,
  output: 'static',
  outDir: 'dist',
  publicDir: 'public',
  trailingSlash: 'never',
  build: {
    inlineStylesheets: 'auto',
  },
  integrations: [
    sitemap(),
  ],
  vite: {
    // content/articulos fuera de src: permitir import FS directo en loaders
    server: {
      fs: {
        allow: ['..'],
      },
    },
  },
});
