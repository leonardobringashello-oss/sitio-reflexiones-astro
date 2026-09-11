import { describe, it, expect } from "vitest";
import Fuse from "fuse.js";

const sample = [
  { titulo: "Conspiranoicos", excerpt: "teorías conspirativas", slug: "3649", versiculos: ["Isaías 8:12"] },
  { titulo: "Inconmensurable", excerpt: "deudas y facturas", slug: "inconmensurable", versiculos: ["Mateo 9:21"] },
];

const fuse = new Fuse(sample, {
  keys: [
    { name: "titulo", weight: 2 },
    { name: "versiculos", weight: 1.5 },
    { name: "excerpt", weight: 1 },
  ],
  threshold: 0.35,
  ignoreDiacritics: true,
  ignoreLocation: true,
  minMatchCharLength: 2,
});

describe("search", () => {
  it("tolera typos", () => {
    expect(fuse.search("conspiranoikos")[0].item.titulo).toBe("Conspiranoicos");
  });

  it("ignora tildes", () => {
    expect(fuse.search("Isaias")[0].item.titulo).toBe("Conspiranoicos");
  });

  it("encuentra por versículo", () => {
    expect(fuse.search("Mateo 9")[0].item.titulo).toBe("Inconmensurable");
  });
});
