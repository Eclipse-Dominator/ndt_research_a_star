# Gradient Descent
import math
'''
def adamSearch(function, searchLocation, B1 = 0.9, B2 = 0.999, learning_rate = 0.001, smoothingTerm = 1.0E-4, interationTot = 10000):
	interation = 0
	dimensions = len(searchLocation)
	Mt = [0] * dimensions
	Vt = [0] * dimensions
	learningV = [learning_rate] * dimensions
	while interation < interationTot:
		Gt = gradient_V = directionalDerivatives(function,searchLocation,0.1)
		Mt = vectorAdd( vectorTimes(B1,Mt), vectorTimes((1-B1), Gt) )
		Vt = vectorAdd( vectorTimes(B2,Vt), vectorTimes((1-B2), vectorETimes(Vt,Vt)) )
		Mbt = vectorContDivide(Mt, 1 - B1)
		Vbt = vectorERoot( vectorContDivide(Vt, 1 - B2) )

		update = vectorETimes( vectorEDivide(learningV, vectorContAdd(smoothingTerm, Vbt)), Mbt )

		print interation+1, searchLocation

		searchLocation = vectorSub(searchLocation, update)

		interation+=1
'''
def adadeltaSearch(function, searchLocation, momentum = 0.9, interationTot = 10000, smoothingTerm = 1.0E-4):
	interation = 0
	dimensions = len(searchLocation)
	decayingGradSquare = 0
	decayingUpdateSquare = 0
	while interation<interationTot:
		print interation+1 , searchLocation
		gradient_V = directionalDerivatives(function,searchLocation,0.01)
		gradient_mag = magnitude_( gradient_V )

		if math.fabs(gradient_mag) < 1.0E-4:
			break

		decayingGradSquare = momentum * decayingGradSquare + ( 1 - momentum ) * gradient_mag * gradient_mag
		#decayingGradSquare = vectorAdd( vectorTimes(momentum, decayingGradSquare), vectorTimes( 1 - momentum, vectorETimes(gradient_V,gradient_V)))
		RMS_Grad = math.sqrt( decayingGradSquare + smoothingTerm )
		#RMS_Grad = vectorERoot( vectorContAdd(smoothingTerm, decayingGradSquare) )
		RMS_Update = math.sqrt( decayingUpdateSquare + smoothingTerm )
		#RMS_Update = vectorERoot( vectorContAdd(smoothingTerm, decayingUpdateSquare) )

		adapatedLearningRate = - RMS_Update / RMS_Grad
		#adapatedLearningRate = vectorEDivide(RMS_Update, RMS_Grad)

		update_V =  vectorTimes( adapatedLearningRate, gradient_V)
		#update_V = vectorETimes( adapatedLearningRate, gradient_V )
		searchLocation = vectorAdd( update_V, searchLocation )
		#searchLocation = vectorSub( update_V, searchLocation )

		update_mag = magnitude_( update_V )
		decayingUpdateSquare = momentum * decayingUpdateSquare + ( 1 - momentum ) * update_mag * update_mag
		#decayingUpdateSquare = vectorAdd( vectorTimes(momentum, decayingUpdateSquare), vectorTimes( 1 - momentum, vectorETimes(update_V,update_V)))

		interation+=1


def adagradSearch(function, searchLocation, momentum = 0.9, learning_rate = 0.01, iterationTot = 10000, smoothingTerm = 1.0E-4):
	iteration = 0
	dimensions = len(searchLocation)
	decayingGradSquare = 0
	prevSearchCheck = searchLocation[:]
	searchCheck = searchLocation[:]
	while iteration<iterationTot:
		if (iteration+1)%10 == 0:
			prevSearchCheck = searchCheck[:]
			searchCheck = searchLocation[:]
			#print math.fabs(magnitude_(vectorSub(prevSearchCheck, searchCheck))) 
			if math.fabs(magnitude_(vectorSub(prevSearchCheck, searchCheck))) < 1.0E-2:
				break

		print iteration+1 , searchLocation
		gradient_V = directionalDerivatives(function,searchLocation,0.01)
		gradient_mag = magnitude_( gradient_V )
		if math.fabs(gradient_mag) < 1.0E-4:
			break
		decayingGradSquare = momentum * decayingGradSquare + ( 1 - momentum ) * gradient_mag * gradient_mag
		RMS_Grad = math.sqrt(smoothingTerm + decayingGradSquare)

		adapatedLearningRate = - learning_rate / RMS_Grad
		update_V =  vectorTimes( adapatedLearningRate, gradient_V)
		searchLocation = vectorAdd( update_V, searchLocation )

		iteration+=1



