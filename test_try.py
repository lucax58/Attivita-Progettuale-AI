import time
import statistics
import subprocess
import minizinc
from pathlib import Path
from versione_dancing_links import risolvi_sudoku_dancing_links
from ortools.sat.python import cp_model


DATA_DIR = Path("data")
RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)

RUNS_PER_PUZZLE = 100

# Dataset per livello
LEVELS = {
    "facile": DATA_DIR / "sudoku_easy.txt",
    "medio": DATA_DIR / "sudoku_medio.txt",
    "difficile": DATA_DIR / "sudoku_hard.txt",
}

# Percorsi solver esterni (aggiornali se diverso)
FSSS2_PATH = Path("fsss2/fsss2.exe")
FASTSOLV_PATH = Path("fast_solv_9r2/fast_solv_9r2.exe")

# ===============================
# FUNZIONI DI SUPPORTO
# ===============================

def read_puzzles(file_path):
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def measure_time(func, *args, runs=100):
    print(f"[Inizio {runs} run...]", end=" ", flush=True)
    times = []
    for i in range(runs):
        if i % 10 == 0:  # Stampa ogni 10 run
            print(f"{i}...", end="", flush=True)
        start = time.perf_counter()
        func(*args)
        times.append(time.perf_counter() - start)
    print(f"{runs}!", end=" ", flush=True)
    return statistics.mean(times)

# ===============================
# MINI ZINC SETUP
# ===============================

model = minizinc.Model("sudoku.mzn")
solver_gecode = minizinc.Solver.lookup("gecode")
solver_ortools_mzn = minizinc.Solver.lookup("cp-sat")

def solve_minizinc(solver, puzzle):
    grid = [[int(ch) if ch != '.' else 0 for ch in puzzle[i:i+9]] for i in range(0, 81, 9)]
    instance = minizinc.Instance(solver, model)
    instance["S"] = 3
    instance["givens"] = grid
    result = instance.solve()
    return result

# ===============================
# OR-TOOLS NATIVO
# ===============================

def solve_ortools_native(puzzle_string):
    """Risolve Sudoku usando OR-Tools CP-SAT nativo (ottimizzato)"""
    # Parsing del puzzle
    grid = []
    for char in puzzle_string:
        if char == '.':
            grid.append(0)
        else:
            grid.append(int(char))
    
    # Creazione del modello
    model = cp_model.CpModel()
    
    # Variabili: 9x9 griglia, ogni cella può avere valore 1-9
    cells = {}
    for i in range(9):
        for j in range(9):
            cells[(i, j)] = model.NewIntVar(1, 9, f'cell_{i}_{j}')
    
    # Vincolo 1: Fissa i numeri già presenti (givens)
    for i in range(9):
        for j in range(9):
            idx = i * 9 + j
            if grid[idx] != 0:
                model.Add(cells[(i, j)] == grid[idx])
    
    # Vincolo 2: Ogni riga contiene tutti i numeri da 1 a 9
    for i in range(9):
        model.AddAllDifferent([cells[(i, j)] for j in range(9)])
    
    # Vincolo 3: Ogni colonna contiene tutti i numeri da 1 a 9
    for j in range(9):
        model.AddAllDifferent([cells[(i, j)] for i in range(9)])
    
    # Vincolo 4: Ogni box 3x3 contiene tutti i numeri da 1 a 9
    for box_i in range(3):
        for box_j in range(3):
            box_cells = []
            for i in range(3):
                for j in range(3):
                    box_cells.append(cells[(box_i * 3 + i, box_j * 3 + j)])
            model.AddAllDifferent(box_cells)
    
    # Risoluzione
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.log_search_progress = False
    
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        solution = []
        for i in range(9):
            for j in range(9):
                solution.append(solver.Value(cells[(i, j)]))
        return solution
    else:
        return None

# ===============================
# SOLVER ESTERNI
# ===============================

def solve_fsss2(puzzle):
    """Esegue fsss2.exe passando il Sudoku su stdin"""
    subprocess.run(
        [str(FSSS2_PATH)], 
        input=puzzle,
        text=True,
        stdout=subprocess.DEVNULL, 
        stderr=subprocess.DEVNULL
    )

