import random

def genera_sudoku_facile():
    # Una griglia 9x9 vuota
    sudoku = [[0] * 9 for _ in range(9)]
    
    # Per un sudoku facile imposto molti numeri iniziali -> 40 numeri iniziali
    celle_piene = 40
    while celle_piene > 0:
        # Generiamo una cella random da riempire
        riga = random.randint(0, 8)
        colonna = random.randint(0, 8)
        
        # Verifica che la cella sia vuota
        if sudoku[riga][colonna] == 0:
            # Assegniamo un numero casuale che non viola le regole del Sudoku
            numero = random.randint(1, 9)
            if verifica_numero(sudoku, riga, colonna, numero):
                sudoku[riga][colonna] = numero
                celle_piene -= 1
    
    return sudoku

def verifica_numero(sudoku, riga, colonna, numero):
    """Controlla se un numero è valido in una posizione (riga, colonna)"""
    # Controllo della riga
    if numero in sudoku[riga]:
        return False
    # Controllo della colonna
    if numero in [sudoku[i][colonna] for i in range(9)]:
        return False
    # Controllo del box 3x3
    box_riga = (riga // 3) * 3
    box_colonna = (colonna // 3) * 3
    for i in range(3):
        for j in range(3):
            if sudoku[box_riga + i][box_colonna + j] == numero:
                return False
    return True


def genera_sudoku_medio():
    sudoku = [[0] * 9 for _ in range(9)]
    
    # Impostiamo un numero medio di celle piene, circa 30 numeri
    celle_piene = 30
    while celle_piene > 0:
        riga = random.randint(0, 8)
        colonna = random.randint(0, 8)
        
        if sudoku[riga][colonna] == 0:
            numero = random.randint(1, 9)
            if verifica_numero(sudoku, riga, colonna, numero):
                sudoku[riga][colonna] = numero
                celle_piene -= 1
    
    return sudoku

def genera_sudoku_difficile():
    sudoku = [[0] * 9 for _ in range(9)]
    
    # Impostiamo un numero ridotto di celle piene, circa 20 numeri
    celle_piene = 20
    while celle_piene > 0:
        riga = random.randint(0, 8)
        colonna = random.randint(0, 8)
        
        if sudoku[riga][colonna] == 0:
            numero = random.randint(1, 9)
            if verifica_numero(sudoku, riga, colonna, numero):
                sudoku[riga][colonna] = numero
                celle_piene -= 1
    
    return sudoku


def stampa_sudoku(sudoku):
    for riga in sudoku:
        print(" ".join(str(num) if num != 0 else '.' for num in riga))
"""
# Testiamo la generazione
print("Sudoku Facile:")
stampa_sudoku(genera_sudoku_facile())

print("\nSudoku Medio:")
stampa_sudoku(genera_sudoku_medio())

print("\nSudoku Difficile:")
stampa_sudoku(genera_sudoku_difficile())
"""