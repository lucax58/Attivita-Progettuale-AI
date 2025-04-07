# import the pygame module, so you can use it
import pygame
import pygame.locals as pl
import pygame.freetype

import os
import platform
import subprocess
from subprocess import Popen, PIPE, check_output


purple = (157, 107, 237)
black = (0,0,0)
# define a main function
def main():
    sudokuValues = [[None] * 9 for i in range(9)]
    sudokuSolutionValues = [[None] * 9 for i in range(9)]
    numSolutions = [""]
    writeStartValues(sudokuValues)
    solveButton = {"x": 120, "y": 640, "name": "Solve!", "clicked": False}
    clearButton = {"x": 260, "y": 640, "name": "Clear!", "clicked": False}

    enteringNumbers = False
    currentSelected = (None, None)
    #Start the path picking main loop
    running = True
    while running:
        #refresh the screen
        screen.fill((240,240,240))
        drawSudokuGrid(numSolutions)
        writeNumbers(sudokuValues, black)
        writeNumbers(sudokuSolutionValues, purple)
        highlightSquare(currentSelected, purple)
        drawButton(solveButton)
        drawButton(clearButton)

        #handle game events
        events = pygame.event.get()
        for event in events:
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                currentSelected = mouseToGrid(x,y)

                if buttonClicked(solveButton, x, y):
                    solveButton["clicked"] = True
                    solvePuzzle(sudokuValues, sudokuSolutionValues, numSolutions)

                if buttonClicked(clearButton, x, y):
                    clearButton["clicked"] = True
                    sudokuValues = [[None] * 9 for i in range(9)]
                    sudokuSolutionValues = [[None] * 9 for i in range(9)]

            if event.type == pygame.MOUSEBUTTONUP:
                solveButton["clicked"] = False
                clearButton["clicked"] = False

            if event.type == pygame.KEYDOWN:
                #Check to see if there is a selected square
                if currentSelected[0] != None and currentSelected[1] != None:
                    if event.unicode.isnumeric():
                        newNumber = event.unicode[0]
                        if(newNumber != "0"):
                            sudokuValues[currentSelected[0]][currentSelected[1]] = newNumber
                            sudokuSolutionValues[currentSelected[0]][currentSelected[1]] = None
                    if event.key == pl.K_BACKSPACE:
                        sudokuValues[currentSelected[0]][currentSelected[1]] = None
                        sudokuSolutionValues[currentSelected[0]][currentSelected[1]] = None

        #screen.blit(currentFrame, currentFrameRect)
        pygame.display.flip()

    #Shut down the pygame window
    pygame.display.quit()
    pygame.quit()


width = height = 700
#Start the pygame window
pygame.init()
pygame.display.set_caption("Sudoku solver")
screen = pygame.display.set_mode((width,height))

titalFont = pygame.freetype.SysFont("georgia", 45)
numberFont = pygame.freetype.SysFont("georgia", 55)
buttonFont = pygame.freetype.SysFont("georgia", 25)
numSolutionsFont = pygame.freetype.SysFont("georgia", 30)
#print(pygame.font.get_fonts())


boarderSize = 70
boxWidth = int((width-(2*boarderSize))/9)

buttonWidth = 100
buttonHeight = 50


gray = (80,80,80)
black = (0,0,0)

