#!/usr/bin/env python3
"""Fronta hledání: předci, kterým chybí rodiče, seřazení od nejlevnějšího dalšího kroku.

Použití (z kořene projektu):  python -I -X utf8 tools/fronta.py [--vse]  -> výpis + pracovni/fronta.md
Body (vyšší = dřív):
  +3  jméno rodiče už je v datech (stačí najít křest nebo ho jen zapsat jako osobu)
  +2  narozen po 1784 (josefínské matriky: dům, rodiče, prarodiče)  /  +1 po 1750
  +2  známe číslo domu,  +1 známe obec narození
  +1  status doc (osoba je doložená)
  −5  rod uzavřený uživatelem (viz UZAVRENE) – bez --vse se nevypisuje
"""
import re, sys
ns = {}
exec(open("data/osoby.py", encoding="utf8").read(), ns)
P, LINES = ns["P"], ns["LINES"]
UZAVRENE = set()          # čísla rodů (8–15), které uživatel uzavřel: bez nové stopy nehledat; seznam si uprav
vse = "--vse" in sys.argv

def rod(k):
    return k >> (k.bit_length() - 4) if k >= 8 else None

def rok(o):
    t = (o.get("y", "") + " " + " ".join(o.get("f", [])))
    m = re.search(r"\*\s*(?:asi\s*)?(?:\d{1,2}\.\s*\d{1,2}\.\s*)?(1[5-9]\d\d)", t)
    return int(m.group(1)) if m else None

rodic_re = re.compile(r"\b(syn|dcera)\s+(?:†\s*)?(?:domkáře|sedláka|mlynáře|chalupníka|kováře|pololáníka)?\s*([A-ZÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ]\w+\s+[A-ZÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ]\w+)")
radky = []
for k, o in P.items():
    if k < 2 or 2 * k in P or 2 * k + 1 in P:
        continue
    r = rod(k)
    t = " ".join(o.get("f", [])) + " " + o.get("note", "")
    b, duvod = 0, []
    m = rodic_re.search(t)
    if m:
        b += 3; duvod.append("rodič v datech: " + m.group(0))
    y = rok(o)
    if y and y >= 1784: b += 2; duvod.append("po 1784")
    elif y and y >= 1750: b += 1
    if re.search(r"čp\.\s*\d+", t): b += 2; duvod.append("dům")
    if re.search(r"\*\s*[^,;]*\b[A-ZÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ]", " ".join(o.get("f", []))): b += 1
    if o.get("st") == "doc": b += 1
    if r in UZAVRENE:
        b -= 5
        if not vse: continue
    radky.append((b, k, o["n"], y or "", LINES.get(r, ("?",))[0] if r else "", "; ".join(duvod)))
radky.sort(key=lambda x: (-x[0], -(x[3] or 0)))
out = ["# Fronta hledání (tools/fronta.py)", "", "| body | č. | osoba | * | rod | proč |", "|---|---|---|---|---|---|"]
out += [f"| {b} | {k} | {n} | {y} | {r} | {d} |" for b, k, n, y, r, d in radky]
open("pracovni/fronta.md", "w", encoding="utf8").write("\n".join(out) + "\n")
print(f"{len(radky)} osob na okraji (uzavřené rody {'zahrnuty' if vse else 'vynechány'}); zapsáno do pracovni/fronta.md")
for x in radky[:25]:
    print(x)
