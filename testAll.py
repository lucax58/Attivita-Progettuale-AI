import time
import os

from versione_backtraking_base import risolvi_sudoku_backtracking 
from versione_backtraking_MRV import risolvi_sudoku_MRV
from versione_dancing_links import solve_sudoku_dancing_links
from generatore_sudoku import genera_sudoku_difficile
from generatore_sudoku import genera_sudoku_medio
from generatore_sudoku import genera_sudoku_facile

# Funzione per testare una singola soluzione
def testa_soluzione(soluzione, sudoku):
    start_time = time.time()
    risultato = list(soluzione((3, 3), sudoku))  # Invoca la soluzione col sudoku
    end_time = time.time()
    tempo_trascorso = end_time - start_time
    if len(risultato) == 0:
        return None, tempo_trascorso  # Nessuna soluzione trovata
    else:
        return risultato[0], tempo_trascorso  # Restituisce la soluzione e il tempo

# Funzione per eseguire il benchmark per ogni solver e scrivere i risultati in file separati
def benchmark_e_scrivi(soluzioni, difficolta, sudoku):
    for nome_soluzione, funzione_soluzione in soluzioni.items():
        nome_file = f"risultati_{nome_soluzione.lower()}_{difficolta}.txt"
        
        with open(nome_file, "a") as file:  # Usa "a" per appendere invece di sovrascrivere
            file.write(f"Risultati per il solver: {nome_soluzione} - Difficoltà: {difficolta}\n")
            file.write(f"\nTest del Sudoku:\n")
            # Stampa il sudoku in formato leggibile
            for riga in sudoku:
                file.write(f"\t{riga}\n")
            
            # Testa solo la soluzione corrente
            soluzione_result, tempo = testa_soluzione(funzione_soluzione, sudoku)
            
            if soluzione_result:
                file.write(f"\tTempo: {tempo:.3f} secondi\n")
                file.write(f"\tSoluzione trovata:\n")
                # Stampa la soluzione in formato leggibile
                for riga in soluzione_result:
                    file.write(f"\t{riga}\n")
            else:
                file.write(f"\tTempo: {tempo:.3f} secondi\n")
                file.write("\tNessuna soluzione trovata\n")
            file.write("="*40 + "\n")  # Separatore tra i test dei Sudoku

# Esegui i test
if __name__ == "__main__":
    
    # Inizializza le soluzioni come dizionario
    soluzioni = {
        "Backtraking": risolvi_sudoku_backtracking,  # Solver backtracking base
        "Backtraking_MRV": risolvi_sudoku_MRV,  # Solver backtraking MRV
        "Dancing_links": solve_sudoku_dancing_links  # Solver con dancing links 
    }

    # Rimuove i file dei risultati precedenti se esistono
    for nome_soluzione in soluzioni:
        for difficolta in ["facile", "medio", "difficile"]:
            nome_file = f"risultati_{nome_soluzione.lower()}_{difficolta}.txt"
            if os.path.exists(nome_file):
                os.remove(nome_file)

    # Esegui i test per ogni livello di difficoltà
    # Facile
    for i in range(10): 
        sudoku = genera_sudoku_facile()
        benchmark_e_scrivi(soluzioni, "facile", sudoku)
    
    # Medio 
    for i in range(10): 
        sudoku = genera_sudoku_medio()
        benchmark_e_scrivi(soluzioni, "medio", sudoku)
    
    # Difficile 
    for i in range(10): 
        sudoku = genera_sudoku_difficile()
        benchmark_e_scrivi(soluzioni, "difficile", sudoku)