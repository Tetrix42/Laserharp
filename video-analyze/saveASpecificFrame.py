import time
import numpy as np
import cv2

count = 0
cap = cv2.VideoCapture('output1.avi')

# Define the codec and create VideoWriter object
fourcc = cv2.cv.CV_FOURCC(*'XVID')
out = cv2.VideoWriter('output3.avi',fourcc, 8.0, (640,480))
#my = cap.get(CV_CAP_PROP_FPS)
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        count += 1
        # frame = cv2.flip(frame,0)
        rot = frame[:,:,2]	# image is sorted BGR
        rs = rot[180:320,:]
        # write the red frame
        out.write(frame)
        # show the red frame
        cv2.imshow('frame', frame)
        '''
        while(1):
	    if cv2.waitKey(1) & 0xFF == ord('n'):
	        print(count)
                break
            if cv2.waitKey(1) & 0xFF == ord('s'):
                cv2.imwrite("hibaby2.jpg", frame)
                break
       '''#time.sleep(1)
        if count == 14:
            cv2.imwrite("bg.jpg", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
