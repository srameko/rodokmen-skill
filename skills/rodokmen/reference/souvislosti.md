# Souvislosti a jiné zdroje – kde hledat, když matrika mlčí

Každý bod je postup, který model zvládne sám. Zdroje jsou jen vodítka; osobu zapisuj až podle matriky nebo vrchnostenské knihy čtené na snímku.

## A. Souvislosti z dat, která už máme (bez nového archivu)
1. **Síť kmotrů a svědků.** Ze všech `shrnuti` v `zaznamy.json` vypiš jména kmotrů, svědků a porodních bab a spočítej,
   kdo se opakuje u více rodin. Kmotři bývali příbuzní (strýc, teta, babička).
2. **Dům jako vlákno.** Číslo popisné se nemění, lidé ano. Vypiš pro každý dům
   všechny zápisy, které ho zmiňují, seřazené podle roku. Kdo v domě žil před naším předkem, je často tchán (přiženění –
   časté).
3. **Sourozenci jako zkratka.** Sňatek nebo úmrtí sourozence často uvádí to, co náš zápis vynechal (rodné příjmení
   matky, obec původu otce). Křest bratra dal oba páry prarodičů, které sňatek nemenoval.
4. **Věk jako filtr, ne jako fakt.** Věk ve sňatku byl u mladých nevěst „vylepšený“ (14½ → 17). Hledej rok narození
   v rozpětí −3 až +1 roku od uvedeného věku; u úmrtí ±5 let.
5. **Pojmenovací zvyk.** První syn často po dědovi z otcovy strany, první dcera po babičce. Seznam dětí → odhad jmen
   prarodičů → užší hledání v rejstříku.
6. **Rozpory jako stopa.** Dvě různá jména matky u sourozenců znamenají
   druhé manželství, nevlastní dítě nebo jinou osobu – vždy prověř, nespojuj potichu.
7. **Celá farnost najednou.** Kde je rejstřík nebo farní index, vypiš všechny výskyty
   příjmení za 50 let a sestav rodiny automaticky; pak napoj na našeho předka. Rychlejší než listování po jednom zápisu.

## B. Jiné zdroje než matriky
| Zdroj | Co dá | Kdy |
|---|---|---|
| Dobový tisk – Kramerius (`tools/kramerius.py`), ANNO (`tools/anno.py`) | úmrtí, parte, spolky, živnosti, soudní zprávy, Baťovské časopisy | lidé po ~1850 |
| Adresáře a ročenky (Kramerius) | živnostníci, mlynáři, kováři, starostové obcí | 1880–1940 |
| Berní rula 1654, Soupis poddaných 1651 | jména hospodářů na gruntech | konec matrik kolem 1650 |
| Tereziánský / josefský / stabilní katastr, indikační skici | majitel podle čísla domu, výměra | 1750–1840 |
| Sčítání lidu 1857–1921 | celá domácnost s daty a místy narození | 1857+ |
| Pozemkové (gruntovní) knihy, urbáře | převody gruntů, výměnky, svatební smlouvy | 1700–1850 |
| Obecní a školní kroniky | události obce, požáry, epidemie, padlí | 1900+ |
| VHA – databáze padlých a legionářů, kmenové listy | vojáci 1. sv. války | narození 1860–1900 |
| Hřbitovy (BillionGraves, Hroby.cz, hřbitovy Brno) | data úmrtí, společné hroby | 1900+ |
| Cizí rodokmeny (FamilySearch, Geni, MyHeritage) | jen jako nápověda, nikdy jako doklad | vše |
| Paměť národa a podobné sbírky vzpomínek | život 20. století | 1900+ |
| Strojové čtení rukopisů (HTR, Transkribus) | plný text celé knihy → hledání jmen bez listování | až budou modely pro kurent |

## C. Pravidla
- Tisk, katastr i cizí stromy jsou **doplněk** – osoba se do `osoby.py` zapisuje jen na základě zápisu, ne podle zmínky
  v novinách nebo cizího stromu. U shody jmen odděl „jisté / pravděpodobné / jmenovec“.
