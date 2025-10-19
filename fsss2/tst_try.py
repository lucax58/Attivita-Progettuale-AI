import subprocess
import time
from pathlib import Path

# Percorso dell’eseguibile (rilevato automaticamente)
SOLVER_PATH = Path.cwd() / "fsss2" / "fsss2.exe"  # oppure Path.cwd() / "fsss2" / "fsss2.exe" se è in sottocartella

# Puzzle di test (81 caratteri, . = cella vuota)
puzzle = "53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79"

def test_solver():
    print(f"🔍 Test del solver FSSS2: {SOLVER_PATH}")
    print("Puzzle di test:")
    print(puzzle)

    if not SOLVER_PATH.exists():
        print(f"❌ Errore: solver non trovato → {SOLVER_PATH}")
        return

    try:
        start = time.time()

        # Invoca il solver passando il puzzle su stdin
        result = subprocess.run(
            [str(SOLVER_PATH)],
            input=puzzle,
            capture_output=True,
            text=True,
            timeout=10
        )

        elapsed = (time.time() - start) * 1000  # tempo in ms
        print(f"\n⏱️ Tempo di esecuzione: {elapsed:.3f} ms")

        if result.returncode != 0:
            print(f"❌ Solver terminato con codice {result.returncode}")
            print("STDERR:", result.stderr.strip())
        else:
            print("✅ Output solver:")
            print(result.stdout.strip())

    except subprocess.TimeoutExpired:
        print("⏰ Timeout: il solver ha impiegato troppo tempo.")
    except Exception as e:
        print(f"⚠️ Errore: {e}")

if __name__ == "__main__":
    test_solver()
