import cv2 as cv

#print("Before URL")
#cap = (cv.VideoCapture('http://admin:admin@192.168.10.11:80'))
cap = (cv.VideoCapture('rtsp://admin:admin@192.168.10.12:554/live/main'))
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Display the resulting frame
    cv.imshow('frame', gray)
    if cv.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()