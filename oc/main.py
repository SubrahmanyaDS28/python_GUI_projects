
import wx
import serial
import serial.tools.list_ports
import datetime
from mna import frameMain, MyDialog1
import threading
import time
import re
import os

JD_OFFSET = 1721424.5


def get_julian_date(dt_object):
	# Calculate the fractional part of the day
	fractional_day = (
				dt_object.hour / 24.0 + dt_object.minute / 1440.0 + dt_object.second / 86400.0 + dt_object.microsecond / 86400000000.0)
	
	# The toordinal() value counts from midnight, so we need to add the fractional day.
	return dt_object.toordinal() + JD_OFFSET + fractional_day


class MainFrame(frameMain):
#define SEL0 LATDbits.LATD8
#define SEL1 LATBbits.LATB5
#define SEL2 LATBbits.LATB6
	def __init__(self, parent=None):
		super().__init__(parent)
		
		# === Set Application Icon ===
		icon_path = os.path.join(os.path.dirname(__file__), "logo.png")
		if os.path.exists(icon_path):
			icon = wx.Icon(icon_path, wx.BITMAP_TYPE_PNG)
			self.SetIcon(icon)
		else:
			print("Warning: logo.png not found")
			
		# Serial
		self.ser = None
		self.selected_port = None
		self.selected_baud = 9600

		# Bind Enter key for INPUT field
		self.m_textCtrl12.Bind(wx.EVT_TEXT_ENTER, self.on_send_input)
		self.m_textCtrl12.SetWindowStyle(wx.TE_PROCESS_ENTER)
		
		self.m_textCtrl1.SetValue("00:00:00")
		self.m_textCtrl2.SetValue("00 00 00")
		self.m_textCtrl3.SetValue("00:00:00")
		self.m_textCtrl11.SetValue("OFF")
		self.m_textCtrl111.SetValue("0.000")
		
		# RA and DEC limit states
		self.ra_limit_state = "CLEAR"
		self.dec_limit_state = "CLEAR"

		# Set default colors
		self.m_textCtrl9.SetForegroundColour(wx.Colour(0, 128, 0))  # Green
		self.m_textCtrl9.SetValue("CLEAR")
		self.m_textCtrl10.SetForegroundColour(wx.Colour(0, 128, 0))  # Green
		self.m_textCtrl10.SetValue("CLEAR")

		# Console / Handset mode
		self.mode = "Console"  # default
		self.buttons = [
			self.m_button4, self.m_button5, self.m_button6, self.m_button7,
			self.m_button41, self.m_button51, self.m_button61, self.m_button71,
			self.m_button42, self.m_button52, self.m_button62, self.m_button72,
			self.m_button43, self.m_button53, self.m_button63, self.m_button73,
			self.m_button24, self.m_button25, self.m_button26, self.m_button27
		]
		
		self.button_command_map = {
			# RA (Right Ascension) - Lowercase for RA
			self.m_button4: 'RASLE',  # RA Button 1 (e.g., East)
			self.m_button5: 'RASLW',  # RA Button 2 (e.g., West)
			self.m_button41: 'RASTE',  # RA Button 3
			self.m_button51: 'RASTW',  # RA Button 4
			self.m_button42: 'RAGE',  # RA Button 5
			self.m_button52: 'RAGW',  # RA Button 6
			self.m_button43: 'RAFGE',  # RA Button 7
			self.m_button53: 'RAFGW',  # RA Button 8
			
			# DEC (Declination) - Uppercase for DEC
			self.m_button6: 'DECSLN',  # DEC Button 1 (e.g., North)
			self.m_button7: 'DECSLS',  # DEC Button 2 (e.g., South)
			self.m_button61: 'DECSTN',  # DEC Button 3
			self.m_button71: 'DECSTS',  # DEC Button 4
			self.m_button62: 'DECGN',  # DEC Button 5
			self.m_button72: 'DECGS',  # DEC Button 6
			self.m_button63: 'DECFGN',  # DEC Button 7
			self.m_button73: 'DECFGS',  # DEC Button 8
			
			# Other buttons (m_button24 to m_button27) - Numerics
			self.m_button24: '1',  # ON
			self.m_button25: '2',  # OFF
			self.m_button26: '3',  # UP
			self.m_button27: '4',  # DOWN
		}

		# Timers
		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.update_time_fields, self.timer)
		self.timer.Start(100)

		# self.serial_timer = wx.Timer(self)
		# self.Bind(wx.EVT_TIMER, self.read_serial_loopback, self.serial_timer)
		# self.serial_timer.Start(100)

		# Menu COM Port Setting
		self.menuItemCOM = wx.MenuItem(self.menuCOM, wx.ID_ANY, "Configure...", "", wx.ITEM_NORMAL)
		self.menuCOM.Append(self.menuItemCOM)
		self.Bind(wx.EVT_MENU, self.open_com_settings, id=self.menuItemCOM.GetId())

		# Bind console/handset
		self.m_checkBox_console.SetValue(True)
		self.m_checkBox_console.Bind(wx.EVT_CHECKBOX, self.set_console)
		self.m_checkBox_handset.Bind(wx.EVT_CHECKBOX, self.set_handset)

		# Bind all buttons
		for btn in self.buttons:
			# btn.Bind(wx.EVT_BUTTON, self.on_button_press)
			btn.Bind(wx.EVT_LEFT_DOWN, self.on_button_down)
			btn.Bind(wx.EVT_LEFT_UP, self.on_button_up)

		# Bind File->Exit menu
		self.Bind(wx.EVT_MENU, self.on_exit, id=self.menuItemExit.GetId())

		# Buttons that should behave with simple press
		self.m_button24.Bind(wx.EVT_BUTTON, self.on_button_press)  # ON
		self.m_button25.Bind(wx.EVT_BUTTON, self.on_button_press)  # OFF
		self.m_button26.Bind(wx.EVT_BUTTON, self.on_button_press)  # UP
		self.m_button27.Bind(wx.EVT_BUTTON, self.on_button_press)  # DOWN

	# -------------------------
	# Mode handlers
	# -------------------------
	def set_console(self, event):
		self.m_checkBox_console.SetValue(True)
		self.m_checkBox_handset.SetValue(False)
		self.mode = "Console"
		self.enable_buttons(True)
		if self.ser and self.ser.is_open:
			self.ser.write("CONSOLE\n".encode("utf-8"))

	def set_handset(self, event):
		self.m_checkBox_console.SetValue(False)
		self.m_checkBox_handset.SetValue(True)
		self.mode = "Handset"
		self.enable_buttons(False)
		if self.ser and self.ser.is_open:
			self.ser.write("HANDSET\n".encode("utf-8"))

	def enable_buttons(self, enable):
		for btn in self.buttons:
			btn.Enable(enable)

	# -------------------------
	# COM Settings Dialog
	# -------------------------
	# def open_com_settings(self, event):
	#     dlg = MyDialog1(self)
	#     ports = [p.device for p in serial.tools.list_ports.comports()]
	#     dlg.m_comboBox1.Set(ports)
	#     dlg.m_comboBox2.Set(["9600", "19200", "38400", "115200"])
	#
	#     def on_ok(evt):
	#         self.selected_port = "/dev/ttyUSB0"
	#         self.selected_baud = 115200
	#         try:
	#             self.ser = serial.Serial(self.selected_port, self.selected_baud, timeout=0.1)
	#             print(f"Connected to {self.selected_port} at {self.selected_baud}")
	#
	#             # Set default RA/DEC limit fields
	#             self.m_textCtrl9.SetForegroundColour(wx.Colour(0, 128, 0))  # green
	#             self.m_textCtrl9.SetValue("Clear")
	#             self.m_textCtrl10.SetForegroundColour(wx.Colour(0, 128, 0))
	#             self.m_textCtrl10.SetValue("Clear")
	#
	#             # Start a timer to read serial continuously
	#             self.serial_timer = wx.Timer(self)
	#             self.Bind(wx.EVT_TIMER, self.read_serial_data, self.serial_timer)
	#             self.serial_timer.Start(100)  # check every 100 ms
	#
	#             dlg.EndModal(wx.ID_OK)
	#         except Exception as e:
	#             wx.MessageBox(f"Error opening serial port: {e}", "Error", wx.ICON_ERROR)
	#
	#     dlg.m_button1.Bind(wx.EVT_BUTTON, on_ok)
	#     dlg.m_button2.Bind(wx.EVT_BUTTON, lambda e: dlg.EndModal(wx.ID_CANCEL))
	#     dlg.ShowModal()
	#     dlg.Destroy()
	
	def open_com_settings(self, event):
		dlg = MyDialog1(self)
		ports = [p.device for p in serial.tools.list_ports.comports()]
		dlg.m_comboBox1.Set(ports)
		dlg.m_comboBox2.Set(["9600", "19200", "38400", "115200"])
		
		def on_ok(evt):
			self.selected_port = "/dev/ttyUSB0"
			self.selected_baud = 115200
			try:
				self.ser = serial.Serial(self.selected_port, self.selected_baud, timeout=0.05)
				print(f"Connected to {self.selected_port} at {self.selected_baud}")
				
				# Default colors
				self.m_textCtrl9.SetForegroundColour(wx.Colour(0, 128, 0))
				self.m_textCtrl9.SetValue("CLEAR")
				self.m_textCtrl10.SetForegroundColour(wx.Colour(0, 128, 0))
				self.m_textCtrl10.SetValue("CLEAR")
				
				# Start background thread for continuous serial reading
				self.serial_running = True
				self.serial_thread = threading.Thread(target=self.read_serial_background, daemon=True)
				self.serial_thread.start()
				
				dlg.EndModal(wx.ID_OK)
			except Exception as e:
				wx.MessageBox(f"Error opening serial port: {e}", "Error", wx.ICON_ERROR)
		
		dlg.m_button1.Bind(wx.EVT_BUTTON, on_ok)
		dlg.m_button2.Bind(wx.EVT_BUTTON, lambda e: dlg.EndModal(wx.ID_CANCEL))
		dlg.ShowModal()
		dlg.Destroy()
	
	def read_serial_background(self):
		"""Continuously read serial in background thread"""
		while getattr(self, "serial_running", False) and self.ser and self.ser.is_open:
			try:
				line = self.ser.readline().decode('utf-8', errors='ignore').strip()
				if not line:
					continue
				
				# Send line to GUI safely
				wx.CallAfter(self.process_serial_line, line)
			
			except Exception as e:
				print(f"Serial read error: {e}")
				time.sleep(0.1)
	
	# -------------------------
	# Button press/release
	# -------------------------
	def on_button_down(self, event):
		if self.mode != "Console": return
		btn = event.GetEventObject()
		# msg = btn.GetLabel()
		msg = self.button_command_map.get(btn)
		if self.ser and self.ser.is_open:
			self.ser.write((msg + "\n").encode())
		print("Pressed:", msg)
		event.Skip()

	def on_button_up(self, event):
		if self.mode != "Console": return
		btn = event.GetEventObject()
		if self.ser and self.ser.is_open:
			self.ser.write(b"STOP\n")
		# print("Released:", btn.GetLabel())
		print("Released:", self.button_command_map.get(btn))
		event.Skip()

	def on_button_press(self, event):
		btn = event.GetEventObject()
		name = btn.GetLabel()
		print(f"Button pressed: {name}")
		if name == "ON":
			self.m_button4.Enable(False)
			self.m_button41.Enable(False)
			self.m_button42.Enable(False)
			self.m_button43.Enable(False)
			self.m_button5.Enable(False)
			self.m_button51.Enable(False)
			self.m_button52.Enable(False)
			self.m_button53.Enable(False)
			self.m_button6.Enable(False)
			self.m_button61.Enable(False)
			self.m_button62.Enable(False)
			self.m_button63.Enable(False)
			self.m_button7.Enable(False)
			self.m_button71.Enable(False)
			self.m_button72.Enable(False)
			self.m_button73.Enable(False)
			
			self.m_textCtrl11.SetValue("ON")
			
			
		if name == "OFF":
			self.m_button4.Enable(True)
			self.m_button41.Enable(True)
			self.m_button42.Enable(True)
			self.m_button43.Enable(True)
			self.m_button5.Enable(True)
			self.m_button51.Enable(True)
			self.m_button52.Enable(True)
			self.m_button53.Enable(True)
			self.m_button6.Enable(True)
			self.m_button61.Enable(True)
			self.m_button62.Enable(True)
			self.m_button63.Enable(True)
			self.m_button7.Enable(True)
			self.m_button71.Enable(True)
			self.m_button72.Enable(True)
			self.m_button73.Enable(True)

			self.m_textCtrl11.SetValue("OFF")
		
		# Send name over serial if connected
		if self.ser and self.ser.is_open:
			try:
				self.ser.write(f"{name}\n".encode())
			except Exception as e:
				print(f"Serial write error: {e}")

	# -------------------------
	# Loopback serial
	# -------------------------
	# def read_serial_loopback(self, event):
	#     if self.ser and self.ser.is_open and self.ser.in_waiting:
	#         data = self.ser.read(self.ser.in_waiting).decode(errors="ignore")
	#         # Append to RA textbox
	#         current = self.m_textCtrl1.GetValue()
	#         self.m_textCtrl1.SetValue(current + data)

	# -------------------------
	# Update time fields
	# -------------------------
	

	# def update_time_fields(self, event):
	#     now = datetime.datetime.utcnow()
	#     ut = now.strftime("%H:%M:%S")
	#     ist = (now + datetime.timedelta(hours=5, minutes=30)).strftime("%H:%M:%S")
	#     lst = ut
	#     # jd = str(now.toordinal())
	#     jd = str(get_julian_date(now))
	#     self.m_textCtrl4.SetValue(lst)
	#     self.m_textCtrl5.SetValue(ut)
	#     self.m_textCtrl6.SetValue(ist)
	#     self.m_textCtrl7.SetValue(jd)
	
	# add this at top of file next to other imports
	
	def hms_to_hours(self, s):
		"""Parse a string like '10:55:02' or '10 55 02' or 'RA = 10:55:02' into decimal hours.
		   Returns float hours or None if it cannot parse.
		"""
		if not s:
			return None
		# find all integer/float groups
		nums = re.findall(r"[-+]?\d+\.?\d*", s)
		if not nums:
			return None
		try:
			h = float(nums[0]) if len(nums) > 0 else 0.0
			m = float(nums[1]) if len(nums) > 1 else 0.0
			sec = float(nums[2]) if len(nums) > 2 else 0.0
			# if RA given in degrees (e.g. 163 45 43) — we won't detect that here,
			# but RA in your GUI should be HMS (hours:minutes:seconds).
			return h + m / 60.0 + sec / 3600.0
		except Exception:
			return None
	
	def hours_to_hms_string(self, hours, show_sign=False):
		"""Convert decimal hours to 'HH:MM:SS' (hours may be negative)."""
		if hours is None:
			return ""
		sign = "-" if hours < 0 else ""
		h = abs(hours)
		hh = int(h)
		mm = int((h - hh) * 60)
		ss = int(round(((h - hh) * 60 - mm) * 60))
		# fix rounding overflow
		if ss >= 60:
			ss -= 60
			mm += 1
		if mm >= 60:
			mm -= 60
			hh += 1
		s = f"{hh:02d}:{mm:02d}:{ss:02d}"
		if show_sign:
			return f"{sign}{s}"
		return s
	
	def update_time_fields(self, event):
		# ---- UTC / IST display (unchanged) ----
		now = datetime.datetime.utcnow()
		ut = now.strftime("%H:%M:%S")
		ist = (now + datetime.timedelta(hours=5, minutes=30)).strftime("%H:%M:%S")
		
		# ---- Julian Date (UTC) ----
		jd = get_julian_date(now)  # your function — uses UTC datetime
		jd_str = f"{jd:.5f}"
		
		# ---- GMST (hours) using common approximation ----
		# GMST_hours = 18.697374558 + 24.06570982441908 * (JD - 2451545.0)
		# normalize to 0-24
		gmst = (18.697374558 + 24.06570982441908 * (jd - 2451545.0)) % 24.0
		
		# ---- Local Sidereal Time (LST) ----
		# Ensure you have self.longitude defined (degrees, east positive). Default 0° if not set.
		if not hasattr(self, "longitude"):
			self.longitude = 77.5775
		lst_hours = (gmst + (self.longitude / 15.0)) % 24.0
		
		# ---- Parse RA from your RA textbox (self.m_textCtrl1) ----
		ra_text = self.m_textCtrl1.GetValue().strip()
		ra_hours = self.hms_to_hours(ra_text)
		
		# ---- Hour Angle: HA = LST - RA ----
		ha_hours = None
		if ra_hours is not None:
			ha_raw = lst_hours - ra_hours
			# normalize to -12..+12 range for human readability
			ha_norm = ((ha_raw + 12.0) % 24.0) - 12.0
			ha_hours = ha_norm
		
		# ---- Populate GUI fields ----
		# LST shown as HH:MM:SS
		lst_str = self.hours_to_hms_string(lst_hours)
		self.m_textCtrl4.SetValue(lst_str)
		
		# UT / IST / JD
		self.m_textCtrl5.SetValue(ut)
		self.m_textCtrl6.SetValue(ist)
		self.m_textCtrl7.SetValue(jd_str)
		
		# HA: show HH:MM:SS and degrees
		if ha_hours is not None:
			ha_hms = self.hours_to_hms_string(ha_hours, show_sign=True)
			ha_deg = ha_hours * 15.0
			# format degrees with sign and one decimal
			ha_deg_str = f"{ha_deg:+07.1f}°"
			self.m_textCtrl3.SetValue(f"{ha_hms} ")
		else:
			self.m_textCtrl3.SetValue("")  # blank if no RA available
	
	

	# def read_serial_data(self, event):
	#     if self.ser and self.ser.is_open and self.ser.in_waiting:
	#         try:
	#             line = self.ser.readline().decode('utf-8').strip()
	#             # RA limits
	#             if line == "RE":
	#                 self.m_textCtrl9.SetForegroundColour(wx.RED)
	#                 self.m_textCtrl9.SetValue("EAST LIMIT REACHED")
	#                 if self.mode == "Console":
	#                     self.ser.write(b"STOP\n")
	#                     self.m_button4.Enable(False)
	#                     self.m_button41.Enable(False)
	#                     self.m_button42.Enable(False)
	#                     self.m_button43.Enable(False)
	#
	#             elif line == "RW":
	#                 self.m_textCtrl9.SetForegroundColour(wx.RED)
	#                 self.m_textCtrl9.SetValue("WEST LIMIT REACHED")
	#                 if self.mode == "Console":
	#                     self.ser.write(b"STOP\n")
	#                     self.m_button5.Enable(False)
	#                     self.m_button51.Enable(False)
	#                     self.m_button52.Enable(False)
	#                     self.m_button53.Enable(False)
	#
	#             elif line == "RC":
	#                 self.m_textCtrl9.SetForegroundColour(wx.Colour(0, 128, 0))
	#                 self.m_textCtrl9.SetValue("CLEAR")
	#
	#                 if self.mode == "Console":
	#                     self.m_button4.Enable(True)
	#                     self.m_button41.Enable(True)
	#                     self.m_button42.Enable(True)
	#                     self.m_button43.Enable(True)
	#
	#                     self.m_button5.Enable(True)
	#                     self.m_button51.Enable(True)
	#                     self.m_button52.Enable(True)
	#                     self.m_button53.Enable(True)
	#
	#             # DEC limits
	#             elif line == "DN":
	#                 self.m_textCtrl10.SetForegroundColour(wx.RED)
	#                 self.m_textCtrl10.SetValue("NORTH LIMIT REACHED")
	#                 if self.mode == "Console":
	#                     self.ser.write(b"STOP\n")
	#                     self.m_button6.Enable(False)
	#                     self.m_button61.Enable(False)
	#                     self.m_button62.Enable(False)
	#                     self.m_button63.Enable(False)
	#
	#             elif line == "DS":
	#                 self.m_textCtrl10.SetForegroundColour(wx.RED)
	#                 self.m_textCtrl10.SetValue("SOUTH LIMIT REACHED")
	#                 if self.mode == "Console":
	#                     self.ser.write(b"STOP\n")
	#                     self.m_button7.Enable(False)
	#                     self.m_button71.Enable(False)
	#                     self.m_button72.Enable(False)
	#                     self.m_button73.Enable(False)
	#
	#             elif line == "DC":
	#                 self.m_textCtrl10.SetForegroundColour(wx.Colour(0, 128, 0))
	#                 self.m_textCtrl10.SetValue("CLEAR")
	#
	#                 if self.mode == "Console":
	#                     self.m_button6.Enable(True)
	#                     self.m_button61.Enable(True)
	#                     self.m_button62.Enable(True)
	#                     self.m_button63.Enable(True)
	#
	#                     self.m_button7.Enable(True)
	#                     self.m_button71.Enable(True)
	#                     self.m_button72.Enable(True)
	#                     self.m_button73.Enable(True)
	#
	#             elif line.startswith("RA"):
	#                 ra_value = line[2:]
	#                 self.m_textCtrl1.SetValue(ra_value)
	#
	#             elif line.startswith("DEC"):
	#                 dec_value = line[3:]
	#                 self.m_textCtrl2.SetValue(dec_value)
	#
	#         except Exception as e:
	#             print(f"Error reading serial data: {e}")
	
	def process_serial_line(self, line):
		"""Handle parsed serial line safely in GUI thread."""
		try:
			# RA limits
			if line == "RE":
				self.m_textCtrl9.SetForegroundColour(wx.RED)
				self.m_textCtrl9.SetValue("EAST LIMIT REACHED")
				if self.mode == "Console":
					self.ser.write(b"STOP\n")
					self.m_button4.Enable(False)
					self.m_button41.Enable(False)
					self.m_button42.Enable(False)
					self.m_button43.Enable(False)
			
			elif line == "RW":
				self.m_textCtrl9.SetForegroundColour(wx.RED)
				self.m_textCtrl9.SetValue("WEST LIMIT REACHED")
				if self.mode == "Console":
					self.ser.write(b"STOP\n")
					self.m_button5.Enable(False)
					self.m_button51.Enable(False)
					self.m_button52.Enable(False)
					self.m_button53.Enable(False)
			
			elif line == "RC":
				self.m_textCtrl9.SetForegroundColour(wx.Colour(0, 128, 0))
				self.m_textCtrl9.SetValue("CLEAR")
				if self.mode == "Console":
					self.m_button4.Enable(True)
					self.m_button41.Enable(True)
					self.m_button42.Enable(True)
					self.m_button43.Enable(True)
					self.m_button5.Enable(True)
					self.m_button51.Enable(True)
					self.m_button52.Enable(True)
					self.m_button53.Enable(True)
			
			# DEC limits
			elif line == "DN":
				self.m_textCtrl10.SetForegroundColour(wx.RED)
				self.m_textCtrl10.SetValue("NORTH LIMIT REACHED")
				if self.mode == "Console":
					self.ser.write(b"STOP\n")
					self.m_button6.Enable(False)
					self.m_button61.Enable(False)
					self.m_button62.Enable(False)
					self.m_button63.Enable(False)
			
			elif line == "DS":
				self.m_textCtrl10.SetForegroundColour(wx.RED)
				self.m_textCtrl10.SetValue("SOUTH LIMIT REACHED")
				if self.mode == "Console":
					self.ser.write(b"STOP\n")
					self.m_button7.Enable(False)
					self.m_button71.Enable(False)
					self.m_button72.Enable(False)
					self.m_button73.Enable(False)
			
			elif line == "DC":
				self.m_textCtrl10.SetForegroundColour(wx.Colour(0, 128, 0))
				self.m_textCtrl10.SetValue("CLEAR")
				if self.mode == "Console":
					self.m_button6.Enable(True)
					self.m_button61.Enable(True)
					self.m_button62.Enable(True)
					self.m_button63.Enable(True)
					self.m_button7.Enable(True)
					self.m_button71.Enable(True)
					self.m_button72.Enable(True)
					self.m_button73.Enable(True)
			
			# Continuous RA/DEC updates
			elif line.startswith("RA_E"):
				ra_value = line[4:].strip()
				self.m_textCtrl1.SetValue(ra_value)
			
			elif line.startswith("DEC_E"):
				dec_value = line[5:].strip()
				self.m_textCtrl2.SetValue(dec_value)
				
			elif line.startswith("ADC"):
				adc_value = line[3:].strip()
				self.m_textCtrl111.SetValue(adc_value)
			
			else:
				# Optional: print unknown lines
				print("Unrecognized:", line)
		
		except Exception as e:
			print(f"Error processing serial line: {e}")
			
	def on_send_input(self, event):
		data = self.m_textCtrl12.GetValue()  # Get text from INPUT field
		if hasattr(self, 'ser') and self.ser is not None:
			try:
				self.ser.write((data + '\n').encode('utf-8'))  # Send over serial
			except Exception as e:
				wx.MessageBox(f"Error sending data: {e}", "Error", wx.ICON_ERROR)
		self.m_textCtrl12.SetValue("")  # Clear input field

	# -------------------------
	# Exit handler
	# -------------------------
	def on_exit(self, event):
		# Stop timer
		if hasattr(self, "timer") and self.timer.IsRunning():
			self.timer.Stop()

		# Close serial port if open
		if self.ser and self.ser.is_open:
			try:
				self.ser.close()
				print(f"Serial port {self.selected_port} closed.")
			except Exception as e:
				print(f"Error closing serial port: {e}")

		# Destroy the frame and exit application
		self.Destroy()

	def __del__(self):
		if self.ser and self.ser.is_open:
			try:
				self.ser.close()
				print(f"Serial port {self.selected_port} closed on cleanup.")
			except:
				pass
			


# class DummySerial:
# 	def __init__(self):
# 		self.buffer = ["RE", "RC", "DN", "DC"]
# 		self.in_waiting = True
#
# 	def readline(self):
# 		if self.buffer:
# 			return (self.buffer.pop(0) + "\n").encode('utf-8')
# 		else:
# 			self.in_waiting = False
# 			return b""




class MyApp(wx.App):
	def OnInit(self):
		self.frame = MainFrame(None)
		self.frame.Show()
		return True

if __name__ == "__main__":
	app = MyApp(False)
	app.MainLoop()
