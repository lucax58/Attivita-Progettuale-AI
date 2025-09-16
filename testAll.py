import time
import os
import statistics

from versione_backtraking_base import risolvi_sudoku_backtracking 
from versione_backtraking_MRV import risolvi_sudoku_MRV
from versione_dancing_links import risolvi_sudoku_dancing_links
from generatore_sudoku import genera_sudoku_difficile
from generatore_sudoku import genera_sudoku_medio
from generatore_sudoku import genera_sudoku_facile


#Funzione per testare una singola soluzione
def testa_soluzione(soluzione, sudoku):
    start_time = time.time()
    risultato = soluzione((3, 3), sudoku)  # Ogni solver restituisce un dizionario
    end_time = time.time()
    tempo_trascorso = end_time - start_time
    return risultato, tempo_trascorso


# Funzione per eseguire il benchmark per ogni solver e scrivere i risultati in file separati
def benchmark_e_scrivi(soluzioni, difficolta, sudoku, stats):
    for nome_soluzione, funzione_soluzione in soluzioni.items():
        nome_file = os.path.join("risultati", f"risultati_{nome_soluzione.lower()}_{difficolta}.txt")
        
        with open(nome_file, "a") as file:  # Usa "a" per appendere invece di sovrascrivere
            file.write(f"Risultati per il solver: {nome_soluzione} - Difficoltà: {difficolta}\n")
            file.write(f"\nTest del Sudoku:\n")
            # Stampa il sudoku in formato leggibile
            for riga in sudoku:
                file.write(f"\t{riga}\n")
            
            # Testa solo la soluzione corrente
            risultato, tempo = testa_soluzione(funzione_soluzione, sudoku)
            
            if risultato["successo"]:
                file.write(f"\tTempo: {tempo:.3f} secondi\n")
                file.write(f"\tRicorsioni: {risultato['ricorsioni']}\n")
                file.write(f"\tSoluzione trovata:\n")
                # Stampa la soluzione in formato leggibile
                for riga in risultato["soluzione"]:
                    file.write(f"\t{riga}\n")

                # Salva le statistiche in memoria
                stats[nome_soluzione][difficolta]["tempi"].append(tempo)
                stats[nome_soluzione][difficolta]["ricorsioni"].append(risultato["ricorsioni"])

            else:
                file.write(f"\tTempo: {tempo:.3f} secondi\n")
                file.write("\tNessuna soluzione trovata\n")
            file.write("="*40 + "\n")  # Separatore tra i test dei Sudoku


# Scrive statistiche totali
def scrivi_statistiche_totali(stats):
    nome_file = os.path.join("risultati", "statistiche_riassuntive.txt")
    with open(nome_file, "w") as file:
        file.write("Statistiche Riassuntive dei Solver\n")
        file.write("="*50 + "\n\n")

        for solver, difficolta_data in stats.items():
            file.write(f"Solver: {solver}\n")
            for diff, dati in difficolta_data.items():
                if dati["tempi"]:  # se ci sono dati
                    tempo_medio = statistics.mean(dati["tempi"])
                    tempo_min = min(dati["tempi"])
                    tempo_max = max(dati["tempi"])
                    ricorsioni_medie = statistics.mean(dati["ricorsioni"])
                    ricorsioni_min = min(dati["ricorsioni"])
                    ricorsioni_max = max(dati["ricorsioni"])

                    file.write(f"  Difficolta: {diff}\n")
                    file.write(f"    Tempo Medio: {tempo_medio:.4f} s | Min: {tempo_min:.4f} s | Max: {tempo_max:.4f} s\n")
                    file.write(f"    Ricorsioni Medie: {ricorsioni_medie:.0f} | Min: {ricorsioni_min} | Max: {ricorsioni_max}\n")
            file.write("-"*50 + "\n")


# Esegui i test
if __name__ == "__main__":

    # Crea cartella risultati
    if not os.path.exists("risultati"):
        os.makedirs("risultati")

    # Inizializza le soluzioni come dizionario
    soluzioni = {
        "Backtraking": risolvi_sudoku_backtracking, 
        "Backtraking_MRV": risolvi_sudoku_MRV,    
        "Dancing_links": risolvi_sudoku_dancing_links  
    }

    # Struttura per salvare statistiche
    stats = {
        nome: {
            "facile": {"tempi": [], "ricorsioni": []},
            "medio": {"tempi": [], "ricorsioni": []},
            "difficile": {"tempi": [], "ricorsioni": []}
        }
        for nome in soluzioni
    }

    # Rimuove i file dei risultati precedenti se esistono
    for nome_soluzione in soluzioni:
        for difficolta in ["facile", "medio", "difficile"]:
            nome_file = os.path.join("risultati", f"risultati_{nome_soluzione.lower()}_{difficolta}.txt")
            if os.path.exists(nome_file):
                os.remove(nome_file)

    # Eseguo test per ogni livello di difficoltà
    for i in range(20): 
        sudoku = genera_sudoku_facile()
        benchmark_e_scrivi(soluzioni, "facile", sudoku, stats)

    for i in range(20): 
        sudoku = genera_sudoku_medio()
        benchmark_e_scrivi(soluzioni, "medio", sudoku, stats)

    for i in range(20): 
        sudoku = genera_sudoku_difficile()
        benchmark_e_scrivi(soluzioni, "difficile", sudoku, stats)

   
    scrivi_statistiche_totali(stats)
