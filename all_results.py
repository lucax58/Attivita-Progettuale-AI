import statistics
from pathlib import Path

RESULTS_DIR = Path("results")
OUTPUT_FILE = RESULTS_DIR / "summary.txt"

def parse_filename(filename):

    parts = filename.stem.split('_')
    if len(parts) >= 2:
        solver = '_'.join(parts[:-1])  # tutto tranne l'ultima parte
        difficulty = parts[-1]  # ultima parte
        return solver.upper(), difficulty
    return None, None

def read_times(file_path):
    """Legge i tempi dal file e li restituisce come lista di float"""
    with open(file_path, 'r') as f:
        return [float(line.strip()) for line in f if line.strip()]

def main():
    # Dizionario per organizzare i risultati
    results = {}
    
    # Leggi tutti i file .txt nella cartella results
    for file_path in sorted(RESULTS_DIR.glob("*.txt")):
        if file_path.name == "summary.txt":
            continue  # Salta il file di output
        
        solver, difficulty = parse_filename(file_path)
        if solver and difficulty:
            times = read_times(file_path)
            mean_time = statistics.mean(times)
            
            # Organizza per solver
            if solver not in results:
                results[solver] = {}
            results[solver][difficulty] = mean_time
            
            print(f" Letto {file_path.name}: media = {mean_time*1000:.2f} ms")
    
    # Scrivi il file riassuntivo
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("RIASSUNTO BENCHMARK SUDOKU SOLVER\n")
        f.write(f"{'Solver':<20} {'Difficoltà':<15} {'Media (ms)':<15}\n")
        f.write("-" * 70 + "\n")
        
        # Ordine delle difficoltà
        difficulty_order = ['facile', 'medio', 'difficile']
        
        for solver in sorted(results.keys()):
            for difficulty in difficulty_order:
                if difficulty in results[solver]:
                    mean_ms = results[solver][difficulty] * 1000
                    f.write(f"{solver:<20} {difficulty:<15} {mean_ms:>12.2f}\n")
            f.write("-" * 70 + "\n")
    
    print(f"\n File riassuntivo salvato in: {OUTPUT_FILE}")
    print("\nContenuto:")
    print("=" * 70)
    with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
        print(f.read())

if __name__ == "__main__":
    main()