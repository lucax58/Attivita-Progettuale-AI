import time
import os

from versione_backtraking_base import risolvi_sudoku_backtracking 
from versione_backtraking_MRV import risolvi_sudoku_MRV
from versione_dancing_links import solve_sudoku_dancing_links
from generatore_sudoku import genera_sudoku_difficile, genera_sudoku_medio, genera_sudoku_facile


# Funzione per testare una singola soluzione
def testa_soluzione(funzione, sudoku):
    start_time = time.time()
    risultato = funzione((3, 3), sudoku)  # Ora tutte restituiscono un dict
    end_time = time.time()
    tempo_trascorso = end_time - start_time
    return risultato, tempo_trascorso


# Funzione per eseguire il benchmark per ogni solver e scrivere i risultati in file separati
def benchmark_e_scrivi(soluzioni, difficolta, sudoku):
    for nome_soluzione, funzione_soluzione in soluzioni.items():
        nome_file = os.path.join("risultati", f"risultati_{nome_soluzione.lower()}_{difficolta}.txt")
        
        with open(nome_file, "a") as file:
            file.write(f"Risultati per il solver: {nome_soluzione} - Difficoltà: {difficolta}\n")
            file.write(f"\nTest del Sudoku:\n")
            for riga in sudoku:
                file.write(f"\t{riga}\n")
            
            risultato, tempo = testa_soluzione(funzione_soluzione, sudoku)

            file.write(f"\tTempo: {tempo:.3f} secondi\n")
            file.write(f"\tRicorsioni: {risultato['ricorsioni']}\n")

            if risultato["successo"]:
                file.write(f"\tSoluzione trovata:\n")
                for riga in risultato["soluzione"]:
                    file.write(f"\t{riga}\n")
            else:
                file.write("\tNessuna soluzione trovata\n")
            file.write("=" * 40 + "\n")


# Esegui i test
if __name__ == "__main__":
    soluzioni = {
        "Backtracking": risolvi_sudoku_backtracking,
        "Backtracking_MRV": risolvi_sudoku_MRV,
        "Dancing_Links": solve_sudoku_dancing_links
    }

    # Assicurati che la cartella "risultati" esista
    os.makedirs("risultati", exist_ok=True)

    # Pulizia file risultati
    for nome_soluzione in soluzioni:
        for difficolta in ["facile", "medio", "difficile"]:
            nome_file = os.path.join("risultati", f"risultati_{nome_soluzione.lower()}_{difficolta}.txt")
            if os.path.exists(nome_file):
                os.remove(nome_file)

    # Test per ogni difficoltà
    for _ in range(10): 
        benchmark_e_scrivi(soluzioni, "facile", genera_sudoku_facile())
        benchmark_e_scrivi(soluzioni, "medio", genera_sudoku_medio())
        benchmark_e_scrivi(soluzioni, "difficile", genera_sudoku_difficile())
