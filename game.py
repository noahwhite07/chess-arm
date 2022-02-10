import cv2 as cv
import numpy as np
from board import board 
from board_state import boardState
import computer_vision


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
# 13. ???
# 14. Profit





# To interpret the player move we need to consider the following cases: 
# 1. Single move/ capture
# 2. Promotion: I think this is the same notation as a single move, the engine knows how to handle it
# 3. Castling: did two white pieces move simultaneously? What direction did they move?
# First just handle single moves, captures and promotions
# It's not even explicitly necessary to track the black pieces.
# If we assume the piece is in the center, and we know the locations of the squares,
#  we can just go to the center of the square to move the black pieces


# This module contains the methods that are called by the engine to fetch the move made by the player
#  and to send the engine move to the arm
    

# Method generates a string representing the player's move (ex. 'e2e4') to feed into the engine
# Takes in and compares two consequtive board states
def generateMove(prevState, currentState):
    # These are the nested lists of occupied squares of each color
    #  taken before and after a player move

    # This method should take two frames from the video stream:
    # one triggered by the robot finishing its move, and one triggered by the player hitting his clock

    prevSquares = prevState.getOccupiedSquares()
    currentSquares = currentState.getOccupiedSquares()

    whitePieceColor = 0



    # Converts the occupied squares for white pieces into a set to compare the lists and find the piece that moved
    prevSet = set(prevSquares)
    currSet = set(currentSquares)

    # Does subtraction on the sets to find the square that changed in each list 
    # Subtraction returns single-element sets, so convert them to lists and use their 0th element
    initSquare = list(prevSet - currSet)
    finalSquare = list(currSet - prevSet)

    # Returns the string containing the move to feed the engine (ex. 'e2e4')
    return (initSquare[0] + finalSquare[0])

def send_move():
    # A string to hold the player's move
    playerMove = ''

    # A list to store two frames taken before and after each player move
    captures = []

    # Begins capturing video from the camera
    cameraIn = cv.VideoCapture(0, cv.CAP_DSHOW)

    # Takes one frame from the video input to initialize the board object
    ret, boardImg = cameraIn.read()

    # Initializes a board object for the game
    myBoard = board(boardImage = boardImg)

    # Loop runs until two captures are taken from the video feed
    while(True):
    
        ret, frame = cameraIn.read()
    
        # Display the video feed
        cv.imshow('frame', frame)

        # Displays the captures taken
        for i, capture in enumerate(captures):
            cv.imshow(f'capture {i}', capture)

        # If the user inputs 'c', take a capture from the video feed
        if cv.waitKey(10) & 0xFF == ord('c'):
            print("captured")
            ret, capture = cameraIn.read()
            captures.append(capture)

        # If the user inputs 'q', exit the program
        if cv.waitKey(20) & 0xFF == ord('q'):
            # After the loop release the cap object
            cameraIn.release()
            # Destroy all the windows
            cv.destroyAllWindows()

        # Once two captures are taken, calculate the move 
        if len(captures) > 1:
            # Initializes board states from the two captures
            prevState = boardState(myBoard, captures[0])
            currentState = boardState(myBoard, captures[1])

            # Generates the move using the two boardStates and assigns it to move
            playerMove = generateMove(prevState, currentState)
            print(f'Move: {playerMove}')
            break

    # Returns a string reperesting the players move (ex. 'e2e4)
    return playerMove

# Eventually, the purpose of this method will be to call whatever program is responsible for moving the arm 
def recieve_move(botMove):
    print(f'engine move: {botMove}')

