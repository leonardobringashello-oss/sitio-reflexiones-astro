import { describe, it, expect } from "vitest";
import { MESES, categoriaPorFecha } from "../scripts/builder/taxonomy.mjs";

describe("taxonomy", () => {
  it("tiene 12 meses", () => {
    expect(MESES).toHaveLength(12);
  });

  it("categoriaPorFecha mapea fecha ISO a id", () => {
    expect(categoriaPorFecha("2026-09-11")).toBe("2026-09");
  });

  it("fecha vacía cae a 2026-01", () => {
    expect(categoriaPorFecha("")).toBe("2026-01");
  });
});
