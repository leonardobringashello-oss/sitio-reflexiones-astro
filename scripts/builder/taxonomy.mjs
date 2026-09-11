// scripts/builder/taxonomy.mjs — Module Taxonomy (deep module)
// Interface: categoriaPorFecha(fechaISO): CategoryId
// Leverage: un único lugar para MESES; locality si se agrega 2026-09
export const MESES = [
  { id: '2026-01', label: 'Enero 2026', short: 'Enero', mes: 1 },
  { id: '2026-02', label: 'Febrero 2026', short: 'Febrero', mes: 2 },
  { id: '2026-03', label: 'Marzo 2026', short: 'Marzo', mes: 3 },
  { id: '2026-04', label: 'Abril 2026', short: 'Abril', mes: 4 },
  { id: '2026-05', label: 'Mayo 2026', short: 'Mayo', mes: 5 },
  { id: '2026-06', label: 'Junio 2026', short: 'Junio', mes: 6 },
  { id: '2026-07', label: 'Julio 2026', short: 'Julio', mes: 7 },
  { id: '2026-08', label: 'Agosto 2026', short: 'Agosto', mes: 8 },
  { id: '2026-09', label: 'Septiembre 2026', short: 'Septiembre', mes: 9 },
  { id: '2026-10', label: 'Octubre 2026', short: 'Octubre', mes: 10 },
  { id: '2026-11', label: 'Noviembre 2026', short: 'Noviembre', mes: 11 },
  { id: '2026-12', label: 'Diciembre 2026', short: 'Diciembre', mes: 12 },
];

export function categoriaPorFecha(fechaISO) {
  if (!fechaISO) return '2026-01';
  const m = fechaISO.slice(5, 7); // "08"
  const id = `2026-${m}`;
  return MESES.some((x) => x.id === id) ? id : '2026-01';
}

export function getCategoryShort(categoria, categories = MESES) {
  const found = categories.find((c) => c.id === categoria);
  return found ? found.short : categoria || '';
}
