import math
import wx
import wx.xrc
import wx.lib.platebtn as platebtn
import wx.adv
import wx.propgrid as pg
from functools import partial
from classes import Cstfunction
from classes import OptimisationFunctions
from classes import NDT_class

class Framework_APP(wx.Frame):
	"""docstring for Framework_APP"""
	def __init__(self, *args, **kw):                    # initialize variables
		super(Framework_APP, self).__init__(*args, **kw)
		self.saveFolderPath = None
		self.cstPath = None
		self.coilPath = None
		self.xopt = []
		self.fopt = 0
		self.Parameter_Data = []
		self.paraStudyResult = [] 
		self.para_output_data = []
		self.optimisation_nameList = []
		self.hole_depth_variable = "hole_depth"
		self.hole_depth_val = 0.7
		self.hole_depth_noneVal = 0
		self.solver = OptimisationFunctions.OptimisationFunctions()

		contentBox = wx.BoxSizer( wx.VERTICAL )			#creating content for main view
		box_paraStudy = wx.BoxSizer( wx.VERTICAL )
		box_paraOptim = wx.BoxSizer( wx.VERTICAL )
		box_Simulation = wx.BoxSizer( wx.VERTICAL )     

		self.btn_paraStudy = wx.Button( self, wx.ID_ANY, u"&Parametric Study", wx.DefaultPosition, wx.DefaultSize, 0 )
		box_paraStudy.Add( self.btn_paraStudy, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )

		self.btn_paraOptim = wx.Button( self, wx.ID_ANY, u"Parameter &Optimisation", wx.DefaultPosition, wx.DefaultSize, 0 )
		box_paraOptim.Add( self.btn_paraOptim, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )

		self.btn_Simulation = wx.Button( self, wx.ID_ANY, u"&Simulation", wx.DefaultPosition, wx.DefaultSize, 0 )
		box_Simulation.Add( self.btn_Simulation, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )

		self.btn_paraStudy.Bind(wx.EVT_BUTTON, self.OpenParaStudy)
		self.btn_paraOptim.Bind(wx.EVT_BUTTON, self.OpenParaOptim)
		self.btn_Simulation.Bind(wx.EVT_BUTTON, self.OpenSimulation)

		contentBox.Add( box_paraStudy, 1, wx.EXPAND, 5 )
		contentBox.Add( box_paraOptim, 1, wx.EXPAND, 5 )
		contentBox.Add( box_Simulation, 1, wx.EXPAND, 5 )

		self.SetSizer( contentBox )
		self.Centre( wx.BOTH )

		self.addMainHeader()
		self.CreateStatusBar()
		self.SetStatusText(u"Welcome to automated framework for NDT!")

		# self.loadFile("D:\School\Research\A-Star\Research\python\ll")

	def addMainHeader(self):          # add menubar for main view
		fileMenu = wx.Menu()

		item_Open = fileMenu.Append(-1, u"&Open Folder\tCtrl+O",u"Open recent project folder")

		fileMenu.AppendSeparator()

		item_Import = fileMenu.Append(-1, u"&Import File Locations\tCtrl+I",u"Select Important Files for Testing")
		item_ParaEdit = fileMenu.Append(-1,u"&Edit Variables\tCtrl+Shift+I",u"Choose parameters/variables you want to model in your program.")
		
		fileMenu.AppendSeparator()

		item_Save = fileMenu.Append(-1, u"&Save\tCtrl+S",u"Save this session.")
		item_Save_As = fileMenu.Append(-1, u"Save &As\tCtrl+Shift+S",u"Save into another folder.")

		fileMenu.AppendSeparator()

		item_Exit = fileMenu.Append(wx.ID_EXIT)

		moreMenu = wx.Menu()
		item_Help =  moreMenu.Append(-1, u"&Help\tCtrl+H",u"Do not know how to use the framework?")
		item_About = moreMenu.Append(-1, u"&About",u"Find out more about this framework!")

		menuBar = wx.MenuBar()
		menuBar.Append(fileMenu, u"&File")
		menuBar.Append(moreMenu, u"&More")

		self.SetMenuBar(menuBar)

		self.Bind(wx.EVT_MENU, self.OnOpenFolder, item_Open)
		self.Bind(wx.EVT_MENU, self.OnSave, item_Save)
		self.Bind(wx.EVT_MENU, self.OnSaveAs, item_Save_As)
		self.Bind(wx.EVT_MENU, self.OnFileImport, item_Import)
		self.Bind(wx.EVT_MENU, self.OnParaEdit, item_ParaEdit)
		self.Bind(wx.EVT_MENU, self.OnExit,  item_Exit)
		self.Bind(wx.EVT_MENU, self.OnHelp, item_Help)
		self.Bind(wx.EVT_MENU, self.OnAbout, item_About)

	def OnOpenFolder(self, event):                          # open project folder 
		print "Open Folder Clicked"
		dlg = wx.DirDialog(self,u"Choose Save Folder",style = wx.DEFAULT_DIALOG_STYLE)
		if dlg.ShowModal() == wx.ID_OK:  
			OpenFolderPath = dlg.GetPath()
			if OpenFolderPath == self.saveFolderPath:
				print "error"
				dial = wx.MessageDialog(None, u'Project is already opened', u'Error', wx.OK | wx.ICON_ERROR)
				dial.ShowModal()
				dial.Destroy()
			else:
				dial = wx.MessageDialog(None, u'Do you wish to open a open the project in a new window?', u'Overwrite Current Project?', wx.YES_NO | wx.ICON_INFORMATION)
				value = dial.ShowModal()
				dial.Destroy()
				if value == 5104:                     # reload current project
					self.loadFile(OpenFolderPath)
				elif value == 5103:					  # open new project in new window
					self.newActivity(OpenFolderPath)
				

	def newActivity(self, OpenFolderPath):          # create new window loaded from folderpath
		appN = wx.App()
		frmN = Framework_APP(None, title = u"Automated Framework for Eddy Current NDT", pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)
		frmN.loadFile(OpenFolderPath)
		frmN.Show()
		appN.MainLoop()


 	def loadFile(self,OpenFolderPath): 			# load data from file locations
		self.saveFolderPath = OpenFolderPath
		SaveFile = self.saveFolderPath + "\File_Locations"
		ParaFile = self.saveFolderPath + "\Input_Parameters"
		paraCheck_File = self.saveFolderPath + "\Parameter_Check"
		rawData_File = self.saveFolderPath + "\Raw_Data"

		self.SetStatusText("NDT Project | "+ OpenFolderPath)
		try:
			with open(SaveFile,'r') as sFile:
				content = sFile.read().splitlines()
				print content
				if len(content) != 0:
					self.cstPath = content[0]
					self.coilPath = content[1]
					self.cstClass = Cstfunction(self.cstPath,self.coilPath)
				else:
					self.cstPath = None
					self.coilPath = None

			with open(ParaFile,'r') as dataFile:
				Datas = dataFile.read().splitlines()
				Datas = [[x.strip() for x in Data.split(',')] for Data in Datas]
				self.Parameter_Data = Datas

			with open(paraCheck_File,'r') as sFile:
				Datas = sFile.read().splitlines()
				self.paraStudyResult = Datas

			with open(rawData_File,'r') as rFile:
				Datas = rFile.read().splitlines()
				paraStudyNum = int(Datas[0])
				self.para_output_data = [0] * paraStudyNum
				current_index = 1
				
				for i in range(paraStudyNum):
					single_para_variable = [0] * 3
					single_para_variable[0] = Datas[current_index + 3 * i]
					single_para_variable[1] = [float(value) for value in Datas[current_index + 3 * i + 1].split(";")[:-1]]
					single_para_variable[2] = [float(value) for value in Datas[current_index + 3 * i + 2].split(";")[:-1]] #last value is empty
					self.para_output_data[i] = single_para_variable[:]
				
				current_index += paraStudyNum * 3

				# optim_result
				is_there_optim_result = int(Datas[current_index])
				if is_there_optim_result:
					current_index += 1
					self.optimisation_nameList = Datas[current_index].split(";")[:-1][:]
					self.xopt = [float(value) for value in Datas[current_index + 1].split(";")[:-1]]
					self.fopt = float(Datas[current_index + 2])

			print "cstPath",self.cstPath
			print "coilPath",self.coilPath
			print "param_data", self.Parameter_Data
			print "paraStudyResult", self.paraStudyResult
			print "para_output_raw", self.para_output_data
			print "optim_name", self.optimisation_nameList
			print "xopt", self.xopt
			print "fopt", self.fopt


		except IOError:
			print "error"
			dial = wx.MessageDialog(None, u'Project Corrupted! Missing vital files!', u'Error', wx.OK | wx.ICON_ERROR)
			dial.ShowModal()
			dial.Destroy()
			self.Destroy()

	def OnSave(self, event):           # save file in save folder
		if self.saveFolderPath == None: # if no save path is stored, prompt for save path
			self.OnSaveAs(wx.EVT_MENU)

		SaveFile = self.saveFolderPath + "\File_Locations"
		ParaFile = self.saveFolderPath + "\Input_Parameters"
		paraCheck_File = self.saveFolderPath + "\Parameter_Check"
		rawData_File = self.saveFolderPath + "\Raw_Data"

		with open(SaveFile,'w+') as sFile:
			print SaveFile
			if self.cstPath != None and self.coilPath != None:
				sFile.write(self.cstPath )
				sFile.write('\n')
				sFile.write(self.coilPath)
				sFile.write('\n')

		with open(ParaFile,'w+') as sFile:
			for data in self.Parameter_Data:
				sFile.write(data[0]+","+data[1]+","+data[2]+","+data[3])
				sFile.write('\n')

		with open(paraCheck_File,'w+') as sFile:
			for data in self.paraStudyResult:
				sFile.write(data)
				sFile.write('\n')

		with open(rawData_File,'w+') as sFile: # para_study_raw, optimisation_result
			num_follow = len(self.para_output_data)  # num_follow -> num_follow number of variable as follow occupying 3 lines per var
			sFile.write( str(num_follow) )
			sFile.write( '\n' )
			for i in range(num_follow):
				sFile.write( self.para_output_data[i][0] ) # name
				sFile.write( '\n' )
				for value in self.para_output_data[i][1]: # X_list
					sFile.write(str(value))
					sFile.write(";")
				sFile.write( '\n' )
				for value in self.para_output_data[i][2]: # Y_list
					sFile.write(str(value))
					sFile.write(";")
				sFile.write( '\n' )

			if len(self.optimisation_nameList) == 0: # optimisation result: 0. is there result? (1,0) 1. param namelist, 2.xopt, 3.fopt
				sFile.write(str(0))
			else:
				sFile.write(str(1))
				sFile.write('\n')
				for name in self.optimisation_nameList: 
					sFile.write(name) 
					sFile.write(";")
				sFile.write('\n')
				for value in self.xopt:
					sFile.write(str(value))
					sFile.write(";")
				sFile.write('\n')
				sFile.write(str(self.fopt))
		print "Save Clicked"

	def OnSaveAs(self, event):      # ask for save folder
		print "Save As Clicked"

		dlg = wx.DirDialog(self,u"Choose Save Folder",style = wx.DEFAULT_DIALOG_STYLE)
		if dlg.ShowModal() == wx.ID_OK:  
			self.saveFolderPath = dlg.GetPath()
			print self.saveFolderPath
		dlg.Destroy()
		self.SetStatusText(u"NDT Project | "+ self.saveFolderPath)
		self.OnSave(wx.EVT_MENU)

	def OnFileImport(self, event):    # call import cst file
		print "File import item Clicked!"
		ImportFileWindow = Popup_ImportFile(self,title = u"Import Files", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_DIALOG_STYLE )
		ImportFileWindow.loadFile(self.cstPath,self.coilPath)
		#ImportFileWindow = Popup_ImportFile(None)
		ImportFileWindow.ShowModal()
		self.cstPath = ImportFileWindow.cstPath
		self.coilPath = ImportFileWindow.coilPath
		self.cstClass = Cstfunction(self.cstPath,self.coilPath)
		ImportFileWindow.Destroy()
		print self.cstPath, self.coilPath

	def OnParaEdit(self, event):
		print "Parameter Import item Clicked!"

		ParaEditWindow = Popup_change_parameter(self,title = u"Edit Parameter", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )
		ParaEditWindow.loadData(self.Parameter_Data)
		#ParaEditWindow.loadData()
		ParaEditWindow.ShowModal()
		self.Parameter_Data = ParaEditWindow.FinalData
		print ParaEditWindow.Data
		ParaEditWindow.Destroy()

	def startCST(self):
		try:
			self.cstClass.createFile()
			return True
		except AttributeError:
			print "error"
			dial = wx.MessageDialog(None, u'An error occured when opening the CST File', u'Error', wx.OK | wx.ICON_ERROR)
			dial.ShowModal()
			dial.Destroy()
			return False
		
	def OnExit(self, event):
		print "Exit item Clicked!"
		self.Close(True)
		self.Destroy()

	def OnHelp(self, event):
		print "Help item Clicked!"

	def OnAbout(self, event):
		print "About item Clicked!"
		
	def OpenParaStudy(self, event):
		print "Parameter Study btn Clicked!"
		paraStudyActivity = ParamtricStudy(None, title = u"Conduct Parametric Study", style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
		paraStudyActivity.loadData(self.Parameter_Data)
		try:
			paraStudyActivity.ShowModal()
			study_data = paraStudyActivity.outputData
			if len(study_data) > 0:
				minV = int(paraStudyActivity.minRequirementLen)
				print self.run_para_study(study_data,minV)
		except RuntimeError:
			print "An Error Occured"

	def run_para_study(self, study_data,topVar):

		if self.cstClass.mws == None:
			if not self.startCST():
				return False

		original_NameList = []

		for item in self.Parameter_Data:
			original_NameList.append(item[0])

		nameList = study_data[0]
		LB_List = study_data[1]
		UB_List = study_data[2]
		Default_List = study_data[3]
		self.paraStudyResult = []

		for i in range(len(nameList)):
			name_index = original_NameList.index(nameList[i])
			self.Parameter_Data[name_index][0] = nameList[i]
			self.Parameter_Data[name_index][1] = LB_List[i]
			self.Parameter_Data[name_index][2] = UB_List[i]
			self.Parameter_Data[name_index][3] = Default_List[i]

		def objectiveFunction(searchList):
			self.cstClass.updateGroupVar(nameList, searchList)
			self.cstClass.rebuildEnvironment()
			self.cstClass.simulate()
			self.cstClass.retrieveData()

			return self.cstClass.Amplitude

		order_result,para_data_out,para_x_data_out = self.solver.parametricAnalysis(LB_List,UB_List,topVar,default_search = Default_List,Function = objectiveFunction)

		self.para_output_data = [0] * len(study_data[0])

		for i in range(len([0])):
			appendArray=[]					#appendArray = [name,[XVar],[YVar]]
			study_data
			xList = para_x_data_out[i][:]
			yList = para_data_out[i][:]

			appendArray.append(nameList[i])
			appendArray.append(xList)
			appendArray.append(yList)

			self.para_output_data[i] = appendArray[:]


		for i in order_result:
			self.paraStudyResult.append(nameList[i])

	def OpenParaOptim(self, event):
		print "Parameter Optimisation btn Clicked!"
		paraOptimActivity = RunOptimisation(None, title = u"Conduct Parameter Optimisation", style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
		paraOptimActivity.loadData(self.Parameter_Data,self.paraStudyResult)
		try:
			paraOptimActivity.ShowModal()
			optim_data = paraOptimActivity.outputData # [ Name_output_List, LB_output_list, UB_output_list, default_output_list ]
			optim_choice = paraOptimActivity.Function_method
			optim_partial = paraOptimActivity.optimise_partial
			if len(optim_data) > 0:
				print "starting optimisation"
				self.run_optimisation( optim_choice, optim_data, optim_partial )
		except RuntimeError:
			print "An Error Occured"
		paraOptimActivity.Destroy()

	def run_optimisation( self, optim_choice, optim_data, optimise_partial ):
		if self.cstClass.mws == None:
			if not self.startCST():
				return False
		# optim_data = # [ Name_output_List, LB_output_list, UB_output_list, default_output_list ]
		self.optimisation_nameList = optim_data[0]
		LB_List = optim_data[1]
		UB_List = optim_data[2]
		default_list = optim_data[3]

		if optim_choice == 0: #PSO
			optimisation_start_function = partial( optimise_partial( self.solver.pso_Search ), LB_List, UB_List )
		elif optim_choice == 1: #GA
			optimisation_start_function = partial( optimise_partial( self.solver.ga_Search ), LB_List, UB_List )
		elif optim_choice == 2: #GD
			optimisation_start_function = partial( optimise_partial( self.solver.adagradSearch ), default_list, LB_List, UB_List )

		def objectiveFunction(searchList):
			print "Searching for", searchList[0]
			self.cstClass.updateGroupVar(self.optimisation_nameList, searchList)
			self.cstClass.changeSpecificVar(self.hole_depth_variable,self.hole_depth_val)
			self.cstClass.rebuildEnvironment()
			self.cstClass.simulate()
			self.cstClass.retrieveData()
			with_hole_aval = self.cstClass.aVal
			with_hole_bval = self.cstClass.bVal

			self.cstClass.updateGroupVar(self.optimisation_nameList, searchList)
			self.cstClass.changeSpecificVar(self.hole_depth_variable,self.hole_depth_noneVal)
			self.cstClass.rebuildEnvironment()
			self.cstClass.simulate()
			self.cstClass.retrieveData()
			without_hole_aval = self.cstClass.aVal
			without_hole_bval = self.cstClass.bVal

			return math.fabs(without_hole_aval - with_hole_aval) + math.fabs( without_hole_bval - with_hole_bval)

		self.solver.set_up( objectiveFunction )

		self.xopt, self.fopt = optimisation_start_function()

	def OpenSimulation(self, event):
		print "Simulator btn Clicked!"

	def __del__(self):
		class_name = self.__class__.__name__
		print class_name, "is closed"

class Popup_ImportFile(wx.Dialog):
	"""docstring for Popup_ImportFile"""

	def __init__(self,*args, **kw):
		super(Popup_ImportFile, self).__init__(*args, **kw)

		import_MainContainer = wx.BoxSizer( wx.VERTICAL )
		
		import_Container = wx.FlexGridSizer( 2, 2, 0, 0 )
		
		cstTxt = wx.StaticText( self, label = u"Select CST FILE:" )
		coilTxt = wx.StaticText( self, label = u"Select Coil Parameter:" )
		#self.cstTxt.Wrap( -1 )
		
		self.cstFileImport = wx.FilePickerCtrl( self, message = u"Select your CST file")
		self.coilFileImport = wx.FilePickerCtrl( self, message = u"Select Coil Parameter Output FIle" )
		
		import_Container.Add( cstTxt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )
		import_Container.Add( self.cstFileImport,0, wx.ALL|wx.EXPAND, 5  )
		
		import_Container.Add( coilTxt,0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )
		import_Container.Add( self.coilFileImport,0, wx.ALL|wx.EXPAND, 5  )	
		
		
		ok_cancel_container = wx.StdDialogButtonSizer()
		ok_key = wx.Button( self, wx.ID_OK )
		cancel_key = wx.Button( self, wx.ID_CANCEL )
				
		ok_cancel_container.AddButton( ok_key )
		ok_cancel_container.AddButton( cancel_key )
		ok_cancel_container.Realize()
		
		import_MainContainer.Add( import_Container, 1, wx.EXPAND, 5 )
		import_MainContainer.Add( ok_cancel_container, 1, wx.EXPAND, 5 )

		ok_key.Bind(wx.EVT_BUTTON, self.OnOkClose)
		cancel_key.Bind(wx.EVT_BUTTON, self.OnCancelClose)
		
		self.SetSizer( import_MainContainer )
		import_MainContainer.Fit( self )
		self.Centre( wx.BOTH )

	def loadFile(self, cstPath, coilPath):
		self.cstPath = cstPath
		if cstPath != None:
			self.cstFileImport.SetPath(self.cstPath)
		self.coilPath = coilPath
		if coilPath != None:
			self.coilFileImport.SetPath(self.coilPath)

	def OnOkClose(self,event):
		self.cstPath = self.cstFileImport.Path
		self.coilPath = self.coilFileImport.Path
		if self.cstPath == "" or self.coilPath == "":
			print "error"
			dial = wx.MessageDialog(None, u'No Path Given!', u'Error', wx.OK | wx.ICON_ERROR)
			dial.ShowModal()
			dial.Destroy()
		else:
			#print self.cstPath, self.coilPath
			self.Destroy()

	def OnCancelClose(self,event):
		self.Destroy()

	def DisplayError(self):
		print("test")

	def __del__(self):
		class_name = self.__class__.__name__
		print class_name, "is closed"

class Popup_change_parameter(wx.Dialog):
	"""docstring for Popup_change_parameter"""
	def __init__(self,*args, **kw):
		super(Popup_change_parameter, self).__init__(*args, **kw)
		self.Data = []
		self.FinalData = []


	def createUI(self):
		self.contentWrapper = wx.BoxSizer( wx.VERTICAL )

		headerWrapper = wx.FlexGridSizer( 1, 5, 0, 0 )

		headerWrapper.AddGrowableCol( 0 )
		headerWrapper.AddGrowableCol( 1 )
		headerWrapper.AddGrowableCol( 2 )
		headerWrapper.AddGrowableCol( 3 )
		headerWrapper.AddGrowableCol( 4 )
		headerWrapper.SetFlexibleDirection( wx.VERTICAL )

		ParaNameTxt = wx.StaticText( self, label = u"Parameter Name" )
		ParaLBTxt = wx.StaticText( self, label = u"Minimum Value" )
		ParaUBTxt = wx.StaticText( self, label = u"Maximum Value" )
		ParaDefaultTxt = wx.StaticText( self, label = u"Default Value" )

		headerWrapper.Add( ParaNameTxt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		headerWrapper.Add( ParaLBTxt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		headerWrapper.Add( ParaUBTxt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		headerWrapper.Add( ParaDefaultTxt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		headerWrapper.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.dataContainer = self.createDataContent()


		dataWrapper = wx.FlexGridSizer( 1, 5, 0, 0 )

		dataWrapper.AddGrowableCol( 0 )
		dataWrapper.AddGrowableCol( 1 )
		dataWrapper.AddGrowableCol( 2 )
		dataWrapper.AddGrowableCol( 3 )
		dataWrapper.AddGrowableCol( 4 )
		dataWrapper.SetFlexibleDirection( wx.VERTICAL )

		self.nameIn = wx.TextCtrl( self )
		self.lbIn = wx.TextCtrl( self )
		self.ubIn = wx.TextCtrl( self )
		self.defaultIn = wx.TextCtrl( self )
		self.Add_btn = platebtn.PlateButton(self, id = -1, label=u"Add", style=platebtn.PB_STYLE_GRADIENT)
		self.Add_btn.Bind(wx.EVT_BUTTON, self.OnAdd)

		dataWrapper.Add( self.nameIn, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		dataWrapper.Add( self.lbIn, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		dataWrapper.Add( self.ubIn, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		dataWrapper.Add( self.defaultIn, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		dataWrapper.Add( self.Add_btn, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		self.btn_container = wx.StdDialogButtonSizer()
		ok_key = wx.Button( self, wx.ID_OK )
		cancel_key = wx.Button( self, wx.ID_CANCEL )
				
		self.btn_container.AddButton( ok_key )
		self.btn_container.AddButton( cancel_key )
		self.btn_container.Realize()

		self.contentWrapper.Add( headerWrapper, 0, wx.EXPAND, 5 )
		self.contentWrapper.Add( self.dataContainer, 0, wx.EXPAND, 5 )
		self.contentWrapper.Add( dataWrapper, 0, wx.EXPAND, 5 )
		self.contentWrapper.Add( self.btn_container, 0, wx.EXPAND, 5 )


		ok_key.Bind(wx.EVT_BUTTON, self.OnOkClose)
		cancel_key.Bind(wx.EVT_BUTTON, self.OnCancelClose)

		self.SetSizer(self.contentWrapper)
		self.contentWrapper.Fit(self)

	def createDataContent(self):
		dataContainer = wx.BoxSizer( wx.VERTICAL )
		self.IndexList = []
		#dataWrapperList = []
		total_data_count = len(self.Data)
		if total_data_count == 0:
			pass
		for i in range(total_data_count):
			dataWrapper = wx.FlexGridSizer( 1, 5, 0, 0 )

			dataWrapper.AddGrowableCol( 0 )
			dataWrapper.AddGrowableCol( 1 )
			dataWrapper.AddGrowableCol( 2 )
			dataWrapper.AddGrowableCol( 3 )
			dataWrapper.AddGrowableCol( 4 )
			dataWrapper.SetFlexibleDirection( wx.VERTICAL )

			name = self.Data[i][0]
			lb = self.Data[i][1]
			ub = self.Data[i][2]
			default_value = self.Data[i][3]

			ParaNameTxt = wx.StaticText( self, label = name )
			ParaLBTxt = wx.StaticText( self, label = lb )
			ParaUBTxt = wx.StaticText( self, label = ub )
			ParaDefaultTxt = wx.StaticText( self, label = default_value )
			remove_btn = platebtn.PlateButton(self, id = i ,label=u"Remove", style=platebtn.PB_STYLE_GRADIENT)

			dataWrapper.Add( ParaNameTxt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
			dataWrapper.Add( ParaLBTxt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
			dataWrapper.Add( ParaUBTxt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
			dataWrapper.Add( ParaDefaultTxt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
			dataWrapper.Add( remove_btn, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
			
			remove_btn.Bind(wx.EVT_BUTTON, self.OnRemove)

			dataContainer.Add( dataWrapper, 1, wx.EXPAND, 5 )
			self.IndexList.append(i)

		return dataContainer

		
	def OnRemove(self,event):
		print "removed"

		#event.GetEventObject().GetLabel()
		index_ =  event.GetEventObject().GetId()
		sizerIndex = self.IndexList.index(index_)
		self.Data.pop(sizerIndex)
		self.nameList.pop(sizerIndex)
		self.IndexList.remove(index_)
		self.dataContainer.Hide(sizerIndex)
		self.dataContainer.Remove(sizerIndex)

		print self.Data

		self.Layout()
		self.contentWrapper.Fit(self)
		#self.loadData()

	def OnAdd(self,event):
		newIndex = 0
		if len(self.IndexList) != 0:
			newIndex = self.IndexList[-1] + 1
		nameVal = self.nameIn.Value.strip()
		lbVal = self.lbIn.Value.strip()
		ubVal = self.ubIn.Value.strip()
		defaultVal = self.defaultIn.Value

		if nameVal == "" or lbVal == "" or ubVal == "" or defaultVal == "" or nameVal in self.nameList or not is_float([lbVal,ubVal,defaultVal]) or float(lbVal)>=float(ubVal) or float(defaultVal)>float(ubVal) or float(defaultVal)<float(lbVal):
			print "error"
			print nameVal in self.nameList
			dial = wx.MessageDialog(None, u'Invalid input or repeated parameters!', u'Error', wx.OK | wx.ICON_ERROR)
			dial.ShowModal()
			dial.Destroy()
			return 0

		dataWrapper = wx.FlexGridSizer( 1, 5, 0, 0 )

		dataWrapper.AddGrowableCol( 0 )
		dataWrapper.AddGrowableCol( 1 )
		dataWrapper.AddGrowableCol( 2 )
		dataWrapper.AddGrowableCol( 3 )
		dataWrapper.AddGrowableCol( 4 )
		dataWrapper.SetFlexibleDirection( wx.VERTICAL )

		ParaNameTxt = wx.StaticText( self, label = nameVal )
		ParaLBTxt = wx.StaticText( self, label = lbVal )
		ParaUBTxt = wx.StaticText( self, label = ubVal )
		ParaDefaultTxt = wx.StaticText( self, label = defaultVal )
		remove_btn = platebtn.PlateButton(self, id = newIndex ,label=u"Remove", style=platebtn.PB_STYLE_GRADIENT)

		dataWrapper.Add( ParaNameTxt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		dataWrapper.Add( ParaLBTxt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		dataWrapper.Add( ParaUBTxt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		dataWrapper.Add( ParaDefaultTxt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		dataWrapper.Add( remove_btn, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		remove_btn.Bind(wx.EVT_BUTTON, self.OnRemove)

		self.dataContainer.Add( dataWrapper, 1, wx.EXPAND, 5 )

		self.IndexList.append(newIndex)
		self.Data.append([nameVal,lbVal,ubVal,defaultVal])
		self.nameList.append(nameVal)

		self.nameIn.SetValue('')
		self.ubIn.SetValue('')
		self.lbIn.SetValue('')
		self.defaultIn.SetValue('')

		self.Layout()
		self.contentWrapper.Fit(self)

		print self.Data
		print "added"
		

	def loadData(self,fileData = []):
		self.nameList = []
		if fileData != []:
			self.Data = fileData[:]
			self.FinalData = fileData[:]
			for data in self.Data:
				self.nameList.append(data[0])


		self.createUI()

	def OnOkClose(self,event):
		self.FinalData = self.Data[:]
		self.Close(True)
		print "OK"
	def OnCancelClose(self,event):
		self.Destroy()

class ParamtricStudy( wx.adv.Wizard ):
	"""docstring for ParamtricStudy"""
	def __init__(self,*args, **kw):
		super(ParamtricStudy, self).__init__(*args, **kw)
		self.dataIn = []
		self.pagesList = []
		self.dataForStudy = []
		self.outputData = []
		self.methodList = ["Min Max Difference"]
		self.searchmethodList = ["Default Sampling"]
		self.prev_btn = self.FindWindowById(wx.ID_BACKWARD)
		self.next_btn = self.FindWindowById(wx.ID_FORWARD) 
		self.next_btn.Bind(wx.EVT_BUTTON,self.onNext)
		#self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGED, self.onPageChanged)


	def loadData(self,Data):
		self.dataIn = Data
		if len(Data) == 0:
			print "error"
			dial = wx.MessageDialog(None, u'Go to file -> Edit Variables to add more variables', u'No Variables / Parameters', wx.OK | wx.ICON_ERROR)
			dial.ShowModal()
			dial.Destroy()
			self.Destroy()

		self.nameList = [a[0] for a in self.dataIn]

		self.settingPage = self.createSetUpPage()
		self.wizDataPage = self.createDataPage()
		self.comfirmDefaultPage = self.EditDefaultPage()

		self.add_page( self.settingPage )
		self.add_page( self.wizDataPage )
		self.add_page( self.comfirmDefaultPage )


		self.Centre( wx.BOTH )
		self.RunWizard( self.settingPage )

	def createDataPage(self):
		dataPage = wx.adv.WizardPageSimple(self)

		contentWrapper = wx.BoxSizer( wx.VERTICAL )

		ParaNameTxt = wx.StaticText( dataPage, label = u"Select Parameters for Parametric Study" )

		self.dataCheckList = wx.CheckListBox( dataPage, choices = self.nameList )
		self.dataCheckList.SetCheckedStrings(self.nameList)
		contentWrapper.Add( ParaNameTxt, 0, wx.ALL, 5 )
		contentWrapper.Add( self.dataCheckList, 1, wx.ALL|wx.EXPAND, 5 )

		dataPage.SetSizer( contentWrapper )
		dataPage.Layout()
		contentWrapper.Fit( dataPage )

		return dataPage

	def createSetUpPage(self):

		SetupPage = wx.adv.WizardPageSimple( self )

		settingContainer = wx.BoxSizer( wx.VERTICAL )
		selectMethod = wx.StaticText( SetupPage, label = u"Select Determination Method:" )
		selectSearchMethod = wx.StaticText( SetupPage, label = u"Select Parametric Study Method:" )
		selectOutPutNum = wx.StaticText( SetupPage, label = u"Select Number of Output Variables:" )

		self.MethodChoice = wx.Choice( SetupPage, choices = self.methodList )
		self.MethodChoice.SetSelection( 0 )
		self.SearchChoice = wx.Choice( SetupPage, choices = self.searchmethodList)
		self.SearchChoice.SetSelection( 0 )
		self.minResult = wx.SpinCtrl( SetupPage, min = 1, max = len(self.dataIn) - 1 )
		if len(self.dataIn) > 3:
			self.minResult.SetValue(3)

		lineBreak = wx.StaticLine( SetupPage )

		settingContainer.Add( selectMethod, 0, wx.ALL, 5 )
		settingContainer.Add( self.MethodChoice, 0, wx.ALL|wx.EXPAND, 5 )
		settingContainer.Add( selectSearchMethod, 0, wx.ALL, 5 )
		settingContainer.Add( self.SearchChoice, 0, wx.ALL|wx.EXPAND, 5 )
		settingContainer.Add( lineBreak, 0, wx.ALL|wx.EXPAND, 5 )
		settingContainer.Add( selectOutPutNum, 0, wx.ALL, 5 )
		settingContainer.Add( self.minResult, 0, wx.ALL|wx.EXPAND, 5 )

		SetupPage.SetSizer( settingContainer )
		SetupPage.Layout()
		settingContainer.Fit( SetupPage )

		#print SetupPage
		return SetupPage

	def EditDefaultPage(self):

		DefaultPage = wx.adv.WizardPageSimple( self )

		datapageContainer = wx.BoxSizer( wx.VERTICAL )
		data_and_name_Container = wx.BoxSizer( wx.VERTICAL )
		self.DataScroll = wx.ScrolledWindow( DefaultPage, style = wx.VSCROLL|wx.HSCROLL )
		self.DataScroll.SetScrollRate( 5, 5 )

		changetxt = wx.StaticText( DefaultPage, label = u"Check your variables" )

		headerWrapper = wx.FlexGridSizer( 1, 4, 0, 0 )

		headerWrapper.AddGrowableCol( 0 )
		headerWrapper.AddGrowableCol( 1 )
		headerWrapper.AddGrowableCol( 2 )
		headerWrapper.AddGrowableCol( 3 )
		headerWrapper.SetFlexibleDirection( wx.VERTICAL )

		ParaNameTxt = wx.StaticText( self.DataScroll, label = u"Parameter Name" )
		ParaLBTxt = wx.StaticText( self.DataScroll, label = u"Minimum Value" )
		ParaUBTxt = wx.StaticText( self.DataScroll, label = u"Maximum Value" )
		ParaDefaultTxt = wx.StaticText( self.DataScroll, label = u"Default Value" )

		headerWrapper.Add( ParaNameTxt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		headerWrapper.Add( ParaLBTxt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		headerWrapper.Add( ParaUBTxt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		headerWrapper.Add( ParaDefaultTxt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		datapageContainer.Add( changetxt, 0, wx.ALL, 5 )
		data_and_name_Container.Add( headerWrapper, 0, wx.EXPAND, 5)

		self.dataContainer = wx.BoxSizer( wx.VERTICAL )
		data_and_name_Container.Add( self.dataContainer, 1,  wx.EXPAND, 5 )

		self.DataScroll.SetSizer( data_and_name_Container )
		self.DataScroll.Layout()
		data_and_name_Container.Fit( self.DataScroll )
		datapageContainer.Add( self.DataScroll, 1, wx.EXPAND|wx.ALL, 5 )

		DefaultPage.SetSizer( datapageContainer )
		
		DefaultPage.Layout()
		datapageContainer.Fit( DefaultPage )

		return DefaultPage

	def updateList(self):
		current_children = self.dataContainer.GetItemCount()
		for i in range(current_children):
			self.dataContainer.Hide(0)
			self.dataContainer.Remove(0)
		self.dataElement = []
		for i in range(len(self.dataForStudy)):
			self.addItem(self.dataForStudy[i],i)

		self.dataContainer.Layout()
		self.comfirmDefaultPage.Layout()
		

	def addItem(self,data,data_id):
		nameVal = data[0]
		lbVal = data[1]
		ubVal = data[2]
		defaultVal = data[3]

		dataWrapper = wx.FlexGridSizer( 1, 4, 0, 0 )
		dataWrapper.AddGrowableCol( 0 )
		dataWrapper.AddGrowableCol( 1 )
		dataWrapper.AddGrowableCol( 2 )
		dataWrapper.AddGrowableCol( 3 )
		dataWrapper.SetFlexibleDirection( wx.VERTICAL )

		ParaNameTxt = wx.StaticText( self.DataScroll, label = nameVal )
		ParaLBEdit = wx.TextCtrl( self.DataScroll, id = 1,   )
		ParaUBEdit = wx.TextCtrl( self.DataScroll, id = 2, name = str(data_id) )
		ParaDefaultEdit = wx.TextCtrl( self.DataScroll, id = 3, name = str(data_id) )

		ParaLBEdit.SetValue(lbVal)
		ParaUBEdit.SetValue(ubVal)
		ParaDefaultEdit.SetValue(defaultVal)

		#ParaLBEdit.Bind( wx.EVT_KILL_FOCUS, self.onTxtCtrlChange )
		#ParaUBEdit.Bind( wx.EVT_KILL_FOCUS, self.onTxtCtrlChange )
		#ParaDefaultEdit.Bind( wx.EVT_KILL_FOCUS, self.onTxtCtrlChange )

		dataWrapper.Add( ParaNameTxt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		dataWrapper.Add( ParaLBEdit, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		dataWrapper.Add( ParaUBEdit, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		dataWrapper.Add( ParaDefaultEdit, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.dataElement.append([ParaNameTxt,ParaLBEdit,ParaUBEdit,ParaDefaultEdit])
		self.dataContainer.Add( dataWrapper, 1, wx.EXPAND, 5 )
	
	def checkStudyData(self):
		result = True
		problemList = []
		Name_output_List = []
		LB_output_list = []
		UB_output_list = []
		default_output_list = []
		for Index in range(len(self.dataElement)):
			Name = self.dataElement[Index][0].GetLabel()
			LBEdit = self.dataElement[Index][1]
			UBEdit = self.dataElement[Index][2]
			DefaultEdit = self.dataElement[Index][3]
			
			lbVal = LBEdit.GetValue()
			ubVal = UBEdit.GetValue()
			defaultVal = DefaultEdit.GetValue()

			if lbVal == "" or ubVal == "" or defaultVal == "" or not is_float([lbVal,ubVal,defaultVal]) or float(lbVal)>=float(ubVal) or float(defaultVal)>float(ubVal) or float(defaultVal)<float(lbVal):
				print "data problem"
				problemList.append(Name)
				result = False
			else:
				Name_output_List.append(str(Name))
				LB_output_list.append(float(lbVal))
				UB_output_list.append(float(ubVal))
				default_output_list.append(float(defaultVal))
		return result,problemList,Name_output_List,LB_output_list,UB_output_list,default_output_list

		print "Changed!"
	

	def onNext(self,event):
		print("Clicked")
		nowPage = self.GetCurrentPage()
		if nowPage == self.settingPage:
			self.minRequirementLen = self.minResult.GetValue()
		elif nowPage == self.wizDataPage:
			nameChosenList = self.dataCheckList.GetCheckedItems()
			print len(nameChosenList) , nameChosenList
			if len(nameChosenList) <= self.minRequirementLen:
				print "error"
				dial = wx.MessageDialog(None, u'Your chosen list is smaller or equal than your output list.', u'In sufficient Variables / Parameters', wx.OK | wx.ICON_ERROR)
				dial.ShowModal()
				dial.Destroy()
				return False
			self.dataForStudy = []
			for item in nameChosenList:
				self.dataForStudy.append(self.dataIn[item])
			self.updateList()
			print self.dataForStudy

		if self.HasNextPage(nowPage):
			nextPage = nowPage.GetNext()
			self.ShowPage(nextPage)
		else:
			result,errorList,Name_output_List,LB_output_list,UB_output_list,default_output_list = self.checkStudyData()
			if result:
				self.outputData = [ Name_output_List, LB_output_list, UB_output_list, default_output_list ]
				print self.outputData
				self.Destroy()
			else:
				txt = "Check the following Parameters:\n"
				for id in range(len(errorList)):
					txt += str(id + 1) + ". " + str(errorList[id]) + "\n"
					print txt
				dial = wx.MessageDialog(None, txt, u'Invalid Parameters', wx.OK | wx.ICON_ERROR)
				dial.ShowModal()
				dial.Destroy()

	def add_page(self, page):
		if len(self.pagesList)>0:
			previous_page = self.pagesList[-1]
			page.SetPrev(previous_page)
			previous_page.SetNext(page)
		self.pagesList.append(page)

class RunOptimisation( wx.adv.Wizard ):
	"""docstring for ParamtricStudy"""
	def __init__(self,*args, **kw):
		super(RunOptimisation, self).__init__(*args, **kw)
		self.dataIn = []
		self.pagesList = []
		self.dataForStudy = []
		self.outputData = []
		self.Function_method = 0
		self.methodList = ["Particle Swarm Optimisation (PSO)","Genetic Algorithm (GA)","Gradient Descent Search (GD)"]
		self.prev_btn = self.FindWindowById(wx.ID_BACKWARD)
		self.next_btn = self.FindWindowById(wx.ID_FORWARD) 
		self.next_btn.Bind(wx.EVT_BUTTON,self.onNext)
		#self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGED, self.onPageChanged)


	def loadData(self,Data,paraStudyResult):
		self.dataIn = Data
		self.paraStudyResult = paraStudyResult
		if len(Data) == 0:
			print "error"
			dial = wx.MessageDialog(None, u'Go to file -> Edit Variables to add more variables', u'No Variables / Parameters', wx.OK | wx.ICON_ERROR)
			dial.ShowModal()
			dial.Destroy()
			self.Destroy()

		self.nameList = [a[0] for a in self.dataIn]

		self.settingPage = self.createSetUpPage()
		self.wizDataPage = self.createDataPage()
		self.comfirmDefaultPage = self.EditDefaultPage()

		self.add_page( self.settingPage )
		self.add_page( self.wizDataPage )
		self.add_page( self.comfirmDefaultPage )


		self.Centre( wx.BOTH )
		self.RunWizard( self.settingPage )

	def createDataPage(self):
		dataPage = wx.adv.WizardPageSimple(self)

		contentWrapper = wx.BoxSizer( wx.VERTICAL )

		ParaNameTxt = wx.StaticText( dataPage, label = u"Select Parameters to Optimise" )

		self.dataCheckList = wx.CheckListBox( dataPage, choices = self.nameList )
		self.dataCheckList.SetCheckedStrings( self.paraStudyResult )

		contentWrapper.Add( ParaNameTxt, 0, wx.ALL, 5 )
		contentWrapper.Add( self.dataCheckList, 1, wx.ALL|wx.EXPAND, 5 )

		dataPage.SetSizer( contentWrapper )
		dataPage.Layout()
		contentWrapper.Fit( dataPage )

		return dataPage

	def createSetUpPage(self):

		SetupPage = wx.adv.WizardPageSimple( self )

		self.setupContainer = wx.BoxSizer( wx.VERTICAL )
		selectMethod = wx.StaticText( SetupPage, label = u"Select Optimisation Method:" )

		self.MethodChoice = wx.Choice( SetupPage, choices = self.methodList )
		self.MethodChoice.SetSelection( 0 )

		pso_contentpage = self.createPSO_Setting( SetupPage )
		ga_contentpage = self.createGA_Setting( SetupPage )
		gd_contentpage = self.createGD_Setting( SetupPage )

		lineBreak = wx.StaticLine( SetupPage )

		self.setupContainer.Add( selectMethod, 0, wx.ALL, 5 )
		self.setupContainer.Add( self.MethodChoice, 0, wx.ALL|wx.EXPAND, 5 )
		self.setupContainer.Add( lineBreak, 0, wx.ALL|wx.EXPAND, 5 )
		self.setupContainer.Add( pso_contentpage, 1, wx.ALL|wx.EXPAND, 5)
		self.setupContainer.Add( ga_contentpage, 1, wx.ALL|wx.EXPAND, 5)
		self.setupContainer.Add( gd_contentpage, 1, wx.ALL|wx.EXPAND, 5)

		self.setupContainer.Hide(4) # 3 (PSO), 4 (GA), 5 (GD)
		self.setupContainer.Hide(5)

		self.MethodChoice.Bind( wx.EVT_CHOICE, self.change_optim_settings )

		SetupPage.SetSizer( self.setupContainer )
		SetupPage.Layout()
		self.setupContainer.Fit( SetupPage )

		#print SetupPage
		return SetupPage

	def EditDefaultPage(self):

		DefaultPage = wx.adv.WizardPageSimple( self )

		datapageContainer = wx.BoxSizer( wx.VERTICAL )
		data_and_name_Container = wx.BoxSizer( wx.VERTICAL )
		self.DataScroll = wx.ScrolledWindow( DefaultPage, style = wx.VSCROLL|wx.HSCROLL )
		self.DataScroll.SetScrollRate( 5, 5 )

		changetxt = wx.StaticText( DefaultPage, label = u"Check your variables" )

		headerWrapper = wx.FlexGridSizer( 1, 4, 0, 0 )

		headerWrapper.AddGrowableCol( 0 )
		headerWrapper.AddGrowableCol( 1 )
		headerWrapper.AddGrowableCol( 2 )
		headerWrapper.AddGrowableCol( 3 )
		headerWrapper.SetFlexibleDirection( wx.VERTICAL )

		ParaNameTxt = wx.StaticText( self.DataScroll, label = u"Parameter Name" )
		ParaLBTxt = wx.StaticText( self.DataScroll, label = u"Minimum Value" )
		ParaUBTxt = wx.StaticText( self.DataScroll, label = u"Maximum Value" )
		ParaDefaultTxt = wx.StaticText( self.DataScroll, label = u"Default Value" )

		headerWrapper.Add( ParaNameTxt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		headerWrapper.Add( ParaLBTxt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		headerWrapper.Add( ParaUBTxt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		headerWrapper.Add( ParaDefaultTxt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		datapageContainer.Add( changetxt, 0, wx.ALL, 5 )
		data_and_name_Container.Add( headerWrapper, 0, wx.EXPAND, 5)

		self.dataContainer = wx.BoxSizer( wx.VERTICAL )
		data_and_name_Container.Add( self.dataContainer, 1,  wx.EXPAND, 5 )

		self.DataScroll.SetSizer( data_and_name_Container )
		self.DataScroll.Layout()
		data_and_name_Container.Fit( self.DataScroll )
		datapageContainer.Add( self.DataScroll, 1, wx.EXPAND|wx.ALL, 5 )

		DefaultPage.SetSizer( datapageContainer )
		
		DefaultPage.Layout()
		datapageContainer.Fit( DefaultPage )

		return DefaultPage

	def updateList(self):
		current_children = self.dataContainer.GetItemCount()
		for i in range(current_children):
			self.dataContainer.Hide(0)
			self.dataContainer.Remove(0)
		self.dataElement = []
		for i in range(len(self.dataForStudy)):
			self.addItem(self.dataForStudy[i],i)

		self.dataContainer.Layout()
		self.comfirmDefaultPage.Layout()
		

	def addItem(self,data,data_id):
		nameVal = data[0]
		lbVal = data[1]
		ubVal = data[2]
		defaultVal = data[3]

		dataWrapper = wx.FlexGridSizer( 1, 4, 0, 0 )
		dataWrapper.AddGrowableCol( 0 )
		dataWrapper.AddGrowableCol( 1 )
		dataWrapper.AddGrowableCol( 2 )
		dataWrapper.AddGrowableCol( 3 )
		dataWrapper.SetFlexibleDirection( wx.VERTICAL )

		ParaNameTxt = wx.StaticText( self.DataScroll, label = nameVal )
		ParaLBEdit = wx.TextCtrl( self.DataScroll, id = 1, name = str(data_id) )
		ParaUBEdit = wx.TextCtrl( self.DataScroll, id = 2, name = str(data_id) )
		ParaDefaultEdit = wx.TextCtrl( self.DataScroll, id = 3, name = str(data_id) )

		ParaLBEdit.SetValue(lbVal)
		ParaUBEdit.SetValue(ubVal)
		ParaDefaultEdit.SetValue(defaultVal)

		#ParaLBEdit.Bind( wx.EVT_KILL_FOCUS, self.onTxtCtrlChange )
		#ParaUBEdit.Bind( wx.EVT_KILL_FOCUS, self.onTxtCtrlChange )
		#ParaDefaultEdit.Bind( wx.EVT_KILL_FOCUS, self.onTxtCtrlChange )

		dataWrapper.Add( ParaNameTxt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		dataWrapper.Add( ParaLBEdit, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		dataWrapper.Add( ParaUBEdit, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		dataWrapper.Add( ParaDefaultEdit, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.dataElement.append([ParaNameTxt,ParaLBEdit,ParaUBEdit,ParaDefaultEdit])
		self.dataContainer.Add( dataWrapper, 1, wx.EXPAND, 5 )
	
	def checkOptimData(self):
		result = True
		problemList = []
		Name_output_List = []
		LB_output_list = []
		UB_output_list = []
		default_output_list = []
		for Index in range(len(self.dataElement)):
			Name = self.dataElement[Index][0].GetLabel()
			LBEdit = self.dataElement[Index][1]
			UBEdit = self.dataElement[Index][2]
			DefaultEdit = self.dataElement[Index][3]
			
			lbVal = LBEdit.GetValue()
			ubVal = UBEdit.GetValue()
			defaultVal = DefaultEdit.GetValue()

			if lbVal == "" or ubVal == "" or defaultVal == "" or not is_float([lbVal,ubVal,defaultVal]) or float(lbVal)>=float(ubVal) or float(defaultVal)>float(ubVal) or float(defaultVal)<float(lbVal):
				print "data problem"
				problemList.append(Name)
				result = False
			else:
				Name_output_List.append(str(Name))
				LB_output_list.append(float(lbVal))
				UB_output_list.append(float(ubVal))
				default_output_list.append(float(defaultVal))
		return result,problemList,Name_output_List,LB_output_list,UB_output_list,default_output_list

		print "Changed!"

	def createPSO_Setting(self, SetupPage):
		setting_wrapper = wx.ScrolledWindow( SetupPage, style = wx.VSCROLL|wx.HSCROLL )
		setting_wrapper.SetScrollRate( 5, 5 )
		settingContainer = wx.BoxSizer( wx.VERTICAL )
		select_iteration = wx.StaticText( setting_wrapper, label = u"Choose Max iterations:" )
		select_particle_num = wx.StaticText( setting_wrapper, label = u"Select Particle Size:" )
		select_A_constant = wx.StaticText( setting_wrapper, label = u"Select velocity constant:" )
		select_B_constant = wx.StaticText( setting_wrapper, label = u"Select second constant:" )
		select_C_constant = wx.StaticText( setting_wrapper, label = u"Select third constant:" )
		select_grad_change = wx.StaticText( setting_wrapper, label = u"Select stop gradient change:" )

		self.iterationTotal = wx.SpinCtrl( setting_wrapper, min = 2, max = 99999 )
		self.iterationTotal.SetValue(100)
		self.particleTotal = wx.SpinCtrl( setting_wrapper, min = 2, max = 9999 )
		self.particleTotal.SetValue(20)
		self.A_constant = wx.TextCtrl( setting_wrapper, value = str(0.5))
		self.B_constant = wx.TextCtrl( setting_wrapper, value = str(0.5))
		self.C_constant = wx.TextCtrl( setting_wrapper, value = str(0.5))
		self.gradient_change = wx.TextCtrl( setting_wrapper, value = str(1.0E-8))

		#horizontalSizer_Temp = wx.BoxSizer( wx.HORIZONTAL )
		settingContainer.Add( select_iteration, 0, wx.ALL, 5 )
		settingContainer.Add( self.iterationTotal, 0, wx.ALL|wx.EXPAND, 5 )
		#settingContainer.Add( horizontalSizer_Temp, 0, wx.EXPAND, 5 )
		#horizontalSizer_Temp = wx.BoxSizer( wx.HORIZONTAL )
		settingContainer.Add( select_particle_num, 0, wx.ALL, 5 )
		settingContainer.Add( self.particleTotal, 0, wx.ALL|wx.EXPAND, 5 )
		#settingContainer.Add( horizontalSizer_Temp, 0, wx.EXPAND, 5 )
		#horizontalSizer_Temp = wx.BoxSizer( wx.HORIZONTAL )
		settingContainer.Add( select_A_constant, 0, wx.ALL, 5 )
		settingContainer.Add( self.A_constant, 0, wx.ALL|wx.EXPAND, 5 )
		#settingContainer.Add( horizontalSizer_Temp, 0, wx.EXPAND, 5 )
		#horizontalSizer_Temp = wx.BoxSizer( wx.HORIZONTAL )
		settingContainer.Add( select_B_constant, 0, wx.ALL, 5 )
		settingContainer.Add( self.B_constant, 0, wx.ALL|wx.EXPAND, 5 )
		#settingContainer.Add( horizontalSizer_Temp, 0, wx.EXPAND, 5 )
		#horizontalSizer_Temp = wx.BoxSizer( wx.HORIZONTAL )
		settingContainer.Add( select_C_constant, 0, wx.ALL, 5 )
		settingContainer.Add( self.C_constant, 0, wx.ALL|wx.EXPAND, 5 )
		#settingContainer.Add( horizontalSizer_Temp, 0, wx.EXPAND, 5 )
		#horizontalSizer_Temp = wx.BoxSizer( wx.HORIZONTAL )
		settingContainer.Add( select_grad_change, 0, wx.ALL, 5 )
		settingContainer.Add( self.gradient_change, 0, wx.ALL|wx.EXPAND, 5 )
		#settingContainer.Add( horizontalSizer_Temp, 0, wx.EXPAND, 5 )

		setting_wrapper.SetSizer( settingContainer )
		setting_wrapper.Layout()

		return setting_wrapper

	def CheckPSO_param(self):
		A = self.A_constant.GetValue()
		B = self.B_constant.GetValue()
		C = self.C_constant.GetValue()
		grad = self.gradient_change.GetValue()
		return is_float([A,B,C,grad])

	def createGA_Setting(self, SetupPage):
		setting_wrapper = wx.ScrolledWindow( SetupPage, style = wx.VSCROLL|wx.HSCROLL )
		setting_wrapper.SetScrollRate( 5, 5 )
		settingContainer = wx.BoxSizer( wx.VERTICAL )
		select_generation_max = wx.StaticText( setting_wrapper, label = u"Choose Generation Limit:" )
		select_initial_generation = wx.StaticText( setting_wrapper, label = u"Select Initial Population Size:" )

		self.max_generation = wx.SpinCtrl( setting_wrapper, min = 2, max = 99999 )
		self.max_generation.SetValue(100)
		self.initial_generation = wx.SpinCtrl( setting_wrapper, min = 2, max = 9999 )
		self.initial_generation.SetValue(20)

		#horizontalSizer_Temp = wx.BoxSizer( wx.HORIZONTAL )
		settingContainer.Add( select_generation_max, 0, wx.ALL, 5 )
		settingContainer.Add( self.max_generation, 0, wx.ALL|wx.EXPAND, 5 )
		#settingContainer.Add( horizontalSizer_Temp, 0, wx.EXPAND, 5 )
		#horizontalSizer_Temp = wx.BoxSizer( wx.HORIZONTAL )
		settingContainer.Add( select_initial_generation, 0, wx.ALL, 5 )
		settingContainer.Add( self.initial_generation, 0, wx.ALL|wx.EXPAND, 5 )

		setting_wrapper.SetSizer( settingContainer )
		setting_wrapper.Layout()

		return setting_wrapper

	def createGD_Setting(self,SetupPage):
		setting_wrapper = wx.ScrolledWindow( SetupPage, style = wx.VSCROLL|wx.HSCROLL )
		setting_wrapper.SetScrollRate( 5, 5 )
		settingContainer = wx.BoxSizer( wx.VERTICAL )

		select_iterations_max = wx.StaticText( setting_wrapper, label = u"Choose Iterations Limit:" )
		select_momentum = wx.StaticText( setting_wrapper, label = u"Select Momentum:" )
		select_learning_rate = wx.StaticText( setting_wrapper, label = u"Select learning rate:" )
		select_gradient_termination = wx.StaticText( setting_wrapper, label = u"Select maximum gradient to terminate search:" )
		select_convergence_termination = wx.StaticText( setting_wrapper, label = u"Select minimum change for termination:" )

		self.max_gd_iteration = wx.SpinCtrl( setting_wrapper, min = 2, max = 99999 )
		self.max_gd_iteration.SetValue(1000)
		self.gd_momentum = wx.TextCtrl( setting_wrapper, value = str(0.9))
		self.gd_learning_rate = wx.TextCtrl( setting_wrapper, value = str(0.01))
		self.gd_grad_break = wx.TextCtrl( setting_wrapper, value = str(1.0E-4))
		self.gd_change_break = wx.TextCtrl( setting_wrapper, value = str(1.0E-2))
		#horizontalSizer_Temp = wx.BoxSizer( wx.HORIZONTAL )
		settingContainer.Add( select_iterations_max, 0, wx.ALL, 5 )
		settingContainer.Add( self.max_gd_iteration, 0, wx.ALL|wx.EXPAND, 5 )
		#settingContainer.Add( horizontalSizer_Temp, 0, wx.EXPAND, 5 )
		#horizontalSizer_Temp = wx.BoxSizer( wx.HORIZONTAL )
		settingContainer.Add( select_momentum, 0, wx.ALL, 5 )
		settingContainer.Add( self.gd_momentum, 0, wx.ALL|wx.EXPAND, 5 )

		settingContainer.Add( select_learning_rate, 0, wx.ALL, 5 )
		settingContainer.Add( self.gd_learning_rate, 0, wx.ALL|wx.EXPAND, 5 )

		settingContainer.Add( select_gradient_termination, 0, wx.ALL, 5 )
		settingContainer.Add( self.gd_grad_break, 0, wx.ALL|wx.EXPAND, 5 )

		settingContainer.Add( select_convergence_termination, 0, wx.ALL, 5 )
		settingContainer.Add( self.gd_change_break, 0, wx.ALL|wx.EXPAND, 5 )

		setting_wrapper.SetSizer( settingContainer )
		setting_wrapper.Layout()

		return setting_wrapper

	def CheckGD_param(self):
		A = self.gd_momentum.GetValue()
		B = self.gd_learning_rate.GetValue()
		C = self.gd_grad_break.GetValue()
		grad = self.gd_change_break.GetValue()
		return is_float([A,B,C,grad])

	def change_optim_settings(self, event):
		print("Changed")
		optim_index = self.MethodChoice.GetSelection()

		if optim_index == 0:
			self.setupContainer.Show(3)
			self.setupContainer.Hide(4) # 3 (PSO), 4 (GA), 5 (GD)
			self.setupContainer.Hide(5)
		elif optim_index == 1:
			self.setupContainer.Hide(3) # 3 (PSO), 4 (GA), 5 (GD)
			self.setupContainer.Show(4)
			self.setupContainer.Hide(5)
		elif optim_index == 2:
			self.setupContainer.Hide(3) # 3 (PSO), 4 (GA), 5 (GD)
			self.setupContainer.Hide(4)
			self.setupContainer.Show(5)

		self.settingPage.Layout()

	def onNext(self,event):
		print("Clicked")
		nowPage = self.GetCurrentPage()
		if nowPage == self.settingPage:
			self.Function_method = self.MethodChoice.GetSelection()
			if self.Function_method == 0:
				print "PSO"  #swarmTot = 100, constA = 0.5, constB = 0.5, constC = 0.5, max_iteration = 100, minerror = 1e-8
				if self.CheckPSO_param():
					iteration_tot = self.iterationTotal.GetValue()
					particle_tot = self.particleTotal.GetValue()
					A = float(self.A_constant.GetValue())
					B = float(self.B_constant.GetValue())
					C = float(self.C_constant.GetValue())
					grad = float(self.gradient_change.GetValue())

					self.optimise_partial = partial( partial, swarmTot = particle_tot, constA = A, constB = B, constC = C, max_iteration = iteration_tot, minerror = grad )
				else:
					dial = wx.MessageDialog(None, "Check your parameters", u'Invalid Parameters', wx.OK | wx.ICON_ERROR)
					dial.ShowModal()
					dial.Destroy()
					return False

			elif self.Function_method == 1:
				print "GA"  #generations_limit = 1000, population_initial = 50
				max_gen = self.max_generation.GetValue()
				gen_ini = self.initial_generation.GetValue()

				self.optimise_partial = partial( partial, generations_limit = max_gen, population_initial = gen_ini )

			elif self.Function_method == 2:
				print "GD" #momentum = 0.9, learning_rate = 0.01, convergingBreak = 1.0E-2, iterationTot = 10000, ErrorGrad = 1.0E-4
				if self.CheckGD_param():
					iteration_tot = self.max_gd_iteration.GetValue()
					momentum = self.gd_momentum.GetValue()
					learning_rate = self.gd_learning_rate.GetValue()
					break_via_grad = self.gd_grad_break.GetValue()
					breal_via_converg = self.gd_change_break.GetValue()

					self.optimise_partial = partial( partial, momentum = momentum, learning_rate = learning_rate, convergingBreak = breal_via_converg, ErrorGrad = break_via_grad, iterationTot = iteration_tot)

		elif nowPage == self.wizDataPage:
			nameChosenList = self.dataCheckList.GetCheckedItems()
			print len(nameChosenList) , nameChosenList
			if len(nameChosenList) == 0:
				print "error"
				dial = wx.MessageDialog(None, u'Please select an variable to optimise.', u'In sufficient Variables / Parameters', wx.OK | wx.ICON_ERROR)
				dial.ShowModal()
				dial.Destroy()
				return False
			self.dataForStudy = []
			for item in nameChosenList:
				self.dataForStudy.append(self.dataIn[item])
			self.updateList()
			print self.dataForStudy

		if self.HasNextPage(nowPage):
			nextPage = nowPage.GetNext()
			self.ShowPage(nextPage)
		else:
			result,errorList,Name_output_List,LB_output_list,UB_output_list,default_output_list = self.checkOptimData()
			if result:
				self.outputData = [ Name_output_List, LB_output_list, UB_output_list, default_output_list ]
				print self.outputData
				self.Destroy()
			else:
				txt = "Check the following Parameters:\n"
				for id in range(len(errorList)):
					txt += str(id + 1) + ". " + str(errorList[id]) + "\n"
					print txt
				dial = wx.MessageDialog(None, txt, u'Invalid Parameters', wx.OK | wx.ICON_ERROR)
				dial.ShowModal()
				dial.Destroy()

	def add_page(self, page):
		if len(self.pagesList)>0:
			previous_page = self.pagesList[-1]
			page.SetPrev(previous_page)
			previous_page.SetNext(page)
		self.pagesList.append(page)


def is_float(STR):
	if isinstance(STR, basestring):
	    try:
	        float(STR)
	        return True
	    except ValueError:
	        return False
	else:
		for item in STR:
			try:
				float(item)
			except ValueError:
				return False
		return True

if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = Framework_APP(None, title = u"Automated Framework for Eddy Current NDT", pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)
    frm.Show()
    app.MainLoop()