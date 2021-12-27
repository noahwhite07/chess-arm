# This program should take in locations of blobs from detect_blobs 
#  to return a 2D array representation of the current board state

import cv2 as cv
import numpy as np
#import detect_blobs
#import squares
import matplotlib.pyplot as plt
import random as rand
from board import board


class boardState:

    # Lists of colors will always be in ROYGBIV format
    # Lists of pieces will always be in PNBRQK format

    # board is the board object responsible for holding physical information about the layout of the board
    # boardImg is a video frame taken during the game to represent the current state of the game
    def __init__(self, board, boardImg):
        self.boardImg = boardImg
        self.board = board
        pass
        


    def getOccupiedSquares(self):
        # Lists of colors will always be in ROYGBIV format
        # Lists of pieces will always be in PNBRQK format

        # A list of the colors for each piece in the aformentioned order
        # Each unique piece will be one of 6 colors, the remaining color will be used to outline the corners of the board
        pieceColors = [0,1,2,3,4,5]

        # Pawn - Red
        # Knight - Orange
        # Bishop - Yellow
        # Rook - Green
        # Queen - Cyan
        # King - Indigo
        

        # A 2D list to store the squares occupied by each piece 
        # Element 0 should be a list of squares occupied by pawns
        # List continues in PNBRQK format
        occupiedSquares = []
        for i, pieceColor in enumerate(pieceColors):

            # colorPoints holds the points in the image at which each pieceColor occurs
            colorPoints = board.getBlobPoints(self.board, pieceColors[i])

            # A list to hold all the squares in which a pieceColor occurs
            colorSquares = []
            #print(f'colorPoints[{i}]: {colorPoints}')
            # Iterates across each point where a pieceColor occurs
            for colorPoint in colorPoints:
                #print(f'colorPoint: {colorPoint}')
                # Finds the square that contains that point and appends it to colorSquares
                square = self.board.getSquare(colorPoint)  
                colorSquares.append(square)

            # Appends the list of squares occupied by a given color to occupiedSquares
            occupiedSquares.append(colorSquares)
        #print(occupiedSquares)

        # Returns a list that contains lists of squares at which each type of piece is located in PNBRQK format 
        return occupiedSquares

# import overhead picture of board
# getSquare positions only works on the image of the blank chessboard. I could modify it to work with pieces
# I could also modify it to just take the picture before the pieces are on the board,
# Simplest solution is simply to draw blobs on the corners of the board. I'll do that
# board = cv.imread('pictures/game.jpg')
# cv.imshow("board", board)

# state1 = boardState(board)

# squares1 = state1.getOccupiedSquares()
# print(squares1)


