import cv2 as cv
import numpy as np
from board import board 
from board_state import boardState

#import sunfish
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

boardImg = cv.imread('pictures/game_2.jpg')
gameBoard = board(boardImg)

prevImg = cv.imread('pictures/prev.jpg')
currentImg = cv.imread('pictures/current.jpg')

prevState = boardState(gameBoard, prevImg)
currentState = boardState(gameBoard, currentImg)


# Method generates a string representing the player's move (ex. e2e4) to feed into the engine
# Takes in and compares two consequtive board states

# There are a few things we need to keep track of
# Odd or even turn? Turns start at 1 so odd turns are always player turns
# If even turn, robot moves, if odd turn, we need to interpret the player move
# To interpret the player move we need to consider the following cases: 
# 1. Single move/ capture
# 2. Promotion: I think this is the same notation as a single move, the engine knows how to handle it
# 3. Castling: did two white pieces move simultaneously? What direction did they move?
# First just handle single moves, captures and promotions
# It's not even explicitly necessary to track the black pieces.
# If we assume the piece is in the center, and we know the locations of the squares,
#  we can just go to the center of the square to move the black pieces

def generateMove(prevState, currentState):
    # These are the nested lists of occupied squares of each color
    #  taken before and after a player move
    prevSquares = prevState.getOccupiedSquares()
    currentSquares = currentState.getOccupiedSquares()

    # We only need one color for all the white pieces now.
    # For now, assume the white pieces are red, and fix the color mess later
    whitePieceColor = 0

    # for i, square in enumerate(prevSquares[whitePieceColor]):
    #     print(f'prev: {square}\t current: {currentSquares[0][i]}')

    # Converts the occupied squares for white pieces into a set to compare the lists and find the piece that moved
    prevSet = set(prevSquares[whitePieceColor])
    currSet = set(currentSquares[whitePieceColor])

    # Does subtraction on the sets to find the square that changed in each list 
    # Subtraction returns single-element sets, so convert them to lists and use their 0th element
    initSquare = list(prevSet - currSet)
    finalSquare = list(currSet - prevSet)

    # Returns the string containing the move to feed the engine (ex. 'e2e4')
    return (initSquare[0] + finalSquare[0])

def send_move():
    return 'e2e4'
def recieve_move(botMove):
    print(f'engine move: {botMove}')

generateMove(prevState, currentState)
