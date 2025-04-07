import pygame
import pygame.locals as pl
import pygame.freetype

from versione_dancing_links import solve_sudoku


viola = (157, 107, 237)
nero = (0, 0, 0)

def main():
    valoriSudoku = [[None] * 9 for _ in range(9)]
    soluzioneSudoku = [[None] * 9 for _ in range(9)]
    numeroSoluzioni = [""]

    scriviValoriIniziali(valoriSudoku)

    bottoneRisolvi = {"x": 120, "y": 640, "name": "Risolvi!", "clicked": False}
    bottonePulisci = {"x": 260, "y": 640, "name": "Pulisci!", "clicked": False}

    selezioneCorrente = (None, None)

    inEsecuzione = True
    while inEsecuzione:
        schermo.fill((240, 240, 240))

        disegnaGriglia(numeroSoluzioni)
        scriviNumeri(valoriSudoku, nero)
        scriviNumeri(soluzioneSudoku, viola)
        evidenziaCasella(selezioneCorrente, viola)
        disegnaBottone(bottoneRisolvi)
        disegnaBottone(bottonePulisci)

        eventi = pygame.event.get()
        for evento in eventi:
            if evento.type == pygame.QUIT:
                inEsecuzione = False

            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                selezioneCorrente = clickToGriglia(x, y)

                if cliccato(bottoneRisolvi, x, y):
                    bottoneRisolvi["clicked"] = True
                    risolviPuzzle(valoriSudoku, soluzioneSudoku, numeroSoluzioni)

                if cliccato(bottonePulisci, x, y):
                    bottonePulisci["clicked"] = True
                    valoriSudoku = [[None] * 9 for _ in range(9)]
                    soluzioneSudoku = [[None] * 9 for _ in range(9)]

            if evento.type == pygame.MOUSEBUTTONUP:
                bottoneRisolvi["clicked"] = False
                bottonePulisci["clicked"] = False

            if evento.type == pygame.KEYDOWN:
                col, row = selezioneCorrente
                if col is not None and row is not None:
                    if evento.unicode.isnumeric():
                        cifra = evento.unicode[0]
                        if cifra != "0":
                            valoriSudoku[col][row] = cifra
                            soluzioneSudoku[col][row] = None
                    if evento.key == pl.K_BACKSPACE:
                        valoriSudoku[col][row] = None
                        soluzioneSudoku[col][row] = None

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()


larghezza = altezza = 700
pygame.init()
pygame.display.set_caption("Risolutore Sudoku")
schermo = pygame.display.set_mode((larghezza, altezza))

fontTitolo = pygame.freetype.SysFont("georgia", 45)
fontNumero = pygame.freetype.SysFont("georgia", 55)
fontBottone = pygame.freetype.SysFont("georgia", 25)
fontSoluzioni = pygame.freetype.SysFont("georgia", 30)

margine = 70
larghezzaCella = int((larghezza - (2 * margine)) / 9)

larghezzaBottone = 100
altezzaBottone = 50

grigio = (80, 80, 80)
nero = (0, 0, 0)


