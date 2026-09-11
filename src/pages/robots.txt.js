export async function GET({ site }) {
  // SITE se resuelve desde astro.config `site` (que a su vez lee env SITE).
  // Fallback demo para builds locales sin env.
  const base = (site?.toString() || process.env.SITE || 'https://reflexiones-demo.leobringasatlife.site').replace(/\/$/, '');
  const body = [
    'User-agent: *',
    'Allow: /',
    '',
    `# Sitemap absoluto (requerido por Google). Se genera con @astrojs/sitemap.`,
    `Sitemap: ${base}/sitemap-index.xml`,
    '',
  ].join('\n');
  return new Response(body, { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
}
