
import time

import numpy as np
import cv2
import scipy.misc
import math
import sys
import copy

#---- CV2 command overview ---#
#cap = cv2.VideoCapture(device)	# 0 for /dev/video0; 1 for /dev/video1; or a filename.
#print("dimension", cap.get(3), cap.get(4)) #http://docs.opencv.org/modules/highgui/doc/reading_and_writing_images_and_video.html#videocapture-get
#print("fps:", cap.get(5))
#print("codec:", cap.get(6))
#print("bright:", cap.get(10))
#print("cont:", cap.get(11))
#print("sat:", cap.get(12))
#print("rgp:", cap.get(16))


class laser:
	lasernumber = 0;

	beams = []	## heigths of beams
	cap = 0		## capture device
	bild = 0	## raster image
	
	height = 0	## properties of the capturing device
	width = 0 	##


	# Default values for point detection:
	threshold = 190
	contourMin = 80
	contourMax = 450
	
	
	#allCoords = []
	callibratedCoords = []
	number = 0

	
	
	

	
	def __init__(self, lasers, device = 0, dummy = 0):	## sets the number of beams. and builds the status array.
		self.lasernumber = lasers;
		self.cap = cv2.VideoCapture(device) # 0 for /dev/video0; 1 for /dev/video1; or a filename.
		ret, self.bild = self.cap.read()
		
		self.height = self.bild.shape[1]
		self.width =  self.bild.shape[0]
		
		for m in range(self.lasernumber):
			self.beams.append(0);


	def drawCalibrationProgress(self):		## its a blocking function, which draws all calibrated lines 
		#print allCoords
		#cap = cv2.VideoCapture(device) # 0 for /dev/video0; 1 for /dev/video1; or a filename.
		#ret, bild = cap.read()
		allCoords = self.callibratedCoords;
		for i in range(len(allCoords)):
			coord11 = int(allCoords[i][0][0])
			coord12 = int(allCoords[i][0][1])
			coord21 = int(allCoords[i][1][0])
			coord22 = int(allCoords[i][1][1])
			#    cv2.drawContours(img,[cnt],0,(255,0,0),2)
			#    cv2.drawContours(mask,[cnt],0,255,-1)
			#    cv2.line(bild, (0,0),(511,511),(255,0,255),3)
			cv2.line(self.bild, (coord11,coord12),(coord21,coord22),(255,185,15),3)
		
		cv2.imshow('frame',self.bild)
		print "All right, press 'AnyKey' if You are satisfied."
		b = cv2.waitKey(0)
		b = chr(b) #get the letter from the number returned by waitKey
		if b=='c':
			sys.exit()



	def distanceOfLineAndPoint(self, coord11,coord12,coord21,coord22,cor1,cor2):
		Dx = coord21-coord11
		Dy = coord22-coord12
		d1 = abs(Dy*cor1-Dx*cor2-coord11*coord22+coord21*coord12)
		linelength = math.sqrt(Dx*Dx+Dy*Dy)
		dis = d1/linelength #This is the shortest distance from the point to the entire line
		# However, we also want to draw this distance.
		# For that we need to know the 'orthogonal' point on the line from where you can draw an orthogonal line to the point
		# We use pythagoras to find it:
		disBeginningOfLineToPoint = math.sqrt((coord11-cor1)*(coord11-cor1)+(coord12-cor2)*(coord12-cor2))
		disEndOfLineToPoint = math.sqrt((coord21-cor1)*(coord21-cor1)+(coord22-cor2)*(coord22-cor2))
		disBeginningOfLineToOrthogonalPoint = math.sqrt(disBeginningOfLineToPoint*disBeginningOfLineToPoint-dis*dis)
		ratio = disBeginningOfLineToOrthogonalPoint/linelength
		#print "ratio: "+str(ratio)
		compare = linelength*linelength-(disEndOfLineToPoint*disEndOfLineToPoint - dis*dis)
		if compare <= 0:
			if disBeginningOfLineToPoint < disEndOfLineToPoint: # These two conditions ensure that the point is nearer to the Beginning
				ratio=0 # If line is too short such that point is outwards of line
						# just connect to the front point of the line
		if ratio > 1:
			ratio=1 # If the line is too short for drawing an orthogonal path from the point to the line,
					# just connect the point to the endpoint of the line
		coordsOfOrthPoint = [coord11+ratio*(coord21-coord11),coord12+ratio*(coord22-coord12)]
		corOr1 = int(coordsOfOrthPoint[0])
		corOr2 = int(coordsOfOrthPoint[1])
		disToPoint = math.sqrt((corOr1-cor1)*(corOr1-cor1)+(corOr2-cor2)*(corOr2-cor2))
		return disToPoint,corOr1,corOr2

	def DistanceToNearestLine(self, cor, draw = True):	## for a coordinate of a point, it returns the closest laser, and the distance to the laser
		allCoords = self.callibratedCoords
		cor1 = int(cor[0])
		cor2 = int(cor[1])
		disray = []
		
		if draw == True:
			#cap = cv2.VideoCapture(device)
			#ret, bild = cap.read()
			self.bild
		
		for i in range(len(allCoords)):
			coord11 = int(allCoords[i][0][0])
			coord12 = int(allCoords[i][0][1])
			coord21 = int(allCoords[i][1][0])
			coord22 = int(allCoords[i][1][1])
			if draw == True:
				cv2.line(self.bild, (coord11,coord12),(coord21,coord22),(255,185,15),3)
			# The above line is the calibration line.
			# We now want to draw distance to newly detected point.
			# For that we use the distance formula defined above
			dis,corOr1,corOr2 = self.distanceOfLineAndPoint(coord11,coord12,coord21,coord22,cor1,cor2)
			#print "Distance "+str(i)+": "+str(dis)
			disray.append(dis)
			#cv2.line(bild, (cor1,cor2),(corOr1,corOr2),(255,0,0),5)
		#print "\nMinimum: "+str(min(disray))
		abstand = min(disray)
		#tonhoehe = np.argmin(disray)*7+instrument
		minlaser = np.argmin(disray)
		
		if draw == True :
			cv2.circle(self.bild, (cor1,cor2), 8, ( 0, 0, 255 ),-1, 8 ) # draw laserpointPosition
			cv2.imshow('frame',self.bild)
			b = cv2.waitKey(1)
			if b!=-1:
				b = chr(b) #get the letter from the number returned by waitKey
				if b=='c':
					sys.exit()
		return abstand,minlaser


	def tuneCalibration(self, b,threshold,contourMin,contourMax):
		#threshold
		if b=='q':
			if threshold > 0:
				threshold = threshold - 5
				print "New threshold: "
				print threshold
		if b=='w':
			if threshold < 255:
				threshold = threshold + 5
				print "New threshold: "
				print threshold
		#contourMin
		if b=='a':
			if contourMin > 0:
				contourMin = contourMin - 5
				print "New Contour-Min: "
				print contourMin
		if b=='s':
			if contourMin < (contourMax-10):
				contourMin = contourMin + 5
				print "New Contour-Min: "
				print contourMin
		#contourMax
		if b=='y':
			if contourMax > contourMin+10:
				contourMax = contourMax - 10
				print "New Contour-Max: "
				print contourMax
		if b=='x':
			contourMax = contourMax + 10
			print "New Contour-Max: "
			print contourMax
		#default values
		if b=='d':
			threshold = 190
			contourMin = 80
			contourMax = 450
			print "Default detection values restored: "
			print "Threshold: "+str(threshold)
			print "Contour-Min: "+str(contourMin)
			print "Contour-Max: "+str(contourMax)
		return threshold, contourMin, contourMax


	def readInputUntilRecognition(self, waiter):
		#global threshold,contourMin,contourMax
		#we want to create a mask and display the subtracted background
		m=0 #declaration for later maximum distance of detected point
		positionOfElement = 0 #same thing
		ret, self.bild = self.cap.read()
		self.height
		tone_old = 100
		keypoints = 0;
		while(True):
			ret, self.bild = self.cap.read()

			img = self.bild
			#img = copy.deepcopy(bild)

			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			gray2 = copy.deepcopy(gray)
			ret,gray = cv2.threshold(gray,self.threshold,255,cv2.THRESH_BINARY)
			mask = np.zeros(gray.shape,np.uint8)
			#contours, hier = cv2.findContours(gray,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
			
			gray2 = 255-gray2
			#gray2 *= gray
			#gray2 = 255-bild[:,:,2]
			#cv2.imshow("frame", gray2)
			
			# Setup SimpleBlobDetector parameters.
			params = cv2.SimpleBlobDetector_Params()
			# Change thresholds
			params.minThreshold = 100
			params.maxThreshold = 255
			# Filter by Area.
			params.filterByArea = True
			params.minArea = 30
			# Filter by CircularitydrawDist
			params.filterByCircularity = True
			params.minCircularity = 0.5
			# Filter by Convexity
			params.filterByConvexity = True
			params.minConvexity = 0.8
			# Filter by Inertia
			params.filterByInertia = True
			params.minInertiaRatio = 0.01
			
			ver = (cv2.__version__).split('.')
			if int(ver[0]) < 3 :
				detector = cv2.SimpleBlobDetector(params)
			else : 
				detector = cv2.SimpleBlobDetector_create(params)
			
			keypoints = detector.detect(gray2)
			#im_with_keypoints = cv2.drawKeypoints(gray, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
			
			for key in keypoints:
				#print(cnt)
				#print(cnt.pt)
				cv2.circle( img, (int(key.pt[0]),int(key.pt[1])),  10, (0,255,0), thickness = 3, lineType=8 );
				
			cv2.imshow('frame',img)
			b = cv2.waitKey(1)
			
			if b!=-1:		## if key was hit, convert its value to character
				b = chr(b)

			if b=='c':		## exit at hit of "c"
				sys.exit()
			
			if waiter==1:
				
				#if b!=-1:
				#    threshold, contourMin, contourMax = self.tuneCalibration(b,threshold,contourMin,contourMax)
				#else:
				#    b = 'r' #repeat loop if user did not enter anything
				if b == 'p':
					if len(keypoints) >= 1:
						selkey  = self.selectKey(keypoints, img)
						if selkey:
							return selkey
			
			
			
			else: #go on by default if harp is in play mode (if waiter==0)
				if waiter==1:
					print "No points detected, try again."
				break;

		return keypoints


	def selectKey(self, keypoints, img): # let user select 
		selected = 0;
		keymax = len(keypoints)
		if keymax >= 1:
			while (True):
				for cnt in keypoints:
					#print(cnt)
					#print(cnt.pt)
					cv2.circle( img, (int(cnt.pt[0]),int(cnt.pt[1])),  10, (0,255,0), thickness = 3, lineType=8 );
				
				cv2.circle( img, (int(keypoints[selected].pt[0]),int(keypoints[selected].pt[1])),  10, (0,0,225), thickness = 3, lineType=8 );
				
				cv2.imshow('frame',img)
				w = cv2.waitKey(1)
				#print w
				if w!=-1:
					w = chr(w)
				if w == '1':
					selected -= 1;
					if selected < 0:
						selected = 0;
				if w == '2':
					selected += 1;
					if selected >= keymax:
						selected = keymax-1;
				if w == 'z':
					return (keypoints[selected])
				if w == 'c':
					break

	def calibration(self):
		#-- Calibration start -#
		print "\n\nCalibration started"
		number = 0
		for i in range(self.lasernumber):
			number = number+1
			print "\   \      |      /   /"
			print "(1) (3)   (5)   (7) (9)"
			print "  \   \    |    /   /  "
			print "  (2) (4) (6) (8) (10) "
			print "    \   \  |  /   /    "
			if i==0:
				#print '\n First You can tune the detection parameters with \n"q","w", "a","s", and "y","x"\n such that the laserpoint is detected correctly at all positions.\n You can press "d" to restore detection values back to default.\n\n When You are done, You have to press "n" everytime you want to mark a point for calibration at a position in the diagram above.\n You can press "c" at any time to interrupt the program.'
				print '\n with "p" freeze the image,\n then with "1" and "2" select the correct key,\n with "z" you confirm this key'
				raw_input("\nPress ENTER when you are done.")

				#~ print "\nDefault detection values: "
				#~ print "Threshold: "+str(threshold)
				#~ print "Contour-Min: "+str(contourMin)
				#~ print "Contour-Max: "+str(contourMax)
			print "\nNow put your hand at position ("+str(number)+") and press 'p' when you want to mark for calibration."

			key1 = self.readInputUntilRecognition(1)
			cor1 = [key1.pt[0], key1.pt[1]]
			number = number+1
			print "Now please put your hand at position ("+str(number)+")"
			key2 = self.readInputUntilRecognition(1)
			cor2 = [key2.pt[0], key2.pt[1]]

			self.callibratedCoords.append([cor1,cor2])
			self.drawCalibrationProgress() #draw lines and stuff next TODO, nparray and lines for coordinates cv2

		#a = raw_input('Calibration finished.\n\nWe now detect the nearest distance of laserpoints to lines.\n')
		print 'Calibration finished.\n\nYou can now start to play the Harp!\nPress "AnyKey" to proceed. Press "c" to interrupt at any time.\n'
		ak2 = cv2.waitKey(0)
		
		
	def calcAmp(self, beam, coor):
		corY = int(coor[1])
		amp = int(127.*corY/self.height)+20
		if amp > 127:
			amp = 127
		self.beams[beam] = amp
