# getting started https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html

import numpy as np
import time
import cv2

import scipy.misc

#cap = cv2.VideoCapture(0)	# 0 for /dev/video0; 1 for /dev/video1; or a filename.
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
    print "image with a with mask = display only bright region of picture"
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
    centroids.apply(bild);
    return centroids






#First of all, we want to create a mask and display the subtracted background

bgs = cv2.BackgroundSubtractorMOG2()
bild = cv2.imread("../material/bild.jpg")

red = bild   [:,:,2]
green = bild [:,:,1]
blue = bild  [:,:,0]


print "green channel"
cv2.imshow('frame',green)
while(1):
	if cv2.waitKey(1) & 0xFF == ord('q'): #proceed only if q is pressed
		break


print "blue channel"
cv2.imshow('frame',blue)
while(1):
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

print "red channel"
cv2.imshow('frame',red)
while(1):
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break


fgmask = bgs.apply(bild)

cv2.imshow('frame',fgmask)
print "picture mask after subtraction of background"
while(1):
	if cv2.waitKey(1) & 0xFF == ord('q'): #proceed only if q is pressed
		break

fgmask_red = bgs.apply(red)
cv2.imshow('frame',fgmask_red)
print "red channel after subtraction of background"
while(1):
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

bild_bitwise_and = cv2.bitwise_and(bild,bild,mask=fgmask) # "bitwise and" probably filters contours by comparing absolute values of the brightness

cv2.imshow('frame',bild_bitwise_and)
print "picture after \"bitwise_and\" operation"
while(1):
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break


whiteLower = (190, 190, 190)
whiteUpper = (255, 255, 255)
candidates = cv2.inRange(bild_bitwise_and, whiteLower, whiteUpper)

cv2.imshow('frame',candidates)
print "candidates for laser points = brightest section of bitwise_and-contours"
while(1):
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

redWhiteLower = 230;
redWhiteUpper = 255;
red_candidates = cv2.inRange(red, redWhiteLower, redWhiteUpper)

cv2.imshow('frame',red_candidates)
print "red candidates for laser points = brightest section of red challenge"
while(1):
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

#bild = cv2.GaussianBlur(bild, (11,11),0 )


#initialize array for laser position
#laser = np.zeros((bild.shape[0], bild.shape[1]))
centroid_laser = get_laser_points(bild);

print "hopefully laser point positions"
cv2.imshow('frame',centroid_laser)
while(1):
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

