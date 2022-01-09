import cv2 as cv
import computer_vision
from board_state import boardState
from board import board
import game

def getSquares():
    prevState = boardState(myBoard, captures[0])
    currentState = boardState(myBoard, captures[1])
    
    move = game.generateMove(prevState, currentState)
    print(f'Move: {move}')
    prevOccupiedSquares = prevState.getOccupiedSquares()
    currentOccupiedSquares = currentState.getOccupiedSquares()
    print(f'previously occupied squares: {prevOccupiedSquares}')
    print(f'currently occupied squares: {currentOccupiedSquares}')

    pass

cameraIn = cv.VideoCapture(0, cv.CAP_DSHOW)
captures = []

# Captures a frame on startup to create the board object with
ret, boardImg = cameraIn.read()
cv.imshow('Initial Frame', boardImg)

# Initializes a board object
myBoard = board(boardImage = boardImg)

boardImg2 = cv.imread('pictures/prev_2.jpg')
# Draws the blobPoints on the initial frame for testing

computer_vision.drawBlobPoints(boardImg2, 7)
computer_vision.drawBlobPoints(boardImg, 7)
computer_vision.drawBlobPoints(boardImg, 6)

while(True):
   

    ret, frame = cameraIn.read()
  
    # Display the resulting frame
    cv.imshow('frame', frame)

    for i, capture in enumerate(captures):
        cv.imshow(f'capture {i}', capture)

    if cv.waitKey(10) & 0xFF == ord('c'):
        print("captured")
        ret, capture = cameraIn.read()
        captures.append(capture)
        whitePoints = computer_vision.getBlobPoints(capture, 7)
        print(f'White Points: {whitePoints}')
        redPoints = computer_vision.getBlobPoints(capture, 6)
        print(f'Pink Points: {redPoints}')

    if cv.waitKey(20) & 0xFF == ord('q'):
        # After the loop release the cap object
        cameraIn.release()
        # Destroy all the windows
        cv.destroyAllWindows()

    if len(captures) > 1:
        getSquares()
        break
        
