import math
from pyswarm import pso
from pyevolve import G1DList
from pyevolve import GSimpleGA
from pyevolve import Selectors
from pyevolve import Mutators
from pyevolve import Initializators
from pyevolve import GAllele
from pyevolve import Consts
from pyevolve import Crossovers
from pyevolve import Scaling


class OptimisationFunctions(object):

	"""
	docstring for OptimisationFunction
	class consisiting of multiple optimsation method
	"""

	def __init__(self):
		self.created = True
	
	def set_up(self, objFun, findMax = True):
		self.objFun = objFun
		self.findMax = findMax

	def pso_Search(self, lb, ub, Function = 3, swarmTot = 100, constA = 0.5, constB = 0.5, constC = 0.5, max_iteration = 100, minerror = 1e-8, MAX = 3):
		if MAX == 3:
			MAX = self.findMax
		if Function == 3:
			Function = self.objFun

		if MAX:
			def negFun(x):
				return -Function(x)
			xopt,fopt = pso(negFun,lb,ub,swarmsize=swarmTot, omega=constA, phip=constB, phig=constC, maxiter=max_iteration, minstep=minerror, minfunc=minerror)
			fopt = - fopt	
		else:
			xopt,fopt = pso(Function,lb,ub,swarmsize=swarmTot, omega=constA, phip=constB, phig=constC, maxiter=max_iteration, minstep=minerror, minfunc=minerror)
		print xopt,fopt
		return xopt, fopt

	def ga_Search(self, lb, ub, Function = 3, MAX = 3, freq_stats = 0, generations_limit = 1000, population_initial = 50,negativeFun = False):
		if MAX == 3:
			MAX = self.findMax
		if Function == 3:
			Function = self.objFun

		AlleleList = GAllele.GAlleles()
		for i in range(len(lb)):
			TempRange = GAllele.GAlleleRange(lb[i],ub[i],real=True)
			TempRange.getRandomAllele()
			AlleleList.add(TempRange)

		genomeIn = G1DList.G1DList(len(lb))
		genomeIn.setParams(allele=AlleleList)

		genomeIn.evaluator.set(Function)
		genomeIn.mutator.set(Mutators.G1DListMutatorAllele)
		genomeIn.initializator.set(Initializators.G1DListInitializatorAllele)

		if(len(lb) == 1):
			genomeIn.crossover.set(Crossovers.G1DListCrossoverUniform)

		ga = GSimpleGA.GSimpleGA(genomeIn)
		ga.selector.set(Selectors.GRouletteWheel)

		if negativeFun:
			pop = ga.getPopulation()
			pop.scaleMethod.set(Scaling.SigmaTruncScaling)

		if MAX:
			ga.setMinimax(Consts.minimaxType["maximize"])
		else:
			ga.setMinimax(Consts.minimaxType["minimize"])

		ga.setGenerations(generations_limit)
		ga.setPopulationSize(population_initial)
		#print genomeIn
		ga.evolve(freq_stats=freq_stats)

		bestResult = ga.bestIndividual()
		#print bestResult
		xopt = bestResult[:]
		Stats = ga.getStatistics()
		if MAX:
			fopt = Stats["rawMax"]
		else:
			fopt = Stats["rawMin"]
		print xopt, fopt

		return xopt, fopt

	def adagradSearch(self, searchLocation, lb, ub, Function = 3, momentum = 0.9, learning_rate = 0.01, convergingBreak = 1.0E-2, iterationTot = 10000, smoothingTerm = 1.0E-4, MAX = 3, debug = False, ErrorGrad = 1.0E-4, boundarySubtract = 0.01):
		if Function == 3:
			Function = self.objFun

		if MAX == 3:
			MAX = self.findMax

		iteration = 0
		dimensions = len(searchLocation)
		decayingGradSquare = 0
		prevSearchCheck = searchLocation[:]
		searchCheck = searchLocation[:]
		xopt = [0] * dimensions
		fopt = 0
		if MAX:
			fopt = -999999999

			while iteration<iterationTot:
				#value = Function(searchLocation)
				gradient_V,value = self.directionalDerivatives(Function,searchLocation,0.001)
				if debug:
					print searchLocation, value
				if value > fopt:
					fopt = value
					xopt = searchLocation[:]
				if (iteration+1)%10 == 0:
					prevSearchCheck = searchCheck[:]
					searchCheck = searchLocation[:]
					#print math.fabs(magnitude_(vectorSub(prevSearchCheck, searchCheck))) 
					if math.fabs(self.magnitude_(self.vectorSub(prevSearchCheck, searchCheck))) < convergingBreak:
						if debug:
							print "Break Via Convergence"
						break

				#gradient_V,value = self.directionalDerivatives(Function,searchLocation,0.001)
				gradient_mag = self.magnitude_( gradient_V )
				for i in range(dimensions):
					if searchLocation[i] <= lb[i] and gradient_V[i] < 0:
						gradient_V[i] = 0
					elif searchLocation[i] >= ub[i] and gradient_V[i] > 0:
						gradient_V[i] = 0

				if math.fabs( gradient_mag ) < ErrorGrad:
					if debug:
						print "Gradient Change <", ErrorGrad
					break
				decayingGradSquare = momentum * decayingGradSquare + ( 1 - momentum ) * gradient_mag * gradient_mag
				RMS_Grad = math.sqrt(smoothingTerm + decayingGradSquare)

				adapatedLearningRate = learning_rate / RMS_Grad
				update_V =  self.vectorTimes( adapatedLearningRate, gradient_V)
				searchLocation = self.vectorAdd( update_V, searchLocation )

				for i in range(dimensions):
					if searchLocation[i] <= lb[i]:
						searchLocation[i] = lb[i] + boundarySubtract
					elif searchLocation[i] >= ub[i]:
						searchLocation[i] = ub[i] - boundarySubtract

				iteration+=1

		else:
			fopt = 999999999
	
			while iteration<iterationTot:
				value = Function(searchLocation)
				if debug:
					print searchLocation, value
				if value < fopt:
					fopt = value
					xopt = searchLocation[:]
				if (iteration+1)%10 == 0:
					prevSearchCheck = searchCheck[:]
					searchCheck = searchLocation[:]
					#print math.fabs(magnitude_(vect orSub(prevSearchCheck, searchCheck))) 
					if math.fabs(self.magnitude_(self.vectorSub(prevSearchCheck, searchCheck))) < convergingBreak:
						if debug:
							print "Break Via Convergence"
						break

				gradient_V = self.directionalDerivatives(Function,searchLocation,0.01)
				gradient_mag = self.magnitude_( gradient_V )
				for i in range(dimensions):
					if searchLocation[i] <= lb[i] and gradient_V[i] < 0:
						gradient_V[i] = 0
					elif searchLocation[i] >= ub[i] and gradient_V[i] > 0:
						gradient_V[i] = 0

				if math.fabs( gradient_mag ) < ErrorGrad:
					if debug:
						print "Gradient Change <", ErrorGrad
					break
				decayingGradSquare = momentum * decayingGradSquare + ( 1 - momentum ) * gradient_mag * gradient_mag
				RMS_Grad = math.sqrt(smoothingTerm + decayingGradSquare)

				adapatedLearningRate = - learning_rate / RMS_Grad
				update_V =  self.vectorTimes( adapatedLearningRate, gradient_V)
				searchLocation = self.vectorAdd( update_V, searchLocation )

				for i in range(dimensions):
					if searchLocation[i] <= lb[i]:
						searchLocation[i] = lb[i] + 0.01
					elif searchLocation[i] >= ub[i]:
						searchLocation[i] = ub[i] - 0.01

				iteration+=1

		print xopt, fopt
		return xopt, fopt

	def directionalDerivatives(self,Function, dimensionalIN,step):
		dimensionTotal = len(dimensionalIN)
		gradientMatrix = [] 
		values = []
		for i in range(dimensionTotal):
			searchVar1 = dimensionalIN[:]
			searchVar2 = dimensionalIN[:]
			searchVar1[i] += step
			searchVar2[i] -= step
			v1 = Function(searchVar1)
			v2 = Function(searchVar2)
			gradientMatrix.append( v1 - v2 / (step * 2) )
			values.append( max(v1,v2) )
		Value = max(values)
		#gradientMagnitude = magnitude_(gradientMatrix)
		#gradientDir = map(math.sqrt,gradientMatrix)
		print gradientMatrix
		return gradientMatrix,Value


	def magnitude_(self,ArrIn):
		unroot = 0
		for Arr in ArrIn:
			unroot += Arr ** 2
		return math.sqrt(unroot)

	def vectorTimes(self,constant, vector):
		return [constant * a for a in vector]

	def vectorAdd(self, vector1,vector2):
		return [a + b for a, b in zip(vector1, vector2)]

	def vectorSub(self,vector1,vector2):
		return [a - b for a, b in zip(vector1, vector2)]

	def parametricAnalysis_function(self, newValue):
		InputArr = self.default_search[:]
		InputArr[self.globalIndex] = newValue[0]
		if self.functionChoice == 3:
			return self.objFun(InputArr)
		else:
			return self.functionChoice(InputArr)

	def parametricAnalysis(self,lb,ub,bestNum,steps_per_var = 20,default_search = False, Function = 3):
		X = [0] * len(lb)
		Y = [0] * len(lb)
		result_value = [0] * len(lb)
		result_x_value = [0] * len(lb)
		maxChange = [0] * len(lb)
		bestIndex = [0] * bestNum

		if Function == 3:
			Function = self.objFun
		if default_search == False:
			default_search = []
			for l,u in zip(lb,ub):
				default_search.append((l+u)/2)

		def objFunction(x,index):
			searchDefault = default_search[:]
			searchDefault[index] = x
			return Function(searchDefault)

		for i in range(len(lb)):
			result_value[i] = [0] * steps_per_var 
			result_x_value[i] = [0] * steps_per_var
			step = (ub[i] - lb[i]) / steps_per_var
			x = lb[i]
			for z in range (steps_per_var):
				result_x_value[i][z] = x
				result_value[i][z] = objFunction(x, i) 
				#print i,z,result_value[i][z]
				x += step
			#print result_value[i]
		for i in range(len(lb)):
			#print result_value[i]
			maxChange[i] = max(result_value[i]) - min(result_value[i])
		maxChangeOri = maxChange[:]
		#print maxChange
		maxChange.sort(reverse = True)
		for i in range(bestNum):
			value = maxChange[0]
			index = ChangeOri.index(value)
			maxChangeOri[index] = -1
			maxChange[0] = -1
			maxChange.sort(reverse = True)
			bestIndex[i] = index
		return bestIndex,result_value,result_x_value

