import json
j=json.loads(open("data/reflexiones.json",encoding="utf-8").read())
item=next(x for x in j["items"] if x["slug"]=="quien-sos-2")
paras=[p.strip() for p in item["contenido"].split("\n\n")]
def ends(s):
    s=s.strip()
    if not s: return True
    TERMINATORS=set(list(".?!:…\"”'»)"))
    last=s[-1]
    if last in TERMINATORS: return True
    if s.endswith("...") or s.endswith("…"): return True
    if len(s)>=2 and s[-2] in ".?!" and last in "\"”'»": return True
    return False

for i,p in enumerate(paras):
    print(f"{i} ends={ends(p)} last={repr(p[-1])} -> {repr(p[:90])}")
