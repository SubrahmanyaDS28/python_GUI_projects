import wx
import wx.lib.gizmos as gizmos
import os
import Keysight_MSOX3054A_MSO_Controller_GUI
# from wx.lib.agw.shapedbutton import SBitmapToggleButton
import csv
import datetime
import time
import sys
import os

from MSOX3054A_OSC import MSOX3054A_OSC

bitmapDir = "./images"
MSOX3054A_RESOURCE_STRING = 'USB0::0x0957::0x17A2::MY53100120::0::INSTR'


class Keysight_MSOX3054A_WaveGen_Controller(Keysight_MSOX3054A_MSO_Controller_GUI.frame_Main):
	""" Sub Class the GUI created with wxFormBuilder and extend the functionality """
	
	def __init__(self, parent):
		Keysight_MSOX3054A_MSO_Controller_GUI.frame_Main.__init__(self, parent)
		
		def resource_path(relative_path):
			try:
				# PyInstaller creates a temp folder and stores path in _MEIPASS
				base_path = sys._MEIPASS
			except Exception:
				base_path = os.path.abspath(".")
			return os.path.join(base_path, relative_path)
		
		try:
			# Use the helper function to get the correct path
			image_path = resource_path("logo.png")
			
			if os.path.exists(image_path):
				icon_image = wx.Image(image_path, wx.BITMAP_TYPE_ANY)
				icon = wx.Icon()
				icon.CopyFromBitmap(wx.Bitmap(icon_image))
				self.SetIcon(icon)
		except Exception as e:
			print(f"Error loading icon: {e}")
		
		self.scope_driver = None
		self.locale = wx.Locale(wx.LANGUAGE_ENGLISH)
		
		# # LED Setup
		# self.led_Display = gizmos.LEDNumberCtrl(self.panel_LED, -1)
		# self.led_Display.SetValue("000.000")
		# self.led_Display.SetAlignment(gizmos.LED_ALIGN_RIGHT)
		# self.led_Display.SetDrawFaded(True)
		# self.led_Display.SetForegroundColour('green')
		# sizer101 = wx.BoxSizer(wx.VERTICAL)
		# sizer101.Add(self.led_Display, 1, wx.EXPAND)
		# self.panel_LED.SetSizer(sizer101)
		# self.panel_LED.Fit()
		
		# LED Setup
		self.led_Display1 = gizmos.LEDNumberCtrl(self.panel_counts, -1)
		self.led_Display1.SetValue("0000.00")
		self.led_Display1.SetAlignment(gizmos.LED_ALIGN_RIGHT)
		self.led_Display1.SetDrawFaded(True)
		self.led_Display1.SetForegroundColour('red')
		sizer11 = wx.BoxSizer(wx.VERTICAL)
		sizer11.Add(self.led_Display1, 1, wx.EXPAND)
		self.panel_counts.SetSizer(sizer11)
		self.panel_counts.Fit()
		
		# LED Setup
		self.led_Display2 = gizmos.LEDNumberCtrl(self.panel_rms, -1)
		self.led_Display2.SetValue("0000.00")
		self.led_Display2.SetAlignment(gizmos.LED_ALIGN_RIGHT)
		self.led_Display2.SetDrawFaded(True)
		self.led_Display2.SetForegroundColour('green')
		sizer121 = wx.BoxSizer(wx.VERTICAL)
		sizer121.Add(self.led_Display2, 1, wx.EXPAND)
		self.panel_rms.SetSizer(sizer121)
		self.panel_rms.Fit()
		
		# LED Setup
		self.led_Display3 = gizmos.LEDNumberCtrl(self.panel_NtoE, -1)
		self.led_Display3.SetValue("0000.00")
		self.led_Display3.SetAlignment(gizmos.LED_ALIGN_RIGHT)
		self.led_Display3.SetDrawFaded(True)
		self.led_Display3.SetForegroundColour('orange')
		sizer13 = wx.BoxSizer(wx.VERTICAL)
		sizer13.Add(self.led_Display3, 1, wx.EXPAND)
		self.panel_NtoE.SetSizer(sizer13)
		self.panel_NtoE.Fit()
		
		# Play Button Setup
		self.m_textCtrl5.SetValue("0000")
		
		self.current_log_file = None
		
		self.logging = False
		
		self.grid_row_counter = 0
		
		self.default_save_dir = r"C:\Users\VBO\Desktop\PMT_data_logger\log_files"
		if os.path.exists(self.default_save_dir):
			self.dirPicker.SetPath(self.default_save_dir)
		else:
			self.dirPicker.SetPath(os.getcwd())
	
	def toggleBtn_MSOX3054A_Connect_OnToggle(self, event):
		if self.toggleBtn_MSOX3054A_Connect.GetValue():
			self.scope_driver = MSOX3054A_OSC(readCallbackFunction=self.mso_receive_message)
			status = self.scope_driver.open()
			if status:
				self.toggleBtn_MSOX3054A_Connect.SetLabel("Disconnect MSOX3054A")
				# self.panel_ButtonsMiddle.Enable()
				# self.panel_ButtonsTop.Enable()
				self.SetStatusText("Instrument Connected", 0)
				idn = self.scope_driver.get_id()
				# print(f"Connected to: {idn}")
				# Start the Background Thread
				self.scope_driver.start()
			
			else:
				self.toggleBtn_MSOX3054A_Connect.SetValue(False)
				wx.MessageBox(f"Failed to Connect: {status}", "Error")
		
		else:
			self.scope_driver.stop()
			self.toggleBtn_MSOX3054A_Connect.SetLabel("Connect MSOX3054A")
			self.SetStatusText("Instrument Disconnected", 0)
	
	# self.panel_ButtonsMiddle.Disable()
	# self.panel_ButtonsTop.Disable()
	
	def mso_receive_message(self, message):
		# print("message=",message)
		message = message.split(',')
		counts = float(message[0])
		ac_vpp = float(message[1])
		ac_rms = float(message[2])
		ac_freq = float(message[3])
		n2e_vrms = float(message[4])
		
		self.led_Display1.SetValue(f"{counts:6.2f}")
		self.led_Display2.SetValue(f"{ac_rms:4.2f}")
		self.led_Display3.SetValue(f"{n2e_vrms:6.2f}")
		
		# 2. Check if Logging is Active (Button is Pressed + File exists)
		if self.logging:
			self.write_to_csv(counts, ac_vpp, ac_rms, ac_freq, n2e_vrms)
	
	def toggleButton_StartLogging_OnToggle(self, event):
		if self.toggleButton_StartLogging.GetValue():
			# 1. Validation: Check if Instrument is connected via button state
			if not self.toggleBtn_MSOX3054A_Connect.GetValue():
				wx.MessageBox("Please connect the Oscilloscope first!", "Error", wx.ICON_ERROR)
				self.toggleButton_StartLogging.SetValue(False)
				return
			
			# 2. Validation: Check if Directory is selected
			save_dir = self.dirPicker.GetPath()
			if not save_dir or not os.path.exists(save_dir):
				wx.MessageBox("Please select a valid log folder.", "Error", wx.ICON_ERROR)
				self.toggleButton_StartLogging.SetValue(False)
				return
			
			# ----
			try:
				voltage = int(self.m_textCtrl5.GetValue())
				if voltage < 800 or voltage > 1800:
					raise ValueError("Out of range")
			
			except ValueError:
				wx.MessageBox("Please put the correct HT Voltage! (Must be between 800 and 1800)", "Error")
				self.toggleButton_StartLogging.SetValue(False)
				return
			
			# 3. Create File Name
			timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
			filename = f"Log_{timestamp}.csv"
			self.current_log_file = os.path.join(save_dir, filename)
			
			# 4. Create File and Write Headers
			try:
				with open(self.current_log_file, mode='w', newline='') as file:
					writer = csv.writer(file)
					writer.writerow(["TIMESTAMPS", "PMT COUNTS(c/s)", "AC RMS (V)", "AC Frequency (Hz)", "AC VPP",
					                 "Neutral to Earth Voltage (V)", "HT_Voltage", "TEMPERATURE_C"])
				
				# --- FIX 6: Removed timer start. Logging happens in on_data_received ---
				self.toggleButton_StartLogging.SetLabel("Stop logging")
				self.SetStatusText(f"Logging to {filename}...", 1)
			except Exception as e:
				wx.MessageBox(f"Failed to create file: {e}", "Error", wx.ICON_ERROR)
				self.toggleButton_StartLogging.SetValue(False)
			self.logging = True
			
			self.grid_Data.ClearGrid()
			for i in range(15):
				self.grid_Data.SetCellBackgroundColour(i, 0, wx.NullColour)
				self.grid_Data.SetCellBackgroundColour(i, 1, wx.NullColour)
				self.grid_Data.SetCellBackgroundColour(i, 2, wx.NullColour)
			self.grid_row_counter = 0
			self.grid_Data.ForceRefresh()
		
		else:
			self.logging = False
			self.toggleButton_StartLogging.SetValue(False)
			self.toggleButton_StartLogging.SetLabel("Start Logging")
			self.SetStatusText("Logging Stopped", 1)
			self.current_log_file = None
			self.m_textCtrl5.SetValue("0000")
	
	def write_to_csv(self, counts, ac_vpp, ac_rms, ac_freq, n2e_vrms):
		ht_val = self.m_textCtrl5.GetValue()
		temp_val = self.m_choice3.GetStringSelection()
		current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		
		with open(self.current_log_file, mode='a', newline='') as file:
			writer = csv.writer(file)
			writer.writerow([current_time, counts, ac_rms, ac_freq, ac_vpp, n2e_vrms, ht_val, temp_val])
		
		# self.SetStatusText(f"Logging...", 1)
		# print(f"Logged: {current_time}, {freq_val:6.3f}, {ht_val}, {temp_val}")
		
		# 1. Get the current row index
		if self.grid_row_counter < 20:
			# We are still filling the empty grid (Rows 0 to 14)
			target_row = self.grid_row_counter
			self.grid_row_counter += 1
		else:
			# The grid is full. We must SCROLL UP.
			target_row = 19  # We will write to the last row
			
			# Shift existing data UP by one
			# Loop from row 0 up to 13
			for i in range(19):
				# Set current row values to the values of the row below it
				self.grid_Data.SetCellValue(i, 0, self.grid_Data.GetCellValue(i + 1, 0))
				self.grid_Data.SetCellValue(i, 1, self.grid_Data.GetCellValue(i + 1, 1))
				self.grid_Data.SetCellValue(i, 2, self.grid_Data.GetCellValue(i + 1, 2))
		
		# Step 2: Write the NEW data to the target row (either the next empty one, or the bottom one)
		self.grid_Data.SetCellValue(target_row, 0, str(counts))
		self.grid_Data.SetCellValue(target_row, 1, f"{float(ac_rms):.3f}")
		self.grid_Data.SetCellValue(target_row, 2, f"{float(n2e_vrms):.3f}")
		
		# Step 3: Manage Highlights (Green Bar)
		# Clear all backgrounds first
		for i in range(20):
			self.grid_Data.SetCellBackgroundColour(i, 0, wx.NullColour)
			self.grid_Data.SetCellBackgroundColour(i, 1, wx.NullColour)
			self.grid_Data.SetCellBackgroundColour(i, 2, wx.NullColour)
		
		# Highlight the row we just wrote to
		highlight_color = wx.Colour(200, 255, 200)
		self.grid_Data.SetCellBackgroundColour(target_row, 0, highlight_color)
		self.grid_Data.SetCellBackgroundColour(target_row, 1, highlight_color)
		self.grid_Data.SetCellBackgroundColour(target_row, 2, highlight_color)
		
		# Make sure the grid shows the bottom row
		self.grid_Data.MakeCellVisible(target_row, 0)
		self.grid_Data.ForceRefresh()
	
	def dirPicker_OnDirChanged(self, event):
		selected_path = event.GetPath()
		if os.path.exists(selected_path):
			self.SetStatusText(f"Log folder set to: {selected_path}", 1)
		event.Skip()
	
	def frameMain_Close(self, event):
		if self.scope_driver:
			self.scope_driver.stop()
			time.sleep(0.1)
		
		print("Quitting... Bye")
		self.Destroy()


if __name__ == "__main__":
	app = wx.App(False)
	GUI = Keysight_MSOX3054A_WaveGen_Controller(None)
	GUI.Show(True)
	app.MainLoop()

