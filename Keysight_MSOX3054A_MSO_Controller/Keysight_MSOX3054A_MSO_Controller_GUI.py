# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid

###########################################################################
## Class frame_Main
###########################################################################

class frame_Main ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Keysight_MSOX3054A_MSO_Controller", pos = wx.DefaultPosition, size = wx.Size( 925,506 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL|wx.BORDER_SUNKEN )
		self.m_panel1.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_SCROLLBAR ) )

		bSizer5 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText10 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"PMT Data Logger", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
		self.m_staticText10.Wrap( -1 )

		self.m_staticText10.SetFont( wx.Font( 18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		bSizer5.Add( self.m_staticText10, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_panel7 = wx.Panel( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_SUNKEN|wx.TAB_TRAVERSAL )
		bSizer9 = wx.BoxSizer( wx.VERTICAL )

		bSizer102 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText7 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"HT(Voltage):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )

		bSizer102.Add( self.m_staticText7, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_textCtrl5 = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer102.Add( self.m_textCtrl5, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText8 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Temperature (deg C):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )

		bSizer102.Add( self.m_staticText8, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		m_choice3Choices = [ u"20", u"00", u"-10", u"-20", u"-30" ]
		self.m_choice3 = wx.Choice( self.m_panel7, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice3Choices, 0 )
		self.m_choice3.SetSelection( 0 )
		bSizer102.Add( self.m_choice3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.toggleBtn_MSOX3054A_Connect = wx.ToggleButton( self.m_panel7, wx.ID_ANY, u"   Connect MSOX3054A   ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.toggleBtn_MSOX3054A_Connect.SetFont( wx.Font( 10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Tahoma" ) )

		bSizer102.Add( self.toggleBtn_MSOX3054A_Connect, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer9.Add( bSizer102, 1, wx.EXPAND, 5 )

		bSizer111 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText9 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Select log file location", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )

		bSizer111.Add( self.m_staticText9, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.dirPicker = wx.DirPickerCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE|wx.DIRP_USE_TEXTCTRL )
		bSizer111.Add( self.dirPicker, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.toggleButton_StartLogging = wx.ToggleButton( self.m_panel7, wx.ID_ANY, u"Start logging", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer111.Add( self.toggleButton_StartLogging, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer9.Add( bSizer111, 1, wx.EXPAND, 5 )


		self.m_panel7.SetSizer( bSizer9 )
		self.m_panel7.Layout()
		bSizer9.Fit( self.m_panel7 )
		bSizer5.Add( self.m_panel7, 3, wx.EXPAND |wx.ALL, 5 )

		self.m_panel6 = wx.Panel( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_SUNKEN|wx.TAB_TRAVERSAL )
		bSizer103 = wx.BoxSizer( wx.VERTICAL )

		fgSizer1 = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSizer1.AddGrowableCol( 1 )
		fgSizer1.AddGrowableRow( 0 )
		fgSizer1.AddGrowableRow( 1 )
		fgSizer1.AddGrowableRow( 2 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText4 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Counts\n", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.m_staticText4.Wrap( -1 )

		self.m_staticText4.SetFont( wx.Font( 14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Sans" ) )
		self.m_staticText4.SetMaxSize( wx.Size( 200,-1 ) )

		fgSizer1.Add( self.m_staticText4, 0, wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

		self.panel_counts = wx.Panel( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.BORDER_SIMPLE )
		self.panel_counts.SetMinSize( wx.Size( 280,-1 ) )

		fgSizer1.Add( self.panel_counts, 3, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText71 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"counts/sec", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
		self.m_staticText71.Wrap( -1 )

		self.m_staticText71.SetFont( wx.Font( 14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Sans" ) )

		fgSizer1.Add( self.m_staticText71, 5, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText5 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"AC RMS\nVoltage ", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.m_staticText5.Wrap( -1 )

		self.m_staticText5.SetFont( wx.Font( 14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Sans" ) )

		fgSizer1.Add( self.m_staticText5, 2, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.panel_rms = wx.Panel( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_SIMPLE )
		self.panel_rms.SetMinSize( wx.Size( 20,-1 ) )

		fgSizer1.Add( self.panel_rms, 2, wx.EXPAND |wx.ALL, 5 )

		self.m_staticText81 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Vrms", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText81.Wrap( -1 )

		self.m_staticText81.SetFont( wx.Font( 14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Sans" ) )

		fgSizer1.Add( self.m_staticText81, 5, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.m_staticText6 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Neutral to Earth\n Voltage       ", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.m_staticText6.Wrap( -1 )

		self.m_staticText6.SetFont( wx.Font( 14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Sans" ) )

		fgSizer1.Add( self.m_staticText6, 2, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.panel_NtoE = wx.Panel( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_SIMPLE )
		self.panel_NtoE.SetMinSize( wx.Size( 20,-1 ) )

		fgSizer1.Add( self.panel_NtoE, 2, wx.EXPAND |wx.ALL, 5 )

		self.m_staticText91 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"V", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText91.Wrap( -1 )

		self.m_staticText91.SetFont( wx.Font( 14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Sans" ) )

		fgSizer1.Add( self.m_staticText91, 5, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )


		bSizer103.Add( fgSizer1, 1, wx.EXPAND, 5 )


		self.m_panel6.SetSizer( bSizer103 )
		self.m_panel6.Layout()
		bSizer103.Fit( self.m_panel6 )
		bSizer5.Add( self.m_panel6, 4, wx.EXPAND |wx.ALL, 5 )


		self.m_panel1.SetSizer( bSizer5 )
		self.m_panel1.Layout()
		bSizer5.Fit( self.m_panel1 )
		bSizer1.Add( self.m_panel1, 1, wx.ALL|wx.EXPAND, 2 )

		self.m_panel8 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_SUNKEN|wx.TAB_TRAVERSAL )
		bSizer15 = wx.BoxSizer( wx.VERTICAL )

		self.grid_Data = wx.grid.Grid( self.m_panel8, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.grid_Data.CreateGrid( 20, 3 )
		self.grid_Data.EnableEditing( True )
		self.grid_Data.EnableGridLines( True )
		self.grid_Data.EnableDragGridSize( False )
		self.grid_Data.SetMargins( 0, 0 )

		# Columns
		self.grid_Data.EnableDragColMove( False )
		self.grid_Data.EnableDragColSize( False )
		self.grid_Data.SetColLabelValue( 0, u"Counts" )
		self.grid_Data.SetColLabelValue( 1, u"RMS" )
		self.grid_Data.SetColLabelValue( 2, u"N-E" )
		self.grid_Data.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.grid_Data.EnableDragRowSize( True )
		self.grid_Data.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.grid_Data.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer15.Add( self.grid_Data, 1, wx.ALL|wx.EXPAND, 5 )


		self.m_panel8.SetSizer( bSizer15 )
		self.m_panel8.Layout()
		bSizer15.Fit( self.m_panel8 )
		bSizer1.Add( self.m_panel8, 1, wx.EXPAND |wx.ALL, 2 )


		self.SetSizer( bSizer1 )
		self.Layout()
		self.statusBar = self.CreateStatusBar( 3, wx.STB_SIZEGRIP|wx.BORDER_SUNKEN, wx.ID_ANY )

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.frameMain_Close )
		self.toggleBtn_MSOX3054A_Connect.Bind( wx.EVT_TOGGLEBUTTON, self.toggleBtn_MSOX3054A_Connect_OnToggle )
		self.dirPicker.Bind( wx.EVT_DIRPICKER_CHANGED, self.dirPicker_OnDirChanged )
		self.toggleButton_StartLogging.Bind( wx.EVT_TOGGLEBUTTON, self.toggleButton_StartLogging_OnToggle )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def frameMain_Close( self, event ):
		event.Skip()

	def toggleBtn_MSOX3054A_Connect_OnToggle( self, event ):
		event.Skip()

	def dirPicker_OnDirChanged( self, event ):
		event.Skip()

	def toggleButton_StartLogging_OnToggle( self, event ):
		event.Skip()


