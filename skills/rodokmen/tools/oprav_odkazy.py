"""Opraví v data/pribeh.md odkazy /osoba/<slug>/, kterým se po doplnění roku narození změnila adresa.
Spouštěj po `npm run data` (čte web/src/data/site.json). Mění jen odkazy s jednoznačnou náhradou."""
import re
slugs = set(re.findall(r'"slug": "([^"]+)"', open("web/src/data/site.json", encoding="utf8").read()))
p = open("data/pribeh.md", encoding="utf8").read()
for b in sorted(set(l for l in re.findall(r"\(/osoba/([^/)]+)/\)", p) if l not in slugs)):
    base = re.sub(r"-\d{4}$", "", b)
    cand = [s for s in slugs if s == base or re.fullmatch(re.escape(base) + r"-\d{4}", s)]
    print(b, "->", cand)
    if len(cand) == 1:
        p = p.replace(f"(/osoba/{b}/)", f"(/osoba/{cand[0]}/)")
open("data/pribeh.md", "w", encoding="utf8").write(p)
