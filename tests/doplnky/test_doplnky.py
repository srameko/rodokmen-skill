"""Testy tools/fronta.py, tools/kmotri.py a tools/oprav_odkazy.py (nástroje nad daty projektu).

Z kořene repozitáře:
  python3 -I tests/doplnky/test_doplnky.py
  (Windows: python -I -X utf8 tests/doplnky/test_doplnky.py)
Nic nestahuje: v dočasné složce se postaví malý projekt (data/, web/src/data/) a nástroje se spustí jako v projektu.
"""
import json, os, subprocess, sys, tempfile

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TOOLS = os.path.join(REPO, "skills", "rodokmen", "tools")
vysledky = []


def ok(nazev, podminka, detail=""):
    vysledky.append(bool(podminka))
    print(("OK   " if podminka else "CHYBA"), nazev, "" if podminka else detail)


def projekt(osoby=None, zaznamy=None, web=None, site=None, pribeh=None):
    d = tempfile.mkdtemp(prefix="doplnky_")
    for p in ("data", "pracovni", os.path.join("web", "src", "data")):
        os.makedirs(os.path.join(d, p))
    def zapis(rel, obsah):
        with open(os.path.join(d, rel), "w", encoding="utf-8", newline="") as fh:
            fh.write(obsah)
    if osoby is not None: zapis("data/osoby.py", osoby)
    if zaznamy is not None: zapis("data/zaznamy.json", json.dumps(zaznamy, ensure_ascii=False))
    if web is not None: zapis("data/web.json", json.dumps(web))
    if site is not None: zapis("web/src/data/site.json", json.dumps(site))
    if pribeh is not None: zapis("data/pribeh.md", pribeh)
    return d


def spust(d, nastroj, *args):
    r = subprocess.run([sys.executable, "-I", "-X", "utf8", os.path.join(TOOLS, nastroj), *args], cwd=d, capture_output=True, text=True, encoding="utf-8")
    return r.returncode, r.stdout, r.stderr


OSOBY = """P = {
 1: {'n': 'Petr Novák', 'y': '* 1980', 'f': ['* 1980 Pardubice']},
 2: {'n': 'Josef Novák', 'y': '* 1952', 'f': ['* 1952 Holice']},
 3: {'n': 'Eva Dvořáková', 'y': '* 1955', 'f': ['* 1955 Chrudim']},
 4: {'n': 'Jan Novák', 'y': '* 1900', 'f': ['* 14. 2. 1900 Holice čp. 112', 'syn Václava Nováka'], 'st': 'doc'},
 5: {'n': 'Marie Králová', 'y': '* 1902', 'f': ['* 1902']},
 8: {'n': 'Václav Novák', 'y': '* 1870', 'f': ['* 1870 Holice']},
}
LINES = {8: ('Novákovi',)}
"""
d = projekt(osoby=OSOBY)
k, out, err = spust(d, "fronta.py")
ok("fronta: doběhne", k == 0, err)
radky = open(os.path.join(d, "pracovni", "fronta.md"), encoding="utf-8").read()
ok("fronta: osoba bez obou rodičů je ve frontě", "| 5 | Marie Králová" in radky and "| 4 | Jan Novák" in radky, radky)
ok("fronta: osoba s oběma rodiči (1 má 2 a 3) ve frontě není", "| 1 | Petr" not in radky, radky)
ok("fronta: u osoby bez obou rodičů je důvod „chybí oba rodiče“", "chybí oba rodiče" in radky, radky)
ok("fronta: zápis má konce řádků LF", b"\r\n" not in open(os.path.join(d, "pracovni", "fronta.md"), "rb").read())

jen_otec = OSOBY.replace(" 5: {", " 10: {'n': 'Otec Jana', 'f': ['* 1870']},\n 5: {")
d = projekt(osoby=jen_otec)
spust(d, "fronta.py")
radky = open(os.path.join(d, "pracovni", "fronta.md"), encoding="utf-8").read()
ok("fronta: osoba s jedním známým rodičem se zařadí (chybí matka)", "| 5 |" in radky and "chybí matka" in radky, radky)

d = projekt(osoby=OSOBY.replace(" 8: {", " 9: {'n': 'Matka Jana', 'f': ['* 1870']},\n 8: {"))
spust(d, "fronta.py")
ok("fronta: s oběma rodiči (4 má 8 a 9) není ve frontě", "| 4 | Jan Novák" not in open(os.path.join(d, "pracovni", "fronta.md"), encoding="utf-8").read())

