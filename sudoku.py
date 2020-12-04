# sudoku.py
# ============================================================================
# Name: Patrick Glowacki
# Date: November 27, 2020
# Description: CS325_400_F2020 Homework 8: Portfolio Project 
#              This program is a sudou solution verifier. A 9x9 sudoku board
#              is hard-coded as a starting point and the user can select their
#              solutions. The program checks the user solutions against the 
#              game criteria to verify if the solution is correct or not. 
# Source: The sudoku pygame GUI is based off the following code, which has
#         been modified to fit the program's needs.
# http://trevorappleton.blogspot.com/2013/10/guide-to-creating-sudoku-solver-using.html 
# ============================================================================
import pygame, sys
from pygame.locals import *

#-----------------------------------------------------------------------------
#                           GLOBAL CONSTANTS
# Number of frames per second
FPS = 10

# Sets size of grid
WINDOWMULTIPLIER = 5 # Modify this number to change size of grid
WINDOWSIZE = 81 # needs to be multiple of 9
WINDOWWIDTH = WINDOWSIZE * WINDOWMULTIPLIER
WINDOWHEIGHT = WINDOWSIZE * WINDOWMULTIPLIER
SQUARESIZE = int((WINDOWSIZE * WINDOWMULTIPLIER) / 3) # size of a 3x3 square
CELLSIZE = int(SQUARESIZE / 3) # Size of a cell
NUMBERSIZE = int(CELLSIZE / 3) # Position of unsolved number

# Set up the colors
BLACK     = (0  ,0  ,0  )
WHITE     = (255,255,255)
LIGHTGRAY = (200,200,200)
BLUE      = (0  ,0  ,255)
GREEN     = (0  ,255,0  )
#------------------------------------------------------------------------------

def drawGrid():
# This function creates the sudoku grid using the pygame module. The grid uses
# the global constants for window height and width.
#  Args: 
#       None
#  Returns: 
#       None

    # Draw Minor Lines
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, BLACK, (x,0),(x,WINDOWHEIGHT))
    for y in range (0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, BLACK, (0,y), (WINDOWWIDTH, y))
    
    # Draw Major Lines
    for x in range(0, WINDOWWIDTH, SQUARESIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, BLACK, (x,0),(x,WINDOWHEIGHT),2)
    for y in range (0, WINDOWHEIGHT, SQUARESIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, BLACK, (0,y), (WINDOWWIDTH, y),2)

def initiateCells():
    initialGrid = {}
    fullCell = [1,2,3,4,5,6,7,8,9]
    for xCoord in range(0,9):
        for yCoord in range(0,9):
            initialGrid[xCoord,yCoord] = list(fullCell) # Copies List
    return initialGrid

# Takes the remaining numbers and displays them in the cells.
def displayCells(currentGrid):
    # Create offset factors to display numbers in right location in cells.
    xFactor = 0
    yFactor = 0
    for item in currentGrid: # item is x,y co-ordinate from 0-8
        cellData = currentGrid[item] # isolates the numbers still available for that cell
        for number in cellData: #incNumtes through each number
            if number != ' ': # ignores those already dismissed
                xFactor = ((number-1)%3) # 1/4/7 = 0 2/5/8 = 1 3/6/9 =2
                if number <= 3:
                    yFactor = 0
                elif number <=6:
                    yFactor = 1
                else:
                    yFactor = 2
                #(item[0] * CELLSIZE) Positions in the right Cell
                #(xFactor*NUMBERSIZE) Offsets to position number
                if cellData.count(' ') < 8:    
                    populateCells(number,(item[0]*CELLSIZE)+(xFactor*NUMBERSIZE),(item[1]*CELLSIZE)+(yFactor*NUMBERSIZE),'small')
                else:
                    populateCells(number,(item[0]*CELLSIZE),(item[1]*CELLSIZE),'large')                   
    return None

# writes cellData at given x, y co-ordinates   
def populateCells(cellData, x, y,size):
    if size == 'small':
        cellSurf = BASICFONT.render('%s' %(cellData), True, LIGHTGRAY)
    elif size == 'large':
        cellSurf = LARGEFONT.render('%s' %(cellData), True, GREEN)
        
    cellRect = cellSurf.get_rect()
    cellRect.topleft = (x, y)
    DISPLAYSURF.blit(cellSurf, cellRect)

def drawBox(mousex, mousey):
    boxx = (mousex // NUMBERSIZE) * NUMBERSIZE
    boxy = (mousey // NUMBERSIZE) * NUMBERSIZE
    pygame.draw.rect(DISPLAYSURF, BLUE, (boxx,boxy,NUMBERSIZE,NUMBERSIZE), 1)
    
def displaySelectedNumber(mousex, mousey, currentGrid):
    modXNumber = (mousex % CELLSIZE) // NUMBERSIZE
    modYNumber = (mousey % CELLSIZE) // NUMBERSIZE
    if modXNumber == 0:
        xChoices = [1,4,7]
        number = xChoices[modYNumber]        
    elif modXNumber == 1:
        xChoices = [2,5,8]
        number = xChoices[modYNumber]
    else:
        xChoices = [3,6,9]
        number = xChoices[modYNumber]
    # need to determine the cell we are in
    xCellNumber = mousex // CELLSIZE
    yCellNumber = mousey // CELLSIZE
   
    # gets a list of current numbers
    currentState = currentGrid[xCellNumber,yCellNumber]
    incNum = 0
    
    while incNum < 9:
        # if NOT number selected
        if incNum+1 != number:
            currentState[incNum] = ' ' # make ' '
        else:
            currentState[incNum] = number # make = number
        #update currentGrid
        currentGrid[xCellNumber,yCellNumber] = currentState
        incNum += 1
    return currentGrid
    
    
def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))

    mouseClicked = False
  
    mousex = 0
    mousey = 0
    
    pygame.display.set_caption('Sudoku Verification')

    global BASICFONT, BASICFONTSIZE, LARGEFONT, LARGEFONTSIZE
    BASICFONTSIZE = 15
    LARGEFONTSIZE = 55
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    LARGEFONT = pygame.font.Font('freesansbold.ttf', LARGEFONTSIZE)

    currentGrid = initiateCells() #sets all cells to have number 1-9
    
    # repaints screen
    DISPLAYSURF.fill(WHITE)
    displayCells(currentGrid)
    drawGrid()

    while True: #main game loop
        mouseClicked = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # mouse movement commands
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos

            #Mouse click commands
            elif event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                mouseClicked = True
            
        if mouseClicked == True:
            # allow number to be selected
            currentGrid = displaySelectedNumber(mousex, mousey, currentGrid)

        # repaints screen
        DISPLAYSURF.fill(WHITE)
        displayCells(currentGrid)
        drawGrid()
        # call function to draw box
        drawBox(mousex,mousey)
        
        pygame.display.update()    
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()