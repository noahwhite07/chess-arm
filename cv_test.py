import cv2 as cv
import numpy as np
from board import board
import matplotlib.pyplot as plt
import computer_vision

boardImg = cv.imread('pictures/prev_2.jpg')
boardImg2 = cv.imread('pictures/frame.jpg')
imgPlot = plt.imshow(boardImg2)
plt.show()
myBoard = board(boardImg2)

square = myBoard.getSquare([100,400])
print(f'square: {square}')

# computer_vision.drawBlobPoints(boardImg, 7)
# cv.waitKey(0)
# computer_vision.drawBlobPoints(boardImg2, 7)
# #square = myBoard.getSquare([660,60])
# cv.waitKey(0)

