import cv2 as cv
import numpy as np
import computer_vision

class board:
    def __init__(self, boardImage):
        self.boardImg = boardImage
        self.squarePositions = self.getSquarePositions()
        
    def getSquarePositions(self):
        print("getSquarePositions ran here")
        #corners = self.getBlobPoints(6)
        cornerColor = 6
        corners = computer_vision.getBlobPoints(self.boardImg, cornerColor)
        print(corners)


        # For two arbitrary points in corners, if abs(x1-x2) > threshold for difference
        #   then larger of the two is the right bound, smaller is the left bound
        # Repeat for y vals
        threshold = 50
        if len(corners) != 4:
            raise Exception(f'getSquarePositions expected 4 corners but detected {len(corners)}')

        for i in range(len(corners) - 1):
            x1 = corners[i][0]
            x2 = corners[i + 1][0]
            print(f'x1: {x1}\tx2: {x2}')

            y1 = corners[i][1]
            y2 = corners[i + 1][1]
            print(f'y1: {y1}\ty2: {y2}')

            if abs(x1 - x2) > threshold:
                if x1 > x2:
                    rightBound = x1
                    leftBound = x2
                else:
                    rightBound = x2
                    leftBound = x1

            if abs(y1 - y2) > threshold:
                if y1 > y2:
                    lowerBound = y1
                    upperBound = y2
                else:
                    lowerBound = y2
                    upperBound = y1   
        # Lists to hold the x coordinates of the vertical lines on the board
        # and the y coordinates of the horizontal lines on the board respectiveley
        vertXVals = []
        horiYVals = []

        # The side length of one square on the board
        squareLength = (rightBound - leftBound) // 8

        for i in range(9):
            vertXVals.append(leftBound + (squareLength * i))
            horiYVals.append(upperBound + (squareLength * i))
                
        return [vertXVals, horiYVals]

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


    def getSquare(self, point):
        if(len(point) < 2):
            raise Exception('point is empty')
        
        #stores the x values of each vertical line in ascending order
        vertXVals = self.squarePositions[0] 
        #print(f'vertXVals = {vertXVals}')

        #stores the y values of each horizontal line in ascending order
        horiYVals = self.squarePositions[1]

        #print(f'horiYVals: {horiYVals}
        #image origin is at top left, but chessboard origin is at bottom left
        vertLabels = ['8','7','6','5','4','3','2','1']
        horiLabels = ['a','b','c','d','e','f','g','h']

        # Sets the default label to X so that if the point does not lie on a square, its label will be XX
        pieceVertLabel = 'x'
        for i in range(len(horiYVals) - 1):
            if (point[1] >= horiYVals[i] and point[1] < horiYVals[i+1]) :
                pieceVertLabel = vertLabels[i]
            
        
        pieceHoriLabel = 'x'
        for i in range(len(vertXVals) - 1):

            if (point[0] >= vertXVals[i] and point[0] < vertXVals[i+1]) :
                pieceHoriLabel = horiLabels[i]
                #print(f'pieceHoriLabel: {pieceHoriLabel}')
                #print(f'peiceVertLabel: {pieceVertLabel}')
                        
                    

                        
                square = pieceHoriLabel + pieceVertLabel
                return square

# boardImage = cv.imread('pictures/game.jpg')
# board1 = board(boardImage)

# square1 = board1.getSquare([200,200])
# print(square1)