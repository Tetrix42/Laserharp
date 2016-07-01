# getting started https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html

import numpy as np
import cv2
import rtmidi_python as rtmidi
import time
import scipy.misc

#cap = cv2.VideoCapture(0)	# 0 for /dev/video0; 1 for /dev/video1; or a filename.
#print("dimension", cap.get(3), cap.get(4)) #http://docs.opencv.org/modules/highgui/doc/reading_and_writing_images_and_video.html#videocapture-get
#print("fps:", cap.get(5))
#print("codec:", cap.get(6))
#print("bright:", cap.get(10))
#print("cont:", cap.get(11))
#print("sat:", cap.get(12))
#print("rgp:", cap.get(16))

#--------#
#configure MIDI
midiout = rtmidi.MidiOut()

for port_name in midiout.ports:
    print port_name

if midiout.ports:
#    midiout.open_virtual_port("My virtual output")
    midiout.open_port(2)
    print "openend port"
else:
    midiout.open_virtual_port("My virtual output")

time.sleep(0.1)

program_change = [0xC0, 19]
midiout.send_message(program_change) 

note_on = [0x90, 60, 127] # channel 1, middle C, velocity 112
note_off = [0x80, 60, 50]
midiout.send_message(note_on)
print "on"
time.sleep(1)
print "off"
midiout.send_message(note_off)
print "did you hear a tone? there is a problem if you didn't."
#--------#

#First of all, we want to create a mask and display the subtracted background

#bild = cv2.imread("../material/bild.jpg")

cap = cv2.VideoCapture('output1.avi')
ret1, bild1 = cap.read()
height = bild1.shape[1]
tone_old = 100;
tonemap = [0];

for i in range(50):
	cap.read();

channels = [0];

def tone_update(tones):
	chan = -1;
	for i in tones:
		chan += 1
		amp = np.int(i *1.5);
		print "amp: " + str(amp)
		pitch = np.round((chan+1)*60)
		print "pitch: " + str(pitch)
		
		#program_change = [0xC0+chan, 19]
		#midiout.send_message(program_change) 
		
		if channels[chan] == 0: 
			midiout.send_message([0x90+chan, pitch, amp])
			channels[chan] = i;
			print "an --------------------- an"
		
		if i == 0:
			pass
			midiout.send_message([0x80+chan, pitch, amp])
			channels[chan] = 0;
			print "aus --------------------- aus"
		
		#midiout.send_message([0xA0+chan, pitch, amp])
		if channels[chan] != 0:
			midiout.send_message([0xB0+chan, 11, amp]) 	## this command is relative
			midiout.send_message([0xB0+chan, 07, amp]) ## here absolute volume is set. 
			##  http://midi-tutor.proboards.com/thread/12/8-controlling-midi-volume
			
		#midiout.send_message([0xD0+chan, amp])
	#end = time.clock()
	#print "%.2f Hz" % (1./(end-start))
	#print "%.2f s" % (end-start)
	#start = time.clock()
	
	#tone_old = tone



while(cap.isOpened()):
    ret, bild = cap.read()

    red = bild   [:,:,2]
#    green = bild [:,:,1]
#    blue = bild  [:,:,0]

    redWhiteLower = 230;
    redWhiteUpper = 255;
    red_candidates = cv2.inRange(red, redWhiteLower, redWhiteUpper)

    cv2.imshow('frame',red_candidates)
    print "red candidates for laser points = brightest section of red challenge"
    #~ while(1):
            #~ if cv2.waitKey(1) & 0xFF == ord('q'):
                    #~ break

    img = bild
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,gray = cv2.threshold(gray,127,255,0)
    gray2 = gray.copy()
    mask = np.zeros(gray.shape,np.uint8)

    contours, hier = cv2.findContours(gray,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    tonemap[0] = 0
    for cnt in contours:
        if 10 < cv2.contourArea(cnt) < 20:
            cv2.drawContours(img,[cnt],0,(0,255,0),2)
            print("Abstand vom oberen Bildschirmrand:")
            distance_above = np.mean(cnt[1])
            cv2.drawContours(mask,[cnt],0,255,-1)
            tone = np.round((height-distance_above)*255/height/3)
            #(tones only have a scale from 0 to 255)
            print(tone)
            tonemap[0] = tone
            #midiout.send_message([0x80, tone_old, 10])
            #end = time.clock()
            #print "%.2f Hz" % (1./(end-start))
            #print "%.2f s" % (end-start)
            #start = time.clock()
            #midiout.send_message([0x90, tone, 127])
            tone_old = tone
    tone_update(tonemap)
    cv2.imshow('frame',mask)
    print "mask"
    #~ while(1):
            #~ if cv2.waitKey(1) & 0xFF == ord('q'):
		#~ break

    cv2.imshow('frame',img)
    print "img"
    #~ while(1):
            #~ if cv2.waitKey(1) & 0xFF == ord('q'):
                    #~ break
    cv2.waitKey(1)
    time.sleep(1/24.)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

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
