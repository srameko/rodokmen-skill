#!/usr/bin/env python3
"""Fronta hledání: předci, kterým chybí aspoň jeden rodič, seřazení od nejlevnějšího dalšího kroku.

Použití (z kořene projektu):  python3 -I -X utf8 tools/fronta.py [--vse]  -> výpis + pracovni/fronta.md
Body (vyšší = dřív):
  +3  jméno rodiče už je v datech (stačí najít křest nebo ho jen zapsat jako osobu)
  +2  narozen po 1784 (josefínské matriky: dům, rodiče, prarodiče)  /  +1 po 1750
  +2  známe číslo domu,  +1 známe obec narození
  +1  status doc (osoba je doložená)
  −5  rod uzavřený uživatelem – bez --vse se nevypisuje
Uzavřené rody: v `data/web.json` klíč "fronta_uzavrene": [čísla rodů 8–15], např. {"fronta_uzavrene": [12, 13]}.
Bez nové stopy je nehledej (nástroj v souboru nic nepřepisuje, takže ho aktualizace skillu neztratí).
Chybí-li jen jeden z rodičů (např. matka), osoba se do fronty zařadí taky.
"""
import json, os, re, sys
for _s in (sys.stdout, sys.stderr):   # UTF-8 výstup i na Windows bez -X utf8
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")


def nacti(cesta):
    try:
        with open(cesta, encoding="utf-8") as fh:
            return fh.read()
    except OSError as e:
        sys.exit(f"Nejde číst {cesta} ({e.strerror}). Spouštěj z kořene projektu.")


ns = {}
exec(nacti("data/osoby.py"), ns)
P, LINES = ns["P"], ns["LINES"]
try:
    UZAVRENE = {int(x) for x in json.loads(nacti("data/web.json")).get("fronta_uzavrene", [])}
except (ValueError, TypeError):
    sys.exit('data/web.json: "fronta_uzavrene" musí být seznam čísel rodů, např. [12, 13].')
except SystemExit:
    UZAVRENE = set()   # web.json nemusí existovat
vse = "--vse" in sys.argv
VELKE = "A-ZÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ"


def rod(k):
    return k >> (k.bit_length() - 4) if k >= 8 else None


def rok(o):
    t = (o.get("y", "") + " " + " ".join(o.get("f", [])))
    m = re.search(r"\*\s*(?:asi\s*)?(?:\d{1,2}\.\s*\d{1,2}\.\s*)?(1[5-9]\d\d)", t)
    return int(m.group(1)) if m else None


rodic_re = re.compile(rf"\b(syn|dcera)\s+(?:†\s*)?(?:domkáře|sedláka|mlynáře|chalupníka|kováře|pololáníka)?\s*([{VELKE}]\w+\s+[{VELKE}]\w+)")
misto_re = re.compile(rf"^\*\s*(?:asi\s*)?(?:\d{{1,2}}\.\s*\d{{1,2}}\.\s*)?\d{{4}}\s+[{VELKE}]")   # „* 1852 Obec“, tj. rok a za ním místo
radky = []
for k, o in P.items():
    if k < 2 or (2 * k in P and 2 * k + 1 in P):   # oba rodiče známe -> není co hledat
        continue
    r = rod(k)
    fakta = o.get("f", [])
    t = " ".join(fakta) + " " + o.get("note", "")
    b, duvod = 0, []
    if 2 * k not in P and 2 * k + 1 not in P:
        duvod.append("chybí oba rodiče")
    else:
        duvod.append("chybí " + ("otec" if 2 * k not in P else "matka"))
    m = rodic_re.search(t)
    if m:
        b += 3; duvod.append("rodič v datech: " + m.group(0))
    y = rok(o)
    if y and y >= 1784: b += 2; duvod.append("po 1784")
    elif y and y >= 1750: b += 1
    if re.search(r"čp\.\s*\d+", t): b += 2; duvod.append("dům")
    if any(misto_re.match(x) for x in fakta): b += 1
    if o.get("st") == "doc": b += 1
    if r in UZAVRENE:
        b -= 5
        if not vse: continue
    radky.append((b, k, o["n"], y or "", LINES.get(r, ("?",))[0] if r else "", "; ".join(duvod)))
radky.sort(key=lambda x: (-x[0], -(x[3] or 0)))
out = ["# Fronta hledání (tools/fronta.py)", "", "| body | č. | osoba | * | rod | proč |", "|---|---|---|---|---|---|"]
out += [f"| {b} | {k} | {n} | {y} | {r} | {d} |" for b, k, n, y, r, d in radky]
os.makedirs("pracovni", exist_ok=True)
with open("pracovni/fronta.md", "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(out) + "\n")
print(f"{len(radky)} osob na okraji (uzavřené rody {'zahrnuty' if vse else 'vynechány'}); zapsáno do pracovni/fronta.md")
for x in radky[:25]:
    print(x)
