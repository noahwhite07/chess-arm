import cv2 as cv
import numpy as np
from board import board 
import board_state
# This program should be responsible for handling the state and progression of the game
# All calls to the engine itself should be made within this program 
# 
# The frames taken from the webcam should be taken here and piped into the other scripts
# For now, assume camera is totally stationary, generation of square coordinates should only be done once
# 
# Calls to whatever program handles movement of the arm should be called from here too
#
# Sequence should be as follows:

# 1. Take initial frame upon startup (probably a button for startup)
# 2. Get the coordinates for all the squares from the first image
#    This should be called once here, not in the constructor of board_state.
# 3. Get and store the initial state  
# 4. Wait for input (user hits clock or some button)
# 5. Get and store the current state 
# 6. Pass the previous and current state to generate_move
# 7. Feed the generated move into the engine
# 8. Use retreive_move to get the move from the engine
# 9. Feed the engine move into a move_arm program that should take in the move
# 10. Make the current state the previous state
# 11. Arm hits clock (this might not be physical)
# 12. Repeat steps 4-11 until robot inevitably wins 
# 13. Robot makes a jacking-off motion towards the player as a taunt
# 14. ???
# 15. Profit
#added comment to test git shit

boardImg = cv.imread('pictures/game.jpg')
gameBoard = board(boardImg)

square = gameBoard.getSquare([500,500])
points = gameBoard.getBlobPoints(3)
print(points)