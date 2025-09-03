import copy

def controllo_valido(riga, colonna, numero, griglia):
    for i in range(9):
        if griglia[riga][i] == numero or griglia[i][colonna] == numero:
            return False

    inizio_riga = riga - riga % 3
    inizio_colonna = colonna - colonna % 3
    for i in range(3):
        for j in range(3):
            if griglia[inizio_riga + i][inizio_colonna + j] == numero:
                return False

    return True

class Chiamate:
    numero = 0

def backtrack(griglia, conteggio):
    conteggio.numero += 1
    for r in range(9):
        for c in range(9):
            if griglia[r][c] == 0: # Trovo una cella vuota
                for numero in range(1, 10):  # Provo numeri da 1 a 9
                    if controllo_valido(r, c, numero, griglia): # Se il numero è valido
                        griglia[r][c] = numero # A quel punto lo inserisco
                        if backtrack(griglia, conteggio):  # Qua faccio la chiamata ricorsiva per verificare se questo assegnamento mi porta alla soluzione
                            return True 
                        griglia[r][c] = 0 # Se la ricorsione fallisce, rimuovo il numero
                return False
    return True

def risolvi_sudoku_backtracking(size, griglia_input):
    griglia = copy.deepcopy(griglia_input)  # Per non modificare l'originale
    conteggio = Chiamate()
    successo = backtrack(griglia, conteggio)


    return {
        "successo": successo,
        "soluzione": griglia if successo else None,
        "ricorsioni": conteggio.numero
    }

# Test per vedere se funziona

sudoku = [
    [0, 0, 3, 0, 2, 0, 6, 0, 0],
    [9, 0, 0, 3, 0, 5, 0, 0, 1],
    [0, 0, 1, 8, 0, 6, 4, 0, 0],
    [0, 0, 8, 1, 0, 2, 9, 0, 0],
    [7, 0, 0, 0, 0, 0, 0, 0, 8],
    [0, 0, 6, 7, 0, 8, 2, 0, 0],
    [0, 0, 2, 6, 0, 9, 5, 0, 0],
    [8, 0, 0, 2, 0, 3, 0, 0, 9],
    [0, 0, 5, 0, 1, 0, 3, 0, 0]
]

risultato = risolvi_sudoku_backtracking((3, 3),sudoku)

if risultato["successo"]:
    print("Soluzione trovata!")
    for r in risultato["soluzione"]:
        print(r)
    print("Ricorsioni:", risultato["ricorsioni"])
else:
    print("Nessuna soluzione trovata.")