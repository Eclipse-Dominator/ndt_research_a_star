from classes import Cstfunction
from pyswarm import pso

File = 'D:/School/Research/A-Star/Research/CST_File/Coil.cst'			# Location of the cst File
SFile = 'D:/School/Research/A-Star/Research/save.data'				# Location of the save.data file
OFile = 'D:/School/Research/A-Star/Research/CST_File/Coil/Result/Coil Parameters.stx'  # Locaion of cst result output file
holeX = 3			#initial holeX value
holeY = 3			#initial holeY value
depthToObject = 2	#inital distance to object value
fun = Cstfunction(File,SFile,OFile,holeX,holeY,depthToObject) #create cstfunction class 
'''
OBJECTIVE FUCNTION: fun.findData(width,z,disToObj,hole_X,hole_Y)
objFun converts input parameter of objective function into array
#input__[0] -> width, input__[1] -> z, input__[2] -> disToObj, input__[3] -> hole_X,input__[4] -> hole_Y
disToObj, hole_X, hole_Y are OPTIONAL inputs
'''
def objFun(input__):
	return -float(fun.findData(input__[0],input__[1],disToObj = input__[2],hole_X = input__[3],hole_Y = input__[4])) #Its negative to inverse the graph along the x-axis such that max pt becomes min pt
lb = [0.5,0.1,0,0.5,2.1] # Lower boundary for each of the individual parameters
ub = [20,20,10,10,10]	 # Upper boudaries for each of the individual parameters

xopt,fopt = pso(objFun,lb,ub) #start particle swarm optimisation with objective function objFun, lower boundary, higherboundary)

print (xopt,fopt) #prints out optimum arrray (xopt) and optimum aplitude (fopt)
