from itertools import product
import time


# Classe per contare le ricorsioni
class Chiamate:
    def __init__(self):
        self.numero = 0


def solve_sudoku_dancing_links(size, grid):   
    R, C = size
    N = R * C

    chiamate = Chiamate()

    # Da qui in poi sto seguendo quello che dice nel paper in the dance steps 
    X = (    # La lista X in questo caso contiene tutti i possibili vincoli
        [("rc", rc) for rc in product(range(N), range(N))]  # row column pair
        + [("rn", rn) for rn in product(range(N), range(1, N + 1))]  # row number pair
        + [("cn", cn) for cn in product(range(N), range(1, N + 1))]  # column number pair 
        + [("bn", bn) for bn in product(range(N), range(1, N + 1))]  # box number pair 
    )   # praticamente questi vincoli mi garantiscono che ogni numero compaio esattamente solo una volta per riga, una per colonna e una per box  
    Y = dict()  # Questo dict va a mappare ogni possibile pizzamento per creare una esatta cover matrix   
    for r, c, n in product(range(N), range(N), range(1, N + 1)):
        b = (r // R) * R + (c // C)
        Y[(r, c, n)] = [
            ("rc", (r, c)), 
            ("rn", (r, n)),
            ("cn", (c, n)), 
            ("bn", (b, n))]   
    X, Y = exact_cover(X, Y)  
    # Come continua a dire dopo For example devo ora convertire i vincoli in una 0 - 1 matrice  
    # e lo faccio con la funzione exact_cover 
    
    """Another typical application arises in backtrack programs [16], which enumerate all solutions to a given set of constraints.
    Backtracking, also called depth-first search, will be the focus of the present paper."""
    
    # Quindi adesso sto iterando nella griglia iniziale e cover i vincoli dei numeri iniziali  
    for i, row in enumerate(grid):
        for j, n in enumerate(row):
            if n:
                cover(X, Y, (i, j, n))

    # Ora, al posto di usare yield, ritorna la prima soluzione trovata
    solution = next(solve(X, Y, [], chiamate), None)
    if solution:
        # Applica la soluzione alla griglia
        for (r, c, n) in solution: 
            grid[r][c] = n
    
    # Restituisci il dizionario con successo, soluzione e ricorsioni
    return {
        "successo": True if solution else False,
        "soluzione": grid if solution else None,
        "ricorsioni": chiamate.numero
    }


# Funzione per costruire la struttura dati con le coperture
def exact_cover(X, Y):  
    X = {j: set() for j in X}
    for i, row in Y.items():
        for j in row:
            X[j].add(i)

    return X, Y

# Funzione che risolve il problema di Sudoku
def solve(X, Y, solution, chiamate): 
    chiamate.numero += 1  # Incrementa ogni volta che viene fatta una ricorsione
    if not X: 
        yield list(solution)
    else: 
        c = min(X, key = lambda c: len(X[c]))  # Seleziona la colonna con il minimo numero di opzioni
        for r in list(X[c]): 
            solution.append(r)
            cols = cover(X, Y, r)  # Copri le colonne
            for s in solve(X, Y, solution, chiamate): 
                yield s
            uncover(X, Y, r, cols)  # Uncover per il backtracking
            solution.pop()


# Funzione che rimuove righe e colonne associate a un dato placement
def cover(X, Y, r):
    cols = []
    for j in Y[r]:
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].remove(i)
        cols.append(X.pop(j))

    return cols

# Funzione che ripristina righe e colonne (uncover)
def uncover(X, Y, r, cols): 
    for j in reversed(Y[r]): 
        X[j] = cols.pop()
        for i in X[j]: 
            for k in Y[i]: 
                if k != j: 
                    X[k].add(i)


# Da qui in poi è per testare se l'algoritmo funziona 
# Griglia di Sudoku di esempio (0 indica una cella vuota)
puzzle = [
    [0, 0, 0, 0, 0, 2, 0, 8, 0],
	[0, 7, 0, 0, 0, 8, 0, 0, 6],
	[8, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 8, 0, 7, 0, 0, 0, 0],
	[0, 0, 0, 0, 1, 0, 9, 0, 0],
	[0, 2, 0, 5, 3, 0, 0, 6, 0],
	[0, 0, 0, 1, 0, 7, 0, 0, 0],
	[5, 0, 1, 0, 0, 0, 2, 0, 8]
]
# Funzione di test 
def test_sudoku():
    size = (3, 3)  # La dimensione della griglia è 3x3, che corrisponde a un Sudoku 9x9
    start_time = time.time()
    result = solve_sudoku_dancing_links(size, puzzle)  # Chiama la funzione solve_sudoku con la griglia
    
    # Stampa i risultati come richiesto
    if result["successo"]:
        print("Sudoku risolto:")
        for row in result["soluzione"]:
            print(row)
    else:
        print("Non è stato trovato nessuna soluzione.")
    
    print(f"Numero di ricorsioni: {result['ricorsioni']}")
    
    end_time = time.time()
    print("Il tempo è " + str(end_time - start_time))


# Chiamare la funzione di test
test_sudoku()
