import json, re

path = "data/reflexiones.json"
data = json.loads(open(path, encoding="utf-8").read())

def ends_with_terminator(s):
    s = s.strip()
    if not s:
        return True
    # strip trailing markdown emphasis
    t = s.rstrip()
    # remove trailing * and _ and whitespace
    while t and t[-1] in "*_":
        t = t[:-1].rstrip()
    if not t:
        return True
    last = t[-1]
    if last in ".?!:…\"”'»)":
        return True
    if t.endswith("..."):
        return True
    if len(t) >= 2 and t[-2] in ".?!" and last in "\"”'»":
        return True
    return False

def fix_content(text):
    paras = [p.strip() for p in text.split("\n\n")]
    paras = [p for p in paras if p != ""]
    fixed = []
    i = 0
    while i < len(paras):
        cur = paras[i].strip()
        # single punctuation alone
        if cur in [".", ",", ":", ";", "!", "?", "\"", "'", "”", "“", "·", "-", "—"]:
            if fixed:
                if cur in [".", ",", ":", ";", "!", "?", "·"]:
                    # attach without extra space if previous doesn't end with space
                    fixed[-1] = fixed[-1].rstrip() + cur
                    # if there is following space content already?
                else:
                    fixed[-1] = fixed[-1] + cur
            else:
                fixed.append(cur)
            i += 1
            continue

        if not ends_with_terminator(cur) and i + 1 < len(paras):
            nxt = paras[i+1].strip()
            # if nxt is punctuation alone, attach correctly
            if nxt in [".", ",", ":", ";", "!", "?"]:
                fixed.append(cur.rstrip() + nxt)
                i += 2
                continue
            if nxt and nxt[0] in ",.;:!?":
                # punctuation at start of next
                fixed.append(cur.rstrip() + " " + nxt.lstrip())
                i += 2
                continue
            # normal merge with space
            merged = cur + " " + nxt
            paras[i+1] = merged
            i += 1
            continue
        else:
            fixed.append(cur)
            i += 1
    # also ensure each paragraph in fixed ends with terminator; already by construction they do except last maybe
    # if last paragraph doesn't end with .?! add dot
    if fixed and not ends_with_terminator(fixed[-1]):
        # check if last char is not punctuation at all, add dot
        if fixed[-1][-1] not in ".?!":
            fixed[-1] = fixed[-1].rstrip() + "."
    return "\n\n".join(fixed)

changed = 0
for item in data["items"]:
    old = item["contenido"]
    new = fix_content(old)
    if new != old:
        changed += 1
        item["contenido"] = new
        # also update excerpt? excerpt is first 90 chars of contenido, recompute
        # keep excerpt as first paragraph plain? recompute simply
        first_para = new.split("\n\n")[0]
        # strip markdown for excerpt? keep simple
        excerpt = re.sub(r"\*\*(.+?)\*\*", r"\1", first_para)
        excerpt = re.sub(r"\*(.+?)\*", r"\1", excerpt)
        excerpt = excerpt.replace("\n", " ").strip()
        if len(excerpt) > 180:
            excerpt = excerpt[:177] + "…"
        item["excerpt"] = excerpt
        # update palabras and lecturaMin
        words = len(re.findall(r"\w+", new))
        item["palabras"] = words
        item["lecturaMin"] = max(1, round(words / 200))

open(path, "w", encoding="utf-8").write(json.dumps(data, ensure_ascii=False, indent=2))
print(f"Fixed {changed}/{len(data['items'])} items")
# quick verify
for slug in ["mi-dios", "entrenamiento-3", "quien-sos-2"]:
    it = next(x for x in data["items"] if x["slug"] == slug)
    paras = it["contenido"].split("\n\n")
    print(f"\n{slug}: {len(paras)} paras")
    bad = []
    for p in paras:
        if not ends_with_terminator(p):
            bad.append(repr(p[:80]))
    print(f" bad endings: {len(bad)}", bad[:3])
