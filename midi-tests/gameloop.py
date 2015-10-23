## programme that plyas sound while key is being pressed
## use "uiaeo"

import time
import rtmidi_python as rtmidi
import pygame
from pygame.locals import *
pygame.init()

width, height = 1000, 100
screen=pygame.display.set_mode((width, height))

midiout = rtmidi.MidiOut()
#available_ports = midiout.get_ports()

for port_name in midiout.ports:
    print port_name

if midiout.ports:
#    midiout.open_virtual_port("My virtual output")
    midiout.open_port(2)
    print "openend port"
else:
    midiout.open_virtual_port("My virtual output")

time.sleep(0.1)
#program_change = [0xC0, 19]
#midiout.send_message(program_change) 

note_on = [0x90, 60, 127] # channel 1, middle C, velocity 112	
note_off = [0x80, 60, 50]
midiout.send_message(note_on)
print "on"
time.sleep(1)
print "off"
midiout.send_message(note_off)
print "did you hear a tone? there is a problem if you didn't."


"""
8x 	1000xxxx 	nn vv 	Note aus
nn=Noten-Nummer
vv=Geschwindigkeit
9x 	1001xxxx 	nn vv 	Note an
nn=Noten-Nummer
vv=Geschwindigkeit
Ax 	1010xxxx 	nn vv 	Noten-Abklingen
nn=Note
vv=Geschwindikkeit
Bx 	1011xxxx 	cc vv 	Kontrollaenderung
cc=Kontrollnummer
vv=Neuer Wert
Cx 	1101xxxx 	cc 	Kanalausklang
cc=Kanalnummer
Ex 	1110xxxx 	bb tt 	Tonhoehenaenderung
bb=Boden
tt=Hoechster Wert
"""
keys = [False, False, False, False, False]

while 1:
	#midiout.send_message(program_change) 
	#midiout.send_message(note_on)
	#print i
	#midiout.send_message(note_on)
	#time.sleep(2)
	#midiout.send_message(note_off)
	#time.sleep(1)

	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			print event.key
			
			midiout.send_message([0x90, event.key, 127])
			if event.key==K_u:
				#midiout.send_message([0x90, 60, 127])
				keys[0]=True
			elif event.key==K_i:
				#midiout.send_message([0x90, 61, 127])
				keys[1]=True
			elif event.key==K_a:
				#midiout.send_message([0x90, 62, 127])
				keys[2]=True
			elif event.key==K_e:
				#midiout.send_message([0x90, 63, 127])
				keys[3]=True
			elif event.key==K_o:
				#midiout.send_message([0x90, 64, 127])
				keys[4]=True
		if event.type == pygame.KEYUP:
			midiout.send_message([0x80, event.key, 10])
			if event.key==pygame.K_u:
				#midiout.send_message([0x80, 60, 127])
				keys[0]=False
			elif event.key==pygame.K_i:
				#midiout.send_message([0x80, 61, 127])
				keys[1]=False
			elif event.key==pygame.K_a:
				#midiout.send_message([0x80, 62, 127])
				keys[2]=False
			elif event.key==pygame.K_e:
				#midiout.send_message([0x80, 63, 127])
				keys[3]=False
			elif event.key==pygame.K_o:
				#midiout.send_message([0x80, 64, 127])
				keys[4]=False
	
	for i in range (5):
		if keys[i] == True:
			pass
			#print i
		if keys[i] == False:
			pass

del midiout
