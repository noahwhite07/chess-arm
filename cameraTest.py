import cv2 as cv

cameraIn = cv.VideoCapture(0, cv.CAP_DSHOW)

while(True):
   

    ret, frame = cameraIn.read()
  
    # Display the resulting frame
    cv.imshow('frame', frame)

    if cv.waitKey(10) & 0xFF == ord('q'):
        # After the loop release the cap object
        cameraIn.release()
        # Destroy all the windows
        cv.destroyAllWindows()