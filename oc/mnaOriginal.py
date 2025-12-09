import wx
import mna  # this is your wxFormBuilder file (rename as needed)


class MyFrame(mna.frameMain):  # subclass
    def __init__(self, parent):
        super().__init__(parent)

        # Example: connect button or toggle events
        self.m_toggleBtn3.Bind(wx.EVT_TOGGLEBUTTON, self.on_toggle_rasle)

    # Override menu event handler
    def menuItemFileOnMenuSelection(self, event):
        wx.MessageBox("New File clicked!", "Info")

    def on_toggle_rasle(self, event):
        if self.m_toggleBtn3.GetValue():
            self.m_textCtrl1.SetValue("RASLE ON")
        else:
            self.m_textCtrl1.SetValue("RASLE OFF")


class MainApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None)
        frame.Show()
        return True


if __name__ == "__main__":
    app = MainApp()
    app.MainLoop()