def drawSudokuGrid(numSolutions):
    titalFont.render_to(screen, (int(width/2) -155, 20), "Sudoku Solver", (0, 0, 0))
    num = str(numSolutions[0])
    numSolutionsFont.render_to(screen, (380, 655), "# Solutions: "+num, purple)

    thinLineWidth = 3
    thickLineWidth = 10

    for columNum in range(10):
        #Subtract thickLineWidth/2 to get rid of parts missing from the corners
        startX = int(columNum*boxWidth)+boarderSize
        startY = boarderSize - (thickLineWidth//2 -1)
        endY = height - boarderSize + (thickLineWidth//2-2)

        if columNum % 3 ==0: #Draw thick lines
            #vertical lines
            pygame.draw.line(screen, black, [startX, startY], [startX, endY], thickLineWidth)
            #horizontal lines
            pygame.draw.line(screen, black, [startY, startX], [endY, startX], thickLineWidth)
        else: #Draw thin lines
            #vertical lines
            pygame.draw.line(screen, black, [startX, startY], [startX, endY], thinLineWidth)
            #horizontalLInes
            pygame.draw.line(screen, black, [startY, startX], [endY, startX], thinLineWidth)

def drawButton(button):
    pygame.draw.rect(screen,(200,200,200),(button["x"], button["y"], buttonWidth, buttonHeight))
    buttonFont.render_to(screen, (button["x"]+15, button["y"]+15), button["name"], (0, 0, 0))

    if button["clicked"]:
        pygame.draw.rect(screen, purple,(button["x"], button["y"], buttonWidth, buttonHeight), 7)

def buttonClicked(button, x, y):
    if x > button["x"] and x < button["x"]+buttonWidth and y > button["y"] and y < button["y"]+buttonHeight:
        return True

    return False


def writeNumber(number, col, row, color):
    if number != None:
        xCordinate = int((col*boxWidth)+(boarderSize*1.24))
        yCordinate = int((row*boxWidth)+(boarderSize*1.165))
        numberFont.render_to(screen, (xCordinate, yCordinate), number, color)

def writeNumbers(sudokuNumbers, color):
    for col in range(9):
        for row in range(9):
            writeNumber(sudokuNumbers[col][row], col, row, color)

def mouseToGrid(x, y):
    col = ((x - boarderSize)//boxWidth)
    row = ((y - boarderSize)//boxWidth)

    if col < 0 or row < 0 or col > 8 or row > 8:
        print("Click outside grid")
        return (None, None)

    print(col+1, row+1)
    return (col, row)

def highlightSquare(currentSelected, color):
    col, row = currentSelected

    #check for null values and don't do anything if null
    if(col != None and row != None):
        rectX = int((col*boxWidth)+boarderSize)
        rectY = int((row*boxWidth)+boarderSize)

        pygame.draw.rect(screen, color, (rectX, rectY, boxWidth, boxWidth), 7)

def solvePuzzle(sudokuValues, sudokuSolutionValues, numSolutions):
    print("solving the puzzle")

    f = open("sudokuNumbers.txt", "w")
    for col in range(9):
        for row in range(9):
            if sudokuValues[row][col] != None:
                f.write(sudokuValues[row][col])
            else:
                f.write("-")
        f.write("\n")

    f.close()


    p = subprocess.call('./sudokuC/cmake-build-debug/sudokuC', stdin=None, stdout=None, stderr=None, shell=True)

    print("Finished!")

    f = open("solutions.txt", "r")
    numSolutions[0] = f.readline()
    if numSolutions[0] == "0":
        print("No solution")
    else:
        for row in range(9):
            rowString = f.readline()
            for col in range(9):
                value = rowString[col]
                if value.isnumeric():
                    sudokuSolutionValues[col][row] = value

    f.close()

    #display the solved outputs

def writeStartValues(sudokuValues):
    sudokuValues[0][0] = "5"
    sudokuValues[1][0] = "3"
    sudokuValues[4][0] = "7"

    sudokuValues[0][1] = "6"
    sudokuValues[3][1] = "1"
    sudokuValues[4][1] = "9"
    sudokuValues[5][1] = "5"

    sudokuValues[1][2] = "9"
    sudokuValues[2][2] = "8"
    sudokuValues[7][2] = "6"

    sudokuValues[0][3] = "8"
    sudokuValues[4][3] = "6"
    sudokuValues[8][3] = "3"

    sudokuValues[0][4] = "4"
    sudokuValues[3][4] = "8"
    sudokuValues[5][4] = "3"
    sudokuValues[8][4] = "1"

    sudokuValues[0][5] = "7"
    sudokuValues[4][5] = "2"
    sudokuValues[8][5] = "6"

    sudokuValues[1][6] = "6"
    sudokuValues[6][6] = "2"
    sudokuValues[7][6] = "8"

    sudokuValues[3][7] = "4"
    sudokuValues[4][7] = "1"
    sudokuValues[5][7] = "9"
    sudokuValues[8][7] = "5"

    sudokuValues[4][8] = "8"
    sudokuValues[7][8] = "7"
    sudokuValues[8][8] = "9"


if __name__=="__main__":
    main()