from classes import Cstfunction
from pyevolve import G1DList
from pyevolve import GSimpleGA
from pyevolve import Selectors
from pyevolve import Mutators
from pyevolve import Initializators
from pyevolve import GAllele


File = 'D:/School/Research/A-Star/Research/CST_File/Coil.cst'			# Location of the cst File
SFile = 'D:/School/Research/A-Star/Research/save.data'				# Location of the save.data file
OFile = 'D:/School/Research/A-Star/Research/CST_File/Coil/Result/Coil Parameters.stx'  # Locaion of cst result output file
holeX = 3			#initial holeX value
holeY = 3			#initial holeY value
depthToObject = 2	#inital distance to object value
fun = Cstfunction(File,SFile,OFile,holeX,holeY,depthToObject) #create cstfunction class with default values
'''
OBJECTIVE FUCNTION: fun.findData(width,z,disToObj,hole_X,hole_Y)
objFun converts input parameter of objective function into array
#input__[0] -> width, input__[1] -> z, input__[2] -> disToObj, input__[3] -> hole_X,input__[4] -> hole_Y
disToObj, hole_X, hole_Y are OPTIONAL inputs
'''
def objFun(input__): #fitness function
	return float(fun.findData(input__[0],input__[1],disToObj = input__[2],hole_X = input__[3],hole_Y = input__[4])) * (10**6) #Its negative to inverse the graph along the x-axis such that max pt becomes min pt
lb = [0.5,0.1,0.0,0.5,2.1] # Lower boundary for each of the individual parameters
ub = [20.0,20.0,10.0,10.0,10.0]	 # Upper boudaries for each of the individual parameters
#Optim = objFun([9.58654548,0.99395079,6.65280725,0.5,7.61612828])
#print(objFun([9.479959122734503, 0.9476287065522162, 6.904977221145576, 0.6072602721506035, 7.912704647867712])) 
#print(objFun([9.532095890130778, 0.501178980415871, 6.896641903791689, 0.534415801141535, 9.826484361699034]))
#lb = [9.0,0.1,6.0,0.5,7.0] # Lower boundary for each of the individual parameters
#ub = [10.0,1.0,7.0,1.0,8.0]	 # Upper boudaries for each of the individual parameters

AlleleList = GAllele.GAlleles()

for i in range(len(lb)):
	TempRange = GAllele.GAlleleRange(lb[i],ub[i],real=True)
	TempRange.getRandomAllele()
	AlleleList.add(TempRange)

genomeIn = G1DList.G1DList(len(lb))
genomeIn.setParams(allele=AlleleList)

genomeIn.evaluator.set(objFun)
genomeIn.mutator.set(Mutators.G1DListMutatorAllele)
genomeIn.initializator.set(Initializators.G1DListInitializatorAllele)

ga = GSimpleGA.GSimpleGA(genomeIn)
ga.selector.set(Selectors.GRouletteWheel)

ga.setGenerations(100)
ga.setPopulationSize(30)
#print genomeIn
ga.evolve(freq_stats=10)

print ga.bestIndividual()
