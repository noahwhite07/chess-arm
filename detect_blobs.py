# Program should take in a string for color and output a list
#
#  of points where a blob of that color appears
#
# There are 6 unique chess pieces, so there should be at least 6 colors hardcoded
# There should probably be more. I might use color to outline the corners of the board
#
# White and black pieces don't need different color schemes because we always know whose turn it is
#
# Colors: green, cyan, indigo, pink, yellow, orange, red 
#
# Color upper and lower values should be stored as a list
# Masks, masked images, and thresholded images should also be stored in a list inthe same order
#
# For consistency, everything should be stored in ROYGBIV format but with pink as violet
#  and cyan as blue
#
# Lists might be more trouble than they're worth. Come back to it
#
#
import cv2 as cv
import numpy as np

# import overhead picture of board
board = cv.imread('pictures/game_2.jpg')

# convert board image to HSV
boardHSV = cv.cvtColor(board, cv.COLOR_BGR2HSV)


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
    maskedImages.append(cv.bitwise_and(board, board, mask = colorMask))

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
    boardsWithKeypoints.append(cv.drawKeypoints(board, keyPoints, np.array([]), (0,0,0), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS))


#given a color 0-6 in ROYGBIV format, getBlobPoints returns the locations (centerpoints) of all the blobs of that color
def getBlobPoints(color):
    points = []
    for keyPoint in keyPointsList[color]:  
        x = keyPoint.pt[0]
        y = keyPoint.pt[1]
        point = [x,y]
        points.append(point)
    return points


#cv.imshow("bbb", board)

# print(getBlobPoints(4))

# cv.imshow("green keypoints", boardsWithKeypoints[3])
# cv.imshow("cyan keypoints", boardsWithKeypoints[4])
# cv.imshow("yellow keypoints", boardsWithKeypoints[2])
# cv.imshow("orange keypoints", boardsWithKeypoints[1]) 
# cv.imshow("indigo keypoints", boardsWithKeypoints[5])
# cv.imshow("pink keypoints", boardsWithKeypoints[6])
# cv.imshow("red keypoints", boardsWithKeypoints[0])



cv.waitKey(0)