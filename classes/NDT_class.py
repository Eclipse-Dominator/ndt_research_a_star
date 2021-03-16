import math
import matplotlib.pyplot as plt
import numpy as np
import OptimisationFunctions
import random
import Cstfunction

class NDT_class(object):

	def __init__(self):
		File = 'D:/School/Research/A-Star/Research/CST_File/Coil.cst'
		OFile = 'D:/School/Research/A-Star/Research/CST_File/Coil/Result/Coil Parameters.stx'
		super(NDT_class, self).__init__
		self.optim = OptimisationFunctions.OptimisationFunctions()
		self.cst = Cstfunction.Cstfunction(File, OFile)
		self.cst.createFile()

	def drawNormalDistribution(self, mu, sigma):
		s = np.random.normal(mu, sigma, 1000)
		count, bins, ignored = plt.hist(s, 30, normed=True)
		plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu)**2 / (2 * sigma**2) ), linewidth=2, color='r')
		plt.show()

	def NDT(self, x_axis_name, x_axis_name_start, x_axis_name_stop, x_step_integer, x_axis_param_name, nameArr, Data, sample_size, hole_position_name, min_change_percentage, default_hole_position, no_hole_postion):
		self.x_value = []
		self.y_value = []
		self.x_name = x_axis_name
		i = x_axis_name_start

		defaultList = []
		for parameter in Data:
			defaultList.append( parameter[0] )

		self.cst.updateGroupVar( nameArr, defaultList )
		self.cst.changeSpecificVar(hole_position_name,no_hole_postion)
		self.cst.rebuildEnvironment()
		self.cst.simulate()
		self.cst.retrieveData()
		Default_amplitude = self.cst.Amplitude

		while i <= x_axis_name_stop:
			self.cst.changeSpecificVar(x_axis_param_name, i)
			self.x_value.append( i )
			y_percentage = self.NDT_Search_Single(nameArr, Data, sample_size, hole_position_name, min_change_percentage, default_hole_position, Default_amplitude)
			self.y_value.append( y_percentage )
			print (i,y_percentage)
			i += x_step_integer
		return self.x_value, self.y_value

	def drawGraph(self,x,y,type = "r-"):
		plt.plot(x,y,type)
		plt.plot( x, y, 'ro' )
		plt.show()
	
	def constructPOD(self):
		plt.plot( self.x_value, self.y_value, 'r-' )
		plt.plot( self.x_value, self.y_value, 'ro' )
		plt.ylabel('Probability')
		plt.xlabel(self.x_name)
		plt.title('Probability of Detection Curve')
		plt.show()

	def NDT_Search_Single(self, nameArr, Data, sample_size, hole_position_name, min_change_percentage, default_hole_position, Default_amplitude):
		search_set = self.generateDataSet(Data,sample_size)
		success_fail_list = []
		true_count = 0
		for search_single in search_set:
			self.cst.changeSpecificVar( hole_position_name, default_hole_position )
			self.cst.updateGroupVar( nameArr, search_single )
			self.cst.rebuildEnvironment()
			self.cst.simulate()
			self.cst.retrieveData()
			y_amplitude = self.cst.Amplitude
			success_fail_list.append( ( np.fabs( y_amplitude - Default_amplitude )  / Default_amplitude * 100 ) >= min_change_percentage )
		
		for result in success_fail_list:
			if result == True:
				true_count += 1

		return ( float(true_count) / float(sample_size) ) * 100


	def generateDataSet(self, Data, sample_size):
		valueList = []
		searchDataSet = []
		for i in range(sample_size):
			searchDataSet.append([])
			for z in range(len(Data)):
				searchDataSet[i].append([])

		for parameter in Data:
			searchLoc = parameter[0]
			Error = parameter[1]
			occurranceRate = parameter[2]
			Sigma = self.findSigma( searchLoc, Error, occurranceRate )
			data = self.sampleSinglePara( searchLoc, Sigma, sample_size ) 
			np.random.shuffle(data)
			valueList.append(data)

		for i in range( len(Data) ):
			for z in range(sample_size):
				searchDataSet[z][i] = valueList[i][z]

		return searchDataSet

	def sampleSinglePara(self, mu, sigma, sample_size):
		return np.random.normal(mu, sigma, sample_size)

	def integrateNormalDistribution(self,upper,lower,mu,sigma):
		return 0.5 * ( math.erf( ( mu - lower ) / ( np.sqrt(2) * sigma ) ) - math.erf( ( mu - upper ) / ( np.sqrt(2) * sigma ) ) )

	def simulateSensorReading(self, hole_variable, Start, End, Step):
		return self.cst.constantChangeVar(hole_variable, Start, End, Step)		# return X_Arr, Y_Arr

	def detectCheck(self, Sensor_changes, min_change_percentage):
		max_Amplitude = max(Sensor_changes)
		max_index = Sensor_changes.index(max_Amplitude)
		min_Amplitude = min(Sensor_changes)
		min_index = Sensor_changes.index(max_Amplitude)
		if max_index > min_index:
			Change = np.fabs( ( max_Amplitude - min_Amplitude ) / min_Amplitude ) * 100
		else:
			Change = np.fabs( ( max_Amplitude - min_Amplitude ) / max_Amplitude ) * 100
		if Change >= min_change_percentage:
			return True
		return False

	def findX(self, mu, sigma, P):
		sigmaSQ = sigma ** 2
		return np.sqrt( -2 * sigmaSQ * np.log( np.sqrt( 2 * np.pi * sigmaSQ ) * P ) + mu )

	def findSigma(self, x, error, error_percentage ):
		self.searchX = x + np.fabs(error)
		self.searchMu = x
		self.errorSearch = error_percentage
		sigmaArr, value = self.optim.pso_Search([0.00000001],[1.0],Function = self.difference,MAX = 0)
		self.sigma = sigmaArr[0]
		return self.sigma

	def difference(self,sigma):
		value = self.normalDistribution(self.searchX,self.searchMu,sigma[0])
		return (value - self.errorSearch) ** 2

	def normalDistribution(self, x, mu, sigma):
		sigmaSQ = float(sigma) ** 2
		#print np.sqrt( 2 * float(np.pi) * sigmaSQ )
		return ( 1 / np.sqrt( 2 * float(np.pi) * sigmaSQ ) ) * ( np.exp( -( ( x - mu ) ** 2 / ( 2 * sigmaSQ ) ) ) )
	
	def findMaxNormalDistribution(self, sigma):
		return 1 / np.sqrt( 2 * np.pi * ( sigma ** 2 ) )
	

	'''
	def getSamplePopulationArr(self, mu, sigma, Perror = 0.1, Pcat = 0.1):
		populationArraySize = []
		populationRangeList = []
		P = self.findMaxNormalDistribution( sigma )
		P -= Pcat
		Xprev = mu
		while P > Perror:
			x = self.findX(mu, sigma, P)
			print x, P
			PercentageProbability = self.integrateNormalDistribution(x, Xprev, mu, sigma) * 2
			populationRangeList.append( [Xprev, x] )
			populationArraySize.append( PercentageProbability )
			Xprev = x
			P -= Pcat
		if P < Perror:
			x = self.findX(mu, sigma, Perror)
			print x,Perror
			PercentageProbability = self.integrateNormalDistribution(x, Xprev, mu, sigma) * 2
			populationRangeList.append( [Xprev, x] )
			populationArraySize.append( PercentageProbability )

		populationTotal = sum(populationArraySize)
		modelledPopulationArrayPercentage = []
		for unmodelled in populationArraySize:
			modelledPopulationArrayPercentage.append( unmodelled / populationTotal )
		return modelledPopulationArrayPercentage, populationRangeList
	'''	