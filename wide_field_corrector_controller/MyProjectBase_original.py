# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

import MyProjectBase
import gettext
_ = gettext.gettext

class MainApp(wx.App):
    def OnInit(self):
        frame = MyProjectBase.MainFrame(None)
        frame1 = MyProjectBase.FilterWheelSetting(None)
        frame2 = MyProjectBase.SerialPortSetting(None)
        frame3 = MyProjectBase.MotorControlSetting(None)
        frame.Show()
        # frame1.Show()
        # frame2.Show()
        # frame3.Show()
        return True


if __name__ == "__main__":
    app = MainApp()
    app.MainLoop()
