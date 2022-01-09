import cv2 as cv
import numpy as np

# The module containing the computer vision methods to find the locations of blobs of color in the board image
import computer_vision

class board:
    def __init__(self, boardImage):
        # The image of the chessboard used to locate the corners of the board
        self.boardImg = boardImage
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

    # This method should not be here but I can't test this code right now so I'm not gonna delete anything
    def getBlobPoints(self, color):
        boardHSV = cv.cvtColor(self.boardImg, cv.COLOR_BGR2HSV)

        # HSV color bounds for green blobs
        green_lower = np.array([40, 40,40])
        green_upper = np.array([70,255,255])

        # HSV color bounds for cyan blobs
        cyan_lower = np.array([80,40,40])
        cyan_upper = np.array([100,255,255])

        # HSV color bounds for indigo blobs
        indigo_lower = np.array([100,40,40])
        indigo_upper = np.array([135,255,255])

        # HSV color bounds for pink blobs
        pink_lower = np.array([140,40,40])
        pink_upper = np.array([169,255,255])

        # HSV color bounds for yellow blobs
        yellow_lower = np.array([25,40,40])
        yellow_upper = np.array([35,255,255])

        # HSV color bounds for orange blobs
        orange_lower = np.array([11,200,150])
        orange_upper = np.array([24,255,255])

        # HSV color bounds for red blobs
        red_lower = np.array([170,200,40])
        red_upper = np.array([180,255,255])

        # A 2D list to hold the pairs of color bounds for each of the 7 colors
        colorBounds = [
            [red_lower,red_upper],
            [orange_lower,orange_upper],
            [yellow_lower,yellow_upper],
            [green_lower,green_upper],
            [cyan_lower, cyan_upper],
            [indigo_lower, indigo_upper],
            [pink_lower,pink_upper]
            ]

        #A list to hold masks for each of the 7 colors in ROYGBIV format
        colorMasks = []
        # Creates a mask for each color and appends the mask to colorMasks
        for bounds in colorBounds:
            colorMasks.append(cv.inRange(boardHSV, bounds[0], bounds[1]))

        # A list to hold the image with each color mask applied
        maskedImages = []

        # Creates a masked image of the board that only contains the blobs of each color
        #   and appends the image to maskedImages
        for colorMask in colorMasks:
            maskedImages.append(cv.bitwise_and(self.boardImg, self.boardImg, mask = colorMask))

        # A list to hold the thresholded image of the blobs of each color
        blobImages = []

        # Converts the masked images to greyscale, performs a binary threshold, 
        #  and appends the thresholded 'blob' image to blobImages
        for maskedImage in maskedImages:
            # converts masked image to greyscale
            grey = cv.cvtColor(maskedImage, cv.COLOR_BGR2GRAY)
            # does an inversed binary threshold of the greyscale masked image
            # threshold is inverted because blob detector works best on black blobs on white
            threshold, blobImage = cv.threshold(grey, 55, 255, cv.THRESH_BINARY_INV) 
            #blobImage = cv.adaptiveThreshold(grey, 255, cv.ADAPTIVE_THRESH_MEAN_C,
            #     cv.THRESH_BINARY, 11, 3)
            blobImages.append(blobImage)


        ##############################################################
        # Setup SimpleBlobDetector parameters.
        params = cv.SimpleBlobDetector_Params()

        # Change thresholds
        params.minThreshold = 50
        params.maxThreshold = 200

        # Filter by Area.
        params.filterByArea = True
        params.minArea = 100

        # Filter by Circularity
        params.filterByCircularity = False
        params.minCircularity = 0.1

        # Filter by Convexity
        params.filterByConvexity = False
        params.minConvexity = 0.87

        # Filter by Inertia
        params.filterByInertia = False
        params.minInertiaRatio = 0.01

        # Create a detector with the parameters
        detector = cv.SimpleBlobDetector_create(params)
        ##############################################################

        # A list to hold the key points for each color given by detector.detect()
        keyPointsList = []
        for blobImage in blobImages:
            keyPointsList.append(detector.detect(blobImage)) 

        # Draw detected blobs as red circles.
        # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
        # the size of the circle corresponds to the size of blob

        # A list to store images of the board with the blobs of each color highlighted 
        #  with a red circle depending on the blob size, one image per color
        boardsWithKeypoints = []

        for keyPoints in keyPointsList:
            boardsWithKeypoints.append(cv.drawKeypoints(self.boardImg, keyPoints, np.array([]), (0,0,0), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS))
            points = []

        for keyPoint in keyPointsList[color]:  
            x = keyPoint.pt[0]
            y = keyPoint.pt[1]
            point = [x,y]
            points.append(point)

        return points

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

