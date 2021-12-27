import cv2 as cv
import numpy as np

img = cv.imread('pictures/goose.jpg')
cv.imshow('image', img)
cv.waitKey(0)