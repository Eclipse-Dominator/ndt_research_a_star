 from classes import Cstfunction
File = 'D:/School/Research/A-Star/Research/cst_file_2/coil.cst'
OFile = 'D:/School/Research/A-Star/Research/cst_file_2/coil/Result/Coil Parameters.stx'
cst = Cstfunction(File,OFile)
cst.createFile()

def showAmplitude():
	cst.rebuildEnvironment()
	cst.simulate()
	cst.retrieveData(debug = True)
	return cst.Amplitude

def showPercentageChange(depth):
	cst.changeSpecificVar("hole_pos", 0, debug = True)
	ori = showAmplitude()
	cst.changeSpecificVar("hole_pos",depth, debug = True)
	new = showAmplitude()
	PCHANGE =(new - ori) / ori * 100
	print "percentage change:", PCHANGE
	return showPercentageChange
