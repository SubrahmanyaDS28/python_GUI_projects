import wx
import numpy as np
from vispy import scene
from vispy.scene import visuals
from MyProjectBase import MainFrame   # replace "gui" with the file name where your generated MainFrame is stored


class VispyEmbed:
    """Embed VisPy SceneCanvas inside a wx.Panel"""
    def __init__(self, parent_panel):
        # Create SceneCanvas
        self.canvas = scene.SceneCanvas(
            keys=None, show=True, bgcolor="black", size=(400, 400)
        )
        # Get wx native widget
        self.widget = self.canvas.native
        self.widget.Reparent(parent_panel)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.widget, 1, wx.EXPAND)
        parent_panel.SetSizer(sizer)
        parent_panel.Layout()

        # Setup 2D view
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = "panzoom"

        # Add point
        self.point = visuals.Markers()
        self.view.add(self.point)

        self.pos = np.array([0.0, 0.0])
        self.update_point()

    def update_point(self):
        data = np.array([self.pos], dtype=float)  # shape (1,2)
        self.point.set_data(data, face_color="red", size=15, edge_width=0.5)
        self.canvas.update()

    def move(self, dx=0, dy=0):
        self.pos[0] += dx
        self.pos[1] += dy
        self.update_point()


class MyApp(MainFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Embed VisPy into m_panel2 (XY Stage Position)
        self.vispy = VispyEmbed(self.m_panel2)

        # Bind direction buttons
        self.m_button4.Bind(wx.EVT_BUTTON, self.on_north)  # North
        self.m_button7.Bind(wx.EVT_BUTTON, self.on_south)  # South
        self.m_button6.Bind(wx.EVT_BUTTON, self.on_east)   # East
        self.m_button5.Bind(wx.EVT_BUTTON, self.on_west)   # West

    # ---- movement callbacks ----
    def on_north(self, event):
        step = self.get_step(self.m_textCtrl22)
        self.vispy.move(0, step)

    def on_south(self, event):
        step = self.get_step(self.m_textCtrl25)
        self.vispy.move(0, -step)

    def on_east(self, event):
        step = self.get_step(self.m_textCtrl24)
        self.vispy.move(step, 0)

    def on_west(self, event):
        step = self.get_step(self.m_textCtrl23)
        self.vispy.move(-step, 0)

    def get_step(self, ctrl):
        try:
            return float(ctrl.GetValue())
        except ValueError:
            return 0.0


if __name__ == "__main__":
    app = wx.App(False)
    frame = MyApp(None)
    frame.Show()
    app.MainLoop()
