# getting started https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html

import numpy as np
import time
import cv2

import scipy.misc

cap = cv2.VideoCapture(0)	# 0 for /dev/video0; 1 for /dev/video1; or a filename.

#print("dimension", cap.get(3), cap.get(4)) #http://docs.opencv.org/modules/highgui/doc/reading_and_writing_images_and_video.html#videocapture-get
#print("fps:", cap.get(5))
#print("codec:", cap.get(6))
#print("bright:", cap.get(10))
#print("cont:", cap.get(11))
#print("sat:", cap.get(12))
#print("rgp:", cap.get(16))



def get_laser_points(image):
    """Return centers of laser-points found in the given image as list of coordinate-tuples."""
    # The color boarders for red laser (appears white on screen)
    whiteLower = (190, 190, 220)
    whiteUpper = (255, 255, 255)
    # get the contour areas for the steppers
    mask = cv2.inRange(image, whiteLower, whiteUpper)
    
    cv2.imshow('frame', mask)
    
    while(1):
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # compute the center of the contour areas
    centroids = []
    for contour in contours:
        m = cv2.moments(contour)
        # avoid division by zero error!
        if m['m00'] != 0:
            cx = int(m['m10'] / m['m00'])
            cy = int(m['m01'] / m['m00'])
            centroids.append((cx, cy))
            # following line manages sorting the found contours from left to right, sorting
            # first tuple value (x coordinate) ascending
            centroids = sorted(centroids)

    return centroids










bild = cv2.imread("../material/hibaby.jpg")

red = bild   [:,:,2]
green = bild [:,:,1]
blue = bild  [:,:,0]



cv2.imshow('frame',bild)
print "red"
while(1):
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break





#~ for x in xrange(red.shape[0]):
	#~ for high in np.where(red[x] < 220):
		#~ for y in high:
			#~ #print x,y
			#~ bild[x,y] = 0

whiteLower = (190, 190, 220)
whiteUpper = (255, 255, 255)
candidates = cv2.inRange(bild, whiteLower, whiteUpper)

print candidates

laser = np.zeros((bild.shape[0], bild.shape[1]))
coords = get_laser_points(bild)

for c in coords:
	laser[c[1], c[0]] = 220


#red = np.where(bild>100)
#print red

cv2.imshow('frame',red)
print "red"
while(1):
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break


print "green"
cv2.imshow('frame',green)
while(1):
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break


print "blue"
cv2.imshow('frame',blue)
while(1):
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

print "laser"
cv2.imshow('frame',laser)
while(1):
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

#print frame


#time.sleep(2)
