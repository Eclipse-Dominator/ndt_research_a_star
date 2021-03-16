'''
import matplotlib.pyplot as plt
import numpy as np
mu, sigma = 0, 0.1 # mean and standard deviation
s = np.random.normal(mu, sigma, 1000)
count, bins, ignored = plt.hist(s, 30, normed=True)
plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *
               np.exp( - (bins - mu)**2 / (2 * sigma**2) ),
         linewidth=2, color='r')
plt.show()
'''
from classes import Cstfunction
import matplotlib.pyplot as plt
import numpy as np

File = 'D:/DHS/A-Star/Research/cst_file_2/coil.cst'
OFile = 'D:/DHS/A-Star/Research/cst_file_2/coil/Result/Coil Parameters.stx'

cst = Cstfunction(File,OFile)
cst.createFile()

def runSimulation(name,value):
	cst.changeSpecificVar(name, value, debug = True)
	cst.rebuildEnvironment()
	cst.simulate()
	cst.retrieveData(debug = True)
	return cst.aVal,cst.bVal,cst.Amplitude

xList = []
aVal_list = []
bVal_list = []
amplitude_list = []
distance_list = []
'''
i = -30
while i<=30:
	r,I,amplitude = runSimulation("hole_pos_y",i)
	aVal_list.append(r)
	bVal_list.append(I)
	amplitude_list.append(amplitude)
	xList.append(i)
	i += 0.05

print xList
print aVal_list
print bVal_list
print amplitude_list

no_r = aVal_list[0]
no_i = bVal_list[0]

for i in range(len(bVal_list)):
	current_r = aVal_list[i]
	current_i = bVal_list[i]
	distance = np.sqrt( (current_r - no_r)**2 + (current_i - no_i )**2 )
	distance_list.append(distance)

print distance_list

cst.changeSpecificVar("hole_pos_y", 0, debug = True)
print "Running parallel \n"
'''
xList2 = []
aVal_list2 = []
bVal_list2 = []
amplitude_list2 = []
distance_list2 = []

i = -30
while i<=30:
	r,I,amplitude = runSimulation("hole_pos_x",i)
	aVal_list2.append(r)
	bVal_list2.append(I)
	amplitude_list2.append(amplitude)
	xList2.append(i)
	i += 0.1
print xList2
print aVal_list2
print bVal_list2
print amplitude_list2

no_r = aVal_list2[0]
no_i = bVal_list2[0]

for i in range(len(bVal_list2)):
	current_r = aVal_list2[i]
	current_i = bVal_list2[i]
	distance = np.sqrt( (current_r - no_r)**2 + (current_i - no_i )**2 )
	distance_list2.append(distance)

print distance_list2

plt.figure(1)
plt.title('Perpendicular to Hole')
plt.plot(xList,aVal_list,'r-')
plt.plot(xList,aVal_list,'ro')
plt.xlabel("sensor position")
plt.ylabel("real value of impedance")

plt.figure(2)
plt.title('Perpendicular to Hole')
plt.plot(xList,bVal_list,'b-')
plt.plot(xList,bVal_list,'bo')
plt.xlabel("sensor position")
plt.ylabel("imaginary value of impedance")

plt.figure(3)
plt.title('Perpendicular to Hole')
plt.plot(xList,amplitude_list,'g-')
plt.plot(xList,amplitude_list,'go')
plt.xlabel("sensor position")
plt.ylabel("Amplitude of impedance")

plt.figure(4)
plt.title('Perpendicular to Hole')
plt.plot(xList,distance_list,'r-')
plt.plot(xList,distance_list,'ro')
plt.xlabel("sensor position")
plt.ylabel("Distance to initial point")

plt.figure(5)
plt.title('Parallel to Hole')
plt.plot(xList2,aVal_list2,'r-')
plt.plot(xList2,aVal_list2,'ro')
plt.xlabel("sensor position")
plt.ylabel("real value of impedance")

plt.figure(6)
plt.title('Parallel to Hole')
plt.plot(xList2,bVal_list2,'b-')
plt.plot(xList2,bVal_list2,'bo')
plt.xlabel("sensor position")
plt.ylabel("imaginary value of impedance")

plt.figure(7)
plt.title('Parallel to Hole')
plt.plot(xList2,amplitude_list2,'g-')
plt.plot(xList2,amplitude_list2,'go')
plt.xlabel("sensor position")
plt.ylabel("Amplitude of impedance")

plt.figure(8)
plt.title('Parallel to Hole')
plt.plot(xList2,distance_list2,'r-')
plt.plot(xList2,distance_list2,'ro')
plt.xlabel("sensor position")
plt.ylabel("Distance to initial point")

plt.show()