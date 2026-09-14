// src/lib/base.js — prefijo de base-path para subruta (GitHub Pages) o raíz.
// En local PAGES_BASE no se define y todo queda igual que antes ('/').
// En CI se define PAGES_BASE=/sitio-reflexiones-astro y los links salen con prefijo.
const RAW = (typeof import.meta !== 'undefined' && import.meta.env?.BASE_URL) || '/';

// '' en raíz, '/subruta' en Pages (sin slash final).
export const SITE_BASE = String(RAW).replace(/\/$/, '');

/** '/x' -> '/x' en raíz, '/subruta/x' en Pages. Acepta con o sin slash inicial. */
export function withBase(p = '/') {
  const s = String(p || '/');
  return `${SITE_BASE}${s.startsWith('/') ? s : `/${s}`}`;
}

/** '/' en raíz, '/subruta/' en Pages. Para concatenar en JS client-side. */
export function basePrefix() {
  return `${SITE_BASE}/`;
}
