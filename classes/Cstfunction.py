from win32com.client import Dispatch
from decimal import Decimal
from math import sqrt

class Cstfunction(object):
	'''
	Class consist of functions and method to interact with CST Studios Suite.
	File_Location -> location where CST File is located
	saveLocation ->saved under global variable self.saveL -> location where save.data file is located
	impedanceFile -> location where cst output file is located
	
	self.xxx files are global file existing within Cstfunction
	'''
	def __init__(self,File_Location,impedanceFile): #init function are first called when class files are created
		self.cstFile = File_Location
		self.impedanceFile = impedanceFile
		self.mws = None
		#self.saveL = saveLocation

	def createFile(self):
		self.cst = Dispatch('CSTStudio.application')            # Searches for CST application and save the COM object as self.cst
		self.mws = Dispatch(self.cst.OpenFile(self.cstFile))   # Opens CST file located in File_Location and save the file COM object as self.mws
		self.ss = self.mws.LFSolver								# save low frequency solver with COM object self.ss

	def changeSpecificVar(self,varName, newValue, debug = False):
		self.mws._FlagAsMethod("StoreParameter")
		self.mws.StoreParameter(varName, newValue)
		if debug == True:
			print varName, "<<<", newValue

	def updateGroupVar(self,nameList, valueList, debug = False):
		for name, value in zip(nameList,valueList):
			self.changeSpecificVar(name,value,debug = debug)

	def rebuildEnvironment(self, debug = False):
		self.mws.rebuild
		if debug == True:
			print "Environment Rebuild!"

	# Launch the Low frequency solver and start saveData function
	def simulate(self, debug = False, dataSave = False):
		self.ss.start

		if debug == True:
			print("Simulation Complete")
		
		#self.saveData()
	#read the output file and save and calculate the amplitude from impedance
	def retrieveData(self, debug = False):
		#String Manipulation
		with open(self.impedanceFile,"r") as _SAVED:
			content = _SAVED.readlines()
			Impedance = None
			for i in range(len(content)):
				content[i] = content[i].strip().split(": ")
				if content[i][0].strip().upper() == "IMPEDANCE":
					Impedance = content[i][1].split()
					break
			self.aVal = float(Impedance[0]) #convert standard to integer (real part of impedance)
			self.bVal = float(Impedance[3]) #convert standard to integer (imaginary part of impedance)
			self.Amplitude = sqrt(self.aVal*self.aVal + self.bVal*self.bVal) # calculate amplitude in 6 S.F float in scientific notation and save it in self.Amplitude
			
			if debug == True:
				print "Impedance:", self.aVal, "+", str(self.bVal) + "i"
				print "Amplitude:", self.Amplitude
				print "Data Retrieve Complete!"

	def constantChangeVar(self, var_name, var_start, var_end, stepNum):
		stepSize = ( var_end - var_start ) / float(stepNum)
		var_value = var_start
		AmplitudeList = []
		xList = []
		for i in range(stepNum):
			xList.append( var_value )
			self.changeSpecificVar(var_name, var_value)
			var_value += stepSize
			self.rebuildEnvironment()
			self.simulate()
			self.retrieveData()
			print self.Amplitude
			AmplitudeList.append( self.Amplitude )

		return xList, AmplitudeList


	# calls retrieveData and saves the file into save.data in the format of (coil_width holeX holeY coilZ distanceToObject Amplitude)
	'''
	def saveData(self):
		self.retrieveData()
		print("Saving Data for coil width = "+str(self.coil_width)+", holeX = "+str(self.holeX)+", holeY = "+str(self.holeY)+", coilZ = "+str(self.Sensor_Z)+" and distance to object = "+str(self.objDepth)+"...")
		with open(self.saveL,"a") as _SAVE:
			_SAVE.write(str(self.coil_width) + " " + str(self.holeX) + " " + str(self.holeY)+ " " + str(self.Sensor_Z) + " " + str(self.objDepth) + " " + str(self.Amplitude)+"\n") #saveData
		print("Saved!\n*************************\n")
	'''



	'''
	# Objective Function, it checks whether the same dataset is already been tested before
	def findData(self, coilWidth, z, disToObj=-1, hole_X=-1, hole_Y=-1):
		if(disToObj == -1):													#refer to line 30 if u dk what's going on
			disToObj=self.objDepth
		if(hole_X == -1):
			hole_X = self.holeX
		if(hole_Y == -1):
			hole_Y = self.holeY

		strSet = str(coilWidth) + " " + str(hole_X) + " " + str(hole_Y)+ " " + str(z) + " " + str(disToObj) # create search string
		with open(self.saveL,"r") as _SAVED:																# Checks save.data file if test data is already been tested to prevent repeates
			dataSet = _SAVED.readlines()
			for _data in dataSet:
				if(strSet in _data):
					dataList = _data.split()
					return dataList[-1]																		# If test data exists, return the corresponding amplitude
		self.updateVar(coilWidth,z,disToObj=disToObj,hole_X=hole_X,hole_Y=hole_Y) # If data set does not exist, calculate the result and add the data to the result file
		self.simulate()															  # Start simulation with the new value
		return self.Amplitude #return Value for the new data
	'''