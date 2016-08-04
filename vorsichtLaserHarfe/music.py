
import rtmidi_python as rtmidi
import time

class music:
	beams = 0;			# number of beams
	active = {};		# status array, to store weather a tone is currently active
	modifier = 1;		# modifier, for future use, such as pedal, to switch the octave.
	lowestpitch = 60	# 60 is normal c, 61 is c#, 62 is d ....
	useFullSteps = True	# use ganzton or halbton steps, 60->62, or 60->61
	midiout = 0;
	instrument = 69;
	
	def __init__(self, beams, mods = 0, lowestpitch = 60, useFullSteps = True, instrument = 69):	## sets the number of beams. and builds the status array.
		self.beams = beams;
		self.active = {}
		self.modifier = mods + 1
		self.lowestpitch = lowestpitch
		self.useFullSteps = useFullSteps
		self.intstrument = instrument
		
		self.midiout = rtmidi.MidiOut()
		print("found following midi ports")
		for port_name in self.midiout.ports:
			print(port_name)
		if self.midiout.ports:
		#    midiout.open_virtual_port("My virtual output")
			self.midiout.open_port(2)
		else:
			self.midiout.open_virtual_port("My virtual output")


		for m in range(self.modifier):
			for b in range(self.beams):
				pit = self.pitch(b, m, self.useFullSteps);
				self.active[pit]= 0;
				#midiout.send_message([0x90, pit, 127]) ## start the tones 
				#midiout.send_message([0xB0, 07, 0])    ## and set their volume to 0
		
	def pitch(self, beam, modifier = 0, full = True):
		if full == True:	
			return self.lowestpitch + beam*2 + modifier*2*self.beams;	## returns pitch with "ganztonschritt"
		if full == False:
			return self.lowestpitch + beam + modifier*self.beams;		## returns pitch with "halbtonschritt"
		midiout.send_message([0xC0+beam,self.intstrument])
	
	def play(self, beam, amp, modifier = 0):
		pit = self.pitch(beam, modifier, self.useFullSteps)
		if amp > 0:
			if self.active[pit] == 0:
				self.midiout.send_message([0x90+beam, pit, 127])
				self.midiout.send_message([0xB0+beam, 07, amp]) ## here absolute volume is set.
				self.active[pit] = amp;
			elif self.active[pit] != 0:
				self.midiout.send_message([0xB0+beam, 07, amp]) ## here absolute volume is set.
		else:	## amp <= 0
			self.midiout.send_message([0x80+beam, pit, 127])
		
	def test(self):
		print("Timidity music test...")
		self.midiout.send_message([0x90, 60, 127])
		self.midiout.send_message([0xB0, 07, 100])
		time.sleep(1);
		self.midiout.send_message([0x80, 60, 127])
		print "Did you hear a tone? There is a problem if you didn't."
		return 0;
