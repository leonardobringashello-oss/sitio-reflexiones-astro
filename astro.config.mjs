import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// Migración in-place Fase Astro: estático puro, sin adapter.
// Publish dir agnóstico: dist/ (Netlify / Cloudflare Pages / Vercel static).
export default defineConfig({
  output: 'static',
  outDir: 'dist',
  publicDir: 'public',
  trailingSlash: 'never',
  build: {
    inlineStylesheets: 'auto',
  },
  integrations: [
    sitemap({
      // site se define vía env SITE en CI; fallback local para build sin deploy
      // Se deja sin site fijo para no romper builds locales.
    }),
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
