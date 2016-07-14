# getting started https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html

import numpy as np
import cv2
import rtmidi_python as rtmidi
import time
import scipy.misc
import math
import sys

lasernumber = 2
tone_old = 100
device = 1
dummy = 0

cap = cv2.VideoCapture(device) # 0 for /dev/video0; 1 for /dev/video1; or a filename.
ret, bild = cap.read()
height = bild.shape[1]
#cap.release()
cv2.waitKey(1)
#cv2.destroyAllWindows()


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

note_on = [0x90, 60, 127] # channel 1, middle C, velocity 112
note_off = [0x80, 60, 50]
midiout.send_message(note_on)
print "on"
time.sleep(1)
print "off"
midiout.send_message(note_off)
print "did you hear a tone? There is a problem if you didn't."
#--------#


#-- Calibration start -#

tone=62
chan=0

midiout.send_message([0xB0+chan, 07, 127]) # here absolute volume is set.
midiout.send_message([0xC0+chan,19])
midiout.send_message([0x90+chan, tone, 127])
height = 1
i=0
while(1):
    i=i+1
    a=0.0001*i
    corY = np.sin(a)*np.sin(a)
    print "corY :"+str(corY)
    amp = int(127.*corY/height)
    print amp
        #print "amp: "+str(amp)
        #tone = np.round(60+2*tonhoehe)
        #(tones only have a scale from 0 to 255)
        #print(tone)
        #midiout.send_message([0xB0+chan, 11, amp]) # here relative volume is set.
    midiout.send_message([0xB0+chan, 07, amp]) # here absolute volume is set.
        #midiout.send_message([0x80, tone_old, 10])
        #end = time.clock()
        #print "%.2f Hz" % (1./(end-start))
        #print "%.2f s" % (end-start)
        #start = time.clock()
        #midiout.send_message([0x90, tone, 127])
        #tone_old = tone

#midiout.send_message([0x80+chan, tone, 50])





