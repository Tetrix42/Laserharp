# getting started https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html

import numpy as np
import cv2
import datetime

import scipy.misc

cap = cv2.VideoCapture(0)	# 0 for /dev/video0; 1 for /dev/video1; or a filename.


print("dimension", cap.get(3), cap.get(4)) #http://docs.opencv.org/modules/highgui/doc/reading_and_writing_images_and_video.html#videocapture-get
print("fps:", cap.get(5))
print("codec:", cap.get(6))
print("bright:", cap.get(10))
print("cont:", cap.get(11))
print("sat:", cap.get(12))
print("rgp:", cap.get(16))


#while(True):
a = datetime.datetime.now()
for x in range(100):
	# Capture frame-by-frame
	ret, frame = cap.read()

	# Our operations on the frame come here
	#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	print(frame.shape)
    
	rot = frame[:,:,2]	# image is sorted BGR
    
    
#	scipy.misc.imsave("b.png", frame[:,:,0]);
#	scipy.misc.imsave("g.png", frame[:,:,1]);
#	scipy.misc.imsave("r.png", frame[:,:,2]);
#	scipy.misc.imsave("bgr.png", frame);  # gives wrong colors, because false sorted BGR interpreted as RGB
    
	# Display the resulting frame
#	cv2.imshow('frame',frame)
#	if cv2.waitKey(1) & 0xFF == ord('q'):
#		break
#	break;
# When everything done, release the capture
b = datetime.datetime.now()
print(b-a)
print((b-a)/100.)
cap.release()
cv2.destroyAllWindows()
