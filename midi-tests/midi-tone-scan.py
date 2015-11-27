# midi  test, plays a tone of all available sound profiles
#
# hi!
import time
import rtmidi_python as rtmidi

midiout = rtmidi.MidiOut()
#available_ports = midiout.get_ports()

for port_name in midiout.ports:
    print port_name

if midiout.ports:
#    midiout.open_virtual_port("My virtual output")
    midiout.open_port(1)   ##-----------------------------------change midi port here
    print "openend port"
else:
    midiout.open_virtual_port("My virtual output")

time.sleep(0.1)
#program_change = [0xC0, 51]
#midiout.send_message(program_change)
note_on = [0x90, 60, 127] # channel 1, middle C, velocity 112
#note_abkling = [0xE0, 0, 127]
note_off = [0x80, 60, 50]
midiout.send_message(note_on)
#midiout.send_message([0x90, 80,112])
time.sleep(2)

#print "abkling"
#midiout.send_message(note_abkling)
time.sleep(1)
print "aus"
midiout.send_message(note_off)

time.sleep(1)

"""
0x8[0-F] 	1000xxxx 	nn vv 	Note aus
nn=Noten-Nummer
vv=Geschwindigkeit
0x9[0-F] 	1001xxxx 	nn vv 	Note an
nn=Noten-Nummer
vv=Geschwindigkeit
A[0-F] 	1010xxxx 	nn vv 	Noten-Abklingen
nn=Note
vv=Geschwindikkeit
B[0-F] 	1011xxxx 	cc vv 	Kontrollaenderung
cc=Kontrollnummer
vv=Neuer Wert
C[0-F] 	1101xxxx 	cc 	Kanalausklang
cc=Kanalnummer
E[0-F] 	1110xxxx 	bb tt 	Tonhoehenaenderung
bb=Boden
tt=Hoechster Wert
"""
for i in range(256):
	print i
	program_change = [0xC0, i]
	midiout.send_message(program_change)
	#midiout.send_message(note_on)
	midiout.send_message(note_on)
	time.sleep(1)
	midiout.send_message(note_off)
	time.sleep(0.1)



time.sleep(1)

del midiout
