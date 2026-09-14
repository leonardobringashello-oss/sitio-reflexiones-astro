// src/lib/seo.js — seoFor() (skill generador-seo-og). Misma regla que scripts/seo/check.mjs.
const SITE_NAME = 'Reflexiones diarias — Pr. Walter Escalante';
const FALLBACK_OG = 'og-image.png';
const OG_LOCALE = 'es_AR';
const OG_IMAGE_ALT_INDEX = 'Reflexiones diarias por Walter Escalante — biblioteca pastoral';
const OG_W = 1200;
const OG_H = 630;

export function seoForIndex(total) {
  const title = `Reflexiones — Biblioteca | Pr. Walter Escalante`;
  const description = `Biblioteca de reflexiones pastorales del Pr. Walter Escalante. Explora por mes, busca por tema y lee cada reflexión con contexto y versículo. (${total} reflexiones)`;
  return {
    title,
    description,
    ogImage: FALLBACK_OG,
    ogImageAlt: OG_IMAGE_ALT_INDEX,
    ogType: 'website',
    canonical: '/',
    jsonLd: {
      '@context': 'https://schema.org',
      '@type': 'WebSite',
      name: SITE_NAME,
      description,
      inLanguage: 'es-AR',
    },
  };
}

export function seoForItem(item) {
  const base = `${item.titulo} — ${SITE_NAME}`.slice(0, 65);
  const desc = (item.excerpt || item.contenido || item.titulo).slice(0, 160);
  const ogImage = item.imagenPath || FALLBACK_OG;
  const ogImageAlt = item.imagenPath ? `${item.titulo} — Reflexiones diarias` : OG_IMAGE_ALT_INDEX;
  return {
    title: base.length < 10 ? `${item.titulo} — ${SITE_NAME}` : base,
    description: desc,
    ogImage,
    ogImageAlt,
    ogType: 'article',
    canonical: `/reflexion/${item.slug}`,
    article: {
      publishedTime: item.fechaISO || undefined,
      modifiedTime: item.fechaISO || undefined,
      section: item.categoria || undefined,
      author: 'Walter Escalante',
    },
    jsonLd: {
      '@context': 'https://schema.org',
      '@type': 'Article',
      headline: item.titulo,
      datePublished: item.fechaISO || undefined,
      dateModified: item.fechaISO || undefined,
      author: { '@type': 'Person', name: 'Pr. Walter Escalante' },
      image: ogImage,
      description: desc,
      inLanguage: 'es-AR',
      publisher: { '@type': 'Organization', name: SITE_NAME },
    },
  };
}

export function escapeHtml(s) {
  if (s == null) return '';
  return String(s).replace(/[&<>"']/g, (m) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[m]));
}