def disegnaGriglia(numeroSoluzioni):
    fontTitolo.render_to(schermo, (int(larghezza / 2) - 155, 20), "Risolutore Sudoku", nero)
    fontSoluzioni.render_to(schermo, (380, 655), "# Soluzioni: " + numeroSoluzioni[0], viola)

    sottile = 3
    spesso = 10

    for i in range(10):
        x = int(i * larghezzaCella) + margine
        y1 = margine - (spesso // 2 - 1)
        y2 = altezza - margine + (spesso // 2 - 2)

        if i % 3 == 0:
            pygame.draw.line(schermo, nero, [x, y1], [x, y2], spesso)
            pygame.draw.line(schermo, nero, [y1, x], [y2, x], spesso)
        else:
            pygame.draw.line(schermo, nero, [x, y1], [x, y2], sottile)
            pygame.draw.line(schermo, nero, [y1, x], [y2, x], sottile)


def disegnaBottone(bottone):
    pygame.draw.rect(schermo, (200, 200, 200), (bottone["x"], bottone["y"], larghezzaBottone, altezzaBottone))
    fontBottone.render_to(schermo, (bottone["x"] + 15, bottone["y"] + 15), bottone["name"], nero)
    if bottone["clicked"]:
        pygame.draw.rect(schermo, viola, (bottone["x"], bottone["y"], larghezzaBottone, altezzaBottone), 7)


def cliccato(bottone, x, y):
    return bottone["x"] < x < bottone["x"] + larghezzaBottone and bottone["y"] < y < bottone["y"] + altezzaBottone


def scriviNumero(numero, col, row, colore):
    if numero is not None:
        x = int((col * larghezzaCella) + (margine * 1.24))
        y = int((row * larghezzaCella) + (margine * 1.165))
        fontNumero.render_to(schermo, (x, y), numero, colore)


def scriviNumeri(griglia, colore):
    for col in range(9):
        for row in range(9):
            scriviNumero(griglia[col][row], col, row, colore)


def clickToGriglia(x, y):
    col = (x - margine) // larghezzaCella
    row = (y - margine) // larghezzaCella
    if not (0 <= col <= 8 and 0 <= row <= 8):
        return (None, None)
    return (col, row)


def evidenziaCasella(selezionata, colore):
    col, row = selezionata
    if col is not None and row is not None:
        x = int(col * larghezzaCella + margine)
        y = int(row * larghezzaCella + margine)
        pygame.draw.rect(schermo, colore, (x, y, larghezzaCella, larghezzaCella), 7)


def risolviPuzzle(valoriSudoku, valoriSoluzione, numSoluzioni):
    print("Sto risolvendo il sudoku usando Dancing Links...")

    # Converti da lista colonne (valoriSudoku[col][row]) a formato [ [riga1], [riga2], ... ]
    griglia = []
    for r in range(9):
        riga = []
        for c in range(9):
            val = valoriSudoku[c][r]
            if val is None:
                riga.append(0)
            else:
                riga.append(int(val))
        griglia.append(riga)

    soluzioni = solve_sudoku((3, 3), griglia)

    try:
        soluzione = next(soluzioni)
        numSoluzioni[0] = "1"  # Dancing Links restituisce solo una soluzione alla volta

        # Inserisci i valori risolti nella matrice soluzione
        for r in range(9):
            for c in range(9):
                if valoriSudoku[c][r] is None:  # Mostra solo i nuovi numeri
                    valoriSoluzione[c][r] = str(soluzione[r][c])

        print("Sudoku risolto!")

    except StopIteration:
        numSoluzioni[0] = "0"
        print("Nessuna soluzione trovata.")


def scriviValoriIniziali(valoriSudoku):
    valoriSudoku[0][0] = "5"
    valoriSudoku[1][0] = "3"
    valoriSudoku[4][0] = "7"

    valoriSudoku[0][1] = "6"
    valoriSudoku[3][1] = "1"
    valoriSudoku[4][1] = "9"
    valoriSudoku[5][1] = "5"

    valoriSudoku[1][2] = "9"
    valoriSudoku[2][2] = "8"
    valoriSudoku[7][2] = "6"

    valoriSudoku[0][3] = "8"
    valoriSudoku[4][3] = "6"
    valoriSudoku[8][3] = "3"

    valoriSudoku[0][4] = "4"
    valoriSudoku[3][4] = "8"
    valoriSudoku[5][4] = "3"
    valoriSudoku[8][4] = "1"

    valoriSudoku[0][5] = "7"
    valoriSudoku[4][5] = "2"
    valoriSudoku[8][5] = "6"

    valoriSudoku[1][6] = "6"
    valoriSudoku[6][6] = "2"
    valoriSudoku[7][6] = "8"

    valoriSudoku[3][7] = "4"
    valoriSudoku[4][7] = "1"
    valoriSudoku[5][7] = "9"
    valoriSudoku[8][7] = "5"

    valoriSudoku[4][8] = "8"
    valoriSudoku[7][8] = "7"
    valoriSudoku[8][8] = "9"


if __name__ == "__main__":
    main()
