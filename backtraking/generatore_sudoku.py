import random
import copy
from versione_backtraking_base import risolvi_sudoku_backtracking,controllo_valido

def genera_soluzione(griglia):
    """Genera una griglia Sudoku completa valida usando backtracking randomizzato."""
    numeri = list(range(1, 10))
    for r in range(9):
        for c in range(9):
            if griglia[r][c] == 0:
                random.shuffle(numeri)
                for numero in numeri:
                    if controllo_valido(r, c, numero, griglia):
                        griglia[r][c] = numero
                        if genera_soluzione(griglia):
                            return True
                        griglia[r][c] = 0
                return False
    return True

def crea_puzzle(celle_da_togliere):
    """Crea un Sudoku con un certo numero di celle vuote in base alla difficolta, poi uso il risolutore per vedere se va bene"""
    #Genera una soluzione completa
    griglia = [[0] * 9 for _ in range(9)]
    genera_soluzione(griglia)

    #Rimuovo celle verificando che il puzzle resti risolvibile
    celle = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(celle)
    celle_rimosse = 0

    while celle and celle_rimosse < celle_da_togliere:
        r, c = celle.pop()
        backup = griglia[r][c]
        griglia[r][c] = 0

        #Uso il risolutore per verificare se rimane risolvibile (per ora ho messo la versione base con backtrack ma posso mettere direttamente dancing links)
        copia = copy.deepcopy(griglia)
        risultato = risolvi_sudoku_backtracking((3, 3), copia)

        if risultato["successo"]:  #risolvibile
            celle_rimosse += 1
        else:  # non risolvibile, ripristina
            griglia[r][c] = backup

    return griglia

# Funzioni per difficoltà
def genera_sudoku_facile():
    return crea_puzzle(40)

def genera_sudoku_medio():
    return crea_puzzle(50)

def genera_sudoku_difficile():
    return crea_puzzle(60)

def stampa_sudoku(sudoku):
    for riga in sudoku:
        print(" ".join(str(num) if num != 0 else '.' for num in riga))

# Test
print("Sudoku Facile:")
stampa_sudoku(genera_sudoku_facile())
