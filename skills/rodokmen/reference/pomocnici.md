# Pomocníci (subagenti) – pravidla a šablona zadání

Pomocník = další kopie Claude, která souběžně na pozadí hledá podle přesného zadání. Výsledky píše jen do
`pracovni/pom_<větev>/vysledky.md`, **nikdy do `data/`**. Hlavní model (ty) každý nález ověří na snímku (aspoň výřez
hlavního řádku, `tools/overit.py`) a teprve pak zapíše do dat, na web a do deníku. Základ je v `SKILL.md` (Pomocníci – šetrně); tady jsou podrobnosti.
Pravidla ze zkušeností jednoho rodinného projektu (autor: Michal Kos, MIT), upravená pro tento skill.

## Pravidla
- Pomocníky spouštěj na pozadí a řekni uživateli jednou větou, co běží a proč. Před velkým kolem, které stojí hodně kreditů, se uživatele zeptej (výjimku udělá jen jeho výslovné svolení).
- **Souběžně 2–4 pomocníci na různé větve.** Nástroje bez prohlížeče (`ebadatelna.py`, `aron_img.py`, `portafontium.py`) nekolidují.
  **Prohlížeč smí mít v jednu chvíli jen jeden pomocník**; ty ho mezitím nepoužívej nebo použij jinou záložku.
- Zadání musí být samostatné (pomocník nezná konverzaci): složka projektu, technické pasti (`reference/matriky.md`), přesná id knih, co je už doloženo
  (jména, data, domy), úkoly v pořadí od nejdůležitějšího a formát výsledku.
- **Síť jen přes brzdu.** Pomocník volá jen nástroje ve `tools/` (ty jdou přes `slusne.py`); na hlášku „zastavený“ skončí a ohlásí to. Žádné hromadné zkoušení adres ani čísel knih
  (procházení stovek id po sobě archiv bere jako zátěž a může počítač zablokovat); čísla knih hledej přes seznam knih obce nebo vyhledávání archivu.
- **Zákaz příkazů na pozadí a čekání** (sleep, hromadné stahování): pomocník se zasekne a nic neodevzdá. Ať píše do `vysledky.md` průběžně po každém nálezu.
- Zakaž pomocníkovi zapisovat do dat (`… svazek`, `zapis.py`); po návratu zkontroluj `git status data`.
- U neúspěchů chtěj **rozsah a co na snímcích skutečně bylo** (rok, první jméno na každém prohlédnutém snímku). „Nenalezeno“ od pomocníka je upozornění, ne důkaz.
- Ve vestavěném prohlížeči se občas objeví ověření robota. Pomocník ho **neobchází**; ohlásí, že se nedostal dál, a ty to vyřešíš s uživatelem.
- `aron_img.py`: úroveň **0 = plné rozlišení**, 2 = čtvrtina. ARON bývá hodiny nedostupný (stahování vyprší) – pak větev odlož.
- **Model podle jistoty vodítka.** Slepé prohledávání (rejstříky, první kolo) = levnější model (`sonnet`). Dobré vodítko bez potvrzení (křest bez sňatku rodičů,
  opakovaný kmotr, rejstřík ukazuje list) nebo těžký rukopis (18. století, slabé mikrofilmy) = silnější model. Slabý výsledek „nenalezeno“ neopakuj stejně, zkus silnější model s užším zadáním.
- **Ověřuj sám.** Čtení pomocníka vždy ověř na snímku (princip čtyř očí); pomocník nezná kontext (dvě rodiny stejného jména ve vsi, dva Janové na statku).

## Co se osvědčilo zadávat
- Osoba narozená po ~1925: sňatek rodičů v místě a letech kolem narození (katolické, evangelické, civilní matriky).
- Starší generace: narození (z věku ve sňatku), sňatek rodičů, úmrtí s věkem (uvádí narození a rodiče).
- Síť kmotrů (výstup `tools/kmotri.py` → křty dětí hledané rodiny; kmotr často ukáže rodinu matky).
- Ověření: „přečti znovu v plném rozlišení a potvrď“ u čtení jiného pomocníka.
- Po návratu: ověř, zapiš (`zapis.py`), deník, `kontrola.py`, nasadit web; pak případně další kolo (`tools/fronta.py` řekne, kdo je na řadě).

## Šablona zadání (SOA Praha, ARON a další nástroje bez prohlížeče)
```
Jsi pomocník při genealogickém výzkumu (soukromý rodokmen). Složka: <kořen projektu>
Python VŽDY `python3 -I -X utf8` (Windows: `python -I -X utf8`), ImageMagick `magick`/`convert`. Do data/ NIC NEZAPISUJ
– výsledky jen do pracovni/pom_<větev>/ (obrázky + vysledky.md).
Nástroje z kořene projektu: <např. tools/ebadatelna.py matriky "Obec" | info <id> | snimek <id> <sn> <out.jpg> [nahled]>
Síť jen přes tyto nástroje (brzda slusne.py); při hlášce „zastavený“ skonči a ohlas to. Žádné hromadné zkoušení adres.
Náhled jen na orientaci (roky); jména čti z plného rozlišení a výřezu (`magick in.jpg -crop WxH+X+Y -resize 2000x out.jpg`),
obrázek prohlédni nástrojem Read. Nejdřív rejstříky, pak kniha. Stahuj jen snímky, které čteš.
Doloženo: <osoby, data, čísla domů, rodiče>.
Knihy: <id – druh – roky – poznámka, kde je který rok>.
Úkoly (v pořadí): 1. … 2. … 3. …
Ke každému nálezu do vysledky.md: kniha, snímek, datum, úplný přepis (jména, stavy, domy, rodiče, prarodiče, kmotři/svědci),
„(?)“ u nejistot, souřadnice zápisu (zlomky 0–1). U neúspěchů rozsah a co tam bylo. Nic nevymýšlej. Na konci krátké shrnutí.
```
