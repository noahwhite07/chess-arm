# This program should take in locations of blobs from detect_blobs 
#  to return a 2D array representation of the current board state

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import random as rand
from board import board
import computer_vision


class boardState:

    # Lists of colors will always be in ROYGBIV format
    # Lists of pieces will always be in PNBRQK format

    # board is the board object responsible for holding physical information about the layout of the board
    # boardImg is a video frame taken during the game to represent the current state of the game
    def __init__(self, board, boardImg):
        self.boardImage = boardImg
        self.board = board
        pass
        

    # Method returns a list of squares occupied by white pieces
    # This is frequently returning an aray with two 'None' values for some reason
    def getOccupiedSquares(self):

        whitePieceColor = 7



        # None of this is necessary as we only need to track the white pieces
        # Pieces also do not need to be distinguished from one another in any way
        


        # A 2D list to store the squares occupied by each piece 
        # Element 0 should be a list of squares occupied by pawns
        # List continues in PNBRQK format
        occupiedSquares = []
            # colorPoints holds the points in the image at which each pieceColor occurs
            #colorPoints = board.getBlobPoints(self.board, pieceColors[i])
        colorPoints = computer_vision.getBlobPoints(self.boardImage, whitePieceColor)


        # Iterates across each point where a white blob occurs
        for colorPoint in colorPoints:
            #print(f'colorPoint: {colorPoint}')
            # Finds the square that contains that point and appends it to colorSquares
            square = self.board.getSquare(colorPoint)  
            occupiedSquares.append(square)


        # Returns a list of squares occupied by white pieces.
        if(len(occupiedSquares) == 0):
            raise Exception('No white pieces detected')
        return occupiedSquares