def gradSearch(function, searchLocation, lb, ub, momentum = 0.9, learning_rate = 0.1, interationTot = 1000):
		interation = 0
		previous_update = [0] * len(searchLocation)
		while interation<interationTot:
			terminationCheck = [0] * len(searchLocation)
			tempLocation = vectorSub(searchLocation, vectorTimes(momentum, previous_update))
			#print tempLocation
			gradient = directionalDerivatives(function,tempLocation,0.1)

			for i in range(len(searchLocation)):
				if tempLocation[i] < ub[i] or tempLocation[i] > lb[i]:
					terminationCheck[i] = gradient[i]
			#print math.fabs(magnitude_(gradient))
			if math.fabs(magnitude_(terminationCheck)) < 1.0E-3:
				break
			update = vectorTimes(learning_rate, gradient)
			velocity = vectorTimes(momentum, previous_update)
			Change = vectorAdd(update,velocity)
					
			print interation,searchLocation
			
			searchLocation = vectorSub(searchLocation,Change)
			
			for i in range(len(searchLocation)):
				Temp = searchLocation[i]
				if Temp <= lb[i]:
					searchLocation[i] = lb[i]
					previous_update[i] = 0
				elif Temp >= ub[i]:
					searchLocation[i] = ub[i]
					previous_update[i] = 0
			previous_update = Change[:]

			interation+=1
		print searchLocation
 


def directionalDerivatives(Function, dimensionalIN,step):
	dimensionTotal = len(dimensionalIN)
	gradientMatrix = [] * dimensionTotal
	for i in range(dimensionTotal):
		searchVar1 = dimensionalIN[:]
		searchVar2 = dimensionalIN[:]
		searchVar1[i] += step
		searchVar2[i] -= step
		gradientMatrix.append( (Function(searchVar1) - Function(searchVar2)) / (step * 2) )
	#gradientMagnitude = magnitude_(gradientMatrix)
	#gradientDir = map(math.sqrt,gradientMatrix)
	return gradientMatrix



def magnitude_(ArrIn):
	unroot = 0
	for Arr in ArrIn:
		unroot += Arr ** 2
	return math.sqrt(unroot)

def vectorTimes(constant, vector):
	return [constant * a for a in vector]

def vectorETimes(vector1, vector2):
	return [a * b for a,b in zip(vector1,vector2)]

def vectorEDivide(vector1, vector2):
	return [a / b for a,b in zip(vector1,vector2)]

def vectorERoot(vector):
	return [math.sqrt(a) for a in vector]

def vectorContAdd(constant, vector):
	return [constant + a for a in vector]

def vectorContDivide(vector, b):
	return [a / b for a in vector]

def vectorAdd(vector1,vector2):
	return [a + b for a, b in zip(vector1, vector2)]

def vectorSub(vector1,vector2):
	return [a - b for a, b in zip(vector1, vector2)]

def unitVector(vector):
	mag = magnitude_(vector)
	return [a / mag for a in vector]

def vectorDot(vector1, vector2):
	tot = 0
	for i in range(len(vector1)):
		tot += vector1 * vector2
	return dimensionTotal

def quad(x):
	#print x[0]
	#return math.sin(x[0] * .2 ) * math.cos( x[1] * .5)
	#return x[0] ** 2
	return (1.5 - x[0] + x[0] * x[1]) ** 2 + (2.25 - x[0] + x[0] * x[1]**2)**2 + (2.625 - x[0] +  x[0] * x[1] ** 3) ** 2


adagradSearch(quad,[0,0])