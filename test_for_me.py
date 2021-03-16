from classes import NDT_class

NDT = NDT_class.NDT_class()

nameArr = ["OBJdepth","sensor_current","sensor_angle_x","sensor_angle_y"]
data = [[0.5,0.2,0.1],[0.05,0.02,0.1],[0,1,0.05],[0,1,0.05]]

NDT.NDT("Width of crack", 0.2, 1.0, 0.4, "hole_width", nameArr, data, 1, "sensor_location", 35, 0, 30)

NDT.constructPOD()
