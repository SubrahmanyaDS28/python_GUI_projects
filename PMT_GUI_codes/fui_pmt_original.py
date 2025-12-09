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

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetFont( wx.Font( 10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_SLANT, wx.FONTWEIGHT_BOLD, False, "Sawasdee" ) )

        self.m_menubar1 = wx.MenuBar( 0 )
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

        bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer4 = wx.BoxSizer( wx.VERTICAL )

        self.m_notebook1 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_notebook1.SetBackgroundColour( wx.Colour( 213, 226, 251 ) )

        self.m_collapsiblePane1 = wx.CollapsiblePane( self.m_notebook1, wx.ID_ANY, _(u"Gate Counter Method"), wx.DefaultPosition, wx.DefaultSize, wx.CP_DEFAULT_STYLE )
        self.m_collapsiblePane1.Collapse( False )

        self.m_collapsiblePane1.SetBackgroundColour( wx.Colour( 182, 157, 157 ) )

        bSizer6 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel5 = wx.Panel( self.m_collapsiblePane1.GetPane(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.m_panel5.SetBackgroundColour( wx.Colour( 194, 184, 184 ) )

        bSizer24 = wx.BoxSizer( wx.VERTICAL )

        bSizer7 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText1 = wx.StaticText( self.m_panel5, wx.ID_ANY, _(u"MyLabel"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )

        bSizer7.Add( self.m_staticText1, 0, wx.ALL, 5 )

        self.m_textCtrl1 = wx.TextCtrl( self.m_panel5, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer7.Add( self.m_textCtrl1, 0, wx.ALL, 5 )

        self.m_staticText2 = wx.StaticText( self.m_panel5, wx.ID_ANY, _(u"MyLabel"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )

        bSizer7.Add( self.m_staticText2, 0, wx.ALL, 5 )


        bSizer24.Add( bSizer7, 0, wx.EXPAND, 5 )

        bSizer9 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText4 = wx.StaticText( self.m_panel5, wx.ID_ANY, _(u"MyLabel"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )

        bSizer9.Add( self.m_staticText4, 0, wx.ALL, 5 )

        m_comboBox1Choices = []
        self.m_comboBox1 = wx.ComboBox( self.m_panel5, wx.ID_ANY, _(u"Combo!"), wx.DefaultPosition, wx.DefaultSize, m_comboBox1Choices, 0 )
        bSizer9.Add( self.m_comboBox1, 0, wx.ALL, 5 )


        bSizer24.Add( bSizer9, 0, wx.EXPAND, 5 )

        bSizer8 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText3 = wx.StaticText( self.m_panel5, wx.ID_ANY, _(u"MyLabel"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )

        bSizer8.Add( self.m_staticText3, 0, wx.ALL, 5 )

        self.m_radioBtn1 = wx.RadioButton( self.m_panel5, wx.ID_ANY, _(u"RadioBtn"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer8.Add( self.m_radioBtn1, 0, wx.ALL, 5 )

        self.m_radioBtn2 = wx.RadioButton( self.m_panel5, wx.ID_ANY, _(u"RadioBtn"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer8.Add( self.m_radioBtn2, 0, wx.ALL, 5 )


        bSizer24.Add( bSizer8, 0, wx.EXPAND, 5 )


        self.m_panel5.SetSizer( bSizer24 )
        self.m_panel5.Layout()
        bSizer24.Fit( self.m_panel5 )
        bSizer6.Add( self.m_panel5, 1, wx.EXPAND |wx.ALL, 5 )


        self.m_collapsiblePane1.GetPane().SetSizer( bSizer6 )
        self.m_collapsiblePane1.GetPane().Layout()
        bSizer6.Fit( self.m_collapsiblePane1.GetPane() )
        self.m_notebook1.AddPage( self.m_collapsiblePane1, _(u"a page"), False )
        self.m_collapsiblePane2 = wx.CollapsiblePane( self.m_notebook1, wx.ID_ANY, _(u"Reciprocal Counter Method"), wx.DefaultPosition, wx.DefaultSize, wx.CP_DEFAULT_STYLE )
        self.m_collapsiblePane2.Collapse( False )

        self.m_collapsiblePane2.SetBackgroundColour( wx.Colour( 223, 217, 187 ) )

        bSizer10 = wx.BoxSizer( wx.VERTICAL )

        bSizer61 = wx.BoxSizer( wx.VERTICAL )


        bSizer10.Add( bSizer61, 1, wx.EXPAND, 5 )

        self.m_panel6 = wx.Panel( self.m_collapsiblePane2.GetPane(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.m_panel6.SetBackgroundColour( wx.Colour( 218, 207, 187 ) )

        bSizer27 = wx.BoxSizer( wx.VERTICAL )

        bSizer71 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText11 = wx.StaticText( self.m_panel6, wx.ID_ANY, _(u"MyLabel"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText11.Wrap( -1 )

        bSizer71.Add( self.m_staticText11, 0, wx.ALL, 5 )

        self.m_textCtrl11 = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer71.Add( self.m_textCtrl11, 0, wx.ALL, 5 )

        self.m_staticText21 = wx.StaticText( self.m_panel6, wx.ID_ANY, _(u"MyLabel"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText21.Wrap( -1 )

        bSizer71.Add( self.m_staticText21, 0, wx.ALL, 5 )


        bSizer27.Add( bSizer71, 0, wx.EXPAND, 5 )

        bSizer81 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText31 = wx.StaticText( self.m_panel6, wx.ID_ANY, _(u"MyLabel"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText31.Wrap( -1 )

        bSizer81.Add( self.m_staticText31, 0, wx.ALL, 5 )

        self.m_radioBtn11 = wx.RadioButton( self.m_panel6, wx.ID_ANY, _(u"RadioBtn"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer81.Add( self.m_radioBtn11, 0, wx.ALL, 5 )

        self.m_radioBtn21 = wx.RadioButton( self.m_panel6, wx.ID_ANY, _(u"RadioBtn"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer81.Add( self.m_radioBtn21, 0, wx.ALL, 5 )


        bSizer27.Add( bSizer81, 0, wx.EXPAND, 5 )

        bSizer91 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText41 = wx.StaticText( self.m_panel6, wx.ID_ANY, _(u"MyLabel"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText41.Wrap( -1 )

        bSizer91.Add( self.m_staticText41, 0, wx.ALL, 5 )

        m_comboBox11Choices = []
        self.m_comboBox11 = wx.ComboBox( self.m_panel6, wx.ID_ANY, _(u"Combo!"), wx.DefaultPosition, wx.DefaultSize, m_comboBox11Choices, 0 )
        bSizer91.Add( self.m_comboBox11, 0, wx.ALL, 5 )


        bSizer27.Add( bSizer91, 0, wx.EXPAND, 5 )


        self.m_panel6.SetSizer( bSizer27 )
        self.m_panel6.Layout()
        bSizer27.Fit( self.m_panel6 )
        bSizer10.Add( self.m_panel6, 1, wx.EXPAND |wx.ALL, 5 )


        self.m_collapsiblePane2.GetPane().SetSizer( bSizer10 )
        self.m_collapsiblePane2.GetPane().Layout()
        bSizer10.Fit( self.m_collapsiblePane2.GetPane() )
        self.m_notebook1.AddPage( self.m_collapsiblePane2, _(u"a page"), True )

        bSizer4.Add( self.m_notebook1, 1, wx.EXPAND |wx.ALL, 5 )

        bSizer16 = wx.BoxSizer( wx.HORIZONTAL )


        bSizer16.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_button1 = wx.Button( self, wx.ID_ANY, _(u"OK"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer16.Add( self.m_button1, 0, wx.ALL, 5 )

        self.m_button2 = wx.Button( self, wx.ID_ANY, _(u"Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer16.Add( self.m_button2, 0, wx.ALL, 5 )


        bSizer4.Add( bSizer16, 0, wx.EXPAND, 5 )


        bSizer2.Add( bSizer4, 1, wx.EXPAND, 5 )

        bSizer5 = wx.BoxSizer( wx.VERTICAL )

        bSizer14 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.m_panel1.SetBackgroundColour( wx.Colour( 234, 202, 202 ) )

        bSizer14.Add( self.m_panel1, 1, wx.EXPAND |wx.ALL, 5 )


        bSizer5.Add( bSizer14, 1, wx.EXPAND, 5 )

        bSizer15 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.m_panel2.SetBackgroundColour( wx.Colour( 208, 200, 200 ) )

        bSizer15.Add( self.m_panel2, 1, wx.EXPAND |wx.ALL, 5 )


        bSizer5.Add( bSizer15, 1, wx.EXPAND, 5 )

        bSizer17 = wx.BoxSizer( wx.HORIZONTAL )


        bSizer17.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_button3 = wx.Button( self, wx.ID_ANY, _(u"Start Plot"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer17.Add( self.m_button3, 0, wx.ALL, 5 )


        bSizer17.Add( ( 0, 0), 1, wx.EXPAND, 5 )


        bSizer5.Add( bSizer17, 0, wx.EXPAND, 5 )


        bSizer2.Add( bSizer5, 3, wx.EXPAND, 5 )


        bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )

        bSizer28 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText13 = wx.StaticText( self, wx.ID_ANY, _(u"MyLabel"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText13.Wrap( -1 )

        bSizer28.Add( self.m_staticText13, 0, wx.ALL, 5 )


        bSizer1.Add( bSizer28, 0, wx.EXPAND, 5 )


        self.SetSizer( bSizer1 )
        self.Layout()

        self.Centre( wx.BOTH )

    def __del__( self ):
        pass




class MainApp(wx.App):
    def OnInit(self):
        frame = MainFrame(None)
        frame.Show()
        return True


if __name__ == "__main__":
    app = MainApp()
    app.MainLoop()
