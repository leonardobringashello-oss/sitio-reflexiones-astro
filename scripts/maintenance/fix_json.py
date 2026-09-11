import json, re

path = "data/reflexiones.json"
j = json.loads(open(path, encoding="utf-8").read())

TERMINATORS = set(list(".?!:…\"”'»)"))  # valid ending chars

def ends_with_terminator(s):
    s = s.strip()
    if not s:
        return True
    last = s[-1]
    if last in TERMINATORS:
        return True
    if s.endswith("..."):
        return True
    # ends with quote after terminator like .", ?"
    if len(s) >= 2 and s[-2] in ".?!" and last in "\"”'»":
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
        if cur in [".", ",", ":", ";", "!", "?", "\"", "'", "”", "“", "·"]:
            if fixed:
                if cur == ".":
                    fixed[-1] = fixed[-1].rstrip() + "."
                else:
                    fixed[-1] = fixed[-1] + cur
            else:
                fixed.append(cur)
            i += 1
            continue
        # if current is single word without terminator and next exists, merge
        if not ends_with_terminator(cur) and i + 1 < len(paras):
            nxt = paras[i + 1].strip()
            if nxt == ".":
                fixed.append(cur + ".")
                i += 2
                continue
            # merge cur + nxt
            merged = cur + " " + nxt
            # replace next with merged and advance
            paras[i + 1] = merged
            i += 1
            continue
        else:
            fixed.append(cur)
            i += 1
    return "\n\n".join(fixed)

# test on mi-dios and entrenamiento-3
for slug in ["mi-dios", "entrenamiento-3"]:
    item = next(x for x in j["items"] if x["slug"] == slug)
    before = len(item["contenido"].split("\n\n"))
    new = fix_content(item["contenido"])
    after = len(new.split("\n\n"))
    print(f"{slug}: {before} -> {after}")
    for idx, p in enumerate(new.split("\n\n")[:8]):
        print(idx, repr(p[:220]))
    print("---")

# test on quien-sos-2 should stay similar
item = next(x for x in j["items"] if x["slug"] == "quien-sos-2")
before = len(item["contenido"].split("\n\n"))
new = fix_content(item["contenido"])
print(f"quien-sos-2: {before} -> {len(new.split(chr(10)+chr(10)))}")
print("UNCHANGED?", before == len(new.split("\n\n")))
