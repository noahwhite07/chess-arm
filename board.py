import cv2 as cv
import numpy as np

# The module containing the computer vision methods to find the locations of blobs of color in the board image
import computer_vision

class board:
    def __init__(self, boardImage):
        # The image of the chessboard used to locate the corners of the board
        self.boardImg = boardImage

        # This is where we should put code for perspective correction
        # 

        # The bounds of the lines on the board
        self.squarePositions = self.getSquarePositions()
    
    # Returns a list containing two lists
    # The first list contains the x values of the vertical lines on the chessboard
    # The second list containst the y values of the horizontal lines on the chessboard 
    # These will be used by getSquare() to determine on which square a given point lies
    def getSquarePositions(self):
        #corners = self.getBlobPoints(6)
        # We are identifying corners with blobs of the color magenta (6 in the colorBounds array in computer_vision.py)
        cornerColor = 6

        # Fetch the points at which magenta blobs occur
        corners = computer_vision.getBlobPoints(self.boardImg, cornerColor)


        # For two arbitrary points in corners, if abs(x1-x2) > threshold for difference
        #   then larger of the two is the right bound, smaller is the left bound
        # Repeat for y vals

        # The threshold for calculating if two x values or two y values are significantly different 
        # Used to determine if two corners lie on a horizontal line or a vertical line
        threshold = 50

        # Raises an exception if the program did not detect 4 corners 
        if len(corners) != 4:
            raise Exception(f'getSquarePositions expected 4 corners but detected {len(corners)}')

        # Iterates through the list of corners to find the bounds of the chess board
        for i in range(len(corners) - 1):
            # Finds the x values of two consecutive corners 
            x1 = corners[i][0]
            x2 = corners[i + 1][0]
            #print(f'x1: {x1}\tx2: {x2}')

            # Finds the y values of two consecutive corners 
            y1 = corners[i][1]
            y2 = corners[i + 1][1]
            #print(f'y1: {y1}\ty2: {y2}')

            # If any two x values are significantly different, we can use these as the horizontal bounds of the board
            if abs(x1 - x2) > threshold:
                # Orders horizontal bounds into left and right based on their value
                if x1 > x2:
                    rightBound = x1
                    leftBound = x2
                else:
                    rightBound = x2
                    leftBound = x1

            # If any two y values are significantly different, we can use these as the vertical bounds of the board
            if abs(y1 - y2) > threshold:
                # Orders vertical bounds into upper and lower based on their value
                if y1 > y2:
                    lowerBound = y1
                    upperBound = y2
                else:
                    lowerBound = y2
                    upperBound = y1  

        # Lists to hold the x coordinates of the vertical lines on the board
        # and the y coordinates of the horizontal lines on the board respectively
        vertXVals = []
        horiYVals = []

        # The side length of one square on the board
        squareLength = (rightBound - leftBound) // 8

        # Calculates horizontal bounds of the lettered labels 
        # and the vertical bounds of the numbered labels for determining the position of squares
        for i in range(9):
            vertXVals.append(leftBound + (squareLength * i))
            horiYVals.append(upperBound + (squareLength * i))

        # Returns horizontal and vertical bounds of the labels      
        return [vertXVals, horiYVals]


    # This method returns the square on which any given point on the image of the chessboard lies (ex. 'e4')
    def getSquare(self, point):

        if(len(point) < 2):
            raise Exception('point is empty')
        
        #stores the x values of each vertical line in ascending order
        vertXVals = self.squarePositions[0] 

        #stores the y values of each horizontal line in ascending order
        horiYVals = self.squarePositions[1]

        #image origin is at top left, but chessboard origin is at bottom left
        vertLabels = ['8','7','6','5','4','3','2','1']
        horiLabels = ['a','b','c','d','e','f','g','h']

        # Sets the default label to X so that if the point does not lie on a square, its vertical label will be 'x'
        pieceVertLabel = 'x'

        # Iterates through the y values of the horizontal lines on the board
        for i in range(len(horiYVals) - 1):
            # If the point lies between two adjacent horizontal lines, we know its vertical label
            # Ex. if a point lies between the y values of the first and second horizontal lines, its square should have vertical label of '1'
            if (point[1] >= horiYVals[i] and point[1] < horiYVals[i+1]) :
                pieceVertLabel = vertLabels[i]

        # Sets the default label to X so that if the point does not lie on a square, its horizontal label will be 'x'        
        pieceHoriLabel = 'x'

        # Iterates through the x values of the vertical lines on the board
        for i in range(len(vertXVals) - 1):
            # If the point lies between two adjacent vertical lines, we know its horizontal label
            # Ex. if a point lies between the x values of the first and second vertical lines, its square should have vertical label of 'a'
            if (point[0] >= vertXVals[i] and point[0] < vertXVals[i+1]) :
                pieceHoriLabel = horiLabels[i]
                #print(f'pieceHoriLabel: {pieceHoriLabel}')
                #print(f'peiceVertLabel: {pieceVertLabel}')

        # Combine the strings in horizontal + vertical order to give the notation required by the engine to describe a square
        # Ex. 'e2'
        square = pieceHoriLabel + pieceVertLabel
        return square

