# programme that runs over all midi ports, to find the current working one 

import time
#import rtmidi
import rtmidi_python as rtmidi


#midiout = rtmidi.MidiOut()
#available_ports = midiout.ports()

#~ if available_ports:
    #~ midiout.open_port(0)
#~ else:
    #~ midiout.open_virtual_port("My virtual output")

#midiout.open_port(0)

for i in range(10):
	midiout = rtmidi.MidiOut()
	midiout.open_port(i)
	note_on = [0x90, 60, 112] # channel 1, middle C, velocity 112
	note_off = [0x80, 60, 0]
	midiout.send_message(note_on)
	print i
	time.sleep(0.5)
	midiout.send_message(note_off)
	del midiout
	time.sleep(1)
del midiout
