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
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Wide Field Corrector Controller"), pos = wx.DefaultPosition, size = wx.Size( 1200,900 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetFont( wx.Font( 10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Noto Sans Soyombo" ) )

        self.m_menubar1 = wx.MenuBar( 0 )
        self.m_menu1 = wx.Menu()
        self.m_menuItem5 = wx.MenuItem( self.m_menu1, wx.ID_ANY, _(u"MyMenuItem"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu1.Append( self.m_menuItem5 )

        self.m_menu1.AppendSeparator()

        self.m_menuItem6 = wx.MenuItem( self.m_menu1, wx.ID_ANY, _(u"MyMenuItem"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu1.Append( self.m_menuItem6 )

        self.m_menuItem7 = wx.MenuItem( self.m_menu1, wx.ID_ANY, _(u"Load Saved Settings"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu1.Append( self.m_menuItem7 )

        self.m_menu1.AppendSeparator()

        self.m_menuItem8 = wx.MenuItem( self.m_menu1, wx.ID_ANY, _(u"Quit"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu1.Append( self.m_menuItem8 )

        self.m_menubar1.Append( self.m_menu1, _(u"File") )

        self.m_menu2 = wx.Menu()
        self.m_menuItem1 = wx.MenuItem( self.m_menu2, wx.ID_ANY, _(u"Parameter Settings"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu2.Append( self.m_menuItem1 )

        self.m_menuItem2 = wx.MenuItem( self.m_menu2, wx.ID_ANY, _(u"COM Port Settings"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu2.Append( self.m_menuItem2 )

        self.m_menuItem3 = wx.MenuItem( self.m_menu2, wx.ID_ANY, _(u"Filter Wheel Settings"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu2.Append( self.m_menuItem3 )

        self.m_menubar1.Append( self.m_menu2, _(u"Settings") )

        self.m_menu3 = wx.Menu()
        self.m_menuItem4 = wx.MenuItem( self.m_menu3, wx.ID_ANY, _(u"About"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu3.Append( self.m_menuItem4 )

        self.m_menubar1.Append( self.m_menu3, _(u"Help") )

        self.SetMenuBar( self.m_menubar1 )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer2 = wx.BoxSizer( wx.VERTICAL )

        sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel1, wx.ID_ANY, _(u"COM Port Settngs") ), wx.HORIZONTAL )


        sbSizer1.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_staticText1 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, _(u"Port"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )

        sbSizer1.Add( self.m_staticText1, 0, wx.ALL, 5 )

        m_comboBox1Choices = []
        self.m_comboBox1 = wx.ComboBox( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, m_comboBox1Choices, 0 )
        sbSizer1.Add( self.m_comboBox1, 0, wx.ALL, 5 )

        self.m_staticText2 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, _(u"Baudrate"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )

        sbSizer1.Add( self.m_staticText2, 0, wx.ALL, 5 )

        m_comboBox2Choices = []
        self.m_comboBox2 = wx.ComboBox( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, m_comboBox2Choices, 0 )
        sbSizer1.Add( self.m_comboBox2, 0, wx.ALL, 5 )


        sbSizer1.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_button1 = wx.Button( sbSizer1.GetStaticBox(), wx.ID_ANY, _(u"OPEN COM PORT"), wx.DefaultPosition, wx.DefaultSize, 0 )
        sbSizer1.Add( self.m_button1, 0, wx.ALL, 5 )


        sbSizer1.Add( ( 0, 0), 1, wx.EXPAND, 5 )


        bSizer2.Add( sbSizer1, 1, wx.EXPAND, 5 )

        sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel1, wx.ID_ANY, _(u"Motor Controls") ), wx.VERTICAL )

        bSizer4 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer11 = wx.BoxSizer( wx.VERTICAL )

        self.m_button2 = wx.Button( sbSizer2.GetStaticBox(), wx.ID_ANY, _(u"INITIAL POSITION"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer11.Add( self.m_button2, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_button3 = wx.Button( sbSizer2.GetStaticBox(), wx.ID_ANY, _(u"CENTER POSITION"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer11.Add( self.m_button3, 1, wx.ALL|wx.EXPAND, 5 )


        bSizer4.Add( bSizer11, 3, wx.EXPAND, 5 )

        bSizer12 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel9 = wx.Panel( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_SUNKEN )
        self.m_panel9.SetMaxSize( wx.Size( 600,240 ) )

        bSizer32 = wx.BoxSizer( wx.VERTICAL )

        bSizer27 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText10 = wx.StaticText( self.m_panel9, wx.ID_ANY, _(u"Give input in arc second."), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.m_staticText10.Wrap( -1 )

        bSizer27.Add( self.m_staticText10, 0, wx.ALL, 5 )


        bSizer32.Add( bSizer27, 0, wx.EXPAND, 5 )

        bSizer14 = wx.BoxSizer( wx.HORIZONTAL )


        bSizer14.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_textCtrl22 = wx.TextCtrl( self.m_panel9, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_textCtrl22.SetMaxSize( wx.Size( 60,40 ) )

        bSizer14.Add( self.m_textCtrl22, 0, wx.ALL, 5 )

        self.m_button4 = wx.Button( self.m_panel9, wx.ID_ANY, _(u"North"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button4.SetMaxSize( wx.Size( 40,40 ) )

        bSizer14.Add( self.m_button4, 0, wx.ALL, 5 )


        bSizer14.Add( ( 0, 0), 1, wx.EXPAND, 5 )


        bSizer32.Add( bSizer14, 1, wx.EXPAND, 5 )

        bSizer15 = wx.BoxSizer( wx.HORIZONTAL )


        bSizer15.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_textCtrl23 = wx.TextCtrl( self.m_panel9, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_textCtrl23.SetMaxSize( wx.Size( 60,40 ) )

        bSizer15.Add( self.m_textCtrl23, 0, wx.ALL, 5 )

        self.m_button5 = wx.Button( self.m_panel9, wx.ID_ANY, _(u"West"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button5.SetMaxSize( wx.Size( 40,40 ) )

        bSizer15.Add( self.m_button5, 0, wx.ALL, 5 )


        bSizer15.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_textCtrl24 = wx.TextCtrl( self.m_panel9, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_textCtrl24.SetMaxSize( wx.Size( 60,40 ) )

        bSizer15.Add( self.m_textCtrl24, 0, wx.ALL, 5 )

        self.m_button6 = wx.Button( self.m_panel9, wx.ID_ANY, _(u"East "), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button6.SetMaxSize( wx.Size( 40,40 ) )

        bSizer15.Add( self.m_button6, 0, wx.ALL, 5 )


        bSizer15.Add( ( 0, 0), 1, wx.EXPAND, 5 )


        bSizer32.Add( bSizer15, 1, wx.EXPAND, 5 )

        bSizer16 = wx.BoxSizer( wx.HORIZONTAL )


        bSizer16.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_textCtrl25 = wx.TextCtrl( self.m_panel9, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_textCtrl25.SetMaxSize( wx.Size( 60,40 ) )

        bSizer16.Add( self.m_textCtrl25, 0, wx.ALL, 5 )

        self.m_button7 = wx.Button( self.m_panel9, wx.ID_ANY, _(u"South"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button7.SetMaxSize( wx.Size( 40,40 ) )

        bSizer16.Add( self.m_button7, 0, wx.ALL, 5 )


        bSizer16.Add( ( 0, 0), 1, wx.EXPAND, 5 )


        bSizer32.Add( bSizer16, 1, wx.EXPAND, 5 )


        self.m_panel9.SetSizer( bSizer32 )
        self.m_panel9.Layout()
        bSizer32.Fit( self.m_panel9 )
        bSizer12.Add( self.m_panel9, 0, wx.EXPAND |wx.ALL, 5 )


        bSizer4.Add( bSizer12, 6, wx.EXPAND, 5 )

        bSizer13 = wx.BoxSizer( wx.VERTICAL )

        bSizer18 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText9 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, _(u"Current Positon"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText9.Wrap( -1 )

        bSizer18.Add( self.m_staticText9, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_textCtrl2 = wx.TextCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer18.Add( self.m_textCtrl2, 1, wx.ALL|wx.EXPAND, 5 )


        bSizer13.Add( bSizer18, 1, wx.EXPAND, 5 )


        bSizer4.Add( bSizer13, 4, wx.EXPAND, 5 )


        sbSizer2.Add( bSizer4, 1, wx.EXPAND, 5 )


        bSizer2.Add( sbSizer2, 0, wx.EXPAND, 5 )

        sbSizer3 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel1, wx.ID_ANY, _(u"Filter Controls") ), wx.VERTICAL )

        bSizer5 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText5 = wx.StaticText( sbSizer3.GetStaticBox(), wx.ID_ANY, _(u"Select Filter"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText5.Wrap( -1 )

        bSizer5.Add( self.m_staticText5, 1, wx.ALL|wx.EXPAND, 5 )


        bSizer5.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_button10 = wx.Button( sbSizer3.GetStaticBox(), wx.ID_ANY, _(u"Filter 1"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer5.Add( self.m_button10, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_button11 = wx.Button( sbSizer3.GetStaticBox(), wx.ID_ANY, _(u"Filter 2"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer5.Add( self.m_button11, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_button12 = wx.Button( sbSizer3.GetStaticBox(), wx.ID_ANY, _(u"Filter 3"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer5.Add( self.m_button12, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_button13 = wx.Button( sbSizer3.GetStaticBox(), wx.ID_ANY, _(u"Filter 4"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer5.Add( self.m_button13, 1, wx.ALL|wx.EXPAND, 5 )


        sbSizer3.Add( bSizer5, 1, wx.EXPAND, 5 )


        bSizer2.Add( sbSizer3, 2, wx.EXPAND, 5 )

        sbSizer4 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel1, wx.ID_ANY, _(u"Output") ), wx.VERTICAL )

        bSizer7 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer19 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText91 = wx.StaticText( sbSizer4.GetStaticBox(), wx.ID_ANY, _(u"XY Stage Position"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText91.Wrap( -1 )

        bSizer19.Add( self.m_staticText91, 0, wx.ALL, 5 )

        self.m_panel2 = wx.Panel( sbSizer4.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_SUNKEN|wx.TAB_TRAVERSAL )
        bSizer19.Add( self.m_panel2, 1, wx.EXPAND |wx.ALL, 5 )


        bSizer7.Add( bSizer19, 2, wx.EXPAND, 5 )

        bSizer20 = wx.BoxSizer( wx.VERTICAL )

        bSizer21 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel3 = wx.Panel( sbSizer4.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_SUNKEN|wx.TAB_TRAVERSAL )
        bSizer21.Add( self.m_panel3, 1, wx.EXPAND |wx.ALL, 5 )


        bSizer20.Add( bSizer21, 1, wx.EXPAND, 5 )

        bSizer22 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel4 = wx.Panel( sbSizer4.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_SUNKEN|wx.TAB_TRAVERSAL )
        bSizer23 = wx.BoxSizer( wx.VERTICAL )

        bSizer24 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText6 = wx.StaticText( self.m_panel4, wx.ID_ANY, _(u"Current Position (x,y)"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText6.Wrap( -1 )

        bSizer24.Add( self.m_staticText6, 1, wx.ALL, 5 )

        self.m_textCtrl3 = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer24.Add( self.m_textCtrl3, 0, wx.ALL, 5 )

        self.m_textCtrl7 = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer24.Add( self.m_textCtrl7, 0, wx.ALL, 5 )


        bSizer23.Add( bSizer24, 1, wx.EXPAND, 5 )

        bSizer25 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText7 = wx.StaticText( self.m_panel4, wx.ID_ANY, _(u"Camara position (x,y)"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText7.Wrap( -1 )

        bSizer25.Add( self.m_staticText7, 1, wx.ALL, 5 )

        self.m_textCtrl4 = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer25.Add( self.m_textCtrl4, 0, wx.ALL, 5 )

        self.m_textCtrl8 = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer25.Add( self.m_textCtrl8, 0, wx.ALL, 5 )


        bSizer23.Add( bSizer25, 1, wx.EXPAND, 5 )

        bSizer26 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText8 = wx.StaticText( self.m_panel4, wx.ID_ANY, _(u"Filter Wheel Position"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText8.Wrap( -1 )

        bSizer26.Add( self.m_staticText8, 1, wx.ALL, 5 )

        self.m_textCtrl5 = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer26.Add( self.m_textCtrl5, 1, wx.ALL, 5 )


        bSizer23.Add( bSizer26, 1, wx.EXPAND, 5 )


        self.m_panel4.SetSizer( bSizer23 )
        self.m_panel4.Layout()
        bSizer23.Fit( self.m_panel4 )
        bSizer22.Add( self.m_panel4, 1, wx.EXPAND |wx.ALL, 5 )


        bSizer20.Add( bSizer22, 1, wx.EXPAND, 5 )


        bSizer7.Add( bSizer20, 1, wx.EXPAND, 5 )


        sbSizer4.Add( bSizer7, 1, wx.EXPAND, 5 )


        bSizer2.Add( sbSizer4, 10, wx.EXPAND, 5 )


        self.m_panel1.SetSizer( bSizer2 )
        self.m_panel1.Layout()
        bSizer2.Fit( self.m_panel1 )
        bSizer1.Add( self.m_panel1, 1, wx.EXPAND |wx.ALL, 5 )


        self.SetSizer( bSizer1 )
        self.Layout()

        self.Centre( wx.BOTH )

    def __del__( self ):
        pass


###########################################################################
## Class FilterWheelSetting
###########################################################################

class FilterWheelSetting ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Filter Wheel Settings"), pos = wx.DefaultPosition, size = wx.Size( 404,320 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer22 = wx.BoxSizer( wx.VERTICAL )


        bSizer22.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_panel5 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_SUNKEN|wx.TAB_TRAVERSAL )
        bSizer23 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText10 = wx.StaticText( self.m_panel5, wx.ID_ANY, _(u"Enter Filter Wheel Names and Positions:"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText10.Wrap( -1 )

        bSizer23.Add( self.m_staticText10, 0, wx.ALL, 5 )

        fgSizer2 = wx.FlexGridSizer( 0, 4, 0, 0 )
        fgSizer2.SetFlexibleDirection( wx.BOTH )
        fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )


        fgSizer2.Add( ( 0, 0), 2, wx.EXPAND, 5 )

        self.m_staticText11 = wx.StaticText( self.m_panel5, wx.ID_ANY, _(u"Filter Name"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText11.Wrap( -1 )

        fgSizer2.Add( self.m_staticText11, 1, wx.ALL, 5 )

        self.m_staticText12 = wx.StaticText( self.m_panel5, wx.ID_ANY, _(u"Filter Position"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText12.Wrap( -1 )

        fgSizer2.Add( self.m_staticText12, 1, wx.ALL, 5 )


        fgSizer2.Add( ( 0, 0), 2, wx.EXPAND, 5 )

        self.m_staticText13 = wx.StaticText( self.m_panel5, wx.ID_ANY, _(u"Filter wheel 1:"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText13.Wrap( -1 )

        fgSizer2.Add( self.m_staticText13, 1, wx.ALL, 5 )

        self.m_textCtrl8 = wx.TextCtrl( self.m_panel5, wx.ID_ANY, _(u"Filter 1"), wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer2.Add( self.m_textCtrl8, 1, wx.ALL, 5 )

        self.m_textCtrl9 = wx.TextCtrl( self.m_panel5, wx.ID_ANY, _(u"0"), wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer2.Add( self.m_textCtrl9, 1, wx.ALL, 5 )

        self.m_staticText14 = wx.StaticText( self.m_panel5, wx.ID_ANY, _(u"(0 to 20000)"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText14.Wrap( -1 )

        fgSizer2.Add( self.m_staticText14, 1, wx.ALL, 5 )

        self.m_staticText15 = wx.StaticText( self.m_panel5, wx.ID_ANY, _(u"Filter wheel 2:"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText15.Wrap( -1 )

        fgSizer2.Add( self.m_staticText15, 1, wx.ALL, 5 )

        self.m_textCtrl10 = wx.TextCtrl( self.m_panel5, wx.ID_ANY, _(u"Filter 2"), wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer2.Add( self.m_textCtrl10, 0, wx.ALL, 5 )

        self.m_textCtrl11 = wx.TextCtrl( self.m_panel5, wx.ID_ANY, _(u"0"), wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer2.Add( self.m_textCtrl11, 0, wx.ALL, 5 )

        self.m_staticText16 = wx.StaticText( self.m_panel5, wx.ID_ANY, _(u"(0 to 20000)"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText16.Wrap( -1 )

        fgSizer2.Add( self.m_staticText16, 0, wx.ALL, 5 )

        self.m_staticText17 = wx.StaticText( self.m_panel5, wx.ID_ANY, _(u"Filter wheel 3:"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText17.Wrap( -1 )

        fgSizer2.Add( self.m_staticText17, 0, wx.ALL, 5 )

        self.m_textCtrl12 = wx.TextCtrl( self.m_panel5, wx.ID_ANY, _(u"Filter 3"), wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer2.Add( self.m_textCtrl12, 0, wx.ALL, 5 )

        self.m_textCtrl13 = wx.TextCtrl( self.m_panel5, wx.ID_ANY, _(u"6666"), wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer2.Add( self.m_textCtrl13, 0, wx.ALL, 5 )

        self.m_staticText18 = wx.StaticText( self.m_panel5, wx.ID_ANY, _(u"(0 to 20000)"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText18.Wrap( -1 )

        fgSizer2.Add( self.m_staticText18, 0, wx.ALL, 5 )

        self.m_staticText19 = wx.StaticText( self.m_panel5, wx.ID_ANY, _(u"Filter wheel 4:"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText19.Wrap( -1 )

        fgSizer2.Add( self.m_staticText19, 0, wx.ALL, 5 )

        self.m_textCtrl14 = wx.TextCtrl( self.m_panel5, wx.ID_ANY, _(u"Filter 4"), wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer2.Add( self.m_textCtrl14, 0, wx.ALL, 5 )

        self.m_textCtrl15 = wx.TextCtrl( self.m_panel5, wx.ID_ANY, _(u"6666"), wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer2.Add( self.m_textCtrl15, 0, wx.ALL, 5 )

        self.m_staticText20 = wx.StaticText( self.m_panel5, wx.ID_ANY, _(u"(0 to 20000)"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText20.Wrap( -1 )

        fgSizer2.Add( self.m_staticText20, 0, wx.ALL, 5 )


        bSizer23.Add( fgSizer2, 1, wx.EXPAND, 5 )


        self.m_panel5.SetSizer( bSizer23 )
        self.m_panel5.Layout()
        bSizer23.Fit( self.m_panel5 )
        bSizer22.Add( self.m_panel5, 1, wx.EXPAND |wx.ALL, 0 )


        bSizer22.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_panel6 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_SUNKEN|wx.TAB_TRAVERSAL )
        bSizer24 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_button12 = wx.Button( self.m_panel6, wx.ID_ANY, _(u"Reset to Default"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer24.Add( self.m_button12, 0, wx.ALL, 5 )


        bSizer24.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_button13 = wx.Button( self.m_panel6, wx.ID_ANY, _(u"OK"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer24.Add( self.m_button13, 0, wx.ALL, 5 )

        self.m_button14 = wx.Button( self.m_panel6, wx.ID_ANY, _(u"Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer24.Add( self.m_button14, 0, wx.ALL, 5 )


        self.m_panel6.SetSizer( bSizer24 )
        self.m_panel6.Layout()
        bSizer24.Fit( self.m_panel6 )
        bSizer22.Add( self.m_panel6, 1, wx.EXPAND |wx.ALL, 3 )


        bSizer22.Add( ( 0, 0), 1, wx.EXPAND, 5 )


        self.SetSizer( bSizer22 )
        self.Layout()

        self.Centre( wx.BOTH )

    def __del__( self ):
        pass


###########################################################################
## Class SerialPortSetting
###########################################################################

class SerialPortSetting ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Serial Port Settings"), pos = wx.DefaultPosition, size = wx.Size( 416,218 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer25 = wx.BoxSizer( wx.VERTICAL )


        bSizer25.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        bSizer26 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText23 = wx.StaticText( self, wx.ID_ANY, _(u"Specify Timeout (seconds):"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText23.Wrap( -1 )

        bSizer26.Add( self.m_staticText23, 1, wx.ALL, 5 )

        self.m_textCtrl16 = wx.TextCtrl( self, wx.ID_ANY, _(u"0"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer26.Add( self.m_textCtrl16, 1, wx.ALL, 5 )


        bSizer25.Add( bSizer26, 1, wx.EXPAND, 5 )

        bSizer27 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText24 = wx.StaticText( self, wx.ID_ANY, _(u"Enter Block Size (bytes):"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText24.Wrap( -1 )

        bSizer27.Add( self.m_staticText24, 1, wx.ALL, 5 )

        self.m_textCtrl17 = wx.TextCtrl( self, wx.ID_ANY, _(u"1000"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer27.Add( self.m_textCtrl17, 1, wx.ALL, 5 )


        bSizer25.Add( bSizer27, 1, wx.EXPAND, 5 )


        bSizer25.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        bSizer28 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_button16 = wx.Button( self, wx.ID_ANY, _(u"Set to Default"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer28.Add( self.m_button16, 0, wx.ALL, 5 )


        bSizer28.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_button17 = wx.Button( self, wx.ID_ANY, _(u"OK"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer28.Add( self.m_button17, 0, wx.ALL, 5 )

        self.m_button18 = wx.Button( self, wx.ID_ANY, _(u"Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer28.Add( self.m_button18, 0, wx.ALL, 5 )


        bSizer25.Add( bSizer28, 1, wx.EXPAND, 5 )


        bSizer25.Add( ( 0, 0), 1, wx.EXPAND, 5 )


        self.SetSizer( bSizer25 )
        self.Layout()

        self.Centre( wx.BOTH )

    def __del__( self ):
        pass


###########################################################################
## Class MotorControlSetting
###########################################################################

class MotorControlSetting ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Motor Control Settings"), pos = wx.DefaultPosition, size = wx.Size( 463,306 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer29 = wx.BoxSizer( wx.VERTICAL )


        bSizer29.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_staticText25 = wx.StaticText( self, wx.ID_ANY, _(u"WARNING: DO NOT EDIT!!"), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.m_staticText25.Wrap( -1 )

        self.m_staticText25.SetFont( wx.Font( 12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Sans" ) )

        bSizer29.Add( self.m_staticText25, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND|wx.FIXED_MINSIZE, 5 )

        self.m_panel7 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_THEME|wx.TAB_TRAVERSAL )
        bSizer31 = wx.BoxSizer( wx.VERTICAL )

        fgSizer2 = wx.FlexGridSizer( 0, 3, 0, 0 )
        fgSizer2.SetFlexibleDirection( wx.BOTH )
        fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m_staticText26 = wx.StaticText( self.m_panel7, wx.ID_ANY, _(u"Enter Motor min Frequency (Hz):   "), wx.DefaultPosition, wx.DefaultSize, 0|wx.BORDER_SUNKEN )
        self.m_staticText26.Wrap( -1 )

        fgSizer2.Add( self.m_staticText26, 0, wx.ALL, 5 )

        self.m_textCtrl18 = wx.TextCtrl( self.m_panel7, wx.ID_ANY, _(u"2500"), wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer2.Add( self.m_textCtrl18, 0, wx.ALL, 5 )

        self.m_staticText27 = wx.StaticText( self.m_panel7, wx.ID_ANY, _(u"(50-2500 Hz)"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText27.Wrap( -1 )

        fgSizer2.Add( self.m_staticText27, 0, wx.ALL, 5 )

        self.m_staticText28 = wx.StaticText( self.m_panel7, wx.ID_ANY, _(u"Enter Motor max Frequency (Hz):   "), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText28.Wrap( -1 )

        fgSizer2.Add( self.m_staticText28, 0, wx.ALL, 5 )

        self.m_textCtrl19 = wx.TextCtrl( self.m_panel7, wx.ID_ANY, _(u"2500"), wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer2.Add( self.m_textCtrl19, 0, wx.ALL, 5 )

        self.m_staticText29 = wx.StaticText( self.m_panel7, wx.ID_ANY, _(u"(50-2500 Hz)"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText29.Wrap( -1 )

        fgSizer2.Add( self.m_staticText29, 0, wx.ALL, 5 )

        self.m_staticText30 = wx.StaticText( self.m_panel7, wx.ID_ANY, _(u"Specify Home Position:"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText30.Wrap( -1 )

        fgSizer2.Add( self.m_staticText30, 0, wx.ALL, 5 )

        self.m_textCtrl20 = wx.TextCtrl( self.m_panel7, wx.ID_ANY, _(u"0"), wx.DefaultPosition, wx.DefaultSize, wx.TE_NO_VSCROLL|wx.TE_PROCESS_ENTER )
        fgSizer2.Add( self.m_textCtrl20, 0, wx.ALL, 5 )

        self.m_staticText31 = wx.StaticText( self.m_panel7, wx.ID_ANY, _(u"(Future Use)"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText31.Wrap( -1 )

        fgSizer2.Add( self.m_staticText31, 0, wx.ALL, 5 )

        self.m_staticText32 = wx.StaticText( self.m_panel7, wx.ID_ANY, _(u"Enter Filter Wheel Gear Ratio:   "), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText32.Wrap( -1 )

        fgSizer2.Add( self.m_staticText32, 0, wx.ALL, 5 )

        self.m_textCtrl21 = wx.TextCtrl( self.m_panel7, wx.ID_ANY, _(u"5.2"), wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer2.Add( self.m_textCtrl21, 0, wx.ALL, 5 )


        bSizer31.Add( fgSizer2, 1, wx.EXPAND, 5 )


        self.m_panel7.SetSizer( bSizer31 )
        self.m_panel7.Layout()
        bSizer31.Fit( self.m_panel7 )
        bSizer29.Add( self.m_panel7, 1, wx.EXPAND |wx.ALL, 5 )

        self.m_panel8 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_THEME|wx.TAB_TRAVERSAL )
        bSizer30 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_button19 = wx.Button( self.m_panel8, wx.ID_ANY, _(u"Reset to Default"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer30.Add( self.m_button19, 0, wx.ALL, 5 )


        bSizer30.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_button20 = wx.Button( self.m_panel8, wx.ID_ANY, _(u"OK"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer30.Add( self.m_button20, 0, wx.ALL, 5 )

        self.m_button21 = wx.Button( self.m_panel8, wx.ID_ANY, _(u"Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer30.Add( self.m_button21, 0, wx.ALL, 5 )


        self.m_panel8.SetSizer( bSizer30 )
        self.m_panel8.Layout()
        bSizer30.Fit( self.m_panel8 )
        bSizer29.Add( self.m_panel8, 1, wx.EXPAND |wx.ALL, 5 )


        bSizer29.Add( ( 0, 0), 1, wx.EXPAND, 5 )


        self.SetSizer( bSizer29 )
        self.Layout()

        self.Centre( wx.BOTH )

    def __del__( self ):
        pass


