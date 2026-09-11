// src/js/modules/filtering.js — Module Filtering (deep module)
// Interface: filteredItems(items, { activeCategory, searchQuery }): Item[]
// Return results, no DOM side effects. Testable sin browser.

/**
 * @param {Array} items - items de data/reflexiones.json
 * @param {Object} opts
 * @param {string} opts.activeCategory - 'all' | '2026-01' ...
 * @param {string} opts.searchQuery - texto libre (trim)
 * @returns {Array}
 */
export function filteredItems(items, { activeCategory = 'all', searchQuery = '' } = {}) {
  let out = items;
  if (activeCategory !== 'all') {
    out = out.filter((i) => i.categoria === activeCategory);
  }
  if (searchQuery) {
    const q = norm(searchQuery);
    out = out.filter(
      (i) =>
        norm(i.titulo).includes(q) ||
        norm(i.excerpt).includes(q) ||
        i.slug.toLowerCase().includes(q.toLowerCase()) ||
        (norm((i.versiculos || []).join(' ')).includes(q))
    );
  }
  return out;
}

function norm(s) {
  return (s || '')
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '');
}
