# This program should take in locations of blobs from detect_blobs 
#  to return a 2D array representation of the current board state

import cv2 as cv
import numpy as np
#import detect_blobs
#import squares
import matplotlib.pyplot as plt
import random as rand
import board


class boardState:

    # Lists of colors will always be in ROYGBIV format
    # Lists of pieces will always be in PNBRQK format

    def __init__(self, boardImg):
        self.board = boardImg
        self.squarePositions = self.getSquarePositions()
        pass
        


    # def getSquarePositions(self):
    #     corners = detect_blobs.getBlobPoints(6)
    #     print(corners)


    #     # For two arbitrary points in corners, if abs(x1-x2) > threshold for difference
    #     #   then larger of the two is the right bound, smaller is the left bound
    #     # Repeat for y vals
    #     threshold = 50

    #     for i in range(len(corners) - 1):
    #         x1 = corners[i][0]
    #         x2 = corners[i + 1][0]
    #         print(f'x1: {x1}\tx2: {x2}')

    #         y1 = corners[i][1]
    #         y2 = corners[i + 1][1]
    #         print(f'y1: {y1}\ty2: {y2}')

    #         if abs(x1 - x2) > threshold:
    #             if x1 > x2:
    #                 rightBound = x1
    #                 leftBound = x2
    #             else:
    #                 rightBound = x2
    #                 leftBound = x1

    #         if abs(y1 - y2) > threshold:
    #             if y1 > y2:
    #                 lowerBound = y1
    #                 upperBound = y2
    #             else:
    #                 lowerBound = y2
    #                 upperBound = y1   
    #     # Lists to hold the x coordinates of the vertical lines on the board
    #     # and the y coordinates of the horizontal lines on the board respectiveley
    #     vertXVals = []
    #     horiYVals = []

    #     # The side length of one square on the board
    #     squareLength = (rightBound - leftBound) // 8

    #     for i in range(9):
    #         vertXVals.append(leftBound + (squareLength * i))
    #         horiYVals.append(upperBound + (squareLength * i))
                
    #     return [vertXVals, horiYVals]

    # def getSquare(self, point):

    #     #stores the x values of each vertical line in ascending order
    #     vertXVals = self.squarePositions[0] 
    #     #print(f'vertXVals = {vertXVals}')

    #     #stores the y values of each horizontal line in ascending order
    #     horiYVals = self.squarePositions[1]

    #     #print(f'horiYVals: {horiYVals}')
    #     #image origin is at top left, but chessboard origin is at bottom left
    #     vertLabels = ['8','7','6','5','4','3','2','1']
    #     horiLabels = ['A','B','C','D','E','F','G','H']

    #     # Sets the default label to X so that if the point does not lie on a square, its label will be XX
    #     pieceVertLabel = 'x'
    #     for i, val in enumerate(horiYVals):
    #         if (point[1] >= horiYVals[i] and point[1] < horiYVals[i+1]) :
    #             pieceVertLabel = vertLabels[i]
            
        
    #     pieceHoriLabel = 'x'
    #     for i, val in enumerate(vertXVals):

    #         if (point[0] >= vertXVals[i] and point[0] < vertXVals[i+1]) :
    #             pieceHoriLabel = horiLabels[i]
    #             #print(f'pieceHoriLabel: {pieceHoriLabel}')
    #             #print(f'peiceVertLabel: {pieceVertLabel}')
                        
                    

                        
    #             square = pieceHoriLabel + pieceVertLabel
    #             return square


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
            colorPoints = board.getBlobPoints(pieceColors[i])

            # A list to hold all the squares in which a pieceColor occurs
            colorSquares = []
            #print(f'colorPoints[{i}]: {colorPoints}')
            # Iterates across each point where a pieceColor occurs
            for colorPoint in colorPoints:
                #print(f'colorPoint: {colorPoint}')
                # Finds the square that contains that point and appends it to colorSquares
                square = self.getSquare(colorPoint)  
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


