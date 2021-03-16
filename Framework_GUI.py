# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Nov  6 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class Starting_Screen
###########################################################################

class Starting_Screen ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Automated Framework for Eddy Current NDT", pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		self.m_statusBar1 = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )
		self.menubar_Main = wx.MenuBar( 0 )
		self.menu_File = wx.Menu()
		self.item_Import = wx.MenuItem( self.menu_File, wx.ID_ANY, u"Import File Locations"+ u"\t" + u"Ctrl+I", u"Select Important Files for Testing", wx.ITEM_NORMAL )
		self.menu_File.Append( self.item_Import )
		
		self.item_selectParam = wx.MenuItem( self.menu_File, wx.ID_ANY, u"Import &Variables"+ u"\t" + u"Ctrl+Shift+I", u"Choose parameters/variables you want to model in your program.", wx.ITEM_NORMAL )
		self.menu_File.Append( self.item_selectParam )
		
		self.menu_File.AppendSeparator()
		
		self.item_Exit = wx.MenuItem( self.menu_File, wx.ID_ANY, u"&Exit", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_File.Append( self.item_Exit )
		
		self.menubar_Main.Append( self.menu_File, u"&File" ) 
		
		self.menu_More = wx.Menu()
		self.item_Help = wx.MenuItem( self.menu_More, wx.ID_ANY, u"&Help"+ u"\t" + u"Ctrl+H", u"Do not know how to use the framework?", wx.ITEM_NORMAL )
		self.menu_More.Append( self.item_Help )
		
		self.item_About = wx.MenuItem( self.menu_More, wx.ID_ANY, u"&About", u"Find out more about this framework!", wx.ITEM_NORMAL )
		self.menu_More.Append( self.item_About )
		
		self.menubar_Main.Append( self.menu_More, u"&More" ) 
		
		self.SetMenuBar( self.menubar_Main )
		
		box_btn_container = wx.BoxSizer( wx.VERTICAL )
		
		box_paraStudy = wx.BoxSizer( wx.VERTICAL )
		
		self.btn_paraStudy = wx.Button( self, wx.ID_ANY, u"&Parameter Study", wx.DefaultPosition, wx.DefaultSize, 0 )
		box_paraStudy.Add( self.btn_paraStudy, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
		
		
		box_btn_container.Add( box_paraStudy, 1, wx.EXPAND, 5 )
		
		box_paraOptim = wx.BoxSizer( wx.VERTICAL )
		
		self.btn_paraOptim = wx.Button( self, wx.ID_ANY, u"Parameter &Optimisation", wx.DefaultPosition, wx.DefaultSize, 0 )
		box_paraOptim.Add( self.btn_paraOptim, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
		
		
		box_btn_container.Add( box_paraOptim, 1, wx.EXPAND, 5 )
		
		box_Simulation = wx.BoxSizer( wx.VERTICAL )
		
		self.btn_Simulation = wx.Button( self, wx.ID_ANY, u"&Simulation", wx.DefaultPosition, wx.DefaultSize, 0 )
		box_Simulation.Add( self.btn_Simulation, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
		
		
		box_btn_container.Add( box_Simulation, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( box_btn_container )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

