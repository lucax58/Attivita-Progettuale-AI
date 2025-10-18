import time
import statistics
import subprocess
import minizinc
from pathlib import Path
from versione_dancing_links import risolvi_sudoku_dancing_links


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
    times = []
    for _ in range(runs):
        start = time.perf_counter()
        func(*args)
        times.append(time.perf_counter() - start)
    return statistics.mean(times), statistics.stdev(times)

# ===============================
# MINI ZINC SETUP
# ===============================

model = minizinc.Model("sudoku.mzn")
solver_gecode = minizinc.Solver.lookup("gecode")
solver_ortools = minizinc.Solver.lookup("ortools")

def solve_minizinc(solver, puzzle):
    grid = [[int(ch) if ch != '.' else 0 for ch in puzzle[i:i+9]] for i in range(0, 81, 9)]
    instance = minizinc.Instance(solver, model)
    instance["S"] = 3
    instance["givens"] = grid
    result = instance.solve()
    return result

# ===============================
# SOLVER ESTERNI
# ===============================

def solve_fsss2(puzzle):
    """Esegue fsss2.exe passando il Sudoku come argomento"""
    subprocess.run([str(FSSS2_PATH), puzzle], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def solve_fast9r2(puzzle):
    """Esegue fast_solv_9r2.exe passando il Sudoku come argomento"""
    subprocess.run([str(FASTSOLV_PATH), puzzle], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# ===============================
# LOOP DI TEST
# ===============================

def run_tests():
    for level_name, file_path in LEVELS.items():
        puzzles = read_puzzles(file_path)
        print(f"\n📘 Livello: {level_name} ({len(puzzles)} puzzle)\n{'-'*50}")

        results = {
            "DLX": {"mean": [], "std": []},
            "Gecode": {"mean": [], "std": []},
            "OR-Tools": {"mean": [], "std": []},
            "FSSS2": {"mean": [], "std": []},
            "Fast9r2": {"mean": [], "std": []},
        }

        for idx, puzzle in enumerate(puzzles, 1):
            print(f"▶️  Puzzle {idx}/{len(puzzles)}")

            # --- DLX (Python)
            t_dlx, std_dlx = measure_time(lambda: risolvi_sudoku_dancing_links((3,3), puzzle), runs=RUNS_PER_PUZZLE)
            results["DLX"]["mean"].append(t_dlx)
            results["DLX"]["std"].append(std_dlx)

            # --- MiniZinc Gecode
            t_gecode, std_gecode = measure_time(lambda: solve_minizinc(solver_gecode, puzzle), runs=RUNS_PER_PUZZLE)
            results["Gecode"]["mean"].append(t_gecode)
            results["Gecode"]["std"].append(std_gecode)

            # --- MiniZinc OR-Tools
            t_ortools, std_ortools = measure_time(lambda: solve_minizinc(solver_ortools, puzzle), runs=RUNS_PER_PUZZLE)
            results["OR-Tools"]["mean"].append(t_ortools)
            results["OR-Tools"]["std"].append(std_ortools)

            # --- FSSS2 (eseguibile)
            t_fsss2, std_fsss2 = measure_time(lambda: solve_fsss2(puzzle), runs=RUNS_PER_PUZZLE)
            results["FSSS2"]["mean"].append(t_fsss2)
            results["FSSS2"]["std"].append(std_fsss2)

            # --- Fast Solver 9r2 (eseguibile)
            t_fast9, std_fast9 = measure_time(lambda: solve_fast9r2(puzzle), runs=RUNS_PER_PUZZLE)
            results["Fast9r2"]["mean"].append(t_fast9)
            results["Fast9r2"]["std"].append(std_fast9)

            print(
                f"DLX: {t_dlx*1000:.2f}±{std_dlx*1000:.2f} ms | "
                f"Gecode: {t_gecode*1000:.2f}±{std_gecode*1000:.2f} ms | "
                f"OR-Tools: {t_ortools*1000:.2f}±{std_ortools*1000:.2f} ms | "
                f"FSSS2: {t_fsss2*1000:.2f}±{std_fsss2*1000:.2f} ms | "
                f"Fast9r2: {t_fast9*1000:.2f}±{std_fast9*1000:.2f} ms"
            )

        # --- Salva i risultati per ogni solver (media e std separate)
        for solver_name, data in results.items():
            # File con le medie
            out_file_mean = RESULTS_DIR / f"{solver_name.lower()}_{level_name}_mean.txt"
            with open(out_file_mean, "w") as f:
                for t in data["mean"]:
                    f.write(f"{t:.6f}\n")
            
            # File con le deviazioni standard
            out_file_std = RESULTS_DIR / f"{solver_name.lower()}_{level_name}_std.txt"
            with open(out_file_std, "w") as f:
                for s in data["std"]:
                    f.write(f"{s:.6f}\n")
            
            print(f"💾 Salvato {solver_name}: {out_file_mean.name} e {out_file_std.name}")

        # --- Pausa manuale tra livelli
        if level_name != "difficile":
            input("\n⏸️  Premi INVIO per continuare con il livello successivo...\n")

if __name__ == "__main__":
    run_tests()