def solve_fast9r2(puzzle):
    """Esegue fast_solv_9r2.exe passando il Sudoku su stdin"""
    subprocess.run(
        [str(FASTSOLV_PATH)],
        input=puzzle,
        text=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

# ===============================
# LOOP DI TEST
# ===============================

def run_tests():
    for level_name, file_path in LEVELS.items():
        puzzles = read_puzzles(file_path)
        print(f"\n Livello: {level_name} ({len(puzzles)} puzzle)\n{'-'*70}")

        results = {
            "DLX": [],
            "Gecode": [],
            "OR-Tools-MZN": [],
            "OR-Tools-Native": [],
            "FSSS2": [],
            "Fast9r2": [],
        }

        for idx, puzzle in enumerate(puzzles, 1):
            print(f"\n Puzzle {idx}/{len(puzzles)}")

            # --- DLX (Python)
            print("  Testing DLX...", end=" ", flush=True)
            t_dlx = measure_time(lambda: risolvi_sudoku_dancing_links((3,3), puzzle), runs=RUNS_PER_PUZZLE)
            results["DLX"].append(t_dlx)
            print(f"✓ {t_dlx*1000:.2f} ms")

            # --- MiniZinc Gecode
            print("  Testing Gecode...", end=" ", flush=True)
            t_gecode = measure_time(lambda: solve_minizinc(solver_gecode, puzzle), runs=RUNS_PER_PUZZLE)
            results["Gecode"].append(t_gecode)
            print(f"✓ {t_gecode*1000:.2f} ms")

            # --- MiniZinc OR-Tools
            print("  Testing OR-Tools (MZN)...", end=" ", flush=True)
            t_ortools_mzn = measure_time(lambda: solve_minizinc(solver_ortools_mzn, puzzle), runs=RUNS_PER_PUZZLE)
            results["OR-Tools-MZN"].append(t_ortools_mzn)
            print(f"✓ {t_ortools_mzn*1000:.2f} ms")

            # --- OR-Tools Native
            print("  Testing OR-Tools (Native)...", end=" ", flush=True)
            t_ortools_native = measure_time(lambda: solve_ortools_native(puzzle), runs=RUNS_PER_PUZZLE)
            results["OR-Tools-Native"].append(t_ortools_native)
            print(f"✓ {t_ortools_native*1000:.2f} ms")

            # --- FSSS2 (eseguibile)
            print("  Testing FSSS2...", end=" ", flush=True)
            t_fsss2 = measure_time(lambda: solve_fsss2(puzzle), runs=RUNS_PER_PUZZLE)
            results["FSSS2"].append(t_fsss2)
            print(f"✓ {t_fsss2*1000:.2f} ms")

            # --- Fast Solver 9r2 (eseguibile)
            print("  Testing Fast9r2...", end=" ", flush=True)
            t_fast9 = measure_time(lambda: solve_fast9r2(puzzle), runs=RUNS_PER_PUZZLE)
            results["Fast9r2"].append(t_fast9)
            print(f"✓ {t_fast9*1000:.2f} ms")

            print(
                f"  DLX: {t_dlx*1000:.2f} ms | "
                f"Gecode: {t_gecode*1000:.2f} ms | "
                f"OR-Tools(MZN): {t_ortools_mzn*1000:.2f} ms | "
                f"OR-Tools(Native): {t_ortools_native*1000:.2f} ms\n"
                f"  FSSS2: {t_fsss2*1000:.2f} ms | "
                f"Fast9r2: {t_fast9*1000:.2f} ms"
            )

        # --- Salva i risultati per ogni solver
        for solver_name, times in results.items():
            out_file = RESULTS_DIR / f"{solver_name.lower()}_{level_name}.txt"
            with open(out_file, "w") as f:
                for t in times:
                    f.write(f"{t:.6f}\n")
            
            print(f"Salvato {solver_name}: {out_file.name}")

        # --- Pausa manuale tra livelli
        if level_name != "difficile":
            input("\n  Premi INVIO per continuare con il livello successivo...\n")

if __name__ == "__main__":
    run_tests()