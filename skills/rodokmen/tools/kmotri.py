#!/usr/bin/env python3
"""Síť kmotrů a svědků: kdo se opakuje u více zápisů (kmotři bývali příbuzní).

Použití (z kořene projektu):  python3 -I -X utf8 tools/kmotri.py  -> výpis + pracovni/kmotri.md
Z každého `shrnuti` v data/zaznamy.json vezme část od slova Kmotr/Kmotři/Svědek/Svědci/Družba (do konce věty)
a vytáhne jména „Jméno Příjmení“. Příjmení sjednotí na mužský tvar (‑ová → ‑), aby se potkali muži i ženy.
Vypíše příjmení, která se objeví u ≥ 2 zápisů, a u nich zápisy, obce a role.
"""
import json, os, re, sys
from collections import defaultdict
for _s in (sys.stdout, sys.stderr):   # UTF-8 výstup i na Windows bez -X utf8
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")
try:
    with open("data/zaznamy.json", encoding="utf-8") as fh:
        Z = json.load(fh)
except (OSError, ValueError) as e:
    sys.exit(f"Nejde číst data/zaznamy.json ({e}). Spouštěj z kořene projektu.")
Z = Z if isinstance(Z, list) else list(Z.values())
VELKE = "A-ZÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ"
jmeno = re.compile(rf"\b([{VELKE}][a-záčďéěíňóřšťúůýž]+)\s+(?:roz\.\s+)?([{VELKE}][a-záčďéěíňóřšťúůýž]+)")
role = re.compile(r"(Kmotr\w*|kmotr\w*|Svěd\w*|svěd\w*|Družb\w*|družb\w*|Porodní bab\w*)[^.]*", re.S)
KRESTNI = set("Josef Jan Václav Tomáš Vojtěch Jakub Matěj František Jiří Martin Ludmila Anna Marie Marianna Kateřina Barbora Dorota Alžběta Rozálie Rosalie Magdalena Ludmila Karel Antonín Ondřej Pavel Petr Matouš Šimon Vít Lukáš Mikuláš Kristián Adam Eva Terezie Veronika Johana Josefa Františka Markéta Ignác Bernard Augustin Leopold Filip Prokop Bartoloměj Řehoř Štěpán Emanuel Wenzel Joseph Johann".split())
NEJMENA = {"Horní", "Dolní", "Nový", "Nové", "Malá", "Velká", "Svatý", "Panna", "Čteno", "Ověřeno"}

def zaklad(p):
    for a, b in (("ová", ""), ("á", "ý")):
        if p.endswith(a) and len(p) > 4:
            return p[: -len(a)] + b
    return p

vyskyt = defaultdict(list)
for z in Z:
    if not isinstance(z, dict) or "klic" not in z:
        continue
    for m in role.finditer(z.get("shrnuti", "")):
        usek = m.group(0)[len(m.group(1)):]   # jména hledáme až za slovem Kmotr/Svědek (jinak by se spojilo se jménem)
        for j, p in jmeno.findall(usek):
            if j in NEJMENA or p in NEJMENA or p in KRESTNI:
                continue
            vyskyt[zaklad(p)].append((z["klic"], f"{j} {p}", m.group(1).lower()[:6]))
rad = sorted(((p, v) for p, v in vyskyt.items() if len({k for k, _, _ in v}) >= 2), key=lambda x: -len({k for k, _, _ in x[1]}))
out = ["# Síť kmotrů a svědků (tools/kmotri.py)", ""]
for p, v in rad:
    out.append(f"## {p} – {len({k for k, _, _ in v})} zápisů")
    out += [f"- {kdo} ({r}) – {k}" for k, kdo, r in v]
    out.append("")
os.makedirs("pracovni", exist_ok=True)
with open("pracovni/kmotri.md", "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(out) + "\n")
print(len(rad), "příjmení u ≥ 2 zápisů; pracovni/kmotri.md")
for p, v in rad[:40]:
    print(p, len({k for k, _, _ in v}), sorted({k.split("_")[0] for k, _, _ in v}))
