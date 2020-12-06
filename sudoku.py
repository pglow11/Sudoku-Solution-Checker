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
DARKGRAY  = (127,127,127)
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
        pygame.draw.line(DISPLAYSURF, BLACK, (x,0),(x,WINDOWHEIGHT),3)
    for y in range (0, WINDOWHEIGHT, SQUARESIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, BLACK, (0,y), (WINDOWWIDTH, y),3)
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def initiateCells():
# This function creates a dictionary to store a list(1..9) at each
# each of the 9x9 cell locations ([xCoord, yCoord]).
#  Args: 
#       None
#  Returns: 
#       initialGrid = {(xCoord, yCoord): [1,2,...9]}

    initialGrid = {}
    fullCell = [1,2,3,4,5,6,7,8,9]
    for xCoord in range(0,9):
        for yCoord in range(0,9):
            initialGrid[xCoord,yCoord] = list(fullCell) # Copies List
    
    # Hard-code in initial cells [x,y]
    # y = 0
    initialGrid[0,0] = [8]
    initialGrid[3,0] = [9]
    initialGrid[4,0] = [3]
    initialGrid[8,0] = [2]
    # y = 1
    initialGrid[2,1] = [9]
    initialGrid[7,1] = [4]
    # y = 2
    initialGrid[0,2] = [7]
    initialGrid[2,2] = [2]
    initialGrid[3,2] = [1]
    initialGrid[6,2] = [9]
    initialGrid[7,2] = [6]
    # y = 3
    initialGrid[0,3] = [2]
    initialGrid[7,3] = [9]
    # y = 4
    initialGrid[1,4] = [6]
    initialGrid[7,4] = [7]     
    # y = 5
    initialGrid[1,5] = [7]
    initialGrid[5,5] = [6]
    initialGrid[8,5] = [5]
    # y = 6
    initialGrid[1,6] = [2]
    initialGrid[2,6] = [7]
    initialGrid[5,6] = [8]
    initialGrid[6,6] = [4]
    initialGrid[8,6] = [6]
    # y = 7
    initialGrid[1,7] = [3]
    initialGrid[6,7] = [5]
    # y = 8
    initialGrid[0,8] = [5]
    initialGrid[4,8] = [6]
    initialGrid[5,8] = [2]
    initialGrid[8,8] = [8]

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
                if len(cellData) == 1:      # For cells that are hard-coded
                    populateCells(number,
                                  (item[0]*CELLSIZE),
                                  (item[1]*CELLSIZE),
                                  'fixed')
                elif cellData.count(' ') < 8:    
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
    elif size == 'fixed':
        cellSurf = LARGEFONT.render('%s' %(cellData), True, DARKGRAY)
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
    if len(currentState) == 1:
        pass
    else:
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
def checkComplete(currentGrid):
# This function runs after each mouse click within the main game loop to 
# determine if the user has finished selecting a value for each of the open 9x9
# cells.
#  Args: 
#       currentGrid = dictionary for each x,y location
#  Returns: 
#       bool (True if all cells have only one number at x,y location)

    for item in currentGrid: # item is x,y co-ordinate from 0-8
        cellData = currentGrid[item] # isolates the numbers still available
        if cellData.count(' ') < 8:
            if len(cellData) == 1:
                pass
            else:
                return False        
    return True
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def checkX(currentGrid):
# This function checks the user selections for each column, specifically by
# verifying that each column only contains 1-9.
#  Args: 
#       currentGrid
#  Returns: 
#       bool (True = column contains numbers 1-9)

    for xCoord in range(0,9):
        tempX = []
        for yCoord in range(0,9):
            for number in currentGrid[xCoord, yCoord]:
                if number != ' ':
                    tempX.append(number)
        tempX.sort()
        for count in range(0,9):
            if tempX[count] != (count + 1):
                return False
    return True
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def checkY(currentGrid):
# This function checks the user selections for each row, specifically by
# verifying that each row only contains 1-9.
#  Args: 
#       currentGrid
#  Returns: 
#       bool (True = column contains numbers 1-9)

    for yCoord in range(0,9):
        tempY = []
        for xCoord in range(0,9):
            for number in currentGrid[xCoord, yCoord]:
                if number != ' ':
                    tempY.append(number)
        tempY.sort()
        for count in range(0,9):
            if tempY[count] != (count + 1):
                return False
    return True
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def checkSquare(currentGrid):
# This function checks the user selections for each 3x3 square, specifically by
# verifying that each square only contains 1-9.
#  Args: 
#       currentGrid
#  Returns: 
#       bool (True = column contains numbers 1-9)

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

    # Initialize currentGrid dictionary for each 9x9 cells & display values
    currentGrid = initiateCells()
    displayCells(currentGrid)                           

    # Main game loop
    complete = False
    while not complete: 
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
            complete = checkComplete(currentGrid)
            
        # Repaints screen
        DISPLAYSURF.fill(WHITE)
        displayCells(currentGrid)
        drawGrid()

        # Draw box & update display based on clock tick
        drawBox(mousex,mousey)        
        pygame.display.update()    
        FPSCLOCK.tick(FPS)

    # Verification of solution 
    print("\n")
    print("You've entered all values. Verifying solution now...")
    resultX = checkX(currentGrid)
    resultY = checkY(currentGrid)
    # resultSquare = checkSquare(currentGrid)
    print(f"Each column (x-coordinates) is verified: {resultX}")
    print(f"Each row (y-coordinates) is verified: {resultY}")
#------------------------------------------------------------------------------

if __name__=='__main__':
    main()