import numpy as np
import cv2

cap = cv2.VideoCapture(0)

for i in range(10):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    #cv2.imshow('frame', frame)
    cv2.imwrite('messigray.png', frame)


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()