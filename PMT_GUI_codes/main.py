#!/usr/bin/env python3
# main.py — connects gui_pmt.py to backend functionality (serial, plotting, logging)

import wx
import threading
import time
import os
import csv
import datetime
import serial
import serial.tools.list_ports

import matplotlib
matplotlib.use("WXAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

from collections import deque
import time, os

import gui_pmt  # your wxFormBuilder generated file (you renamed pmt_gui -> gui_pmt)


class PMTMainFrame(gui_pmt.MainFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # === Set Application Icon ===
        icon_path = os.path.join(os.path.dirname(__file__), "logo1.png")
        if os.path.exists(icon_path):
            icon = wx.Icon(icon_path, wx.BITMAP_TYPE_PNG)
            self.SetIcon(icon)
        else:
            print("Warning: logo.png not found")
            
            
        self.current_gate_value = 1
        self.m_textCtrl1.SetValue("1")
        # ---- Status / runtime fields ----
        self.CreateStatusBar(2)
        self.SetStatusText("Ready", 0)
        self.SetStatusText("", 1)

        # serial / logging / plotting state
        self.ser = None
        self.port_name = "/dev/ttyUSB0"
        self.baudrate = 115200
        self.running = False
        self.read_thread = None
        self.read_thread_exit = threading.Event()

        self.log_folder = None
        self.log_file = None
        self.log_writer = None

        # data buffers
        self.x_data = []
        self.y_data = []
        self.start_time = None

        # ---------------- Recent window control (SpinCtrl) ---------------- #
        if hasattr(self, "m_spinCtrl2"):
            self.m_spinCtrl2.SetRange(5, 300)
            self.m_spinCtrl2.SetValue(20)
            self.recent_window = self.m_spinCtrl2.GetValue()
            self.m_spinCtrl2.Bind(wx.EVT_SPINCTRL, self.on_recent_window_change)
        else:
            self.recent_window = 20

        # ---------------- Matplotlib figures ---------------- #
        self.fig1 = Figure(figsize=(6, 3))
        self.ax1 = self.fig1.add_subplot(111)
        self.canvas1 = FigureCanvas(self.m_panel1, -1, self.fig1)

        self.fig2 = Figure(figsize=(6, 2.5))
        self.ax2 = self.fig2.add_subplot(111)
        self.canvas2 = FigureCanvas(self.m_panel2, -1, self.fig2)

        # Match panel backgrounds
        for fig, ax, panel in [(self.fig1, self.ax1, self.m_panel1),
                               (self.fig2, self.ax2, self.m_panel2)]:
            bg = panel.GetBackgroundColour()
            rgb = tuple(c / 255.0 for c in bg.Get(includeAlpha=False))
            fig.patch.set_facecolor(rgb)
            ax.set_facecolor(rgb)

        # Attach canvases to panel sizers
        for canvas, panel in [(self.canvas1, self.m_panel1),
                              (self.canvas2, self.m_panel2)]:
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(canvas, 1, wx.EXPAND)
            panel.SetSizer(sizer)
            panel.Layout()

        # ---------------- Cursor coordinate display ---------------- #
        self.m_staticText_coords = wx.StaticText(self, wx.ID_ANY, "Cursor: (0.00, 0.00)")
        top_sizer = self.GetSizer()  # get top-level sizer from wxFormBuilder
        if top_sizer:
            top_sizer.Add(self.m_staticText_coords, 0, wx.ALL | wx.EXPAND, 5)
            self.Layout()

        # Connect cursor motion event to display coordinates
        self.canvas1.mpl_connect("motion_notify_event", self.on_plot_hover)
        self.canvas2.mpl_connect("motion_notify_event", self.on_plot_hover)

        # ---------------- Timer for GUI updates ---------------- #
        self.gui_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.gui_timer)

        # ---------------- COM / Log / About menu ---------------- #
        id_com_settings = wx.NewIdRef()
        id_log_folder = wx.NewIdRef()
        id_about = wx.NewIdRef()

        try:
            self.m_menu3.Append(id_com_settings, "Open COM Settings...")
            self.Bind(wx.EVT_MENU, self.on_open_com_settings, id=id_com_settings)
        except Exception:
            pass

        try:
            self.m_menu4.Append(id_log_folder, "Set Log Folder...")
            self.Bind(wx.EVT_MENU, self.on_set_log_folder, id=id_log_folder)
        except Exception:
            pass

        try:
            self.m_menu6.Append(id_about, "About")
            self.Bind(wx.EVT_MENU, self.on_about, id=id_about)
        except Exception:
            pass

        # ---------------- Start Plot button ---------------- #
        if hasattr(self, "m_button3"):
            self.m_button3.Bind(wx.EVT_BUTTON, self.on_start_stop_clicked)

        # ---------------- Initial plots ---------------- #
        self.draw_initial_plots()

        # ---------------- COM port refresh timer ---------------- #
        self.port_refresh_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self._on_refresh_ports_timer, self.port_refresh_timer)
        self.port_refresh_timer.Start(3000)

        # --- Hook up SpinCtrl from wxFormBuilder ---
        if hasattr(self, "m_spinCtrl2"):  # replace m_spinCtrl1 with your real name
            self.m_spinCtrl2.SetRange(5, 300)  # seconds range
            self.m_spinCtrl2.SetValue(20)  # default 20s
            self.recent_window = self.m_spinCtrl2.GetValue()
            self.m_spinCtrl2.Bind(wx.EVT_SPINCTRL, self.on_recent_window_change)

        self.m_button1.Bind(wx.EVT_BUTTON, self.on_ok_clicked)
        self.m_button2.Bind(wx.EVT_BUTTON, self.on_cancel_clicked)

    def on_recent_window_change(self, event):
        self.recent_window = self.m_spinCtrl2.GetValue()
        self.SetStatusText(f"Recent window set to {self.recent_window}s", 0)

    # ---------- Menus / dialogs ----------
    def on_open_com_settings(self, event):
        """
        Show the generated MyDialog1 which contains:
         - m_comboBox4 -> COM Ports
         - m_comboBox5 -> BaudRate
         - m_button6 (OK) and m_button7 (Cancel)
        We will populate the combo boxes, bind OK/Cancel, and run the dialog.
        """
        dlg = gui_pmt.MyDialog1(self)

        # Populate COM ports list
        ports = [p.device for p in serial.tools.list_ports.comports()]
        try:
            dlg.m_comboBox4.Clear()
            for p in ports:
                dlg.m_comboBox4.Append(p)
            if ports:
                dlg.m_comboBox4.SetValue(str(self.port_name))
                # dlg.m_comboBox4.SetValue(ports[0])

        except Exception:
            # If the generated names differ, skip gracefully
            pass

        # Populate common baud rates
        baud_list = ["9600", "19200", "38400", "57600", "115200", "230400", "460800", "921600"]
        try:
            dlg.m_comboBox5.Clear()
            for b in baud_list:
                dlg.m_comboBox5.Append(b)
            dlg.m_comboBox5.SetValue(str(self.baudrate))
        except Exception:
            pass


        # Bind OK and Cancel buttons to close the modal with our IDs
        def on_ok(evt):
            # read selections and apply
            try:
                selected_port = dlg.m_comboBox4.GetValue()
                selected_baud = int(dlg.m_comboBox5.GetValue())
            except Exception:
                wx.MessageBox("Please choose a valid COM port and baud rate.", "COM Settings", wx.OK | wx.ICON_WARNING)
                return
            # try to open serial right away (close existing first)
            if self.ser and self.ser.is_open:
                try:
                    self.ser.close()
                except Exception:
                    pass
            try:
                self.ser = serial.Serial(selected_port, selected_baud, timeout=0.2)
                self.port_name = selected_port
                self.baudrate = selected_baud
                self.SetStatusText(f"Connected: {self.port_name} @ {self.baudrate}", 0)
                dlg.EndModal(wx.ID_OK)
            except Exception as e:
                wx.MessageBox(f"Failed to open serial port:\n{e}", "Serial Error", wx.OK | wx.ICON_ERROR)

        def on_cancel(evt):
            dlg.EndModal(wx.ID_CANCEL)

        # Bind buttons (they are plain buttons in generated dialog)
        try:
            dlg.m_button6.Bind(wx.EVT_BUTTON, on_ok)
            dlg.m_button7.Bind(wx.EVT_BUTTON, on_cancel)
        except Exception:
            # If names differ or missing, fallback to default OK/Cancel behavior
            pass

        dlg.CenterOnParent()
        dlg.ShowModal()
        dlg.Destroy()
    
    def on_ok_clicked(self, event):
        # Detect which page is active: 0 = Gate, 1 = Reciprocal
        page_index = self.m_notebook1.GetSelection()
        
        if page_index == 0:  # Gate page
            value = self.m_textCtrl1.GetValue().strip()
            
            if not value.isdigit():
                wx.MessageBox("Please enter a number between 1 and 1000", "Error", wx.OK | wx.ICON_ERROR)
                return
            
            number = int(value)
            if number < 1 or number > 1000:
                wx.MessageBox("Value must be between 1 and 1000", "Error", wx.OK | wx.ICON_ERROR)
                return
            
            # Store the gate value for use in the background thread's data validation
            self.current_gate_value = number
            
            msg = f"*G{number}#\n"
            # msg = f"*G#\n"
        
        else:  # Reciprocal page
            # msg = "R\n"
            msg = "*R#\n"
            
            # The reciprocal mode does not use a gate value,
            # but we keep self.current_gate_value set to the last used gate
            # (which should be 1 if 'Start Plot' was clicked first)
            # or you might reset it to a default like 1 if needed.
            # self.current_gate_value = 1 # Optional reset for reciprocal mode
        
        # Send over serial
        if self.ser and self.ser.is_open:
            self.ser.write(msg.encode("utf-8"))
            print("Sent:", msg)
            
            # Disable page switching + grey out OK button
            self.m_notebook1.Enable(False)
            self.m_button1.Enable(False)  # OK button disabled
        else:
            wx.MessageBox("Serial port not open", "Error", wx.OK | wx.ICON_ERROR)

    def on_cancel_clicked(self, event):
        if self.ser and self.ser.is_open:
            stop_msg = "STOP\n"
            self.ser.write(stop_msg.encode("utf-8"))
            print("Sent:", stop_msg)

        # Re-enable page switching + OK button
        self.m_notebook1.Enable(True)
        self.m_button1.Enable(True)

    def on_set_log_folder(self, event):
        dd = wx.DirDialog(self, "Select folder to save CSV logs", style=wx.DD_DEFAULT_STYLE)
        if dd.ShowModal() == wx.ID_OK:
            self.log_folder = dd.GetPath()
            self.SetStatusText(f"Log folder: {self.log_folder}", 1)
        dd.Destroy()

    def on_about(self, event):
        wx.MessageBox("PMT GUI\nwxPython front-end\nDeveloped by DSS IIA", "About", wx.OK | wx.ICON_INFORMATION)

    # ---------- Plot helpers ----------
    def draw_initial_plots(self):
        # placeholder initial plots
        self.ax1.clear()
        self.ax1.set_title("Real-Time PMT Signal (Recent)")
        self.ax1.set_xlabel("Samples")
        self.ax1.set_ylabel("Counts")
        self.ax1.grid(True)
        self.canvas1.draw()

        self.ax2.clear()
        self.ax2.set_title("Full Signal History")
        self.ax2.set_xlabel("Samples")
        self.ax2.set_ylabel("Counts")
        self.ax2.grid(True)
        self.canvas2.draw()

    # ---------- Start/Stop handling ----------
    def on_start_stop_clicked(self, evt):
        if not self.running:
            # start reading & plotting
            if not (self.ser and self.ser.is_open):
                # Try to automatically open last-known serial if possible
                if self.port_name:
                    try:
                        self.ser = serial.Serial(self.port_name, self.baudrate, timeout=0.2)
                    except Exception as e:
                        wx.MessageBox(f"Cannot open serial port {self.port_name}:\n{e}", "Serial Error", wx.OK | wx.ICON_ERROR)
                        return
                else:
                    wx.MessageBox("No serial port open. Use COM Port Settings to open one.", "Serial", wx.OK | wx.ICON_WARNING)
                    return

            # set up logging if folder chosen
            if self.log_folder:
                # create/open file for today's date + method
                method = "PMT"
                date_str = datetime.datetime.now().strftime("%Y%m%d")
                fname = f"{date_str}_{method}.csv"
                fpath = os.path.join(self.log_folder, fname)
                new_file = not os.path.exists(fpath)
                try:
                    self.log_file = open(fpath, "a", newline="")
                    self.log_writer = csv.writer(self.log_file)
                    if new_file:
                        self.log_writer.writerow(["# PMT Counter Log"])
                        self.log_writer.writerow([f"# Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"])
                        self.log_writer.writerow([f"# Method: {method}"])
                        self.log_writer.writerow([f"# COM Port: {self.port_name}"])
                        self.log_writer.writerow([f"# Baud Rate: {self.baudrate}"])
                        self.log_writer.writerow([])
                    # run-specific header
                    self.log_writer.writerow([f"# New Run Started at {datetime.datetime.now().strftime('%H:%M:%S')}"])
                    self.log_writer.writerow(["Time (s)", "Counts"])
                    self.log_file.flush()
                    self.SetStatusText(f"Logging to {fpath}", 1)
                except Exception as e:
                    wx.MessageBox(f"Cannot open log file:\n{e}", "Log Error", wx.OK | wx.ICON_ERROR)
                    self.log_file = None
                    self.log_writer = None

            # reset data
            self.x_data = []
            self.y_data = []
            self.start_time = time.time()
            self.read_thread_exit.clear()
            self.running = True
            self.read_thread = threading.Thread(target=self._read_serial_loop, daemon=True)
            self.read_thread.start()

            # start GUI timer (update plots every 700 ms)
            self.gui_timer.Start(700)
            self.m_button3.SetLabel("Stop Plot")
            self.SetStatusText("Running...", 0)
        else:
            # stop reading
            self._stop_running()

    def _stop_running(self):
        self.running = False
        self.read_thread_exit.set()
        if self.read_thread and self.read_thread.is_alive():
            self.read_thread.join(timeout=1.0)
        self.gui_timer.Stop()
        self.m_button3.SetLabel("Start Plot")
        # close log file if open
        if self.log_file:
            try:
                self.log_writer.writerow([f"# Run Ended at {datetime.datetime.now().strftime('%H:%M:%S')}"])
                self.log_writer.writerow([])
                self.log_file.flush()
                self.log_file.close()
            except Exception:
                pass
            self.log_file = None
            self.log_writer = None
        self.SetStatusText("Stopped", 0)


    # def error_correction(self, i: int) -> int:
    #     if i < 50:
    #         return i + 2
    #     elif i < 100:
    #         return i + 3
    #     elif i < 150:
    #         return i + 4
    #     elif i < 200:
    #         return i + 5
    #     elif i < 300:
    #         return i + 7
    #     else:
    #         return i


    def _read_serial_loop(self):
        """
        Continuously read from serial and append values to buffers.
        Handles:
          - ASCII newline-terminated integers (for manual send/debug)
          - Raw 4-byte little-endian unsigned ints (DMA stream)
        """

        buffer = bytearray()

        # ensure time base
        if self.start_time is None:
            self.start_time = time.time()

        while not self.read_thread_exit.is_set() and self.ser and self.ser.is_open:
            try:
                # read whatever is available
                data = self.ser.read(self.ser.in_waiting or 1)
                if data:
                    buffer.extend(data)

                    # --- Try ASCII lines first ---
                    if b"\n" in buffer:
                        line, _, rest = buffer.partition(b"\n")
                        buffer = bytearray(rest)

                        try:
                            s = line.decode("ascii", errors="ignore").strip()
                            if s.isdigit():
                                val = int(s)
                            else:
                                val = int(float(s))  # handle "123.4"
                        except Exception:
                            val = None

                        if val is not None:
                            t = time.time() - self.start_time
                            self.x_data.append(t)
                            self.y_data.append(val)

                            if self.log_writer:
                                self.log_writer.writerow([f"{t:.3f}", val])
                                if len(self.y_data) % 50 == 0:
                                    self.log_file.flush()
                            continue  # handled ASCII, skip binary parse

                    # --- If not ASCII, parse binary in 4-byte chunks ---
                    while len(buffer) >= 4:
                        value = int.from_bytes(buffer[:4], "little", signed=False)

                        # sanity check: adjust range for your expected data
                        if 0 <= value <= 300 * self.current_gate_value:
                            # val = self.error_correction(value)
                            val = value
                            buffer = buffer[4:]

                        else:
                            # misaligned, drop one byte and retry
                            buffer = buffer[1:]
                            continue

                        # Append data with timestamp
                        t = time.time() - self.start_time
                        self.x_data.append(t)
                        self.y_data.append(val)

                        if self.log_writer:
                            self.log_writer.writerow([f"{t:.3f}", val])
                            if len(self.y_data) % 50 == 0:
                                self.log_file.flush()

                    # # --- keep only last N points ---
                    # if len(self.x_data) > 5000:
                    #     self.x_data = self.x_data[-5000:]
                    #     self.y_data = self.y_data[-5000:]
                    max_points = 2000
                    total_points = len(self.x_data)
                    if total_points > max_points:
                        step = max(1, total_points // max_points)
                        xs_full = self.x_data[::step]
                        ys_full = self.y_data[::step]
                    else:
                        xs_full = self.x_data
                        ys_full = self.y_data


                else:
                    time.sleep(0.0001)

            except Exception as e:
                # prevent thread crash
                time.sleep(0.01)
                continue

    # ---------- GUI timer handler ----------
    def on_timer(self, event):
        """
        Update two plots:
          - ax1: recent window (last self.recent_window seconds or m_spinCtrl2 value)
          - ax2: full history since start
        """
        # nothing to do if no data
        if not getattr(self, "x_data", None) or not getattr(self, "y_data", None):
            return

        # recent window length from spin control, fallback 20s
        recent_window = self.m_spinCtrl2.GetValue() if hasattr(self, "m_spinCtrl2") else 20.0

        # last timestamp available
        last_time = self.x_data[-1]

        # threshold time for the recent window
        threshold = last_time - recent_window

        # find first index >= threshold
        start_idx = 0
        for i, t in enumerate(self.x_data):
            if t >= threshold:
                start_idx = i
                break

        # slice recent data
        xs_recent = self.x_data[start_idx:]
        ys_recent = self.y_data[start_idx:]

        # fallback if slicing produced no points
        if not xs_recent:
            fallback_N = min(100, len(self.x_data))
            xs_recent = self.x_data[-fallback_N:]
            ys_recent = self.y_data[-fallback_N:]
            threshold = xs_recent[0] if xs_recent else last_time - recent_window

        # ---- Recent plot (ax1) ----
        self.ax1.clear()
        self.ax1.plot(xs_recent, ys_recent, linewidth=1)
        self.ax1.set_title(f"Recent ({recent_window:.0f} s)")
        self.ax1.set_xlabel("Time (s)")
        self.ax1.set_ylabel("Counts")
        self.ax1.grid(True)

        # x-limits follow actual time (e.g. 30→50 if last_time=50 and window=20)
        if xs_recent:
            self.ax1.set_xlim(xs_recent[0], xs_recent[-1])

        # autoscale y a bit
        if ys_recent:
            y_min = min(ys_recent)
            y_max = max(ys_recent)
            if y_min == y_max:
                self.ax1.set_ylim(y_min - 1, y_max + 1)
            else:
                pad = 0.08 * (y_max - y_min)
                self.ax1.set_ylim(y_min - pad, y_max + pad)

        self.canvas1.draw()

        # ---- Full history plot (ax2) ----
        self.ax2.clear()
        max_points = 2000
        total_points = len(self.x_data)
        if total_points > max_points:
            step = max(1, total_points // max_points)
            xs_full = self.x_data[::step]
            ys_full = self.y_data[::step]
        else:
            xs_full = self.x_data
            ys_full = self.y_data

        self.ax2.plot(xs_full, ys_full, linewidth=0.7)
        self.ax2.set_title("Full Signal History")
        self.ax2.set_xlabel("Time (s) (since start)")
        self.ax2.set_ylabel("Counts")
        self.ax2.grid(True)

        # autoscale x for full history (start at 0, end at last point)
        if xs_full:
            self.ax2.set_xlim(0, xs_full[-1])

        # autoscale y
        if ys_full:
            y_min = min(ys_full)
            y_max = max(ys_full)
            if y_min == y_max:
                self.ax2.set_ylim(y_min - 1, y_max + 1)
            else:
                pad = 0.08 * (y_max - y_min)
                self.ax2.set_ylim(y_min - pad, y_max + pad)

        self.canvas2.draw()

        # ---- Status update ----
        elapsed = int(last_time) if last_time is not None else 0
        last_val = self.y_data[-1] if self.y_data else 0
        self.SetStatusText(f"Port: {self.port_name or 'None'} | Baud: {self.baudrate}", 0)
        self.SetStatusText(f"Run: {elapsed}s | Last: {last_val}", 1)

        # ---- Status update ----
        # elapsed = int(last_time) if last_time is not None else 0
        # last_val = self.y_data[-1] if self.y_data else 0
        # last_x = self.x_data[-1] if self.x_data else 0

        # self.SetStatusText(f"Port: {self.port_name or 'None'} | Baud: {self.baudrate}", 0)
        # self.SetStatusText(f"Run: {elapsed}s | Last: {last_val} | Last Coord: ({last_x:.2f}, {last_val})", 1)

    # ---------- periodic COM refresh (non-blocking) ----------
    def _on_refresh_ports_timer(self, event):
        # If COM dialog open this could update the dialog; here we just keep the menu working
        # No heavy work — just a quick check to ensure device presence isn't stale
        pass

    # ---------- cleanup ----------
    def Close(self, *args, **kwargs):
        # safe cleanup on window close
        try:
            self._stop_running()
        except Exception:
            pass
        try:
            if self.ser and self.ser.is_open:
                self.ser.close()
        except Exception:
            pass
        super().Close(*args, **kwargs)

    # def on_mouse_move(self, event):
    #     """
    #     Update coordinates label when mouse moves over ax2 plot.
    #     """
    #     if event.inaxes:  # only if mouse is over the plot
    #         x, y = event.xdata, event.ydata
    #         self.m_staticText_coords.SetLabel(f"Cursor: ({x:.2f}, {y:.2f})")
    #     else:
    #         self.m_staticText_coords.SetLabel("Cursor: (---, ---)")

    def on_plot_hover(self, event):
        """
        Called when the mouse moves over either plot.
        Updates the static text with (x, y) coordinates.
        """
        if event.inaxes and event.xdata is not None and event.ydata is not None:
            self.m_staticText_coords.SetLabel(f"Cursor: ({event.xdata:.2f}, {event.ydata:.2f})")

def main():
    app = wx.App(False)
    frame = PMTMainFrame(None)
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()
