from classes import NDT_class

NDT = NDT_class.NDT_class()

nameArr = ["lift_off_Varying","coil_current"]
data = [[0.02,0.01,0.1],[0.05,0.003,0.1]]

NDT.NDT("Width of crack", 0.1, 1.0, 0.1, "crky", nameArr, data, 100, "Hole_location", 70, 0, 3.5)

NDT.constructPOD()
