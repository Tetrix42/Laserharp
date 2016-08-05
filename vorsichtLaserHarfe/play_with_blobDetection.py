# getting started https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html


from music import music
from laser import laser




lasernumber = 5
device = 1
dummy = 0
instrument = 61


mc = music(lasernumber ,0,60,True, instrument);
mc.test();

harfe = laser(lasernumber, device, dummy);
harfe.calibration()


while(1):
#	ak = cv2.waitKey(1)
#	if ak != -1:
#		ak = chr(ak)
#		if ak == 'c':
#			sys.exit()
	keylist = harfe.readInputUntilRecognition(0)
	
	for i in range(lasernumber):
		harfe.beams[i] = 0;
	
	for key in keylist:
		cor = [key.pt[0], key.pt[1]]
		abstand,beam = harfe.DistanceToNearestLine(cor, False)
		
		if abstand < 10:
			#print(beam, abstand)
			harfe.calcAmp(beam, cor)
	
	for i in range(lasernumber):
		#print(i, beams[i])
		mc.play(i, harfe.beams[i])
		






