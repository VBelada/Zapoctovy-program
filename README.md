# Zadání

Cílem projektu je vytvořit program, který je schopen:

1. vyhodnotit, zda z výchozí šachové pozice existuje vynucený mat do 3 tahů
2. zaznamenat dostatek vynucených matů, abychom pokryli libovolnou obranu druhého hráče
3. v případě existence vynuceného matu do 3 tahů dát uživateli možnost prozkoumat možné sekvence (v závislosti na obranných tazích)

# Uživatelská dokumentace

## Instalace

Pro úspěšné spuštění programu budete potřebovat:

1. IDE pro Python (typicky VS Code, PyCharm, IDLE...)

- Pro stažení můžete použít například následující url:

<https://www.python.org/downloads>

1. Pythonový skript „3 moves to mate“
2. Knihovnu python-chess

- Lze nainstalovat příkazem „pip install python-chess“ do příkazového řádku

## Spuštění programu a zadání výchozí pozice

Pokud jste úspěšně dokončili předchozí kroky, můžete nyní v editoru své volby kód spustit.

Do konzole je nutné vložit šachovou pozici pomocí kódu FEN. Ten lze jednoduše získat zadáním šachové pozice do jednoho z veřejně přístupných programů (např. <https://www.redhotpawn.com/chess/chess-fen-viewer.php>). Do programu tedy zadejte analyzovanou šachovou pozici, zkopírujte FEN kód, ten vložtě do konzole a stiskněte Enter.

V případě, že byl zadán neplatný FEN kód, je uživatel automaticky vyzván k zadání kódu nového. Jinak by se měl na obrazovce v rámci několika vteřin objevit výsledný verdikt, tedy zda z výchozí pozice existuje mat do 3 tahů či ne.

## Hra za obránce

Jestliže program vyhodnotí, že z výchozí pozice nelze z pohledu útočníka (tj. hráče na tahu) nuceně docílit matu do 3 tahů, je tato informace zobrazena v konzoli a program je ihned ukončen.

V opačném případě je uživateli nabídnuta možnost hrát za obránce a sledovat tahy vedoucí k matu při libovolné hře obránce. Pokud uživatel tuto možnost přijme, objeví se na displeji text s prvním tahem útočníka. Za předpokladu, že se nejedná o mat, je uživateli nabídnuta možnost zadat libovolný legální tah z této nové pozice. Tento proces se opakuje až do dosažení matu.

Tahy je nutné do konzole zadávat ve tvaru notace UCI. Tento systém funguje následovně: Pokud chci táhnout nějakou figurkou z pole a1 na pole g6, bude notace jednoduše a1g6, tedy dohromady psané „odkud kam“.

Výjimkou jsou pouze:

- proměny pěšce – za standardní kód je navíc bez mezery psán kód figurky, ve kterou chceme pěšce proměnit (dáma – q, věž – r, kůň – n, střelec – b)
- rošáda – zaznamenána jakožto pohyb krále na cílové pole (např. e1g1)

Pokud náhodou při hře za obránce dojde k chybnému zapsání tahu, je uživateli nabídnuta možnost zapsat tah znovu.

## Příklady pozic

Zde je pár příkladů zajímavých pozic, které lze využít k otestování správného chodu programu:
- ladder mate: 8/8/7k/1R6/2R5/8/8/K7 w - - 0 1
- promotion mate: 7k/4Q3/8/1P6/8/8/8/K7 w - - 0 1
- knight and bishop mate: 7k/8/4N1K1/6B1/8/8/8/8 w - - 0 1
- smothered mate in 2: 5rrk/6pp/3N4/6N1/8/5P2/5QPP/6RK w - - 0 1
- další: - r5rk/5p1p/5R2/4B3/8/8/7P/7K w - - 0 1
         - 5rrk/4Nbpp/5p2/8/5N2/P7/1P6/1K1R4 w - - 0 1
         - R6R/1r3pp1/4p1kp/3pP3/1r2qPP1/7P/1P1Q3K/8 w - - 1 0

# Technická dokumentace

Celý program je psán v jazyku Python. Jeho vnitřní strukturu lze pak rozdělit do několika částí.

## Načtení dat

Pro načtení FEN kódu je použita klauzule Try-Except. Jestliže pak z nějakého důvodu nelze kód převést na objekt Chess.Board, uživatel je vyzván k zadání nového.

## Dvojice funkcí Attacker a Defender

Tyto dvě funkce slouží k vyhodnocení zadané šachové pozice. Fungují na principu procházení stavového stromu do hloubky.

Na počáteční pozici je zavolána funkce Attacker, která vrací dvojici list\[bool, list\[list\[Chess.Move\]\]. True je vráceno právě tehdy, když z pozice existuje vynucený mat do 3 tahů. Pokud je samotná pozice mat nebo pat (obránce vyhrál, tedy se i ubránil, bez zahrání jediného tahu), potom bude zřejmě vracená hodnota False.  
V případě, že nelze pozice vyhodnotit předchozím způsobem, se postupně zkouší útočné tahy, dokud není nalezen jeden, který vede k nucenému matu – vrací se True – , nebo dokud útočné tahy nedojdou – vrací se False. Informaci o „správnosti“ daného tahu pak vrací funkce Defender.

Funkce Defender již vrací pouze bool (není nutné vracet seznam matů, jelikož ten je potřeba až po vyhodnocení celé počáteční pozice a my na začátku voláme funkci Attacker). Konkrétně, stejně jako u funkce Attacker, True se vrací právě tehdy, když z pozice existuje vynucený mat pro útočníka do zbývajícího množství tahů (lze také chápat tak, že se obránce z této pozice není schopen ubránit). To je zřejmě pravda, pokud je samotná pozice mat. Každý dosažený mat je zaznamenán do seznamu Mates. Naopak funkce zřejmě bude vracet False, pokud útočník překročil maximální počet tahů nebo je pozice pat.  
Pokud opět není pozice takto jednoduše vyhodnotitelná, jsou zkoušeny všechny legální obranné tahy, dokud nejsou vyčerpány – vrací se True – nebo není nalezen jeden, který nevede nutně k matu – vrací se False.

Za předpokladu, že z výchozí pozice existuje vynucený mat do 3 tahů pro útočníka, v seznamu Mates na konci vyhodnocování skončí právě maty, které:

1. pokryjí libovolnou obranu obránce
2. jsou nucené – tj. pro každý mat platí, po i-tém tahu obránce jsme vždy schopni mu dát mat do maximálně (3-i) tahů útočníka

## Hra za obránce

Jednoduchým stromem rozhodnutí je uživateli dána možnost hrát za obránce, což po technické stránce znamená vstup do funkce user_interface.

V této funkci je používán právě seznam matů, ze kterého postupně vybíráme pouze ty, které odpovídají dosavadním tahům uživatele (neboli obránce).  
Jelikož je v mates obsažena odpověď pro každou možnou strategii obránce, prázdný výběr odpovídajících sekvencí znamená špatně zapsaný nebo zvolený tah ze strany uživatele, kterému je dána možnost tah zadat znovu.
