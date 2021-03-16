import matplotlib.pyplot as plt
import numpy as np

# perpendicular movements
sensor_position = [-3.5, -3.0, -2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]
real_values = [0.0002403829, 0.0002424737, 0.0002454693, 0.0002392607, 0.0002358432, 0.0002268006, 0.0002105036, 0.0001931991, 0.0002118456, 0.0002290144, 0.0002363943, 0.0002387485, 0.0002411113, 0.0002458481, 0.0002411915]
imaginary_values = [0.1441137, 0.1434904, 0.142243, 0.143571, 0.1432454, 0.144438, 0.1436966, 0.1440615, 0.1441728, 0.1439092, 0.1437865, 0.1435899, 0.1433098, 0.142891, 0.1436757]
#amplitude_values = [0.14411390048024034, 0.14349060486894322, 0.14224321180350663, 0.1435711993635303, 0.14324559414926166, 0.1444381780642229, 0.14369675418507413, 0.1440616295484063, 0.1441729556414733, 0.14390938222449362, 0.14378669432362326, 
distance_values = []
no_r = real_values[0]
no_i = imaginary_values[0]
for i in range(len(real_values)):
	current_r = real_values[i]
	current_i = imaginary_values[i]
	distance = np.sqrt( (current_r - no_r)**2 + (current_i - no_i )**2 )
	distance_values.append(distance)

plt.figure(1)
plt.plot(sensor_position,real_values,'r-')
plt.plot(sensor_position,real_values,'ro')
plt.xlabel("sensor position")
plt.ylabel("real value of impedance")

plt.figure(2)
plt.plot(sensor_position,imaginary_values,'b-')
plt.plot(sensor_position,imaginary_values,'bo')
plt.xlabel("sensor position")
plt.ylabel("imaginary value of impedance")
'''
plt.figure(3)
plt.plot(sensor_position,amplitude_values,'g-')
plt.plot(sensor_position,amplitude_values,'go')
plt.xlabel("sensor position")
plt.ylabel("Amplitude of impedance")
'''
plt.figure(3)
plt.plot(sensor_position,distance_values,'r-')
plt.plot(sensor_position,distance_values,'ro')
plt.xlabel("sensor position")
plt.ylabel("Distance to initial point")

plt.show()