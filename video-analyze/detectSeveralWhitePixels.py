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


#First of all, we want to create a mask and display the subtracted background

#bild = cv2.imread("../material/bild.jpg")

cap = cv2.VideoCapture('output1.avi')
while(cap.isOpened()):
    ret, bild = cap.read()

    red = bild   [:,:,2]
    green = bild [:,:,1]
    blue = bild  [:,:,0]

    redWhiteLower = 230;
    redWhiteUpper = 255;
    red_candidates = cv2.inRange(red, redWhiteLower, redWhiteUpper)

    cv2.imshow('frame',red_candidates)
    print "red candidates for laser points = brightest section of red challenge"
    while(1):
            if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    img = bild
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,gray = cv2.threshold(gray,127,255,0)
    gray2 = gray.copy()
    mask = np.zeros(gray.shape,np.uint8)

    contours, hier = cv2.findContours(gray,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if 10 < cv2.contourArea(cnt) < 20:
            cv2.drawContours(img,[cnt],0,(0,255,0),2)
            cv2.drawContours(mask,[cnt],0,255,-1)

    cv2.imshow('frame',mask)
    print "mask"
    while(1):
            if cv2.waitKey(1) & 0xFF == ord('q'):
		break

    cv2.imshow('frame',img)
    print "img"
    while(1):
            if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

"""
cv2.imshow('frame',red_candidates)
print "red candidates for laser points = brightest section of red challenge"
while(1):
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break



bgs = cv2.BackgroundSubtractorMOG()
fgmask_red = bgs.apply(red)
cv2.imshow('frame',fgmask_red)
print "red channel after subtraction of background"
while(1):
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

bild_blurred = cv2.GaussianBlur(bild, (5,5),0 )

cv2.imshow('frame',bild_blurred)
print "blurred picture"
while(1):
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

red_blurred = bild_blurred[:,:,2]

redBlurredWhiteLower = 230;
redBlurredWhiteUpper = 255;
red_blurred_candidates = cv2.inRange(red_blurred, redBlurredWhiteLower, redBlurredWhiteUpper)
cv2.imshow('frame',red_blurred_candidates)
print "red candidates for blurred picture"
while(1):
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

"""

"""
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


#initialize array for laser position
#laser = np.zeros((bild.shape[0], bild.shape[1]))
centroid_laser = get_laser_points(bild);

print "hopefully laser point positions"
cv2.imshow('frame',centroid_laser)
while(1):
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
"""
