import pygame
import pygame.locals as pl
import pygame.freetype
import time

from versione_dancing_links import risolvi_sudoku_dancing_links
from generatore_sudoku import genera_sudoku_facile

viola = (157, 107, 237)
nero = (0, 0, 0)

def main():
    valoriSudoku = [[None] * 9 for _ in range(9)]
    soluzioneSudoku = [[None] * 9 for _ in range(9)]
    tempoRisoluzione = [""]  # stringa per mostrare il tempo

    scriviValoriIniziali(valoriSudoku)

    bottoneRisolvi = {"x": 120, "y": 640, "name": "Risolvi!", "clicked": False}
    bottoneGenera = {"x": 260, "y": 640, "name": "Genera!", "clicked": False}

    selezioneCorrente = (None, None)
    inEsecuzione = True

    while inEsecuzione:
        schermo.fill((240, 240, 240))

        disegnaGriglia()
        scriviNumeri(valoriSudoku, nero)
        scriviNumeri(soluzioneSudoku, viola)
        evidenziaCasella(selezioneCorrente, viola)
        disegnaBottone(bottoneRisolvi)
        disegnaBottone(bottoneGenera)

        # mostra il tempo
        fontSoluzioni.render_to(schermo, (380, 655), "Tempo: " + tempoRisoluzione[0], viola)

        eventi = pygame.event.get()
        for evento in eventi:
            if evento.type == pygame.QUIT:
                inEsecuzione = False

            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                selezioneCorrente = clickToGriglia(x, y)

                if cliccato(bottoneRisolvi, x, y):
                    bottoneRisolvi["clicked"] = True
                    tempoRisoluzione[0] = risolviPuzzle(valoriSudoku, soluzioneSudoku)

                if cliccato(bottoneGenera, x, y):
                    bottoneGenera["clicked"] = True
                    griglia_generata = genera_sudoku_facile()
                    
                    # Converti la griglia generata nel formato corretto
                    for r in range(9):
                        for c in range(9):
                            if griglia_generata[r][c] == 0:
                                valoriSudoku[c][r] = None
                            else:
                                valoriSudoku[c][r] = str(griglia_generata[r][c])
                    
                    soluzioneSudoku[:] = [[None] * 9 for _ in range(9)]
                    tempoRisoluzione[0] = ""

            if evento.type == pygame.MOUSEBUTTONUP:
                bottoneRisolvi["clicked"] = False
                bottoneGenera["clicked"] = False

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


def disegnaGriglia():
    fontTitolo.render_to(schermo, (int(larghezza / 2) - 155, 20), "Risolutore Sudoku", nero)

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
    # Non mostrare None, 0 o "0"
    if numero is not None and numero != 0 and numero != "0":
        numero = str(numero)
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


def risolviPuzzle(valoriSudoku, valoriSoluzione):
    print("Sto risolvendo il sudoku usando Dancing Links...")
    griglia = []
    for r in range(9):
        riga = []
        for c in range(9):
            val = valoriSudoku[c][r]
            # Tratta sia None che "0" come celle vuote
            if val is None or val == "0" or val == 0:
                riga.append(0)
            else:
                riga.append(int(val))
        griglia.append(riga)

    start = time.time()
    risultato = risolvi_sudoku_dancing_links((3, 3), griglia)
    end = time.time()

    if risultato["successo"]:
        for r in range(9):
            for c in range(9):
                # Solo per le celle che erano vuote, mostra la soluzione
                val_originale = valoriSudoku[c][r]
                if val_originale is None or val_originale == "0" or val_originale == 0:
                    valoriSoluzione[c][r] = str(risultato["soluzione"][r][c])
        print("Sudoku risolto!")
    else:
        print("Nessuna soluzione trovata!")

    durata = end - start
    return f"{durata:.3f} s"


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