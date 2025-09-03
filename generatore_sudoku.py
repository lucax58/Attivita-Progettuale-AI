import random
import copy


def controllo_valido(griglia, riga, colonna, numero):
    """Controlla se un numero può essere inserito in (riga, colonna)."""
    for i in range(9):
        if griglia[riga][i] == numero or griglia[i][colonna] == numero:
            return False

    inizio_riga = (riga // 3) * 3
    inizio_colonna = (colonna // 3) * 3
    for i in range(3):
        for j in range(3):
            if griglia[inizio_riga + i][inizio_colonna + j] == numero:
                return False
    return True


def risolvi_sudoku(griglia):
    """Risolutore semplice con backtracking, restituisce True se risolvibile."""
    for r in range(9):
        for c in range(9):
            if griglia[r][c] == 0:  # Trova cella vuota
                for numero in range(1, 10):
                    if controllo_valido(griglia, r, c, numero):
                        griglia[r][c] = numero
                        if risolvi_sudoku(griglia):
                            return True
                        griglia[r][c] = 0
                return False
    return True


def genera_soluzione(griglia):
    """Genera una griglia Sudoku completa valida con backtracking."""
    numeri = list(range(1, 10))
    for r in range(9):
        for c in range(9):
            if griglia[r][c] == 0:
                random.shuffle(numeri)
                for numero in numeri:
                    if controllo_valido(griglia, r, c, numero):
                        griglia[r][c] = numero
                        if genera_soluzione(griglia):
                            return True
                        griglia[r][c] = 0
                return False
    return True


def crea_puzzle(celle_da_togliere):
    """Crea un Sudoku con un numero di celle vuote specifico."""
    #Genera una soluzione completa
    griglia = [[0] * 9 for _ in range(9)]
    genera_soluzione(griglia)

    #Rimuovi celle in modo casuale, verificando che resti risolvibile
    celle = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(celle)
    celle_rimosse = 0

    while celle and celle_rimosse < celle_da_togliere:
        r, c = celle.pop()
        backup = griglia[r][c]
        griglia[r][c] = 0

        copia = copy.deepcopy(griglia)
        if risolvi_sudoku(copia):  #Verifica risolvibilità
            celle_rimosse += 1
        else:
            griglia[r][c] = backup  #Non è risolvibile, ripristina

    return griglia


def genera_sudoku_facile():
    return crea_puzzle(40)  # circa 40 celle vuote → facile

def genera_sudoku_medio():
    return crea_puzzle(50)  # circa 50 celle vuote → medio

def genera_sudoku_difficile():
    return crea_puzzle(60)  # circa 60 celle vuote → difficile



def stampa_sudoku(sudoku):
    for riga in sudoku:
        print(" ".join(str(num) if num != 0 else '.' for num in riga))

#Test
print("Sudoku Facile:")
stampa_sudoku(genera_sudoku_facile())

print("\nSudoku Medio:")
stampa_sudoku(genera_sudoku_medio())

print("\nSudoku Difficile:")
stampa_sudoku(genera_sudoku_difficile())
