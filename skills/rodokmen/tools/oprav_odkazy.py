#!/usr/bin/env python3
"""Opraví v data/pribeh.md odkazy /osoba/<slug>/, kterým se po doplnění roku narození změnila adresa.

Použití (z kořene projektu, po `npm run data`):  python3 -I -X utf8 tools/oprav_odkazy.py
Čte web/src/data/site.json; mění jen odkazy s jednoznačnou náhradou a soubor přepíše jen když se něco změnilo.
"""
import json, re, sys
for _s in (sys.stdout, sys.stderr):   # UTF-8 výstup i na Windows bez -X utf8
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")
try:
    with open("web/src/data/site.json", encoding="utf-8") as fh:
        slugs = {o["slug"] for o in json.load(fh)["people"].values() if isinstance(o, dict) and o.get("slug")}
except (OSError, ValueError, KeyError, AttributeError) as e:
    sys.exit(f"Nejde číst web/src/data/site.json ({e}). Spusť nejdřív `cd web; npm run data` a spouštěj z kořene projektu.")
try:
    with open("data/pribeh.md", encoding="utf-8") as fh:
        puvodni = p = fh.read()
except OSError:
    sys.exit("Soubor data/pribeh.md neexistuje – není co opravovat.")
for b in sorted({l for l in re.findall(r"\(/osoba/([^/)]+)/\)", p) if l not in slugs}):
    base = re.sub(r"-\d{4}$", "", b)
    cand = [s for s in slugs if s == base or re.fullmatch(re.escape(base) + r"-\d{4}", s)]
    print(b, "->", cand)
    if len(cand) == 1:
        p = p.replace(f"(/osoba/{b}/)", f"(/osoba/{cand[0]}/)")
if p != puvodni:
    with open("data/pribeh.md", "w", encoding="utf-8", newline="\n") as fh:
        fh.write(p)
    print("data/pribeh.md opraven")
else:
    print("Beze změny.")
