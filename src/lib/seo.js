// src/lib/seo.js — seoFor() (skill generador-seo-og). Misma regla que scripts/seo/check.mjs.
const SITE_NAME = 'Biblioteca Reflexiones';
const FALLBACK_OG = 'imagenes/logos/logo-we.webp';

export function seoForIndex(total) {
  const title = `Reflexiones — Biblioteca | Pr. Walter Escalante`;
  const description = `Biblioteca de reflexiones pastorales del Pr. Walter Escalante. Explora por mes, busca por tema y lee cada reflexión con contexto y versículo. (${total} reflexiones)`;
  return { title, description, ogImage: FALLBACK_OG, canonical: '/' };
}

export function seoForItem(item) {
  const base = `${item.titulo} — ${SITE_NAME}`.slice(0, 65);
  const desc = (item.excerpt || item.contenido || item.titulo).slice(0, 160);
  const ogImage = item.imagenPath || FALLBACK_OG;
  return {
    title: base.length < 10 ? `${item.titulo} — ${SITE_NAME}` : base,
    description: desc,
    ogImage,
    canonical: `/reflexion/${item.slug}`,
    jsonLd: {
      '@context': 'https://schema.org',
      '@type': 'Article',
      headline: item.titulo,
      datePublished: item.fechaISO || undefined,
      author: { '@type': 'Person', name: 'Walter Escalante' },
      image: ogImage,
      description: desc,
    },
  };
}

export function escapeHtml(s) {
  if (s == null) return '';
  return String(s).replace(/[&<>"']/g, (m) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[m]));
}
