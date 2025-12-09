# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

import gettext
_ = gettext.gettext

###########################################################################
## Class frameMain
###########################################################################

class frameMain ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"16 inch Telescope Controller"), pos = wx.DefaultPosition, size = wx.Size( 782,550 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.Size( 1200,900 ), wx.Size( 1200,900 ) )
        self.SetFont( wx.Font( 18, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Sans" ) )
        self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DDKSHADOW ) )

        self.menubarMain = wx.MenuBar( 0 )
        self.menuFile = wx.Menu()
        self.menuItemFile = wx.MenuItem( self.menuFile, wx.ID_ANY, _(u"New")+ u"\t" + u"Ctrl+N", wx.EmptyString, wx.ITEM_NORMAL )
        self.menuFile.Append( self.menuItemFile )

        self.menuItemOpen = wx.MenuItem( self.menuFile, wx.ID_ANY, _(u"Open")+ u"\t" + u"Ctrl+O", wx.EmptyString, wx.ITEM_NORMAL )
        self.menuFile.Append( self.menuItemOpen )

        self.menuItemSave = wx.MenuItem( self.menuFile, wx.ID_ANY, _(u"Save")+ u"\t" + u"Ctrl+S", wx.EmptyString, wx.ITEM_NORMAL )
        self.menuFile.Append( self.menuItemSave )

        self.menuItemSaveas = wx.MenuItem( self.menuFile, wx.ID_ANY, _(u"Save As..."), wx.EmptyString, wx.ITEM_NORMAL )
        self.menuFile.Append( self.menuItemSaveas )

        self.menuFile.AppendSeparator()

        self.menuItemExit = wx.MenuItem( self.menuFile, wx.ID_ANY, _(u"Exit"), wx.EmptyString, wx.ITEM_NORMAL )
        self.menuFile.Append( self.menuItemExit )

        self.menubarMain.Append( self.menuFile, _(u"File") )

        self.menuEdit = wx.Menu()
        self.menubarMain.Append( self.menuEdit, _(u"Edit") )

        self.menuCOM = wx.Menu()
        self.menubarMain.Append( self.menuCOM, _(u"COM Port Setting") )

        self.menuHelp = wx.Menu()
        self.menubarMain.Append( self.menuHelp, _(u"Help") )

        self.SetMenuBar( self.menubarMain )

        bSizerFrameMain = wx.BoxSizer( wx.VERTICAL )

        bSizerFrameMain.SetMinSize( wx.Size( 750,500 ) )
        self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizerMainFrame = wx.BoxSizer( wx.HORIZONTAL )

        bSizer14 = wx.BoxSizer( wx.VERTICAL )

        bSizer14.SetMinSize( wx.Size( 300,500 ) )
        bSizer16 = wx.BoxSizer( wx.VERTICAL )

        bSizer16.SetMinSize( wx.Size( 250,210 ) )
        self.m_panel3 = wx.Panel( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.m_panel3.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOTEXT ) )
        self.m_panel3.SetBackgroundColour( wx.Colour( 192, 215, 161 ) )

        bSizer23 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText511 = wx.StaticText( self.m_panel3, wx.ID_ANY, _(u"Telescope Information"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText511.Wrap( -1 )

        self.m_staticText511.SetFont( wx.Font( 20, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Sans" ) )

        bSizer23.Add( self.m_staticText511, 1, wx.ALL|wx.EXPAND, 5 )

        bSizer18 = wx.BoxSizer( wx.HORIZONTAL )


        bSizer18.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_staticText2 = wx.StaticText( self.m_panel3, wx.ID_ANY, _(u"RA"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )

        self.m_staticText2.SetFont( wx.Font( 30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer18.Add( self.m_staticText2, 3, wx.ALL|wx.EXPAND, 5 )

        self.m_textCtrl1 = wx.TextCtrl( self.m_panel3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_textCtrl1.SetFont( wx.Font( 20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer18.Add( self.m_textCtrl1, 8, wx.ALL|wx.EXPAND, 5 )


        bSizer23.Add( bSizer18, 2, wx.ALL|wx.EXPAND, 5 )

        bSizer19 = wx.BoxSizer( wx.HORIZONTAL )


        bSizer19.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_staticText3 = wx.StaticText( self.m_panel3, wx.ID_ANY, _(u"DEC"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )

        self.m_staticText3.SetFont( wx.Font( 30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer19.Add( self.m_staticText3, 3, wx.ALL|wx.EXPAND, 5 )

        self.m_textCtrl2 = wx.TextCtrl( self.m_panel3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_textCtrl2.SetFont( wx.Font( 20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer19.Add( self.m_textCtrl2, 8, wx.ALL|wx.EXPAND, 5 )


        bSizer23.Add( bSizer19, 2, wx.ALL|wx.EXPAND, 5 )

        bSizer20 = wx.BoxSizer( wx.HORIZONTAL )


        bSizer20.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_staticText4 = wx.StaticText( self.m_panel3, wx.ID_ANY, _(u"HA"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )

        self.m_staticText4.SetFont( wx.Font( 30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer20.Add( self.m_staticText4, 3, wx.ALL|wx.EXPAND, 5 )

        self.m_textCtrl3 = wx.TextCtrl( self.m_panel3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_textCtrl3.SetFont( wx.Font( 20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer20.Add( self.m_textCtrl3, 8, wx.ALL|wx.EXPAND, 5 )


        bSizer23.Add( bSizer20, 2, wx.ALL|wx.EXPAND, 5 )


        self.m_panel3.SetSizer( bSizer23 )
        self.m_panel3.Layout()
        bSizer23.Fit( self.m_panel3 )
        bSizer16.Add( self.m_panel3, 1, wx.EXPAND |wx.ALL, 5 )


        bSizer14.Add( bSizer16, 3, wx.EXPAND, 5 )

        bSizer17 = wx.BoxSizer( wx.VERTICAL )

        bSizer17.SetMinSize( wx.Size( 300,240 ) )
        self.m_panel4 = wx.Panel( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.m_panel4.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DDKSHADOW ) )
        self.m_panel4.SetBackgroundColour( wx.Colour( 232, 190, 208 ) )

        bSizer24 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText51 = wx.StaticText( self.m_panel4, wx.ID_ANY, _(u"Time Information"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText51.Wrap( -1 )

        self.m_staticText51.SetFont( wx.Font( 20, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Sans" ) )

        bSizer24.Add( self.m_staticText51, 1, wx.ALL|wx.EXPAND, 5 )

        bSizer12 = wx.BoxSizer( wx.HORIZONTAL )


        bSizer12.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_staticText6 = wx.StaticText( self.m_panel4, wx.ID_ANY, _(u"LST"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText6.Wrap( -1 )

        self.m_staticText6.SetFont( wx.Font( 30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer12.Add( self.m_staticText6, 3, wx.ALL|wx.EXPAND, 5 )

        self.m_textCtrl4 = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_textCtrl4.SetFont( wx.Font( 20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer12.Add( self.m_textCtrl4, 8, wx.ALL|wx.EXPAND, 5 )


        bSizer24.Add( bSizer12, 2, wx.EXPAND, 5 )

        bSizer13 = wx.BoxSizer( wx.HORIZONTAL )


        bSizer13.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_staticText7 = wx.StaticText( self.m_panel4, wx.ID_ANY, _(u"UT"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText7.Wrap( -1 )

        self.m_staticText7.SetFont( wx.Font( 30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer13.Add( self.m_staticText7, 3, wx.ALL|wx.EXPAND, 5 )

        self.m_textCtrl5 = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_textCtrl5.SetFont( wx.Font( 20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer13.Add( self.m_textCtrl5, 8, wx.ALL|wx.EXPAND, 5 )


        bSizer24.Add( bSizer13, 2, wx.EXPAND, 5 )

        bSizer141 = wx.BoxSizer( wx.HORIZONTAL )


        bSizer141.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_staticText8 = wx.StaticText( self.m_panel4, wx.ID_ANY, _(u"IST"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText8.Wrap( -1 )

        self.m_staticText8.SetFont( wx.Font( 30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer141.Add( self.m_staticText8, 3, wx.ALL|wx.EXPAND, 5 )

        self.m_textCtrl6 = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_textCtrl6.SetFont( wx.Font( 20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer141.Add( self.m_textCtrl6, 8, wx.ALL|wx.EXPAND, 5 )


        bSizer24.Add( bSizer141, 2, wx.EXPAND, 5 )

        bSizer151 = wx.BoxSizer( wx.HORIZONTAL )


        bSizer151.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_staticText9 = wx.StaticText( self.m_panel4, wx.ID_ANY, _(u"JD"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText9.Wrap( -1 )

        self.m_staticText9.SetFont( wx.Font( 30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer151.Add( self.m_staticText9, 3, wx.ALL|wx.EXPAND, 5 )

        self.m_textCtrl7 = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_textCtrl7.SetFont( wx.Font( 20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer151.Add( self.m_textCtrl7, 8, wx.ALL|wx.EXPAND, 5 )


        bSizer24.Add( bSizer151, 2, wx.EXPAND, 5 )


        self.m_panel4.SetSizer( bSizer24 )
        self.m_panel4.Layout()
        bSizer24.Fit( self.m_panel4 )
        bSizer17.Add( self.m_panel4, 1, wx.EXPAND |wx.ALL, 5 )


        bSizer14.Add( bSizer17, 4, wx.EXPAND, 5 )


        bSizerMainFrame.Add( bSizer14, 40, wx.EXPAND, 5 )

        bSizer15 = wx.BoxSizer( wx.VERTICAL )

        bSizer15.SetMinSize( wx.Size( 300,500 ) )
        self.m_panel2 = wx.Panel( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.m_panel2.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DDKSHADOW ) )
        self.m_panel2.SetBackgroundColour( wx.Colour( 196, 217, 238 ) )

        bSizer22 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText10 = wx.StaticText( self.m_panel2, wx.ID_ANY, _(u"Telescope Operational Switches"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText10.Wrap( -1 )

        self.m_staticText10.SetFont( wx.Font( 20, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Sans" ) )

        bSizer22.Add( self.m_staticText10, 4, wx.ALL|wx.EXPAND, 5 )

        bSizer161 = wx.BoxSizer( wx.HORIZONTAL )


        bSizer161.Add( ( 0, 0), 11, wx.EXPAND, 5 )

        self.m_checkBox_console = wx.CheckBox( self.m_panel2, wx.ID_ANY, _(u"Console"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_checkBox_console.SetValue(True)
        self.m_checkBox_console.SetFont( wx.Font( 30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer161.Add( self.m_checkBox_console, 16, wx.ALL|wx.EXPAND, 5 )


        bSizer161.Add( ( 0, 0), 0, wx.EXPAND, 5 )

        self.m_checkBox_handset = wx.CheckBox( self.m_panel2, wx.ID_ANY, _(u"Handset"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_checkBox_handset.SetFont( wx.Font( 30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer161.Add( self.m_checkBox_handset, 15, wx.ALL|wx.EXPAND, 5 )


        bSizer161.Add( ( 0, 0), 10, wx.EXPAND, 5 )


        bSizer22.Add( bSizer161, 4, wx.EXPAND, 5 )

        self.m_staticline1 = wx.StaticLine( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer22.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )

        bSizer1611 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText13 = wx.StaticText( self.m_panel2, wx.ID_ANY, _(u"RA \nlimit"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText13.Wrap( -1 )

        self.m_staticText13.SetFont( wx.Font( 20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer1611.Add( self.m_staticText13, 13, wx.ALL|wx.EXPAND, 5 )

        self.m_textCtrl9 = wx.TextCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_textCtrl9.SetFont( wx.Font( 18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer1611.Add( self.m_textCtrl9, 60, wx.ALL|wx.EXPAND, 5 )


        bSizer1611.Add( ( 0, 0), 9, wx.EXPAND, 5 )

        self.m_staticText14 = wx.StaticText( self.m_panel2, wx.ID_ANY, _(u"DEC \nlimit"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText14.Wrap( -1 )

        self.m_staticText14.SetFont( wx.Font( 20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer1611.Add( self.m_staticText14, 15, wx.ALL|wx.EXPAND, 5 )

        self.m_textCtrl10 = wx.TextCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_textCtrl10.SetFont( wx.Font( 18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer1611.Add( self.m_textCtrl10, 60, wx.ALL|wx.EXPAND, 5 )


        bSizer22.Add( bSizer1611, 4, wx.EXPAND, 5 )

        self.m_staticline11 = wx.StaticLine( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer22.Add( self.m_staticline11, 0, wx.EXPAND |wx.ALL, 5 )

        bSizer31 = wx.BoxSizer( wx.HORIZONTAL )


        bSizer31.Add( ( 0, 0), 10, wx.EXPAND, 5 )

        self.m_staticText21 = wx.StaticText( self.m_panel2, wx.ID_ANY, _(u"RIGHT ASCENSION"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText21.Wrap( -1 )

        self.m_staticText21.SetFont( wx.Font( 19, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Sans" ) )

        bSizer31.Add( self.m_staticText21, 40, wx.ALIGN_BOTTOM, 5 )


        bSizer31.Add( ( 0, 0), 15, wx.EXPAND, 5 )

        self.m_staticText22 = wx.StaticText( self.m_panel2, wx.ID_ANY, _(u"DECLINATION"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText22.Wrap( -1 )

        self.m_staticText22.SetFont( wx.Font( 19, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Sans" ) )

        bSizer31.Add( self.m_staticText22, 30, wx.ALIGN_BOTTOM, 5 )


        bSizer31.Add( ( 0, 0), 5, wx.EXPAND, 5 )


        bSizer22.Add( bSizer31, 2, wx.EXPAND, 5 )

        bSizer33 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_button4 = wx.Button( self.m_panel2, wx.ID_ANY, _(u"SLEW\nEAST"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button4.SetFont( wx.Font( 17, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer33.Add( self.m_button4, 15, wx.ALL|wx.EXPAND, 5 )

        self.m_button5 = wx.Button( self.m_panel2, wx.ID_ANY, _(u"SLEW\nWEST"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button5.SetFont( wx.Font( 17, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer33.Add( self.m_button5, 15, wx.ALL|wx.EXPAND, 5 )


        bSizer33.Add( ( 0, 0), 4, wx.EXPAND, 5 )

        self.m_button6 = wx.Button( self.m_panel2, wx.ID_ANY, _(u" SLEW\nNORTH"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button6.SetFont( wx.Font( 17, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer33.Add( self.m_button6, 15, wx.ALL|wx.EXPAND, 5 )

        self.m_button7 = wx.Button( self.m_panel2, wx.ID_ANY, _(u" SLEW\nSOUTH"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button7.SetFont( wx.Font( 17, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer33.Add( self.m_button7, 15, wx.ALL|wx.EXPAND, 5 )


        bSizer22.Add( bSizer33, 8, wx.EXPAND, 5 )

        bSizer331 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_button41 = wx.Button( self.m_panel2, wx.ID_ANY, _(u" SET \nEAST"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button41.SetFont( wx.Font( 17, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer331.Add( self.m_button41, 15, wx.ALL|wx.EXPAND, 5 )

        self.m_button51 = wx.Button( self.m_panel2, wx.ID_ANY, _(u" SET \nWEST"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button51.SetFont( wx.Font( 17, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer331.Add( self.m_button51, 15, wx.ALL|wx.EXPAND, 5 )


        bSizer331.Add( ( 0, 0), 4, wx.EXPAND, 5 )

        self.m_button61 = wx.Button( self.m_panel2, wx.ID_ANY, _(u"   SET \nNORTH"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button61.SetFont( wx.Font( 17, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer331.Add( self.m_button61, 15, wx.ALL|wx.EXPAND, 5 )

        self.m_button71 = wx.Button( self.m_panel2, wx.ID_ANY, _(u"   SET \nSOUTH"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button71.SetFont( wx.Font( 17, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer331.Add( self.m_button71, 15, wx.ALL|wx.EXPAND, 5 )


        bSizer22.Add( bSizer331, 8, wx.EXPAND, 5 )

        bSizer332 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_button42 = wx.Button( self.m_panel2, wx.ID_ANY, _(u"GUIDE \n  EAST"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button42.SetFont( wx.Font( 17, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer332.Add( self.m_button42, 15, wx.ALL|wx.EXPAND, 5 )

        self.m_button52 = wx.Button( self.m_panel2, wx.ID_ANY, _(u"GUIDE \n WEST"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button52.SetFont( wx.Font( 17, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer332.Add( self.m_button52, 15, wx.ALL|wx.EXPAND, 5 )


        bSizer332.Add( ( 0, 0), 4, wx.EXPAND, 5 )

        self.m_button62 = wx.Button( self.m_panel2, wx.ID_ANY, _(u"GUIDE \nNORTH"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button62.SetFont( wx.Font( 17, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer332.Add( self.m_button62, 15, wx.ALL|wx.EXPAND, 5 )

        self.m_button72 = wx.Button( self.m_panel2, wx.ID_ANY, _(u"GUIDE \nSOUTH"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button72.SetFont( wx.Font( 17, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer332.Add( self.m_button72, 15, wx.ALL|wx.EXPAND, 5 )


        bSizer22.Add( bSizer332, 8, wx.EXPAND, 5 )

        bSizer333 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_button43 = wx.Button( self.m_panel2, wx.ID_ANY, _(u"FINE GUIDE \n      EAST"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button43.SetFont( wx.Font( 17, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer333.Add( self.m_button43, 15, wx.ALL|wx.EXPAND, 5 )

        self.m_button53 = wx.Button( self.m_panel2, wx.ID_ANY, _(u"FINE GUIDE \n      WEST"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button53.SetFont( wx.Font( 17, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer333.Add( self.m_button53, 15, wx.ALL|wx.EXPAND, 5 )


        bSizer333.Add( ( 0, 0), 4, wx.EXPAND, 5 )

        self.m_button63 = wx.Button( self.m_panel2, wx.ID_ANY, _(u"FINE GUIDE \n    NORTH"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button63.SetFont( wx.Font( 17, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer333.Add( self.m_button63, 15, wx.ALL|wx.EXPAND, 5 )

        self.m_button73 = wx.Button( self.m_panel2, wx.ID_ANY, _(u"FINE GUIDE \n    SOUTH"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button73.SetFont( wx.Font( 17, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer333.Add( self.m_button73, 15, wx.ALL|wx.EXPAND, 5 )


        bSizer22.Add( bSizer333, 8, wx.EXPAND, 5 )

        self.m_staticline12 = wx.StaticLine( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer22.Add( self.m_staticline12, 0, wx.EXPAND |wx.ALL, 5 )

        bSizer1613 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText15 = wx.StaticText( self.m_panel2, wx.ID_ANY, _(u"RA track"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText15.Wrap( -1 )

        self.m_staticText15.SetFont( wx.Font( 20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer1613.Add( self.m_staticText15, 20, wx.ALL|wx.EXPAND, 5 )

        self.m_button24 = wx.Button( self.m_panel2, wx.ID_ANY, _(u"ON"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button24.SetFont( wx.Font( 17, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer1613.Add( self.m_button24, 12, wx.ALL|wx.EXPAND, 5 )

        self.m_button25 = wx.Button( self.m_panel2, wx.ID_ANY, _(u"OFF"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button25.SetFont( wx.Font( 17, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer1613.Add( self.m_button25, 12, wx.ALL|wx.EXPAND, 5 )


        bSizer1613.Add( ( 0, 0), 5, wx.EXPAND, 5 )

        self.m_staticText16 = wx.StaticText( self.m_panel2, wx.ID_ANY, _(u"Status"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText16.Wrap( -1 )

        self.m_staticText16.SetFont( wx.Font( 20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer1613.Add( self.m_staticText16, 15, wx.ALL|wx.EXPAND, 5 )

        self.m_textCtrl11 = wx.TextCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_textCtrl11.SetFont( wx.Font( 20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer1613.Add( self.m_textCtrl11, 30, wx.ALL|wx.EXPAND, 5 )


        bSizer22.Add( bSizer1613, 4, wx.EXPAND, 5 )

        bSizer16131 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText151 = wx.StaticText( self.m_panel2, wx.ID_ANY, _(u"Secondary\n Focus    "), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText151.Wrap( -1 )

        self.m_staticText151.SetFont( wx.Font( 14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer16131.Add( self.m_staticText151, 20, wx.ALL|wx.EXPAND, 5 )

        self.m_button26 = wx.Button( self.m_panel2, wx.ID_ANY, _(u"UP"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button26.SetFont( wx.Font( 17, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer16131.Add( self.m_button26, 12, wx.ALL|wx.EXPAND, 5 )

        self.m_button27 = wx.Button( self.m_panel2, wx.ID_ANY, _(u"DOWN"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button27.SetFont( wx.Font( 17, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer16131.Add( self.m_button27, 12, wx.ALL|wx.EXPAND, 5 )


        bSizer16131.Add( ( 0, 0), 5, wx.EXPAND, 5 )

        self.m_staticText161 = wx.StaticText( self.m_panel2, wx.ID_ANY, _(u"Status"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText161.Wrap( -1 )

        self.m_staticText161.SetFont( wx.Font( 20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer16131.Add( self.m_staticText161, 15, wx.ALL|wx.EXPAND, 5 )

        self.m_textCtrl111 = wx.TextCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_textCtrl111.SetFont( wx.Font( 20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer16131.Add( self.m_textCtrl111, 30, wx.ALL|wx.EXPAND, 5 )


        bSizer22.Add( bSizer16131, 4, wx.EXPAND, 5 )

        self.m_staticline13 = wx.StaticLine( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer22.Add( self.m_staticline13, 0, wx.EXPAND |wx.ALL, 5 )

        bSizer30 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText20 = wx.StaticText( self.m_panel2, wx.ID_ANY, _(u"INPUT"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText20.Wrap( -1 )

        self.m_staticText20.SetFont( wx.Font( 20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer30.Add( self.m_staticText20, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_textCtrl12 = wx.TextCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_textCtrl12.SetFont( wx.Font( 20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer30.Add( self.m_textCtrl12, 4, wx.ALL|wx.EXPAND, 5 )


        bSizer22.Add( bSizer30, 1, wx.ALIGN_BOTTOM|wx.EXPAND, 5 )


        self.m_panel2.SetSizer( bSizer22 )
        self.m_panel2.Layout()
        bSizer22.Fit( self.m_panel2 )
        bSizer15.Add( self.m_panel2, 0, wx.EXPAND |wx.ALL, 5 )


        bSizerMainFrame.Add( bSizer15, 0, wx.EXPAND, 5 )


        self.m_panel1.SetSizer( bSizerMainFrame )
        self.m_panel1.Layout()
        bSizerMainFrame.Fit( self.m_panel1 )
        bSizerFrameMain.Add( self.m_panel1, 1, wx.EXPAND |wx.ALL, 5 )


        self.SetSizer( bSizerFrameMain )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.Bind( wx.EVT_MENU, self.menuItemFileOnMenuSelection, id = self.menuItemFile.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItemOpenOnMenuSelection, id = self.menuItemOpen.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItemSaveOnMenuSelection, id = self.menuItemSave.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItemSaveasOnMenuSelection, id = self.menuItemSaveas.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItemExitOnMenuSelection, id = self.menuItemExit.GetId() )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def menuItemFileOnMenuSelection( self, event ):
        event.Skip()

    def menuItemOpenOnMenuSelection( self, event ):
        event.Skip()

    def menuItemSaveOnMenuSelection( self, event ):
        event.Skip()

    def menuItemSaveasOnMenuSelection( self, event ):
        event.Skip()

    def menuItemExitOnMenuSelection( self, event ):
        event.Skip()


###########################################################################
## Class MyDialog1
###########################################################################

class MyDialog1 ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"COM Port Settings"), pos = wx.DefaultPosition, size = wx.Size( 300,200 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer25 = wx.BoxSizer( wx.VERTICAL )

        bSizer32 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText17 = wx.StaticText( self, wx.ID_ANY, _(u"COM_Port_Setting "), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText17.Wrap( -1 )

        self.m_staticText17.SetFont( wx.Font( 10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Sans" ) )

        bSizer32.Add( self.m_staticText17, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )


        bSizer25.Add( bSizer32, 0, wx.EXPAND, 5 )

        bSizer29 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText18 = wx.StaticText( self, wx.ID_ANY, _(u"Select Port :"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText18.Wrap( -1 )

        bSizer29.Add( self.m_staticText18, 1, wx.ALL|wx.EXPAND, 5 )

        m_comboBox1Choices = []
        self.m_comboBox1 = wx.ComboBox( self, wx.ID_ANY, _(u"Ports"), wx.DefaultPosition, wx.Size( 150,30 ), m_comboBox1Choices, 0 )
        bSizer29.Add( self.m_comboBox1, 2, wx.ALL, 5 )


        bSizer25.Add( bSizer29, 1, wx.EXPAND, 5 )

        bSizer30 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText19 = wx.StaticText( self, wx.ID_ANY, _(u"Baudrate:"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText19.Wrap( -1 )

        bSizer30.Add( self.m_staticText19, 1, wx.ALL, 5 )

        m_comboBox2Choices = []
        self.m_comboBox2 = wx.ComboBox( self, wx.ID_ANY, _(u"BaudRate"), wx.DefaultPosition, wx.DefaultSize, m_comboBox2Choices, 0 )
        bSizer30.Add( self.m_comboBox2, 2, wx.ALL, 5 )


        bSizer25.Add( bSizer30, 1, wx.EXPAND, 5 )

        bSizer31 = wx.BoxSizer( wx.HORIZONTAL )


        bSizer31.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_button1 = wx.Button( self, wx.ID_ANY, _(u"OK"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer31.Add( self.m_button1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

        self.m_button2 = wx.Button( self, wx.ID_ANY, _(u"Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer31.Add( self.m_button2, 0, wx.ALL, 5 )


        bSizer25.Add( bSizer31, 1, wx.EXPAND, 5 )


        self.SetSizer( bSizer25 )
        self.Layout()

        self.Centre( wx.BOTH )

    def __del__( self ):
        pass


