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
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"PMT Controller"), pos = wx.DefaultPosition, size = wx.Size( 750,500 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.Size( 1600,900 ), wx.Size( -1,-1 ) )
        self.SetFont( wx.Font( 10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_SLANT, wx.FONTWEIGHT_BOLD, False, "Sawasdee" ) )

        self.m_menubar1 = wx.MenuBar( 0 )
        self.m_menubar1.SetMinSize( wx.Size( 1600,900 ) )

        self.m_menu1 = wx.Menu()
        self.m_menubar1.Append( self.m_menu1, _(u"File") )

        self.m_menu2 = wx.Menu()
        self.m_menubar1.Append( self.m_menu2, _(u"Options") )

        self.m_menu3 = wx.Menu()
        self.m_menubar1.Append( self.m_menu3, _(u"COM Port Settings") )

        self.m_menu4 = wx.Menu()
        self.m_menubar1.Append( self.m_menu4, _(u"Log Settings") )

        self.m_menu5 = wx.Menu()
        self.m_menubar1.Append( self.m_menu5, _(u"Help") )

        self.m_menu6 = wx.Menu()
        self.m_menubar1.Append( self.m_menu6, _(u"About") )

        self.SetMenuBar( self.m_menubar1 )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel7 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.m_panel7.SetBackgroundColour( wx.Colour( 246, 215, 235 ) )

        bSizer35 = wx.BoxSizer( wx.VERTICAL )

        bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer4 = wx.BoxSizer( wx.VERTICAL )

        self.m_notebook1 = wx.Notebook( self.m_panel7, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_notebook1.SetBackgroundColour( wx.Colour( 235, 195, 232 ) )
        self.m_notebook1.SetMaxSize( wx.Size( 400,-1 ) )

        self.m_panel61 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer6 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel5 = wx.Panel( self.m_panel61, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.m_panel5.SetBackgroundColour( wx.Colour( 194, 184, 184 ) )

        bSizer24 = wx.BoxSizer( wx.VERTICAL )

        bSizer7 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText1 = wx.StaticText( self.m_panel5, wx.ID_ANY, _(u"Gate Size \n (1 - 1000)"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )

        bSizer7.Add( self.m_staticText1, 2, wx.ALL, 5 )


        bSizer7.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_textCtrl1 = wx.TextCtrl( self.m_panel5, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer7.Add( self.m_textCtrl1, 2, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText2 = wx.StaticText( self.m_panel5, wx.ID_ANY, _(u"x 10us"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )

        bSizer7.Add( self.m_staticText2, 2, wx.ALL|wx.EXPAND, 5 )


        bSizer24.Add( bSizer7, 0, wx.EXPAND, 5 )


        self.m_panel5.SetSizer( bSizer24 )
        self.m_panel5.Layout()
        bSizer24.Fit( self.m_panel5 )
        bSizer6.Add( self.m_panel5, 1, wx.EXPAND |wx.ALL, 5 )


        self.m_panel61.SetSizer( bSizer6 )
        self.m_panel61.Layout()
        bSizer6.Fit( self.m_panel61 )
        self.m_notebook1.AddPage( self.m_panel61, _(u"Gate Counter"), False )
        self.m_panel71 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer10 = wx.BoxSizer( wx.VERTICAL )

        bSizer61 = wx.BoxSizer( wx.VERTICAL )


        bSizer10.Add( bSizer61, 1, wx.EXPAND, 5 )

        self.m_panel6 = wx.Panel( self.m_panel71, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.m_panel6.SetBackgroundColour( wx.Colour( 218, 207, 187 ) )

        bSizer27 = wx.BoxSizer( wx.VERTICAL )


        self.m_panel6.SetSizer( bSizer27 )
        self.m_panel6.Layout()
        bSizer27.Fit( self.m_panel6 )
        bSizer10.Add( self.m_panel6, 1, wx.EXPAND |wx.ALL, 5 )


        self.m_panel71.SetSizer( bSizer10 )
        self.m_panel71.Layout()
        bSizer10.Fit( self.m_panel71 )
        self.m_notebook1.AddPage( self.m_panel71, _(u"Reciprocal Counter"), False )
        self.m_panel8 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer22 = wx.BoxSizer( wx.VERTICAL )

        bSizer23 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText5 = wx.StaticText( self.m_panel8, wx.ID_ANY, _(u"Observer Name"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText5.Wrap( -1 )

        bSizer23.Add( self.m_staticText5, 1, wx.ALL, 5 )

        self.m_textCtrl2 = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer23.Add( self.m_textCtrl2, 2, wx.ALL, 5 )


        bSizer22.Add( bSizer23, 0, wx.EXPAND, 5 )

        bSizer231 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText6 = wx.StaticText( self.m_panel8, wx.ID_ANY, _(u"Object Name"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText6.Wrap( -1 )

        bSizer231.Add( self.m_staticText6, 1, wx.ALL, 5 )

        self.m_textCtrl3 = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer231.Add( self.m_textCtrl3, 2, wx.ALL, 5 )


        bSizer22.Add( bSizer231, 0, wx.EXPAND, 5 )

        bSizer232 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText7 = wx.StaticText( self.m_panel8, wx.ID_ANY, _(u"Exposure Time"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText7.Wrap( -1 )

        bSizer232.Add( self.m_staticText7, 1, wx.ALL, 5 )

        self.m_textCtrl4 = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer232.Add( self.m_textCtrl4, 2, wx.ALL, 5 )


        bSizer22.Add( bSizer232, 0, wx.EXPAND, 5 )

        bSizer233 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText8 = wx.StaticText( self.m_panel8, wx.ID_ANY, _(u"Image Type"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText8.Wrap( -1 )

        bSizer233.Add( self.m_staticText8, 1, wx.ALL, 5 )

        m_comboBox4Choices = []
        self.m_comboBox4 = wx.ComboBox( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, m_comboBox4Choices, 0 )
        bSizer233.Add( self.m_comboBox4, 2, wx.ALL, 5 )


        bSizer22.Add( bSizer233, 0, wx.EXPAND, 5 )

        bSizer2331 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText81 = wx.StaticText( self.m_panel8, wx.ID_ANY, _(u"Shutter Mode"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText81.Wrap( -1 )

        bSizer2331.Add( self.m_staticText81, 1, wx.ALL, 5 )

        m_comboBox41Choices = []
        self.m_comboBox41 = wx.ComboBox( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, m_comboBox41Choices, 0 )
        bSizer2331.Add( self.m_comboBox41, 2, wx.ALL, 5 )


        bSizer22.Add( bSizer2331, 1, wx.EXPAND, 5 )


        self.m_panel8.SetSizer( bSizer22 )
        self.m_panel8.Layout()
        bSizer22.Fit( self.m_panel8 )
        self.m_notebook1.AddPage( self.m_panel8, _(u"Addings"), True )

        bSizer4.Add( self.m_notebook1, 1, wx.EXPAND |wx.ALL, 5 )

        bSizer16 = wx.BoxSizer( wx.HORIZONTAL )


        bSizer16.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_button1 = wx.Button( self.m_panel7, wx.ID_ANY, _(u"OK"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer16.Add( self.m_button1, 0, wx.ALL, 5 )

        self.m_button2 = wx.Button( self.m_panel7, wx.ID_ANY, _(u"Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer16.Add( self.m_button2, 0, wx.ALL, 5 )


        bSizer4.Add( bSizer16, 0, wx.EXPAND, 5 )


        bSizer2.Add( bSizer4, 1, wx.EXPAND, 5 )

        bSizer5 = wx.BoxSizer( wx.VERTICAL )

        bSizer14 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel1 = wx.Panel( self.m_panel7, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.m_panel1.SetBackgroundColour( wx.Colour( 234, 202, 202 ) )

        bSizer14.Add( self.m_panel1, 1, wx.EXPAND |wx.ALL, 5 )


        bSizer5.Add( bSizer14, 1, wx.EXPAND, 5 )

        bSizer15 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel2 = wx.Panel( self.m_panel7, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.m_panel2.SetBackgroundColour( wx.Colour( 192, 221, 182 ) )

        bSizer15.Add( self.m_panel2, 1, wx.EXPAND |wx.ALL, 5 )


        bSizer5.Add( bSizer15, 1, wx.EXPAND, 5 )

        bSizer17 = wx.BoxSizer( wx.HORIZONTAL )


        bSizer17.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_button3 = wx.Button( self.m_panel7, wx.ID_ANY, _(u"Start Plot"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer17.Add( self.m_button3, 1, wx.ALL, 5 )


        bSizer17.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_spinCtrl2 = wx.SpinCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10, 0 )
        bSizer17.Add( self.m_spinCtrl2, 0, wx.ALL, 5 )


        bSizer5.Add( bSizer17, 0, wx.EXPAND, 5 )


        bSizer2.Add( bSizer5, 3, wx.EXPAND, 5 )


        bSizer35.Add( bSizer2, 1, wx.EXPAND, 5 )


        self.m_panel7.SetSizer( bSizer35 )
        self.m_panel7.Layout()
        bSizer35.Fit( self.m_panel7 )
        bSizer1.Add( self.m_panel7, 1, wx.EXPAND |wx.ALL, 5 )


        self.SetSizer( bSizer1 )
        self.Layout()

        self.Centre( wx.BOTH )

    def __del__( self ):
        pass


###########################################################################
## Class MyDialog1
###########################################################################

class MyDialog1 ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"COM Port Settings"), pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHints( wx.Size( 350,250 ), wx.Size( 350,250 ) )

        bSizer29 = wx.BoxSizer( wx.VERTICAL )


        bSizer29.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        bSizer30 = wx.BoxSizer( wx.HORIZONTAL )


        bSizer30.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_staticText14 = wx.StaticText( self, wx.ID_ANY, _(u"MyLabel"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText14.Wrap( -1 )

        bSizer30.Add( self.m_staticText14, 0, wx.ALL, 5 )


        bSizer30.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        m_comboBox4Choices = []
        self.m_comboBox4 = wx.ComboBox( self, wx.ID_ANY, _(u"COM Ports"), wx.DefaultPosition, wx.DefaultSize, m_comboBox4Choices, 0 )
        bSizer30.Add( self.m_comboBox4, 0, wx.ALL, 5 )


        bSizer30.Add( ( 0, 0), 1, wx.EXPAND, 5 )


        bSizer29.Add( bSizer30, 2, wx.EXPAND, 5 )

        bSizer31 = wx.BoxSizer( wx.HORIZONTAL )


        bSizer31.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_staticText15 = wx.StaticText( self, wx.ID_ANY, _(u"MyLabel"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText15.Wrap( -1 )

        bSizer31.Add( self.m_staticText15, 0, wx.ALL, 5 )


        bSizer31.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        m_comboBox5Choices = []
        self.m_comboBox5 = wx.ComboBox( self, wx.ID_ANY, _(u"BaudRate"), wx.DefaultPosition, wx.DefaultSize, m_comboBox5Choices, 0 )
        bSizer31.Add( self.m_comboBox5, 0, wx.ALL, 5 )


        bSizer31.Add( ( 0, 0), 1, wx.EXPAND, 5 )


        bSizer29.Add( bSizer31, 2, wx.EXPAND, 5 )

        bSizer32 = wx.BoxSizer( wx.HORIZONTAL )


        bSizer32.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_button6 = wx.Button( self, wx.ID_ANY, _(u"OK"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer32.Add( self.m_button6, 0, wx.ALL, 5 )

        self.m_button7 = wx.Button( self, wx.ID_ANY, _(u"Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer32.Add( self.m_button7, 0, wx.ALL, 5 )


        bSizer29.Add( bSizer32, 0, wx.EXPAND, 5 )


        bSizer29.Add( ( 0, 0), 1, wx.EXPAND, 5 )


        self.SetSizer( bSizer29 )
        self.Layout()
        bSizer29.Fit( self )

        self.Centre( wx.BOTH )

    def __del__( self ):
        pass


