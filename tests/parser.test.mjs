import { describe, it, expect } from "vitest";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { parseMd } from "../scripts/builder/parser.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(__dirname, "..");

describe("parser", () => {
  it("parsea 3649.md (Conspiranoicos)", () => {
    const item = parseMd(path.join(projectRoot, "content", "articulos", "3649.md"));
    expect(item.titulo).toBe("Conspiranoicos");
    expect(item.fechaISO).toBe("2026-09-11");
    expect(item.categoria).toBe("2026-09");
    expect(item.imagenPath).toBe("imagenes/3649.png");
    expect(item.versiculos).toContain("Isaías 8:12");
  });
});
