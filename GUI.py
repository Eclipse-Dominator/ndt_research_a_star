import wx
import wx.xrc
import wx.adv
import wx.grid

class MyWizard1 ( wx.adv.Wizard ):
   
   def __init__( self, parent ):
      wx.adv.Wizard.__init__ ( self, parent, id = wx.ID_ANY, title = u"Conduct Parametric Study", bitmap = wx.NullBitmap, pos = wx.DefaultPosition, style = wx.DEFAULT_DIALOG_STYLE )
      
      self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
      self.m_pages = []
      
      self.m_wizPage1 = wx.adv.WizardPageSimple( self  )
      self.add_page( self.m_wizPage1 )
      
      bSizer7 = wx.BoxSizer( wx.VERTICAL )
      
      self.m_staticText7 = wx.StaticText( self.m_wizPage1, wx.ID_ANY, u"Select Parameters for Parametric Study", wx.DefaultPosition, wx.DefaultSize, 0 )
      self.m_staticText7.Wrap( -1 )
      bSizer7.Add( self.m_staticText7, 0, wx.ALL, 5 )
      
      m_checkList2Choices = [u"1234123", u"1234"]
      self.m_checkList2 = wx.CheckListBox( self.m_wizPage1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_checkList2Choices, wx.LB_SORT )
      bSizer7.Add( self.m_checkList2, 1, wx.ALL|wx.EXPAND, 5 )
      
      
      self.m_wizPage1.SetSizer( bSizer7 )
      self.m_wizPage1.Layout()
      bSizer7.Fit( self.m_wizPage1 )
      self.m_wizPage2 = wx.adv.WizardPageSimple( self  )
      self.add_page( self.m_wizPage2 )
      
      bSizer8 = wx.BoxSizer( wx.VERTICAL )
      
      self.m_staticText10 = wx.StaticText( self.m_wizPage2, wx.ID_ANY, u"Select Determination Method:", wx.DefaultPosition, wx.DefaultSize, 0 )
      self.m_staticText10.Wrap( -1 )
      bSizer8.Add( self.m_staticText10, 0, wx.ALL, 5 )
      
      m_choice2Choices = [ u"Min Max Difference" ]
      self.m_choice2 = wx.Choice( self.m_wizPage2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice2Choices, 0 )
      self.m_choice2.SetSelection( 0 )
      bSizer8.Add( self.m_choice2, 0, wx.ALL|wx.EXPAND, 5 )
      
      self.m_staticText8 = wx.StaticText( self.m_wizPage2, wx.ID_ANY, u"Select Parametric Study Method:", wx.DefaultPosition, wx.DefaultSize, 0 )
      self.m_staticText8.Wrap( -1 )
      bSizer8.Add( self.m_staticText8, 0, wx.ALL, 5 )
      
      m_choice3Choices = [ u"Genetic Algorithm" ]
      self.m_choice3 = wx.Choice( self.m_wizPage2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice3Choices, 0 )
      self.m_choice3.SetSelection( 0 )
      bSizer8.Add( self.m_choice3, 0, wx.ALL|wx.EXPAND, 5 )
      
      self.m_staticline1 = wx.StaticLine( self.m_wizPage2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
      bSizer8.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
      
      self.m_staticText9 = wx.StaticText( self.m_wizPage2, wx.ID_ANY, u"Select Number of Output Variables:", wx.DefaultPosition, wx.DefaultSize, 0 )
      self.m_staticText9.Wrap( -1 )
      bSizer8.Add( self.m_staticText9, 0, wx.ALL, 5 )
      
      self.m_spinCtrl1 = wx.SpinCtrl( self.m_wizPage2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 10, 1 )
      bSizer8.Add( self.m_spinCtrl1, 0, wx.ALL|wx.EXPAND, 5 )
      
      
      self.m_wizPage2.SetSizer( bSizer8 )
      self.m_wizPage2.Layout()
      bSizer8.Fit( self.m_wizPage2 )

###########################################################################################################################################################
      DefaultPage = wx.adv.WizardPageSimple( self  )
      self.add_page( DefaultPage )
      
      datapageContainer = wx.BoxSizer( wx.VERTICAL )
      
      changetxt = wx.StaticText( DefaultPage, label = u"Check your variables" )
      
      DataScroll = wx.ScrolledWindow( DefaultPage, style = wx.VSCROLL|wx.HSCROLL )
      DataScroll.SetScrollRate( 5, 5 )
      data_and_name_Container = wx.BoxSizer( wx.VERTICAL )
      
      headerWrapper = wx.FlexGridSizer( 0, 4, 0, 0 )
      headerWrapper.AddGrowableCol( 0 )
      headerWrapper.AddGrowableCol( 1 )
      headerWrapper.AddGrowableCol( 2 )
      headerWrapper.AddGrowableCol( 3 )
      headerWrapper.SetFlexibleDirection( wx.BOTH )
      headerWrapper.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
      
      ParaNameTxt = wx.StaticText( DataScroll, label = u"Parameter Name" )    
      ParaLBTxt = wx.StaticText( DataScroll, label = u"Minimum Value" )
      ParaUBTxt = wx.StaticText( DataScroll, label = u"Maximum Value" )
      ParaDefaultTxt = wx.StaticText( DataScroll, label = u"Default Value" )
      
      headerWrapper.Add( ParaNameTxt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
      headerWrapper.Add( ParaDefaultTxt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
      headerWrapper.Add( ParaLBTxt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
      headerWrapper.Add( ParaUBTxt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
      
      datapageContainer.Add( changetxt, 0, wx.ALL, 5 )
      data_and_name_Container.Add( headerWrapper, 0, wx.EXPAND, 5 )
      
      contentWrap = wx.BoxSizer( wx.VERTICAL )
      
      data_and_name_Container.Add( contentWrap, 1, wx.EXPAND, 5 )
      
      
      DataScroll.SetSizer( data_and_name_Container )
      DataScroll.Layout()
      data_and_name_Container.Fit( DataScroll )
      datapageContainer.Add( DataScroll, 1, wx.EXPAND |wx.ALL, 5 )
      
      
      DefaultPage.SetSizer( datapageContainer )
      DefaultPage.Layout()
      datapageContainer.Fit( DefaultPage )
      self.Centre( wx.BOTH )
      self.RunWizard( self.m_wizPage1 )
      
   def add_page(self, page):
      if self.m_pages:
         previous_page = self.m_pages[-1]
         page.SetPrev(previous_page)
         previous_page.SetNext(page)
      self.m_pages.append(page)
   
   def __del__( self ):
      pass
   
   


#self.RunWizard( self.m_wizPage1 )
app = wx.App() 
dlg = MyWizard1(None) 
app.MainLoop()

'''
fgSizer311 = wx.FlexGridSizer( 0, 4, 0, 0 )
fgSizer311.AddGrowableCol( 0 )
fgSizer311.AddGrowableCol( 1 )
fgSizer311.AddGrowableCol( 2 )
fgSizer311.AddGrowableCol( 3 )
fgSizer311.SetFlexibleDirection( wx.BOTH )
fgSizer311.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

self.m_textCtrl511 = wx.TextCtrl( DataScroll, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
fgSizer311.Add( self.m_textCtrl511, 0, wx.ALL, 5 )

self.m_textCtrl611 = wx.TextCtrl( DataScroll, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
fgSizer311.Add( self.m_textCtrl611, 0, wx.ALL, 5 )

self.m_textCtrl711 = wx.TextCtrl( DataScroll, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
fgSizer311.Add( self.m_textCtrl711, 0, wx.ALL, 5 )

self.m_textCtrl811 = wx.TextCtrl( DataScroll, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
fgSizer311.Add( self.m_textCtrl811, 0, wx.ALL, 5 )


contentWrap.Add( fgSizer311, 0, wx.EXPAND, 5 )
'''
