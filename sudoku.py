# sudoku.py
# ============================================================================
# Name: Patrick Glowacki
# Date: November 27, 2020
# Description: CS325_400_F2020 Homework 8: Portfolio Project 
#              
# ============================================================================
import numpy as np
import pygame

import pygame, sys
from pygame.locals import *

#Number of frames per second
FPS = 10

# Sets size of grid
WINDOWMULTIPLIER = 5 # Modify this number to change size of grid
WINDOWSIZE = 90
WINDOWWIDTH = WINDOWSIZE * WINDOWMULTIPLIER
WINDOWHEIGHT = WINDOWSIZE * WINDOWMULTIPLIER
SQUARESIZE = int((WINDOWSIZE * WINDOWMULTIPLIER) / 3) # size of a 3x3 square
CELLSIZE = int(SQUARESIZE / 3) # Size of a cell

# Set up the colours
BLACK =     (0,  0,  0)
WHITE =     (255,255,255)
LIGHTGRAY = (200, 200, 200)

def drawGrid():
    ### Draw Minor Lines
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, LIGHTGRAY, (x,0),(x,WINDOWHEIGHT))
    for y in range (0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, LIGHTGRAY, (0,y), (WINDOWWIDTH, y))
    
    ### Draw Major Lines
    for x in range(0, WINDOWWIDTH, SQUARESIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, BLACK, (x,0),(x,WINDOWHEIGHT))
    for y in range (0, WINDOWHEIGHT, SQUARESIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, BLACK, (0,y), (WINDOWWIDTH, y))

    return None

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    pygame.display.set_caption('Sudoku Solver')

    DISPLAYSURF.fill(WHITE)

    drawGrid()
    while True: #main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()    
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()