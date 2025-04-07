import copy
import time

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

class ChiamateMRV:
    numero = 0

def backtrack_MRV(griglia, chiamate):
        chiamate.numero += 1
        caselle = []

        for r in range(9):
            for c in range(9):
                if griglia[r][c] == 0:
                    opzioni = [n for n in range(1, 10) if controllo_valido(r, c, n, griglia)]
                    caselle.append(((r, c), len(opzioni), opzioni))
                    
            
        if not caselle:
            return True  #è risolto

        # qua ordino le caselle per numero minimo di opzioni cioè è l'euristica MRV
        caselle.sort(key=lambda x: x[1])
        (riga, colonna), _, opzioni = caselle[0]

        for numero in opzioni:
            griglia[riga][colonna] = numero
            if backtrack_MRV(griglia,chiamate):
                return True
            griglia[riga][colonna] = 0

        return False


def risolvi_sudoku_MRV(size, griglia_input):
    griglia = copy.deepcopy(griglia_input)
    chiamate = ChiamateMRV()

    successo = backtrack_MRV(griglia, chiamate)

    return {
        "successo": successo,
        "soluzione": griglia if successo else None,
        "ricorsioni": chiamate.numero
    }


#Test per vedere se funziona

sudoku = [
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

start_time = time.time()
risultato = risolvi_sudoku_MRV((3, 3), sudoku)
elapsed = time.time() - start_time

if risultato["successo"]:
    print("Soluzione trovata con MRV!")
    for riga in risultato["soluzione"]:
        print(riga)
    print("Ricorsioni:", risultato["ricorsioni"])
    print("Il tempo è " + str(elapsed))
else:
    print("Nessuna soluzione trovata.")
