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
## Class Popup_importFile
###########################################################################

class Popup_importFile ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Import Files", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_DIALOG_STYLE )

		import_MainContainer = wx.BoxSizer( wx.VERTICAL )
		
		import_Container = wx.FlexGridSizer( 2, 2, 0, 0 )
		
		cstTxt = wx.StaticText( self, label = "Select CST FILE:" )
		coilTxt = wx.StaticText( self, label = "Select Coil Parameter:" )
		#self.cstTxt.Wrap( -1 )
		
		cstFileImport = wx.FilePickerCtrl( self, message = "Select your CST file")
		coilFileImport = wx.FilePickerCtrl( self, message = "Select Coil Parameter Output FIle" )
		
		import_Container.Add( cstTxt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )
		import_Container.Add( cstFileImport,0, wx.ALL|wx.EXPAND, 5  )
		
		import_Container.Add( coilTxt,0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )
		import_Container.Add( coilFileImport,0, wx.ALL|wx.EXPAND, 5  )
		
		
		ok_cancel_container = wx.StdDialogButtonSizer()
		ok_key = wx.Button( self, wx.ID_OK )
		cancel_key = wx.Button( self, wx.ID_CANCEL )
				
		ok_cancel_container.AddButton( ok_key )
		ok_cancel_container.AddButton( cancel_key )
		ok_cancel_container.Realize()
		
		import_MainContainer.Add( import_Container, 1, wx.EXPAND, 5 )
		import_MainContainer.Add( ok_cancel_container, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( import_MainContainer )

		import_MainContainer.Fit( self )
		
		self.Centre( wx.BOTH )


	
	def __del__( self ):
		pass
	

app = wx.App()
frm = Popup_importFile(None)
frm.Show()
app.MainLoop()