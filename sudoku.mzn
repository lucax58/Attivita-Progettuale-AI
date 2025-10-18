include "globals.mzn";

% Dimensione del blocco (3 per Sudoku 9x9)
int: S;

int: N = S * S;

array[1..N, 1..N] of var 1..N: X;
array[1..N, 1..N] of 0..N: givens;

% vincoli: righe, colonne e blocchi
constraint
  forall(i in 1..N) (all_different([X[i, j] | j in 1..N])) /\
  forall(j in 1..N) (all_different([X[i, j] | i in 1..N])) /\
  forall(br in 0..S-1, bc in 0..S-1) (
    all_different([
      X[br*S + r, bc*S + c] | r in 1..S, c in 1..S
    ])
  );

% vincoli: celle già riempite
constraint
  forall(i, j in 1..N where givens[i, j] != 0) (
    X[i, j] = givens[i, j]
  );

solve satisfy;

output [
  if j = 1 then "\n" else " " endif ++ show(X[i, j])
  | i in 1..N, j in 1..N
];
