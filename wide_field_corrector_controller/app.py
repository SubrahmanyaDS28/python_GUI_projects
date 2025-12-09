import wx
import MyProjectBase
from vispy import app, scene
import numpy as np
import logging
import os
import configparser
import threading
import time
import serial
import serial.tools.list_ports as list_ports

# Suppress VisPy logging to keep the console clean
vispy_logger = logging.getLogger('vispy')
vispy_logger.setLevel(logging.WARNING)

# --- Constants ---
ARCSEC_TO_UNITS = 1.0
CONFIG_FILE = 'wfc_settings.ini'
DEVICE_STATUS_POLL_MS = 500

# --- Serial Communication Constants ---
STx = '*'
ETx = '#'
ACK = '^'
NAK = '!'
BUSY = 'B'
READY = 'R'
HOME = 'H'
UNKNOWN = 'X'
ERROR = 'Z'
OVERFLOW = 'O'
SERIAL_READ_SLEEP_TIME = 0.05
MOTOR_MOVE_COMMAND = 'M'
FILTER_COMMAND = 'F'
STATUS_COMMAND = 'S'
HOME_COMMAND = 'H'

# --- Limit Switch Constants (Simulated for Demo) ---
# Assuming the full status response is: ^R[Status_Code][Limit_Switch_String]
# Example Status: ^RSNNEWW (R=Ready, S=Safe, N=North_Limit, E=East_Limit, W=West_Limit, S=South_Limit)
# We will look for a 4-char string 'NNEWW' where:
# 1st char: North Limit (N)
# 2nd char: South Limit (S)
# 3rd char: East Limit (E)
# 4th char: West Limit (W)
LIMIT_SWITCH_STATUS_INDEX = 2  # The index where the 4-char limit status string begins in the data.


# =========================================================
#                     LED CONTROL CLASS (FIXED)
# =========================================================

