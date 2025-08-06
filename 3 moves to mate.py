import chess

while True:
    FEN = input().strip()
    try:
        starting_position = chess.Board(FEN)
    except ValueError:
        print('Tento kód bohužel nereprezentuje žádnou šachovou pozici. Zkontrolujte, prosím, zda se kód'
              ' správně zkopíroval, a zkuste znovu')
    else:
        break

print(starting_position)

def defender(position: chess.Board, move_number: int, mates: list[list[chess.Move]], possible: list[chess.Move]) -> bool:
    """
    - Simuluje tah obránce
    - Snaží se najít alespoň jeden tah, který nemusí nutně vést k matu a:
        - pokud ho najde, vrácí útočníkovi informaci o neúspěchu jeho posledního tahu
            - pokud si (1) útočník již vyčerpal všechny 3 tahy a aktuální pozice není mat nebo (2) aktuální pozice je pat,
              pak je útočníkovi rovnou navrácena informace o neúspěchu jeho posledního tahu
        - jinak vrací útočníkovi informaci o úspěchu posledního tahu
            - pokud je navíc obránce v aktuální pozici v matu, mat se zaznamená

    parametry:
    - position - aktuální pozice, ze které hledá obránce vhodný tah
    - move number - číslo tahu, na kterém se právě nacházíme (abychom nepřekročili hranici 3 tahů)
    - mates - seznam všech matových sekvencí z počáteční pozice, které zatím nebyly vyvráceny
    - possible - tahy, které vedly k aktuální pozici

    vrací:
    - True, pokud se z pozice existuje nucený mat
    - False, naopak (pokud už jsme překročili limit tahů bez dosažení matu/útočník omylem způsobil pat/obránce je
      schopen nějakým tahem zabránit matu)
    """

    # útočníkovi se podařilo dát mat
    if position.is_checkmate():
        mates.append(possible.copy())
        return True

    else:
        # útočník už využil všechny 3 tahy bez matu/omylem způsobil pat
        if move_number == 6 or position.is_stalemate():
            return False

        else:
            for move in list(position.legal_moves):
                position.push(move)
                possible.append(move)
                result = attacker(position, move_number + 1, mates, possible)[0]
                position.pop()
                possible.pop()
                # obránce našel tah, který nevede k nucenému matu do 3 tahů
                if not result:
                    return False
            return True


def attacker(position: chess.Board, move_number: int, mates: list[list[chess.Move]],
             possible: list[chess.Move]) -> [bool, list[list[chess.Move]]]:
    """
    - Simuluje tah útočníka
    - Snaží se najít alespoň jeden tah z aktuální pozice, který vede k vynucenému matu:
        - pokud ho najde, vrací tuto informaci obránci, který má následně možnost změnit jeho obranu
            - jestliže se jedná o první tah, je nám vrácena informace o existenci vynuceného matu z počáteční pozice
        - jinak vrací obránci informaci o úspěchu jeho obrany
            - zároveň to znamená, že tento útočný tah je 'chybný' a všechny maty, kterých bylo tímto tahem dosaženo
              jsou tedy zamezitelné - tyto maty tedy nejsou vynucené a jsou vymazány

    parametry:
        - analogicky...

    vrací dvojici obsahující:
        - True/False - podle existence vynuceného matu
        - Seznam matových sekvencí (na konci prázdný pokud False)
    """
    # obránci se podařilo zabránit matu od útočníka
    if position.is_checkmate() or position.is_stalemate():
        return [False, mates]

    else:
        moves = list(position.legal_moves)
        for move in moves:
            position.push(move)
            possible.append(move)
            result = defender(position, move_number + 1, mates, possible)
            position.pop()
            possible.pop()
            # tah vede k vynucenému matu
            if result:
                return [True, mates]
            else:
                prefix = possible.copy()
                # všechny matové sekvence začínající tímto prefixem jsou ubránitelné - nejsou vynucené - musíme vymazat
                mates[:] = [m for m in mates if m[:len(prefix)] != prefix]
        return [False, mates]


def user_interface(mates):
    """
    - Funkce, která dává uživateli možnost hrát za obránce
    - Pro libovolný legální tah od obránce funkce najde odpovídající tah pro útočníka
    """
    # první tah je v každé sekvenci stejný (pokud se najde jeden „dobrý“ počáteční tah, program je ukončen)
    if len(mates[0]) == 1:
        print(f'1. tah: {mates[0][0]}... mat :)')
        return
    else:
        print(f'1. tah: {mates[0][0]}')

    while True:
        second = input('2. tah: ').strip()
        right_line = [x for x in mates if x[1].uci() == second]

        # pokud uživatel zadal legální tah, bude mu odpovídat alespoň jedna matová sekvence -> seznam nebude prázdný
        if right_line:
            break
        else:
            decision1 = input('Toto bohužel není legální tah, chceš to zkusit znovu? (ANO pro potvrzení)\n').strip()
            # v případě překlepu/zadání ilegálního tahu dáme uživateli možnost se opravit
            if decision1 != 'ANO':
                print('Dobře tedy... :)')
                return
    # třetí tah první matové sekvence (jedna z možností výběru)
    if len(right_line[0]) == 3:
        print(f'3. tah: {right_line[0][2]}... mat :)')
        return
    else:
        print(f'3. tah: {right_line[0][2]}')

    while True:
        fourth = input('4. tah: ').strip()
        for i in right_line:
            if i[3].uci() == fourth:
                print(f'5. tah: {i[4]}... mat :)')
                return
        decision2 = input('Toto bohužel není legální tah, chceš to zkusit znovu? (ANO pro potvrzení)\n').strip()
        if decision2 != 'ANO':
            print('Dobře tedy... :)')
            return


final_result = attacker(starting_position, 1, [], [])
color = FEN.split()[1]

if color == 'w':
    color = 'bílého'

if color == 'b':
    color = 'černého'
if not final_result[0]:
    print(f'Z této pozice neexistuje pro {color} vynucený mat do 3 tahů\n')

else:
    decision = input(f'Z této pozice existuje pro {color} vynucený mat do 3 tahů, '
             f'přejete se dozvědět, kam tahat figurkami? (ANO pro otvrzení)\n').strip()
    if decision == 'ANO':
        user_interface(final_result[1])
    else:
        print('Dobře tedy... :)')