'''
	def parametricAnalysis(self, lb, ub, default_search = False, Function = 3, population = 30, generation = 500, freq_stats = 0, topNumber = 3, debug = False):
		self.functionChoice = Function
		if default_search == False:
			default_search = []
			for l,u in zip(lb,ub):
				default_search.append((l+u)/2)
		self.default_search = default_search

		differenceList = [] * len(default_search)
		bestIndex = []

		for i in range(len(default_search)):
			self.globalIndex = i

			#print self.globalIndex

			genome = G1DList.G1DList(1)
			genome.evaluator.set(self.parametricAnalysis_function)
			genome.setParams(rangemin=lb[i], rangemax=ub[i])
			genome.initializator.set(Initializators.G1DListInitializatorReal)
			genome.crossover.set(Crossovers.G1DListCrossoverUniform)

			ga = GSimpleGA.GSimpleGA(genome)
			ga.selector.set(Selectors.GRouletteWheel)
			ga.terminationCriteria.set(GSimpleGA.ConvergenceCriteria)
			ga.setGenerations(generation)
			ga.setPopulationSize(population)

			ga.setMinimax(Consts.minimaxType["minimize"])
			ga.evolve(freq_stats=freq_stats)

			Out = ga.bestIndividual()
			VVV = ga.getStatistics()
			Min_ = VVV["rawMin"]
			value1 = self.default_search[:]
			value1[self.globalIndex] = Out[0]
			#print "Min:", value1,Min_

			ga.setMinimax(Consts.minimaxType["maximize"])
			ga.evolve(freq_stats=freq_stats)

			Out = ga.bestIndividual()
			VVV = ga.getStatistics()
			Max_ = VVV["rawMax"]
			value1 = self.default_search[:]
			value1[self.globalIndex] = Out[0]
			if debug:
				print "Max:", value1,Max_

			difference = Max_ - Min_
			differenceList.append(difference)
			#print "Difference:",difference
		differenceListTemp = differenceList[:]
		differenceListTemp.sort(reverse = True)

		for i in range(topNumber):
			value = differenceListTemp[i]
			bestIndex.append( differenceList.index(value) )

		return bestIndex
	'''