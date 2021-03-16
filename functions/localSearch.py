def locSearch(Function,Arr_,UL,LL,CL = 0.0001, learningStep = 0.1, maxStep = 3,maxIteration = 9999,freq = 1):
	'''
	Function -> fitness Function
	Arr_ -> Initial Search location
	UL   -> Upper Limit
	LL   -> Lower Limit
	CL   -> min Change
	freq -> Var update frequency

	'''
	Length = len(Arr_)
	ArrNext = [0.0]*Length
	Arr_T = Arr_[:]
	tempY = [0.0]*Length
	diffY = [0.0]*Length
	for i in range(Length):
		ArrNext[i] = Arr_[i]+1


	for n in range(maxIteration):
		breakCondition = [False]*Length
		Y0 = Function(Arr_)
		for i in range(Length):
			if ArrNext[i]>=UL[i]:
				ArrNext[i] = UL[i]-learningStep
				Arr_[i] = ArrNext[i]
				continue
			elif ArrNext[i] <= LL[i]:
				ArrNext[i] = LL[i]-learningStep
				Arr_[i] = ArrNext[i]
				continue
			ArrTemp = Arr_[:]
			ArrTemp[i] = ArrNext[i]
			tempY[i] = Function(ArrTemp)
			diffY[i] = (tempY[i] - Y0)/(ArrNext[i] - Arr_[i])
			#Placeholder = ArrNext[i]
			if learningStep*diffY[i]>=maxStep:
				Arr_T[i] = ArrNext[i] + maxStep * (learningStep*diffY[i] / abs(learningStep*diffY[i]))
			else:
				Arr_T[i] = ArrNext[i] + learningStep*diffY[i]
			#Arr_[i] = Placeholder
		
		Placeholder = ArrNext[:]
		ArrNext = Arr_T[:]
		Arr_ = Placeholder[:]

		if (n+1)%freq == 0:
			print "Interations:",n+1,"| Current Data:",Arr_,"Value:",Y0

		for i in range(Length):
			#print ArrNext[i] - Arr_[i]
			if abs(ArrNext[i] - Arr_[i]) <= CL:
				breakCondition[i] = True
		if all(breakCondition):
			print "Maximum Dataset:",Arr_,"Value:",Y0
			return Arr_
		n+=1