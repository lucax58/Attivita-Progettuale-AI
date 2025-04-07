import pygame
import sys
import time
from versione_dancing_links import solve_sudoku


pygame.init()

# Dimensioni
LARGHEZZA_FINESTRA = 800
ALTEZZA_FINESTRA = 800

fastest_time = None
# Colori
NERO = (0, 0, 0)
BIANCO = (255, 255, 255)
GRIGIO = (200, 200, 200)
BLU = (50, 50, 200)

# Finestra
finestra = pygame.display.set_mode((LARGHEZZA_FINESTRA, ALTEZZA_FINESTRA))
pygame.display.set_caption("Sudoku")

#  Font
font = pygame.font.SysFont("arial", 40, bold=True)

#Griglia iniziale
board = [ 
    [0,0,0,0,0,0,5,7,3],
    [8,0,0,0,2,0,0,0,0],
    [7,0,0,9,0,0,8,1,0],
    [5,8,0,7,0,6,0,0,0],
    [0,0,1,8,0,0,0,6,0],
    [2,3,0,0,4,0,0,0,9],
    [9,1,5,0,0,0,0,0,0],
    [0,0,0,0,8,0,6,0,1],
    [0,0,0,0,0,0,0,4,0]
]

#Disegna la griglia
def draw_grid():
    finestra.fill(BIANCO)
    
    for i in range(10):  
        spessore = 4 if i % 3 == 0 else 1  # Linee più spesse per separare i blocchi
        pygame.draw.line(finestra, NERO, (i * 50, 0), (50 * i, 450), spessore)
        pygame.draw.line(finestra, NERO, (0, 50 * i), (450, 50 * i), spessore)

# Stampa i numeri
def draw_board(board):
    draw_grid()
    
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                numero = font.render(str(board[i][j]), True, BLU)
                finestra.blit(numero, (j * 50 + 15, i * 50 + 10 ))
    
    pygame.display.update()

def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x + w > mouse[0] > x and y+h > mouse[1] > y: 
        pygame.draw.rect(finestra, ac, (x, y, w, h))
        if click[0] == 1 and action != None: 
            action()
    else:
        pygame.draw.rect(finestra, ic, (x, y, w, h))

    text_surf = font.render(msg, True, NERO)
    text_rect = text_surf.get_rect(center = ((x + (w/2)), (y + (h/2))))
    finestra.blit(text_surf, text_rect)
    # Non aggiorniamo qui il display perché lo faremo nel loop principale


def solve(): 
    size = (3, 3)
    start_time = time.time()
    for solution in solve_sudoku(size, board): 
        for i in range(9): 
            for j in range(9): 
                board[i][j] = solution[i][j]
        draw_board(board)
        break
    end_time = time.time()
    elapsed_time = end_time - start_time
    if fastest_time is None or elapsed_time < fastest_time: 
        fastest_time = elapsed_time

def display_time(): 
    if fastest_time is not None: 
        fastest_time_surf = font.render(f"Fastest Time: {fastest_time: .4f}sec", True, BIANCO)
        finestra.blit(fastest_time_surf, (500, 160))

#Loop di gioco
def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        draw_board(board)  # Disegna la griglia e i numeri
        
        # Disegna il bottone con colori diversi
        button("Solve", 450, 20, 100, 50, GRIGIO, BLU, solve)
        
        # Aggiorna il display una volta dopo aver disegnato tutto
        pygame.display.update()

    pygame.quit()
    sys.exit()


main()
