from itertools import product
import time


# Classe per contare le ricorsioni
class ChiamateDLX:
    def __init__(self):
        self.numero = 0


def risolvi_sudoku_dancing_links(size, griglia_input):
    R, C = size
    N = R * C

    chiamate = ChiamateDLX()
    
    # Conversione per prendersi la stringa 
    if isinstance(griglia_input, str):
        griglia = []
        for i in range(N):
            riga = []
            for j in range(N):
                char = griglia_input[i * N + j]
                riga.append(int(char) if char.isdigit() and char != '0' else 0)
            griglia.append(riga)
    else:
        # Se è già una lista, fai una copia per non modificare l'originale
        griglia = [riga[:] for riga in griglia_input]

    # Da qui in poi sto seguendo quello che dice nel paper in the dance steps 
    X = (    # La lista X in questo caso contiene tutti i possibili vincoli
        [("rc", rc) for rc in product(range(N), range(N))]  # vincolo (riga, colonna)
        + [("rn", rn) for rn in product(range(N), range(1, N + 1))]  # vincolo (riga, numero)
        + [("cn", cn) for cn in product(range(N), range(1, N + 1))]  # vincolo (colonna, numero)
        + [("bn", bn) for bn in product(range(N), range(1, N + 1))]  # vincolo (box, numero)
    )   # praticamente questi vincoli mi garantiscono che ogni numero compaia esattamente una volta per riga, una per colonna e una per box  

    Y = dict()  # Questo dict va a mappare ogni possibile piazzamento di un numero per creare la matrice di copertura esatta   
    for r, c, n in product(range(N), range(N), range(1, N + 1)):
        b = (r // R) * R + (c // C)
        Y[(r, c, n)] = [
            ("rc", (r, c)), 
            ("rn", (r, n)),
            ("cn", (c, n)), 
            ("bn", (b, n))]   

    X, Y = costruisci_cover_esatto(X, Y)  
    # Come dice il paper, ora devo convertire i vincoli in una matrice 0 - 1 
    # e lo faccio con la funzione costruisci_cover_esatto 
    
    # Quindi adesso sto iterando nella griglia iniziale e copro i vincoli dei numeri già presenti  
    for i, riga in enumerate(griglia):
        for j, numero in enumerate(riga):
            if numero:
                copri(X, Y, (i, j, numero))

    # Ora cerco una soluzione
    soluzione = next(solve_dlx(X, Y, [], chiamate), None)
    if soluzione:
        # Applica la soluzione alla griglia
        for (r, c, n) in soluzione: 
            griglia[r][c] = n
    
    # Restituisci il dizionario con successo, soluzione e ricorsioni
    return {
        "successo": True if soluzione else False,
        "soluzione": griglia if soluzione else None,
        "ricorsioni": chiamate.numero
    }


# Funzione per costruire la struttura dati con le coperture
def costruisci_cover_esatto(X, Y):  
    X = {j: set() for j in X}
    for i, riga in Y.items():
        for j in riga:
            X[j].add(i)

    return X, Y


# Funzione che risolve il Sudoku con Dancing Links
def solve_dlx(X, Y, soluzione, chiamate): 
    chiamate.numero += 1  # Incrementa ogni volta che viene fatta una ricorsione
    if not X: 
        yield list(soluzione)
    else: 
        # Seleziona la colonna con il minimo numero di opzioni
        c = min(X, key=lambda c: len(X[c]))  
        for r in list(X[c]): 
            soluzione.append(r)
            colonne_coperte = copri(X, Y, r)  # Copro le colonne
            for s in solve_dlx(X, Y, soluzione, chiamate): 
                yield s
            scopri(X, Y, r, colonne_coperte)  # Ripristino per il backtracking
            soluzione.pop()


# Funzione che rimuove righe e colonne associate a un dato piazzamento
def copri(X, Y, r):
    colonne = []
    for j in Y[r]:
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].remove(i)
        colonne.append(X.pop(j))
    return colonne


# Funzione che ripristina righe e colonne (uncover)
def scopri(X, Y, r, colonne): 
    for j in reversed(Y[r]): 
        X[j] = colonne.pop()
        for i in X[j]: 
            for k in Y[i]: 
                if k != j: 
                    X[k].add(i)

