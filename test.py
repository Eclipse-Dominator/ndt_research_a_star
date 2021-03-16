from classes import OptimisationFunctions
from classes import Cstfunction

File = 'D:/School/Research/A-Star/Research/CST_File/Coil.cst'			# Location of the cst File
OFile = 'D:/School/Research/A-Star/Research/CST_File/Coil/Result/Coil Parameters.stx'  # Locaion of cst result output file

cst = Cstfunction(File,OFile)
cst.createFile()

parameterNameList = ["OBJdepth","inY","inX","Sensor_Z"] # Parameters used in optimisation
Data_LB = [0,3,3,5] # lower bound
Data_UB = [2,6,6,20] # upper bound

def objFun(valueList,nameList = parameterNameList):
	cst.updateGroupVar(nameList, valueList, debug = True)
	cst.rebuildEnvironment(debug = True)
	cst.simulate()
	cst.retrieveData(debug = True)
	return cst.Amplitude


optim = OptimisationFunctions.OptimisationFunctions()

optim.set_up(objFun, findMax = True)
optim.pso_Search(Data_LB,Data_UB) # Choose one
optim.ga_Search(Data_LB,Data_UB) # Choose one