import rss from "@astrojs/rss";
import { loadItems } from "../lib/items.js";

export async function GET(context) {
  const { items } = loadItems();
  return rss({
    title: "Reflexiones diarias — Pr. Walter Escalante",
    description: "Pensamientos, reflexiones y bosquejos del púlpito. Iglesia Restauración, Florencio Varela.",
    site: context.site ?? "https://prwalterescalante.com",
    items: items
      .filter((i) => i.fechaISO)
      .map((i) => ({
        title: i.titulo,
        pubDate: new Date(i.fechaISO),
        description: i.excerpt,
        link: `/reflexion/${i.slug}/`,
      })),
  });
}
