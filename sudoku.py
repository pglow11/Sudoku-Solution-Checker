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
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def initiateCells():
# This function creates a dictionary to store a list(0..8) at each
# each of the 9x9 cell locations ([xCoord, yCoord]).
#  Args: 
#       None
#  Returns: 
#       initialGrid = {(xCoord, yCoord): [0,1,...8]}

    initialGrid = {}
    fullCell = [1,2,3,4,5,6,7,8,9]
    for xCoord in range(0,9):
        for yCoord in range(0,9):
            initialGrid[xCoord,yCoord] = list(fullCell) # Copies List
    return initialGrid
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def displayCells(currentGrid):
# This function takes the remaining numbers in the 9x9 cells and displays them
# using populateCells() function.
#  Args: 
#       currentGrid = {(xCoord, yCoord): [1,2,...9]}
#  Returns: 
#       None

    # Create offset factors to display numbers in right location in cells.
    xFactor = 0
    yFactor = 0
    for item in currentGrid: # item is x,y co-ordinate from 0-8
        cellData = currentGrid[item] # isolates the numbers still available 
        for number in cellData: 
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
                    populateCells(number,
                                  (item[0]*CELLSIZE)+(xFactor*NUMBERSIZE),
                                  (item[1]*CELLSIZE)+(yFactor*NUMBERSIZE),
                                  'small')
                else:
                    populateCells(number,
                                  (item[0]*CELLSIZE),
                                  (item[1]*CELLSIZE),
                                  'large')                   
    return None
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------  
def populateCells(cellData, x, y,size):
# This helper function for the displayCells() function writes cellData at given 
# x, y co-ordinates.
#  Args: 
#       cellData = value to be displayed (int/string)
#       x        = x coordinate postion (int)
#       y        = y coordinate position (int)
#       size     = string
#  Returns: 
#       None

    if size == 'small':
        cellSurf = BASICFONT.render('%s' %(cellData), True, LIGHTGRAY)
    elif size == 'large':
        cellSurf = LARGEFONT.render('%s' %(cellData), True, GREEN)
        
    cellRect = cellSurf.get_rect()
    cellRect.topleft = (x, y)
    DISPLAYSURF.blit(cellSurf, cellRect)
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def drawBox(mousex, mousey):
# This function takes the x,y coordinates of the mouse position and draws a 
# blue box around the number that would be selected. The blue box does not move
# around freely with the mouse, but uses the NUMBERSIZE boundary to stay on a 
# value until the mouse position is fully off the NUMBERSIZE cell.
# The function uses pygame module's draw.rect method to draw the box.
#  Args: 
#       mousex = mouse x-coordinate position
#       mousey = mouse y-coordinate position
#  Returns: 
#       None

    # Sets x,y coordinates of blue rectangle to the top left corner of the 
    # of the value where the mouse is currently located.
    boxx = (mousex // NUMBERSIZE) * NUMBERSIZE 
    boxy = (mousey // NUMBERSIZE) * NUMBERSIZE

    pygame.draw.rect(DISPLAYSURF, BLUE, (boxx,boxy,NUMBERSIZE,NUMBERSIZE), 1)
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------    
def displaySelectedNumber(mousex, mousey, currentGrid):
# This function identifies the number selected and updates the dictionary which
# holds the information regarding the current state of the grid.
#  Args: 
#       mousex = mouse x-coordinate position
#       mousey = mouse y-coordinate position
#       currentGrid = current dictionary listing available values for cell 
#  Returns: 
#       currentGrid = updated dictionary for value selected

    # Identify what 1/3 of the cell mouse is in using its x,y coordinates
    # % CELLSIZE "normalizes" x,y coordinates to size of cell 
    # // NUMBERSIZE uses floor division to find top left corner
    modXNumber = (mousex % CELLSIZE) // NUMBERSIZE  
    modYNumber = (mousey % CELLSIZE) // NUMBERSIZE 

    if modXNumber == 0:     # First 1/3
        xChoices = [1,4,7]
        number = xChoices[modYNumber]        
    elif modXNumber == 1:   # Second 1/3
        xChoices = [2,5,8]
        number = xChoices[modYNumber]
    else:                   # Third 1/3
        xChoices = [3,6,9]
        number = xChoices[modYNumber]

    # Determine the cell based on mouse x,y position
    xCellNumber = mousex // CELLSIZE
    yCellNumber = mousey // CELLSIZE
   
    # Gets a list of current numbers
    currentState = currentGrid[xCellNumber,yCellNumber]
    
    # Update cell's currentGrid dictionary based on user selection
    incNum = 0    
    while incNum < 9:
        # if NOT number selected
        if (incNum + 1) != number:
            currentState[incNum] = ' ' # make ' '
        else:
            currentState[incNum] = number
        # Update dictionary's list at cell's x,y location
        currentGrid[xCellNumber,yCellNumber] = currentState
        incNum += 1
    return currentGrid
#------------------------------------------------------------------------------ 

#------------------------------------------------------------------------------
def main():
# This function is the driver code to run the sudoku GUI and verification.
#  Args: 
#       None
#  Returns: 
#       None

    # Initialize & set up pygame module
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))

    # Initial mouse variables
    mouseClicked = False
    mousex = 0
    mousey = 0
    
    # Setup pygame fonts    
    global BASICFONT, BASICFONTSIZE, LARGEFONT, LARGEFONTSIZE
    BASICFONTSIZE = 15
    LARGEFONTSIZE = 55
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    LARGEFONT = pygame.font.Font('freesansbold.ttf', LARGEFONTSIZE)
    
    # Initialize sudoku board
    pygame.display.set_caption('Sudoku Verification')   # Title
    DISPLAYSURF.fill(WHITE)                             # Paint board
    drawGrid()                                          # Draw grid lines

    # Initialize currentGrid dictionary for each 9x9 cells
    currentGrid = initiateCells()
    displayCells(currentGrid)                           # Display values

    # Main game loop
    while True: 
        mouseClicked = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # Mouse movement commands
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            # Mouse click commands
            elif event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                mouseClicked = True            
        if mouseClicked == True:
            currentGrid = displaySelectedNumber(mousex, mousey, currentGrid)

        # Repaints screen
        DISPLAYSURF.fill(WHITE)
        displayCells(currentGrid)
        drawGrid()

        # Draw box
        drawBox(mousex,mousey)
        
        pygame.display.update()    
        FPSCLOCK.tick(FPS)
#------------------------------------------------------------------------------

if __name__=='__main__':
    main()