d = projekt(osoby=OSOBY, web={"fronta_uzavrene": [8]})
k, out, err = spust(d, "fronta.py")
ok("fronta: uzavřený rod z data/web.json se vynechá", "Václav Novák" not in open(os.path.join(d, "pracovni", "fronta.md"), encoding="utf-8").read(), out)
k, out, err = spust(d, "fronta.py", "--vse")
ok("fronta: --vse uzavřený rod ukáže", "Václav Novák" in open(os.path.join(d, "pracovni", "fronta.md"), encoding="utf-8").read())
d = projekt(osoby=OSOBY, web={"fronta_uzavrene": "x"})
k, out, err = spust(d, "fronta.py")
ok("fronta: špatný tvar nastavení končí srozumitelnou hláškou", k != 0 and "fronta_uzavrene" in err and "Traceback" not in err, err)
k, out, err = spust(tempfile.mkdtemp(prefix="doplnky_"), "fronta.py")
ok("fronta: mimo projekt hláška místo tracebacku", k != 0 and "Traceback" not in err, err)

ZAZNAMY = [
    {"klic": "a", "shrnuti": "Křest. Kmotr Jan Hrubý, Anna Dvořáková."},
    {"klic": "b", "shrnuti": "Sňatek. Svědci: Josef Hrubý a Marie Hrubá."},
    {"klic": "c", "shrnuti": "Křest. Kmotři Karel Vávra a Eva Černá."},
    {"klic": "d", "shrnuti": "Bez kmotrů."},
    {"bez_klice": 1},
]
d = projekt(zaznamy=ZAZNAMY)
k, out, err = spust(d, "kmotri.py")
text = open(os.path.join(d, "pracovni", "kmotri.md"), encoding="utf-8").read()
ok("kmotri: doběhne i se záznamem bez klíče", k == 0, err)
ok("kmotri: první jméno za slovem Kmotr se neztratí (Jan Hrubý)", "Jan Hrubý" in text, text)
ok("kmotri: příjmení ve dvou zápisech se spojí a ženský tvar se sjednotí (Hrubý/Hrubá)", "## Hrubý – 2 zápisů" in text, text)
ok("kmotri: příjmení jen v jednom zápisu se nevypíše", "Vávra" not in text, text)
ok("kmotri: soubor má LF", b"\r\n" not in open(os.path.join(d, "pracovni", "kmotri.md"), "rb").read())

SITE = {"people": {"jan-novak-1890": {"slug": "jan-novak-1890"}, "marie-kralova": {"slug": "marie-kralova"}, "x-novak-1900": {"slug": "x-novak-1900"}, "x-novak-1901": {"slug": "x-novak-1901"}}}
PRIBEH = "Viz [Jan](/osoba/jan-novak/) a [Marie](/osoba/marie-kralova-1925/) a [X](/osoba/x-novak/) a [OK](/osoba/jan-novak-1890/).\r\n"
d = projekt(site=SITE, pribeh=PRIBEH)
k, out, err = spust(d, "oprav_odkazy.py")
novy = open(os.path.join(d, "data", "pribeh.md"), "rb").read().decode("utf-8")
ok("oprav_odkazy: jednoznačnou náhradu opraví (jan-novak → jan-novak-1890)", "(/osoba/jan-novak-1890/) a [Marie]" in novy, novy)
ok("oprav_odkazy: odkaz s rokem bez roku v datech opraví na slug bez roku", "(/osoba/marie-kralova/)" in novy, novy)
ok("oprav_odkazy: nejednoznačný odkaz nechá", "(/osoba/x-novak/)" in novy, novy)
d = projekt(site=SITE, pribeh="Hotovo [Jan](/osoba/jan-novak-1890/)\r\n")
k, out, err = spust(d, "oprav_odkazy.py")
ok("oprav_odkazy: bez změny soubor nepřepisuje (zůstane CRLF)", b"\r\n" in open(os.path.join(d, "data", "pribeh.md"), "rb").read() and "Beze změny" in out, out)
k, out, err = spust(projekt(pribeh="x"), "oprav_odkazy.py")
ok("oprav_odkazy: chybějící site.json = srozumitelná hláška", k != 0 and "npm run data" in err and "Traceback" not in err, err)
k, out, err = spust(projekt(site=SITE), "oprav_odkazy.py")
ok("oprav_odkazy: chybějící pribeh.md = srozumitelná hláška", k != 0 and "pribeh.md" in err and "Traceback" not in err, err)

print(f"\n{sum(vysledky)} z {len(vysledky)} v pořádku")
sys.exit(0 if all(vysledky) else 1)
