import cv2 as cv
import numpy as np

# Image of the previous board state
state1 = cv.imread('pictures/game.jpg')

# Image of the current board state
state2 = cv.imread('pictures/game_2.jpg')

cv.imshow("previous state", state1)
cv.imshow("current state", state2)

