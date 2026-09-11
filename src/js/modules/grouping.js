// src/js/modules/grouping.js — agrupa items por categoría para sidebar
/**
 * @param {Array} categories - DATA.categories (MESES)
 * @param {Array} items - ya filtrados
 * @returns {Array<{cat, items}>} ordenado desc por id (más reciente primero)
 */
export function groupByCategory(categories, items) {
  const ordered = [...categories].sort((a, b) => b.id.localeCompare(a.id));
  return ordered.map((cat) => ({
    cat,
    items: items.filter((i) => i.categoria === cat.id),
  }));
}