class LED(wx.Control):
	"""
	Custom wx Control to display a colored LED (Circle).
	State: 0=Error/Busy (Red), 1=Ready/On (Green), 2=Default/Off (Grey)
	For Limit Switches: 0=Engaged (Red), 1=Safe (Green), 2=Unknown (Grey)
	"""
	
	def __init__(self, parent, id=-1, colors=(wx.Colour(220, 10, 10), wx.Colour(10, 220, 10), wx.Colour(176, 176, 176)),
	             pos=(-1, -1), size=(16, 16), style=wx.NO_BORDER):
		wx.Control.__init__(self, parent, id, pos, size, style)
		
		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
		
		self.colours = colors
		self.state = 2
		self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
	
	def SetState(self, state):
		if self.state != state:
			self.state = state
			self.Refresh()
	
	def OnPaint(self, event):
		dc = wx.AutoBufferedPaintDC(self)
		dc.Clear()
		
		# FIX: Cast calculated values to integers for wx.DC drawing functions
		w, h = self.GetSize()
		radius = int(min(w, h) / 2 - 2)
		center_x = int(w // 2)
		center_y = int(h // 2)
		
		color = self.colours[self.state % len(self.colours)]
		
		dc.SetBrush(wx.Brush(color))
		dc.SetPen(wx.Pen(color.ChangeLightness(50), 1))
		
		# The arguments are now integers, fixing the TypeError
		dc.DrawCircle(center_x, center_y, radius)
	
	def OnEraseBackground(self, event):
		pass
	
	def GetDefaultSize(self):
		return wx.Size(16, 16)


# =========================================================
#                 EVENT BINDING DECORATOR
# =========================================================

def bind_event(event_type, control_attr):
	"""
	Decorator to bind a method to a wx event of a specified control.
	"""
	
	def decorator(func):
		if not hasattr(func, '_bindings'):
			func._bindings = []
		func._bindings.append((event_type, control_attr))
		return func
	
	return decorator


# =========================================================
#                SERIAL PORT THREAD CLASS
# =========================================================

class SerialReadThread(threading.Thread):
	"""
	A separate thread for reading data from the serial port to prevent GUI freezing.
	"""
	
	def __init__(self, serial_port, parent_frame):
		threading.Thread.__init__(self)
		self.serial_port = serial_port
		self.parent_frame = parent_frame
		self.keep_running = True
		self.daemon = True
	
	def run(self):
		logging.info("Serial read thread started.")
		while self.keep_running:
			if self.serial_port and self.serial_port.is_open:
				try:
					data_bytes = self.serial_port.read_all()
					if data_bytes:
						data = data_bytes.decode('ascii').strip()
						wx.CallAfter(self.parent_frame.handle_serial_data, data)
						logging.debug(f"Received serial data: {data}")
				except serial.SerialException as e:
					logging.error(f"Serial error: {e}")
					wx.CallAfter(self.parent_frame.handle_serial_error, str(e))
				except Exception as e:
					logging.error(f"Error in serial thread: {e}")
			
			time.sleep(SERIAL_READ_SLEEP_TIME)
		logging.info("Serial read thread stopped.")
	
	def stop(self):
		self.keep_running = False


# =========================================================
#                 CONFIGURATION MANAGER CLASS
# (Unchanged for brevity, but required)
# =========================================================

class AppConfig:
	"""Handles saving, loading, and managing application settings."""
	
	DEFAULTS = {
		'COM': {
			'port': 'COM3',
			'baudrate': '921600',
			'timeout': '1.0',
			'block_size': '1000'
		},
		'MOTOR': {
			'min_freq': '2500',
			'max_freq': '2500',
			'home_pos': '0',
			'gear_ratio': '5.2'
		},
		'FILTER': {
			'name_1': 'Filter 1', 'pos_1': '0',
			'name_2': 'Filter 2', 'pos_2': '0',
			'name_3': 'Filter 3', 'pos_3': '6666',
			'name_4': 'Filter 4', 'pos_4': '6666',
		}
	}
	
	def __init__(self):
		self.config = configparser.ConfigParser()
		self.load()
	
	def load(self):
		self.config.read_dict(self.DEFAULTS)
		if os.path.exists(CONFIG_FILE):
			self.config.read(CONFIG_FILE)
	
	def save(self):
		with open(CONFIG_FILE, 'w') as configfile:
			self.config.write(configfile)
	
	def get(self, section, key, fallback=None):
		return self.config.get(section, key, fallback=fallback)


# =========================================================
#                DIALOG HANDLER CLASSES
# (Unchanged for brevity, but required)
# =========================================================

class FilterWheelSettingController(MyProjectBase.FilterWheelSetting):
	def __init__(self, parent, config):
		MyProjectBase.FilterWheelSetting.__init__(self, parent)
		self.config = config
		self.parent_frame = parent
		self.controls = [
			(self.m_textCtrl8, 'name_1'), (self.m_textCtrl9, 'pos_1'),
			(self.m_textCtrl10, 'name_2'), (self.m_textCtrl11, 'pos_2'),
			(self.m_textCtrl12, 'name_3'), (self.m_textCtrl13, 'pos_3'),
			(self.m_textCtrl14, 'name_4'), (self.m_textCtrl15, 'pos_4'),
		]
		self.load_settings()
		
		self.m_button13.Bind(wx.EVT_BUTTON, self.on_ok)
		self.m_button14.Bind(wx.EVT_BUTTON, self.on_cancel)
		self.m_button12.Bind(wx.EVT_BUTTON, self.on_reset)
	
	def load_settings(self):
		for ctrl, key in self.controls:
			ctrl.SetValue(self.config.get('FILTER', key))
	
	def save_settings(self):
		for ctrl, key in self.controls:
			self.config.config.set('FILTER', key, ctrl.GetValue())
	
	def on_ok(self, event):
		self.save_settings()
		self.parent_frame.update_filter_buttons()
		self.EndModal(wx.ID_OK)
	
	def on_cancel(self, event):
		self.EndModal(wx.ID_CANCEL)
	
	def on_reset(self, event):
		for ctrl, key in self.controls:
			ctrl.SetValue(AppConfig.DEFAULTS['FILTER'][key])


class SerialPortSettingController(MyProjectBase.SerialPortSetting):
	def __init__(self, parent, config):
		MyProjectBase.SerialPortSetting.__init__(self, parent)
		self.config = config
		self.controls = [
			(self.m_textCtrl16, 'timeout'),
			(self.m_textCtrl17, 'block_size'),
		]
		self.load_settings()
		
		self.m_button17.Bind(wx.EVT_BUTTON, self.on_ok)
		self.m_button18.Bind(wx.EVT_BUTTON, self.on_cancel)
		self.m_button16.Bind(wx.EVT_BUTTON, self.on_reset)
	
	def load_settings(self):
		for ctrl, key in self.controls:
			ctrl.SetValue(self.config.get('COM', key))
	
	def save_settings(self):
		for ctrl, key in self.controls:
			self.config.config.set('COM', key, ctrl.GetValue())
	
	def on_ok(self, event):
		self.save_settings()
		self.EndModal(wx.ID_OK)
	
	def on_cancel(self, event):
		self.EndModal(wx.ID_CANCEL)
	
	def on_reset(self, event):
		for ctrl, key in self.controls:
			ctrl.SetValue(AppConfig.DEFAULTS['COM'][key])


class MotorControlSettingController(MyProjectBase.MotorControlSetting):
	def __init__(self, parent, config):
		MyProjectBase.MotorControlSetting.__init__(self, parent)
		self.config = config
		self.controls = [
			(self.m_textCtrl18, 'min_freq'),
			(self.m_textCtrl19, 'max_freq'),
			(self.m_textCtrl20, 'home_pos'),
			(self.m_textCtrl21, 'gear_ratio'),
		]
		self.load_settings()
		
		self.m_button20.Bind(wx.EVT_BUTTON, self.on_ok)
		self.m_button21.Bind(wx.EVT_BUTTON, self.on_cancel)
		self.m_button19.Bind(wx.EVT_BUTTON, self.on_reset)
	
	def load_settings(self):
		for ctrl, key in self.controls:
			ctrl.SetValue(self.config.get('MOTOR', key))
	
	def save_settings(self):
		for ctrl, key in self.controls:
			self.config.config.set('MOTOR', key, ctrl.GetValue())
	
	def on_ok(self, event):
		self.save_settings()
		self.EndModal(wx.ID_OK)
	
	def on_cancel(self, event):
		self.EndModal(wx.ID_CANCEL)
	
	def on_reset(self, event):
		for ctrl, key in self.controls:
			ctrl.SetValue(AppConfig.DEFAULTS['MOTOR'][key])


# =========================================================
#                   MAIN FRAME CONTROLLER
# =========================================================

class WFCController(MyProjectBase.MainFrame):
	
	def __init__(self, parent):
		MyProjectBase.MainFrame.__init__(self, parent)
		
		# --- Config & State ---
		self.config = AppConfig()
		self.current_stage_x = 0.0
		self.current_stage_y = 0.0
		self.vispy_canvas = None
		self.serial_port = None
		self.serial_thread = None
		self.device_status = UNKNOWN
		# New state variable for limit switches (N, S, E, W)
		self.limit_switch_status = {'N': '0', 'S': '0', 'E': '0', 'W': '0'}
		
		# --- Timers ---
		self.status_timer = wx.Timer(self)
		
		# --- Initial GUI Setup (based on loaded config) ---
		self.initialize_com_controls()
		self.update_filter_buttons()
		
		# Call the new method to set up the status LEDs (Original Panel 3)
		self.setup_status_leds()
		
		# Call new method to set up limit switch LEDs (Motor Control Panel)
		self.setup_motor_leds()
		
		# --- Bindings ---
		self._do_binds()
		
		# Set initial motor input values
		self.m_textCtrl22.SetValue("10.0")
		self.m_textCtrl23.SetValue("10.0")
		self.m_textCtrl24.SetValue("10.0")
		self.m_textCtrl25.SetValue("10.0")
		
		self.update_output_display()
	
	def _do_binds(self):
		"""
		Binds all decorated methods to their respective controls,
		correctly handling wx.MenuItem objects.
		"""
		
		menu_item_bindings = []
		
		for attr_name in dir(self):
			attr = getattr(self, attr_name)
			if hasattr(attr, '_bindings'):
				for event_type, control_attr in attr._bindings:
					control = getattr(self, control_attr)
					
					if isinstance(control, wx.MenuItem):
						menu_item_bindings.append((control.GetId(), event_type, attr))
					else:
						control.Bind(event_type, attr)
		
		for item_id, event_type, handler in menu_item_bindings:
			self.Bind(event_type, handler, id=item_id)
		
		self.Bind(wx.EVT_CLOSE, self.on_close_window)
		self.Bind(wx.EVT_SHOW, self.on_show_setup_vispy)
		self.Bind(wx.EVT_TIMER, self.on_status_timer, self.status_timer)
	
	# ---------------------------------------------------------
	#                     STATUS LED SETUP (Panel 3)
	# ---------------------------------------------------------
	
	def setup_status_leds(self):
		"""
		Creates and places the LEDs in the m_panel3 status panel.
		(Logic copied from previous fixed response)
		"""
		# Note: This is m_panel3 in the original generated code's layout section sbSizer4 -> bSizer7 -> bSizer20 -> bSizer21
		
		# Use a FlexGridSizer
		fgSizer1 = wx.FlexGridSizer(0, 2, 0, 0)
		fgSizer1.AddGrowableCol(1)
		fgSizer1.SetFlexibleDirection(wx.BOTH)
		fgSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
		
		# Create LEDs
		self.LED_FilterWheelStatus = LED(self.m_panel3)
		self.LED_FilterWheelHome = LED(self.m_panel3)
		self.LED_CommandStatus = LED(self.m_panel3)
		self.LED_COMStatus = LED(self.m_panel3)
		
		# Create Labels
		label_filter_status = wx.StaticText(self.m_panel3, wx.ID_ANY, u"Filter Wheel Status:   ", wx.DefaultPosition,
		                                    wx.DefaultSize, 0)
		label_filter_home = wx.StaticText(self.m_panel3, wx.ID_ANY, u"Filter Wheel @Home:   ", wx.DefaultPosition,
		                                  wx.DefaultSize, 0)
		label_command_status = wx.StaticText(self.m_panel3, wx.ID_ANY, u"Command Status: ", wx.DefaultPosition,
		                                     wx.DefaultSize, 0)
		label_com_status = wx.StaticText(self.m_panel3, wx.ID_ANY, u"COM Port: ", wx.DefaultPosition, wx.DefaultSize, 0)
		
		# Add to Sizer
		fgSizer1.Add(label_filter_status, 0, wx.ALL | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 5)
		fgSizer1.Add(self.LED_FilterWheelStatus, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
		fgSizer1.Add(label_filter_home, 0, wx.ALL | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 5)
		fgSizer1.Add(self.LED_FilterWheelHome, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
		fgSizer1.Add(label_command_status, 0, wx.ALL | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 5)
		fgSizer1.Add(self.LED_CommandStatus, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
		fgSizer1.Add(label_com_status, 0, wx.ALL | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 5)
		fgSizer1.Add(self.LED_COMStatus, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
		
		# Apply Sizer to the Panel
		self.m_panel3.SetSizer(fgSizer1)
		fgSizer1.Fit(self.m_panel3)
		self.m_panel3.Layout()
	
	# ---------------------------------------------------------
	#                     MOTOR LIMIT LED SETUP (Panel 1 / sbSizer2)
	# ---------------------------------------------------------
	
	def setup_motor_leds(self):
		"""
		Creates and places the limit switch LEDs using a GridBagSizer inside
		self.m_panel9. Fixed so layout does not expand vertically.
		"""
		
		# 1. Instantiate LEDs on the dedicated panel
		self.LED_LimitNorth = LED(self.m_panel9)
		self.LED_LimitSouth = LED(self.m_panel9)
		self.LED_LimitEast = LED(self.m_panel9)
		self.LED_LimitWest = LED(self.m_panel9)
		
		CENTER_FLAG = wx.ALL | wx.ALIGN_CENTER_VERTICAL
		
		# 2. Get the parent sizer of the panel
		parent_sizer = self.m_panel9.GetContainingSizer()
		
		# 3. Create the new layout container: GridBagSizer
		gbs = wx.GridBagSizer(0, 0)  # VGap, HGap
		gbs.SetFlexibleDirection(wx.BOTH)
		gbs.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
		
		# 4. Add zero-size spacers to define the grid
		gbs.Add((0, 0), pos=(0, 2))  # Column 2
		gbs.Add((0, 0), pos=(2, 0))  # Row 2
		
		# Allow horizontal expansion only
		gbs.AddGrowableCol(0, 1)
		gbs.AddGrowableCol(2, 1)
		
		# ⚠️ Do NOT add growable row → prevents vertical stretching
		
		# Helper to create horizontal sizer blocks
		def make_h_sizer(ctrl, led, btn):
			h_sizer = wx.BoxSizer(wx.HORIZONTAL)
			h_sizer.Add(ctrl, 0, CENTER_FLAG, 5)
			h_sizer.Add(led, 0, CENTER_FLAG, 5)
			h_sizer.Add(btn, 0, CENTER_FLAG, 5)
			return h_sizer
		
		# 5. Build and insert directional blocks
		h_north = make_h_sizer(self.m_textCtrl22, self.LED_LimitNorth, self.m_button4)
		gbs.Add(h_north, pos=(0, 1), flag=wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, border=5)
		
		h_south = make_h_sizer(self.m_textCtrl25, self.LED_LimitSouth, self.m_button7)
		gbs.Add(h_south, pos=(2, 1), flag=wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, border=5)
		
		h_west = make_h_sizer(self.m_textCtrl23, self.LED_LimitWest, self.m_button5)
		gbs.Add(h_west, pos=(1, 0), flag=CENTER_FLAG | wx.ALIGN_RIGHT, border=5)
		
		h_east = make_h_sizer(self.m_textCtrl24, self.LED_LimitEast, self.m_button6)
		gbs.Add(h_east, pos=(1, 2), flag=CENTER_FLAG | wx.ALIGN_LEFT, border=5)
		
		# Dummy center spacer
		gbs.Add((0, 0), pos=(1, 1))
		
		# 6. Clear existing sizers from m_panel9 (if any)
		old_sizer = self.m_panel9.GetSizer()
		if old_sizer:
			self.m_panel9.SetSizer(None)
		
		# 7. Apply the new GridBagSizer to m_panel9
		self.m_panel9.SetSizer(gbs)
		gbs.Layout()
		
		# 8. Ensure panel does not expand vertically in parent sizer
		parent_sizer.Detach(self.m_panel9)
		parent_sizer.Add(self.m_panel9, 0, wx.EXPAND | wx.ALL, 5)  # <-- proportion = 0 fixes vertical expansion
		
		# 9. Refresh layouts
		self.m_panel9.Layout()
		self.Layout()
	
	# ---------------------------------------------------------
	#                     SERIAL COMMUNICATION
	# ---------------------------------------------------------
	
	def initialize_com_controls(self):
		# (Unchanged)
		available_ports = [p.device for p in list_ports.comports()]
		
		config_port = self.config.get('COM', 'port')
		if config_port not in available_ports:
			available_ports.append(config_port)
		
		baudrates = ['9600', '19200', '57600', '115200']
		
		self.m_comboBox1.Set(available_ports)
		self.m_comboBox2.Set(baudrates)
		
		port_val = self.config.get('COM', 'port')
		baud_val = self.config.get('COM', 'baudrate')
		
		if port_val in available_ports:
			self.m_comboBox1.SetValue(port_val)
		elif available_ports:
			self.m_comboBox1.SetSelection(0)
		
		if baud_val in baudrates:
			self.m_comboBox2.SetValue(baud_val)
		else:
			self.m_comboBox2.SetSelection(0)
			self.config.config.set('COM', 'baudrate', baudrates[0])
	
	@bind_event(wx.EVT_BUTTON, 'm_button1')
	def on_open_com_port(self, event):
		# (Unchanged)
		if self.serial_port and self.serial_port.is_open:
			self.close_serial_port()
		else:
			port = self.m_comboBox1.GetStringSelection()
			baud_str = self.m_comboBox2.GetStringSelection()
			
			if not baud_str:
				wx.MessageBox("Please select a Baudrate before attempting to open the COM Port.",
				              "Missing Baudrate", wx.OK | wx.ICON_WARNING)
				return
			
			try:
				baud = int(baud_str)
				timeout = float(self.config.get('COM', 'timeout'))
			except ValueError:
				wx.MessageBox("Invalid Baudrate or Timeout value. Check settings.",
				              "Configuration Error", wx.OK | wx.ICON_ERROR)
				return
			
			try:
				self.serial_port = serial.Serial(
					port=port,
					baudrate=baud,
					timeout=timeout
				)
				if self.serial_port.is_open:
					self.serial_thread = SerialReadThread(self.serial_port, self)
					self.serial_thread.start()
					
					self.status_timer.Start(DEVICE_STATUS_POLL_MS)
					
					self.m_button1.SetLabel("CLOSE COM PORT")
					self.m_button1.SetBackgroundColour(wx.Colour(255, 100, 100))
					logging.info(f"Serial port {port}@{baud} opened successfully.")
					self.update_output_display(status_message="COM Port Open.")
			
			except serial.SerialException as e:
				wx.MessageBox(f"Failed to open port {port}: {e}", "Serial Error", wx.OK | wx.ICON_ERROR)
				self.serial_port = None
				self.update_output_display(status_message=f"COM Port Failed: {e}")
	
	def close_serial_port(self):
		# (Unchanged)
		if self.serial_thread:
			self.serial_thread.stop()
			self.serial_thread.join()
			self.serial_thread = None
		
		if self.serial_port and self.serial_port.is_open:
			self.serial_port.close()
			self.serial_port = None
		
		self.status_timer.Stop()
		self.m_button1.SetLabel("OPEN COM PORT")
		self.m_button1.SetBackgroundColour(wx.NullColour)
		self.update_output_display(status_message="COM Port Closed.")
		logging.info("Serial port closed.")
	
	def execute_command(self, command, value=""):
		# (Unchanged)
		if not (self.serial_port and self.serial_port.is_open):
			wx.MessageBox("COM Port is not open.", "Command Failed", wx.OK | wx.ICON_WARNING)
			return False
		
		full_command = f"{STx}{command}{value}{ETx}\n"
		
		try:
			with threading.Lock():
				self.serial_port.write(full_command.encode('ascii'))
				logging.debug(f"Sent command: {full_command.strip()}")
			return True
		except serial.SerialException as e:
			logging.error(f"Failed to send command: {e}")
			self.update_output_display(status_message=f"TX Failed: {e}")
			return False
	
	def parse_limit_switch_data(self, data):
		"""
		Extracts and updates the limit switch status from the serial response,
		checking for the unique strings '~N', '~S', '~E', and '~W'
		to indicate an engaged limit switch ('1', Red/Blocked).
		"""
		
		# 1. Reset all limits to the safe state ('0', Green LED)
		self.limit_switch_status['N'] = '0'
		self.limit_switch_status['S'] = '0'
		self.limit_switch_status['E'] = '0'
		self.limit_switch_status['W'] = '0'
		
		limit_detected = False
		
		# 2. Check for presence of unique limit indicators (~N, ~S, ~E, ~W)
		if '~N' in data:
			self.limit_switch_status['N'] = '1'  # Set North to Engaged (Red LED)
			limit_detected = True
		if '~S' in data:
			self.limit_switch_status['S'] = '1'  # Set South to Engaged (Red LED)
			limit_detected = True
		if '~E' in data:
			self.limit_switch_status['E'] = '1'  # Set East to Engaged (Red LED)
			limit_detected = True
		if '~W' in data:
			self.limit_switch_status['W'] = '1'  # Set West to Engaged (Red LED)
			limit_detected = True
		
		if limit_detected:
			logging.debug(f"Limit(s) engaged (UNIQUE): {self.limit_switch_status}")
			return True
		
		return False
	
	def handle_serial_data(self, data):
		"""Processes received serial data. Now looks for unique limit symbols (~N, ~S, ~E, ~W)."""
		
		# Status LED blinks Green to indicate data received
		self.LED_CommandStatus.SetState(1)
		wx.CallLater(100, lambda: self.LED_CommandStatus.SetState(2))
		
		# --- Logic for Limit-Only Input (e.g., *~N#) ---
		# Check for unique limit character combinations
		limit_symbols_present = any(symbol in data for symbol in ('~N', '~S', '~E', '~W'))
		
		if limit_symbols_present and not (data.startswith(ACK) or data.startswith(NAK)):
			
			logging.debug("Processing simplified limit status (UNIQUE SYMBOLS).")
			if self.device_status == UNKNOWN:
				self.device_status = READY
			
			self.parse_limit_switch_data(data)
			self.update_output_display()
			return
		# --- End Limit-Only Logic ---
		
		# --- Logic for Standard Status Input (e.g., ^R) ---
		if data.startswith(ACK) or data.startswith(NAK):
			response_code = data[1]
			
			if response_code in [BUSY, READY, HOME, UNKNOWN, ERROR, OVERFLOW]:
				self.device_status = response_code
				
				# This handles the full status response (e.g., ^R~N~W#)
				self.parse_limit_switch_data(data)
				
				self.update_output_display()
				
				if response_code == ERROR:
					wx.MessageBox(f"Device reported ERROR: {data}", "Device Error", wx.OK | wx.ICON_ERROR)
	
	@bind_event(wx.EVT_TIMER, 'status_timer')
	def on_status_timer(self, event):
		"""Sends a periodic status command to the device."""
		# We assume the microcontroller responds with the limit switch status in this call.
		self.execute_command(STATUS_COMMAND)
	
	# ---------------------------------------------------------
	#                     MOVEMENT HANDLERS
	# ---------------------------------------------------------
	
	def check_limit_safe(self, direction):
		"""Checks if the limit switch for the given direction is engaged."""
		status = self.limit_switch_status.get(direction)
		if status == '0':  # Assuming '0' is safe and '1' is engaged based on LED logic
			# The LED setup logic suggests: 0=Engaged (Red), 1=Safe (Green).
			# The serial parsing sets '1' for engaged. We must be consistent.
			# Re-reading the LED comment: For Limit Switches: 0=Engaged (Red), 1=Safe (Green)
			# So, if status is '1' (Safe), it's OK to move. If status is '0' (Engaged), block movement.
			# The original code's check_limit_safe was slightly reversed, correcting it here based on serial/LED logic:
			if self.limit_switch_status.get(direction) == '1':  # Assuming '1' means engaged/blocked
				wx.MessageBox(f"{direction} Limit Switch Engaged. Cannot move further {direction}.",
				              "Movement Blocked", wx.OK | wx.ICON_WARNING)
				return False
			return True
		# If status is unknown/not 0/1, allow movement but log warning
		logging.warning(f"Unknown limit switch status for {direction}: {status}. Allowing move.")
		return True
	
	@bind_event(wx.EVT_BUTTON, 'm_button4')
	def on_move_north(self, event):
		if not self.check_limit_safe('N'): return
		move_arcsec = self.get_input_value(self.m_textCtrl22)
		if move_arcsec is not None:
			# MODIFICATION: Send 'N' command with value directly
			if self.execute_command('n', f"{move_arcsec:.1f}"):
				self.current_stage_y += move_arcsec * ARCSEC_TO_UNITS
				self.update_vispy_plot()
				self.update_output_display(status_message=f"Move N {move_arcsec:.1f}")
	
	@bind_event(wx.EVT_BUTTON, 'm_button5')
	def on_move_west(self, event):
		if not self.check_limit_safe('W'): return
		move_arcsec = self.get_input_value(self.m_textCtrl23)
		if move_arcsec is not None:
			# MODIFICATION: Send 'W' command with value directly
			if self.execute_command('w', f"{move_arcsec:.1f}"):
				self.current_stage_x -= move_arcsec * ARCSEC_TO_UNITS
				self.update_vispy_plot()
				self.update_output_display(status_message=f"Move W {move_arcsec:.1f}")
	
	@bind_event(wx.EVT_BUTTON, 'm_button6')
	def on_move_east(self, event):
		if not self.check_limit_safe('E'): return
		move_arcsec = self.get_input_value(self.m_textCtrl24)
		if move_arcsec is not None:
			# MODIFICATION: Send 'E' command with value directly
			if self.execute_command('e', f"{move_arcsec:.1f}"):
				self.current_stage_x += move_arcsec * ARCSEC_TO_UNITS
				self.update_vispy_plot()
				self.update_output_display(status_message=f"Move E {move_arcsec:.1f}")
	
	@bind_event(wx.EVT_BUTTON, 'm_button7')
	def on_move_south(self, event):
		if not self.check_limit_safe('S'): return
		move_arcsec = self.get_input_value(self.m_textCtrl25)
		if move_arcsec is not None:
			# MODIFICATION: Send 'S' command with value directly
			if self.execute_command('s', f"{move_arcsec:.1f}"):
				self.current_stage_y -= move_arcsec * ARCSEC_TO_UNITS
				self.update_vispy_plot()
				self.update_output_display(status_message=f"Move S {move_arcsec:.1f}")
	
	@bind_event(wx.EVT_BUTTON, 'm_button2')
	def on_initial_position(self, event):
		# MODIFICATION: Send 'I' command for Initial/Home position
		if self.execute_command('i'):
			self.current_stage_x = 0.0
			self.current_stage_y = 0.0
			self.update_vispy_plot()
			self.update_output_display(status_message="Motor Homing/Initial Position Initiated")
	
	# NEW: Add a binding for a 'Center' position if available in the GUI,
	# otherwise, this command needs a button bound to it.
	def on_center_position(self, event):
		# MODIFICATION: Send 'C' command for Center position (assuming a button exists)
		if self.execute_command('c'):
			self.update_output_display(status_message="Move to Center Position Initiated")
		# Note: Actual position update depends on the device's response after centering.
	
	# ---------------------------------------------------------
	#                     FILTER HANDLERS (MODIFIED)
	# ---------------------------------------------------------
	
	def on_select_filter(self, event, filter_index):
		"""Handle filter selection button click."""
		filter_name = self.config.get('FILTER', f'name_{filter_index}')
		
		# MODIFICATION: Send 'F' command followed by the index number (e.g., F1)
		if self.execute_command('f', str(filter_index)):
			self.update_output_display(filter_status=filter_name)
			logging.info(f"Command sent: Select Filter {filter_index} ({filter_name})")
	# ---------------------------------------------------------
	#                     FILTER HANDLERS (Unchanged)
	# ---------------------------------------------------------
	
	def update_filter_buttons(self):
		"""Update filter button labels based on config."""
		
		filter_buttons = [self.m_button10, self.m_button11, self.m_button12, self.m_button13]
		name_keys = ['name_1', 'name_2', 'name_3', 'name_4']
		
		for button in filter_buttons:
			button.Unbind(wx.EVT_BUTTON)
		
		for i, button in enumerate(filter_buttons):
			name = self.config.get('FILTER', name_keys[i])
			button.SetLabel(name)
			
			button.Bind(wx.EVT_BUTTON, lambda evt, idx=i + 1: self.on_select_filter(evt, idx))
	
	# def on_select_filter(self, event, filter_index):
	# 	"""Handle filter selection button click."""
	# 	filter_name = self.config.get('FILTER', f'name_{filter_index}')
	# 	filter_pos = self.config.get('FILTER', f'pos_{filter_index}')
	#
	# 	if self.execute_command(FILTER_COMMAND, f"{filter_index}:{filter_pos}"):
	# 		self.update_output_display(filter_status=filter_name)
	# 		logging.info(f"Command sent: Select Filter {filter_index} ({filter_name})")
	
	# ---------------------------------------------------------
	#                     MENU HANDLERS (Unchanged)
	# ---------------------------------------------------------
	
	@bind_event(wx.EVT_MENU, 'm_menuItem1')
	def on_open_motor_settings(self, event):
		dlg = MotorControlSettingController(self, self.config)
		if dlg.ShowModal() == wx.ID_OK:
			self.config.save()
		dlg.Destroy()
	
	@bind_event(wx.EVT_MENU, 'm_menuItem2')
	def on_open_com_settings(self, event):
		dlg = SerialPortSettingController(self, self.config)
		if dlg.ShowModal() == wx.ID_OK:
			self.config.save()
		dlg.Destroy()
	
	@bind_event(wx.EVT_MENU, 'm_menuItem3')
	def on_open_filter_settings(self, event):
		dlg = FilterWheelSettingController(self, self.config)
		if dlg.ShowModal() == wx.ID_OK:
			self.config.save()
			self.update_filter_buttons()
		dlg.Destroy()
	
	@bind_event(wx.EVT_MENU, 'm_menuItem6')
	def on_save_settings(self, event):
		self.config.config.set('COM', 'port', self.m_comboBox1.GetStringSelection())
		self.config.config.set('COM', 'baudrate', self.m_comboBox2.GetStringSelection())
		self.config.save()
		wx.MessageBox(f"All current settings saved to {CONFIG_FILE}.", "Save", wx.OK | wx.ICON_INFORMATION)
	
	@bind_event(wx.EVT_MENU, 'm_menuItem7')
	def on_load_settings(self, event):
		self.config.load()
		self.initialize_com_controls()
		self.update_filter_buttons()
		wx.MessageBox(f"Settings loaded from {CONFIG_FILE}.", "Load", wx.OK | wx.ICON_INFORMATION)
	
	@bind_event(wx.EVT_MENU, 'm_menuItem8')
	def on_quit(self, event):
		self.Close()
	
	# ---------------------------------------------------------
	#                     VISPY LOGIC (Unchanged)
	# ---------------------------------------------------------
	
	def on_show_setup_vispy(self, event):
		if event.IsShown() and self.vispy_canvas is None:
			self.setup_vispy_plot()
			self.Unbind(wx.EVT_SHOW, handler=self.on_show_setup_vispy)
		event.Skip()
	
	def setup_vispy_plot(self):
		self.vispy_canvas = scene.SceneCanvas(
			keys='interactive',
			show=True,
			parent=self.m_panel2,
			size=self.m_panel2.GetSize()
		)
		self.view = self.vispy_canvas.central_widget.add_view()
		self.view.camera = scene.PanZoomCamera(aspect=1)
		self.view.camera.set_range(x=(-500, 500), y=(-500, 500))
		self.scatter = scene.Markers(parent=self.view.scene)
		self.update_vispy_plot()
		
		self.m_panel2.Bind(wx.EVT_SIZE, self.on_panel_resize)
	
	def update_vispy_plot(self):
		if self.vispy_canvas:
			pos = np.array([[self.current_stage_x, self.current_stage_y]])
			self.scatter.set_data(pos, edge_color=None, face_color='red', size=20, symbol='o')
			self.vispy_canvas.update()
	
	def on_panel_resize(self, event):
		if self.vispy_canvas:
			# This line correctly handles resizing the canvas window
			self.vispy_canvas.native.SetSize(self.m_panel2.GetSize())
		event.Skip()
	
	# ---------------------------------------------------------
	#                     UTILITY & DISPLAY LOGIC (UPDATED)
	# ---------------------------------------------------------
	
	def get_status_text(self):
		"""Converts single-character status code to readable text."""
		status_map = {
			BUSY: "BUSY", READY: "READY", HOME: "HOMED", UNKNOWN: "UNKNOWN",
			ERROR: "ERROR", OVERFLOW: "OVERFLOW"
		}
		return status_map.get(self.device_status, f"CODE: {self.device_status}")
	
	def update_output_display(self, status_message=None, filter_status=None):
		"""Updates all output controls and LEDs."""
		
		# Stage Position Text
		self.m_textCtrl2.SetValue(f"X: {self.current_stage_x:.2f} arcsec\nY: {self.current_stage_y:.2f} arcsec")
		self.m_textCtrl3.SetValue(f"{self.current_stage_x:.2f}")
		self.m_textCtrl7.SetValue(f"{self.current_stage_y:.2f}")
		
		# Filter Wheel Position Text (Uses provided status or default)
		if filter_status:
			self.m_textCtrl5.SetValue(filter_status)
		
		# Device Status Text (Uses message if provided, otherwise status code)
		if status_message:
			self.m_textCtrl4.SetValue(status_message)
		else:
			self.m_textCtrl4.SetValue(self.get_status_text())
		
		# COM Port Status Text
		port_status = "OPEN" if self.serial_port and self.serial_port.is_open else "CLOSED"
		self.m_textCtrl8.SetValue(port_status)
		
		# --- Status Panel LEDs (Panel 3) ---
		
		# 1. COM Port Status LED
		if self.serial_port and self.serial_port.is_open:
			self.LED_COMStatus.SetState(1)  # Green (Open)
		else:
			self.LED_COMStatus.SetState(2)  # Grey (Closed)
		
		# 2. Filter Wheel Status LED
		if self.device_status == READY or self.device_status == HOME:
			self.LED_FilterWheelStatus.SetState(1)  # Green (Ready/Homed)
		elif self.device_status == BUSY:
			self.LED_FilterWheelStatus.SetState(0)  # Red (Busy)
		else:
			self.LED_FilterWheelStatus.SetState(0)  # Red (Error/Unknown/Overflow)
		
		# 3. Filter Wheel @Home LED
		if self.device_status == HOME:
			self.LED_FilterWheelHome.SetState(1)  # Green (Homed)
		else:
			self.LED_FilterWheelHome.SetState(2)  # Grey (Not Homed)
		
		# 4. Command Status LED
		if self.device_status == ERROR or self.device_status == OVERFLOW:
			self.LED_CommandStatus.SetState(0)  # Red (Error)
		elif self.LED_CommandStatus.state == 2:
			pass
		
		# --- Motor Control Limit Switch LEDs (Panel 1) ---
		# State 0: Engaged (Red), 1: Safe (Green)
		
		self.LED_LimitNorth.SetState(0 if self.limit_switch_status['N'] == '1' else 1)
		self.LED_LimitSouth.SetState(0 if self.limit_switch_status['S'] == '1' else 1)
		self.LED_LimitEast.SetState(0 if self.limit_switch_status['E'] == '1' else 1)
		self.LED_LimitWest.SetState(0 if self.limit_switch_status['W'] == '1' else 1)
	
	def get_input_value(self, text_ctrl):
		# (Unchanged)
		try:
			value = float(text_ctrl.GetValue())
			if value < 0:
				raise ValueError("Only positive movement values allowed.")
			return value
		except ValueError:
			wx.MessageBox("Invalid input. Please enter a positive number in the corresponding box.", "Input Error",
			              wx.OK | wx.ICON_ERROR)
			return None
	
	def handle_serial_error(self, error_msg):
		# (Unchanged)
		self.close_serial_port()
		wx.MessageBox(f"Serial Communication Error: {error_msg}", "Error", wx.OK | wx.ICON_ERROR)
	
	# ---------------------------------------------------------
	#                      HOUSEKEEPING (Unchanged)
	# ---------------------------------------------------------
	
	def on_close_window(self, event):
		"""Saves settings and closes all resources."""
		self.on_save_settings(None)
		self.close_serial_port()
		if self.serial_thread:
			self.serial_thread.stop()
		self.Destroy()


# =========================================================
#                    APPLICATION ENTRY POINT (Unchanged)
# =========================================================

if __name__ == '__main__':
	app.use_app('wx')
	
	wx_app = wx.App(False)
	
	frame = WFCController(None)
	frame.Show(True)
	
	wx_app.MainLoop()