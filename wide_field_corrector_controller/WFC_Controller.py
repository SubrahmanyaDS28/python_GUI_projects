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
import re

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
STATUS_COMMAND = 'Q'
HOME_COMMAND = 'H'

# --- Limit Switch Constants ---
LIMIT_SWITCH_STATUS_INDEX = 2


# =========================================================
#                     LED CONTROL CLASS
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
		
		w, h = self.GetSize()
		radius = int(min(w, h) / 2 - 2)
		center_x = int(w // 2)
		center_y = int(h // 2)
		
		color = self.colours[self.state % len(self.colours)]
		
		dc.SetBrush(wx.Brush(color))
		dc.SetPen(wx.Pen(color.ChangeLightness(50), 1))
		
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
		print("[INFO] Serial read thread started.")
		while self.keep_running:
			if self.serial_port and self.serial_port.is_open:
				try:
					data_bytes = self.serial_port.read_all()
					if data_bytes:
						data = data_bytes.decode('utf-8', errors='replace').strip()
						wx.CallAfter(self.parent_frame.handle_serial_data, data)
				except serial.SerialException as e:
					print(f"[ERROR] Serial error: {e}")
					wx.CallAfter(self.parent_frame.handle_serial_error, str(e))
				except Exception as e:
					print(f"[ERROR] Error in serial thread: {e}")
			
			time.sleep(SERIAL_READ_SLEEP_TIME)
		print("[INFO] Serial read thread stopped.")
	
	def stop(self):
		self.keep_running = False


# =========================================================
#                 CONFIGURATION MANAGER CLASS
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
		self.limit_switch_status = {'N': '0', 'S': '0', 'E': '0', 'W': '0'}
		
		# --- Timers ---
		self.status_timer = wx.Timer(self)
		
		# --- Initial GUI Setup ---
		self.initialize_com_controls()
		self.update_filter_buttons()
		self.setup_status_leds()
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
		Binds all decorated methods to their respective controls.
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
	#                     STATUS LED SETUP
	# ---------------------------------------------------------
	
	def setup_status_leds(self):
		fgSizer1 = wx.FlexGridSizer(0, 2, 0, 0)
		fgSizer1.AddGrowableCol(1)
		fgSizer1.SetFlexibleDirection(wx.BOTH)
		fgSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
		
		self.LED_FilterWheelStatus = LED(self.m_panel3)
		self.LED_FilterWheelHome = LED(self.m_panel3)
		self.LED_CommandStatus = LED(self.m_panel3)
		self.LED_COMStatus = LED(self.m_panel3)
		
		label_filter_status = wx.StaticText(self.m_panel3, wx.ID_ANY, u"Filter Wheel Status:   ", wx.DefaultPosition,
		                                    wx.DefaultSize, 0)
		label_filter_home = wx.StaticText(self.m_panel3, wx.ID_ANY, u"Filter Wheel @Home:   ", wx.DefaultPosition,
		                                  wx.DefaultSize, 0)
		label_command_status = wx.StaticText(self.m_panel3, wx.ID_ANY, u"Command Status: ", wx.DefaultPosition,
		                                     wx.DefaultSize, 0)
		label_com_status = wx.StaticText(self.m_panel3, wx.ID_ANY, u"COM Port: ", wx.DefaultPosition, wx.DefaultSize, 0)
		
		fgSizer1.Add(label_filter_status, 0, wx.ALL | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 5)
		fgSizer1.Add(self.LED_FilterWheelStatus, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
		fgSizer1.Add(label_filter_home, 0, wx.ALL | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 5)
		fgSizer1.Add(self.LED_FilterWheelHome, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
		fgSizer1.Add(label_command_status, 0, wx.ALL | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 5)
		fgSizer1.Add(self.LED_CommandStatus, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
		fgSizer1.Add(label_com_status, 0, wx.ALL | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 5)
		fgSizer1.Add(self.LED_COMStatus, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
		
		self.m_panel3.SetSizer(fgSizer1)
		fgSizer1.Fit(self.m_panel3)
		self.m_panel3.Layout()
	
	# ---------------------------------------------------------
	#                     MOTOR LIMIT LED SETUP
	# ---------------------------------------------------------
	
	def setup_motor_leds(self):
		self.LED_LimitNorth = LED(self.m_panel9)
		self.LED_LimitSouth = LED(self.m_panel9)
		self.LED_LimitEast = LED(self.m_panel9)
		self.LED_LimitWest = LED(self.m_panel9)
		
		CENTER_FLAG = wx.ALL | wx.ALIGN_CENTER_VERTICAL
		
		# Create a master vertical sizer for the panel
		main_v_sizer = wx.BoxSizer(wx.VERTICAL)
		
		# Safely add the existing title text to the top
		main_v_sizer.Add(self.m_staticText10, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
		
		# Create the GridBagSizer for the cross layout (added 5px gaps for breathing room)
		gbs = wx.GridBagSizer(5, 5)
		gbs.SetFlexibleDirection(wx.BOTH)
		gbs.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
		
		gbs.Add((0, 0), pos=(0, 2))
		gbs.Add((0, 0), pos=(2, 0))
		gbs.AddGrowableCol(0, 1)
		gbs.AddGrowableCol(2, 1)
		
		def make_h_sizer(ctrl, led, btn):
			h_sizer = wx.BoxSizer(wx.HORIZONTAL)
			h_sizer.Add(ctrl, 0, CENTER_FLAG, 5)
			h_sizer.Add(led, 0, CENTER_FLAG, 5)
			h_sizer.Add(btn, 0, CENTER_FLAG, 5)
			return h_sizer
		
		h_north = make_h_sizer(self.m_textCtrl22, self.LED_LimitNorth, self.m_button4)
		gbs.Add(h_north, pos=(0, 1), flag=wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, border=5)
		
		h_south = make_h_sizer(self.m_textCtrl25, self.LED_LimitSouth, self.m_button7)
		gbs.Add(h_south, pos=(2, 1), flag=wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, border=5)
		
		h_west = make_h_sizer(self.m_textCtrl23, self.LED_LimitWest, self.m_button5)
		gbs.Add(h_west, pos=(1, 0), flag=CENTER_FLAG | wx.ALIGN_RIGHT, border=5)
		
		h_east = make_h_sizer(self.m_textCtrl24, self.LED_LimitEast, self.m_button6)
		gbs.Add(h_east, pos=(1, 2), flag=CENTER_FLAG | wx.ALIGN_LEFT, border=5)
		
		gbs.Add((0, 0), pos=(1, 1))
		
		# Add the cross layout below the text
		main_v_sizer.Add(gbs, 1, wx.EXPAND | wx.ALL, 5)
		
		# Clear the old broken sizer and apply the new master sizer
		old_sizer = self.m_panel9.GetSizer()
		if old_sizer:
			self.m_panel9.SetSizer(None)
		
		self.m_panel9.SetSizer(main_v_sizer)
		self.m_panel9.Layout()
		self.Layout()
	
	# ---------------------------------------------------------
	#                     SERIAL COMMUNICATION
	# ---------------------------------------------------------
	
	def initialize_com_controls(self):
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
		print("\n[ACTION] Attempting to Toggle COM Port...")
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
				self.serial_port = serial.Serial(port=port, baudrate=baud, timeout=timeout)
				if self.serial_port.is_open:
					self.serial_thread = SerialReadThread(self.serial_port, self)
					self.serial_thread.start()
					self.status_timer.Start(DEVICE_STATUS_POLL_MS)
					
					self.m_button1.SetLabel("CLOSE COM PORT")
					self.m_button1.SetBackgroundColour(wx.Colour(255, 100, 100))
					print(f"[SUCCESS] Serial port {port}@{baud} opened.")
					self.update_output_display(status_message="COM Port Open.")
			
			except serial.SerialException as e:
				wx.MessageBox(f"Failed to open port {port}: {e}", "Serial Error", wx.OK | wx.ICON_ERROR)
				self.serial_port = None
				print(f"[FAIL] Failed to open port {port}: {e}")
				self.update_output_display(status_message=f"COM Port Failed: {e}")
	
	def close_serial_port(self):
		print("[ACTION] Closing COM Port...")
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
		print("[SUCCESS] Serial port closed.")
	
	def execute_command(self, command, args=""):
		if not (self.serial_port and self.serial_port.is_open):
			print(f"[WARNING] Attempted to send '{command}{args}' but COM port is closed.")
			wx.MessageBox("COM Port is not open.", "Command Failed", wx.OK | wx.ICON_WARNING)
			return False
		
		full_command = f"{STx}{command}{args}{ETx}\n"
		
		try:
			with threading.Lock():
				self.serial_port.write(full_command.encode('ascii'))
				print(f">>> TX: {full_command.strip()}")
			return True
		except serial.SerialException as e:
			print(f"[ERROR] Failed to send TX: {e}")
			self.update_output_display(status_message=f"TX Failed: {e}")
			return False
	
	def parse_limit_switch_data(self, data):
		self.limit_switch_status['N'] = '0'
		self.limit_switch_status['S'] = '0'
		self.limit_switch_status['E'] = '0'
		self.limit_switch_status['W'] = '0'
		
		limit_detected = False
		if '~N' in data:
			self.limit_switch_status['N'] = '1'
			limit_detected = True
		if '~S' in data:
			self.limit_switch_status['S'] = '1'
			limit_detected = True
		if '~E' in data:
			self.limit_switch_status['E'] = '1'
			limit_detected = True
		if '~W' in data:
			self.limit_switch_status['W'] = '1'
			limit_detected = True
		
		if limit_detected:
			print(f"[LIMIT] Switch engaged: {self.limit_switch_status}")
			return True
		return False
	
	def handle_serial_data(self, data):
		# Optional: Commenting out the raw RX print so it doesn't flood your console every 500ms
		print(f"<<< RX: {data}")
		
		self.LED_CommandStatus.SetState(1)
		wx.CallLater(100, lambda: self.LED_CommandStatus.SetState(2))
		
		# --- BUG 1 FIX: Filter out echoed commands (like *Z#) ---
		# This removes everything between '*' and '#' so echoes don't trigger limits
		clean_data = re.sub(r'\*.*?\#', '', data)
		
		# --- Catch Motor Counts from 'Q' Command ---
		if 'Q:' in data:
			try:
				# Extract the part after 'Q:' and before any other characters (like the ACK '^')
				counts_part = data.split('Q:')[1].split('^')[0].split('#')[0]
				counts = counts_part.split(',')
				
				if len(counts) == 2:
					motor_a_val = int(counts[0])
					motor_b_val = int(counts[1])
					
					# Sync the GUI positions with the REAL hardware counts!
					self.current_stage_x = motor_a_val * ARCSEC_TO_UNITS
					self.current_stage_y = motor_b_val * ARCSEC_TO_UNITS
					
					self.update_output_display()
					self.update_vispy_plot()
					
			except Exception as e:
				print(f"[ERROR] Failed to parse counts from Q command: {e}")
		
		# --- Catch hardware limit switch triggers ---
		if 'Y' in clean_data:
			print("\n[HARDWARE LIMIT] West limit switch hit!")
			self.limit_switch_status['W'] = '1'  # 1 = Engaged/Red
			self.update_output_display()
		
		if 'Z' in clean_data:
			print("\n[HARDWARE LIMIT] South limit switch hit!")
			self.limit_switch_status['S'] = '1'  # 1 = Engaged/Red
			self.update_output_display()
		
		if 'X' in clean_data:
			print("\n[HARDWARE LIMIT] East limit switch hit!")
			self.limit_switch_status['E'] = '1'  # 1 = Engaged/Red
			self.update_output_display()
		
		if 'W' in clean_data:
			print("\n[HARDWARE LIMIT] North limit switch hit!")
			self.limit_switch_status['N'] = '1'  # 1 = Engaged/Red
			self.update_output_display()
		
		limit_symbols_present = any(symbol in data for symbol in ('~N', '~S', '~E', '~W'))
		
		if limit_symbols_present and not (data.startswith(ACK) or data.startswith(NAK)):
			if self.device_status == UNKNOWN:
				self.device_status = READY
			self.parse_limit_switch_data(data)
			self.update_output_display()
			return
		
		if data.startswith(ACK) or data.startswith(NAK):
			response_code = data[1] if len(data) > 1 else ' '
			if response_code in [BUSY, READY, HOME, UNKNOWN, ERROR, OVERFLOW]:
				self.device_status = response_code
				self.parse_limit_switch_data(data)
				self.update_output_display()
				if response_code == ERROR:
					wx.MessageBox(f"Device reported ERROR: {data}", "Device Error", wx.OK | wx.ICON_ERROR)
	
	@bind_event(wx.EVT_TIMER, 'status_timer')
	def on_status_timer(self, event):
		# Commenting out the print for status timer to avoid flooding the console
		# print("[POLL] Sending Status Command")
		self.execute_command(STATUS_COMMAND)
	
	# ---------------------------------------------------------
	#                     MOVEMENT HANDLERS
	# ---------------------------------------------------------
	
	# def check_limit_safe(self, direction):
	# 	status = self.limit_switch_status.get(direction)
	# 	if status == '0':
	# 		if self.limit_switch_status.get(direction) == '1':
	# 			print(f"[BLOCKED] {direction} Limit Switch Engaged. Cannot move further {direction}.")
	# 			wx.MessageBox(f"{direction} Limit Switch Engaged. Cannot move further {direction}.",
	# 			              "Movement Blocked", wx.OK | wx.ICON_WARNING)
	# 			return False
	# 		return True
	# 	return True
		
		# ---------------------------------------------------------
		#                     MOVEMENT HANDLERS
		# ---------------------------------------------------------
		
	def check_limit_safe(self, direction):
		status = self.limit_switch_status.get(direction)
		# If the status is '1', the limit switch is engaged/blocked.
		if status == '1':
			print(f"[BLOCKED] {direction} Limit Switch Engaged.")
			wx.MessageBox(f"{direction} Limit Switch Engaged. Cannot move further {direction}.",
			              "Movement Blocked", wx.OK | wx.ICON_WARNING)
			return False
		return True
	
	@bind_event(wx.EVT_BUTTON, 'm_button4')
	def on_move_north(self, event):
		print("\n[GUI ACTION] 'North' step button clicked.")
		if not self.check_limit_safe('N'): return
		move_arcsec = self.get_input_value(self.m_textCtrl22)
		if move_arcsec is not None:
			step_counts = int(move_arcsec)
			if self.execute_command('1', str(step_counts)):
				self.limit_switch_status['S'] = '0'  # Clear South Limit LED
				self.update_output_display(status_message=f"Step N {step_counts}")
	
	@bind_event(wx.EVT_BUTTON, 'm_button5')
	def on_move_west(self, event):
		print("\n[GUI ACTION] 'West' step button clicked.")
		if not self.check_limit_safe('W'): return
		move_arcsec = self.get_input_value(self.m_textCtrl23)
		if move_arcsec is not None:
			step_counts = int(move_arcsec)
			if self.execute_command('4', str(step_counts)):
				self.limit_switch_status['E'] = '0'  # Clear East Limit LED
				self.update_output_display(status_message=f"Step W {step_counts}")
	
	@bind_event(wx.EVT_BUTTON, 'm_button6')
	def on_move_east(self, event):
		print("\n[GUI ACTION] 'East' step button clicked.")
		if not self.check_limit_safe('E'): return
		move_arcsec = self.get_input_value(self.m_textCtrl24)
		if move_arcsec is not None:
			step_counts = int(move_arcsec)
			if self.execute_command('3', str(step_counts)):
				self.limit_switch_status['W'] = '0'  # Clear West Limit LED
				self.update_output_display(status_message=f"Step E {step_counts}")
	
	@bind_event(wx.EVT_BUTTON, 'm_button7')
	def on_move_south(self, event):
		print("\n[GUI ACTION] 'South' step button clicked.")
		if not self.check_limit_safe('S'): return
		move_arcsec = self.get_input_value(self.m_textCtrl25)
		if move_arcsec is not None:
			step_counts = int(move_arcsec)
			if self.execute_command('2', str(step_counts)):
				self.limit_switch_status['N'] = '0'  # Clear North Limit LED
				self.update_output_display(status_message=f"Step S {step_counts}")
	
	@bind_event(wx.EVT_BUTTON, 'm_button2')
	def on_initial_position(self, event):
		print("\n[GUI ACTION] 'INITIAL POSITION' button clicked.")
		if self.execute_command('Z'):
			self.current_stage_x = 0.0
			self.current_stage_y = 0.0
			self.update_vispy_plot()
			self.update_output_display(status_message="Motor Homing/Initial Position Initiated")
	
	@bind_event(wx.EVT_BUTTON, 'm_button3')
	def on_center_position(self, event):
		print("\n[GUI ACTION] 'CENTER POSITION' button clicked.")
		if self.execute_command('c'):
			# Moving to the safe center zone, so clear all limit LEDs!
			self.limit_switch_status['N'] = '0'
			self.limit_switch_status['S'] = '0'
			self.limit_switch_status['E'] = '0'
			self.limit_switch_status['W'] = '0'
			self.update_output_display(status_message="Move to Center Position Initiated")
	
	@bind_event(wx.EVT_BUTTON, 'm_button25')
	def on_parking_position(self, event):
		print("\n[GUI ACTION] 'PARKING POSITION' button clicked.")
		if self.execute_command('P'):
			# Moving to the safe parking zone, so clear all limit LEDs!
			self.limit_switch_status['N'] = '0'
			self.limit_switch_status['S'] = '0'
			self.limit_switch_status['E'] = '0'
			self.limit_switch_status['W'] = '0'
			self.update_output_display(status_message="Moving to Parking Position Initiated")
	
	@bind_event(wx.EVT_BUTTON, 'm_button31')
	def on_stop_motors(self, event):
		print("\n[GUI ACTION] 'STOP MOTORS' button clicked.")
		if self.execute_command('S'):
			# Force all software limits off just in case
			self.update_output_display(status_message="ALL MOTORS STOPPED")
	# ---------------------------------------------------------
	#            CONTINUOUS MOVEMENT HANDLERS (NEW)
	# ---------------------------------------------------------
	# --- EAST ---
	@bind_event(wx.EVT_LEFT_DOWN, 'm_button21')
	def on_press_east(self, event):
		print("\n[GUI ACTION] 'East' button pressed.")
		if not self.check_limit_safe('E'): return
		if self.execute_command('A'):
			# We are moving East, so the West limit is now safe!
			self.limit_switch_status['W'] = '0'
			self.update_output_display(status_message="Moving East (Continuous)...")
		event.Skip()
	
	@bind_event(wx.EVT_LEFT_UP, 'm_button21')
	def on_release_east(self, event):
		print("\n[GUI ACTION] 'East' button released.")
		if self.execute_command('S'):
			self.update_output_display(status_message="Stopped East.")
		event.Skip()
	
	# --- WEST ---
	@bind_event(wx.EVT_LEFT_DOWN, 'm_button22')
	def on_press_west(self, event):
		print("\n[GUI ACTION] 'West' button pressed.")
		if not self.check_limit_safe('W'): return
		if self.execute_command('B'):
			# We are moving West, so the East limit is now safe!
			self.limit_switch_status['E'] = '0'
			self.update_output_display(status_message="Moving West (Continuous)...")
		event.Skip()
	
	@bind_event(wx.EVT_LEFT_UP, 'm_button22')
	def on_release_west(self, event):
		print("\n[GUI ACTION] 'West' button released.")
		if self.execute_command('S'):
			self.update_output_display(status_message="Stopped West.")
		event.Skip()
	
	# --- NORTH ---
	@bind_event(wx.EVT_LEFT_DOWN, 'm_button23')
	def on_press_north(self, event):
		print("\n[GUI ACTION] 'North' button pressed.")
		if not self.check_limit_safe('N'): return
		if self.execute_command('C'):
			# We are moving North, so the South limit is now safe!
			self.limit_switch_status['S'] = '0'
			self.update_output_display(status_message="Moving North (Continuous)...")
		event.Skip()
	
	@bind_event(wx.EVT_LEFT_UP, 'm_button23')
	def on_release_north(self, event):
		print("\n[GUI ACTION] 'North' button released.")
		if self.execute_command('S'):
			self.update_output_display(status_message="Stopped North.")
		event.Skip()
	
	# --- SOUTH ---
	@bind_event(wx.EVT_LEFT_DOWN, 'm_button24')
	def on_press_south(self, event):
		print("\n[GUI ACTION] 'South' button pressed.")
		if not self.check_limit_safe('S'): return
		if self.execute_command('D'):
			# We are moving South, so the North limit is now safe!
			self.limit_switch_status['N'] = '0'
			self.update_output_display(status_message="Moving South (Continuous)...")
		event.Skip()
	
	@bind_event(wx.EVT_LEFT_UP, 'm_button24')
	def on_release_south(self, event):
		print("\n[GUI ACTION] 'South' button released.")
		if self.execute_command('S'):
			self.update_output_display(status_message="Stopped South.")
		event.Skip()
		
	# ---------------------------------------------------------
	#                     SPEED TOGGLE HANDLERS (NEW)
	# ---------------------------------------------------------
	
	@bind_event(wx.EVT_TOGGLEBUTTON, 'm_toggleBtn1')
	def on_toggle_fast(self, event):
		# If Fast was just pressed ON
		if self.m_toggleBtn1.GetValue():
			self.m_toggleBtn2.SetValue(False)  # Visually pop up the Slow button
			print("\n[GUI ACTION] 'Fast' speed selected.")
			if self.execute_command('f'):
				self.update_output_display(status_message="Speed set to Fast.")
		else:
			# If the user tries to turn off Fast, default back to Slow
			self.m_toggleBtn2.SetValue(True)
			print("\n[GUI ACTION] Reverting to 'Slow' speed.")
			if self.execute_command('s'):
				self.update_output_display(status_message="Speed set to Slow.")
	
	@bind_event(wx.EVT_TOGGLEBUTTON, 'm_toggleBtn2')
	def on_toggle_slow(self, event):
		# If Slow was just pressed ON
		if self.m_toggleBtn2.GetValue():
			self.m_toggleBtn1.SetValue(False)  # Visually pop up the Fast button
			print("\n[GUI ACTION] 'Slow' speed selected.")
			if self.execute_command('s'):
				self.update_output_display(status_message="Speed set to Slow.")
		else:
			# If the user tries to turn off Slow, default back to Fast
			self.m_toggleBtn1.SetValue(True)
			print("\n[GUI ACTION] Reverting to 'Fast' speed.")
			if self.execute_command('f'):
				self.update_output_display(status_message="Speed set to Fast.")
				
	# ---------------------------------------------------------
	#                     FILTER HANDLERS
	# ---------------------------------------------------------
	
	def update_filter_buttons(self):
		filter_buttons = [self.m_button10, self.m_button11, self.m_button12, self.m_button13]
		name_keys = ['name_1', 'name_2', 'name_3', 'name_4']
		
		for button in filter_buttons:
			button.Unbind(wx.EVT_BUTTON)
		
		for i, button in enumerate(filter_buttons):
			name = self.config.get('FILTER', name_keys[i])
			button.SetLabel(name)
			button.Bind(wx.EVT_BUTTON, lambda evt, idx=i + 1: self.on_select_filter(evt, idx))
	
	def on_select_filter(self, event, filter_index):
		filter_name = self.config.get('FILTER', f'name_{filter_index}')
		print(f"\n[GUI ACTION] Filter {filter_index} ({filter_name}) selected.")
		if self.execute_command('f', str(filter_index)):
			self.update_output_display(filter_status=filter_name)
	
	# ---------------------------------------------------------
	#                     MENU HANDLERS
	# ---------------------------------------------------------
	
	@bind_event(wx.EVT_MENU, 'm_menuItem1')
	def on_open_motor_settings(self, event):
		print("[GUI ACTION] Opened Motor Settings.")
		dlg = MotorControlSettingController(self, self.config)
		if dlg.ShowModal() == wx.ID_OK:
			self.config.save()
		dlg.Destroy()
	
	@bind_event(wx.EVT_MENU, 'm_menuItem2')
	def on_open_com_settings(self, event):
		print("[GUI ACTION] Opened COM Settings.")
		dlg = SerialPortSettingController(self, self.config)
		if dlg.ShowModal() == wx.ID_OK:
			self.config.save()
		dlg.Destroy()
	
	@bind_event(wx.EVT_MENU, 'm_menuItem3')
	def on_open_filter_settings(self, event):
		print("[GUI ACTION] Opened Filter Settings.")
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
		print("[ACTION] Settings Saved.")
		wx.MessageBox(f"All current settings saved to {CONFIG_FILE}.", "Save", wx.OK | wx.ICON_INFORMATION)
	
	@bind_event(wx.EVT_MENU, 'm_menuItem7')
	def on_load_settings(self, event):
		self.config.load()
		self.initialize_com_controls()
		self.update_filter_buttons()
		print("[ACTION] Settings Loaded.")
		wx.MessageBox(f"Settings loaded from {CONFIG_FILE}.", "Load", wx.OK | wx.ICON_INFORMATION)
	
	@bind_event(wx.EVT_MENU, 'm_menuItem8')
	def on_quit(self, event):
		print("[ACTION] Quitting Application...")
		self.Close()
	
	# ---------------------------------------------------------
	#                     VISPY LOGIC
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
			size=self.m_panel2.GetSize(),
			bgcolor='black'  # Dark theme provides better contrast for the red dot
		)
		self.view = self.vispy_canvas.central_widget.add_view()
		self.view.camera = scene.PanZoomCamera(aspect=1)
		
		# Expand the camera range so the 100,000 center point is visible
		self.view.camera.set_range(x=(-10000, 210000), y=(-10000, 210000))
		
		# --- VISUAL HELPERS ---
		# 1. Permanent Center Crosshair
		CENTER_X, CENTER_Y = 100000, 100000
		
		self.center_marker = scene.Markers(parent=self.view.scene)
		self.center_marker.set_data(np.array([[CENTER_X, CENTER_Y]]), edge_color='green', face_color='green', size=20,
		                            symbol='+')
		
		# 2. Draw the 70710 Radius Boundary Circle
		radius = 70710
		theta = np.linspace(0, 2 * np.pi, 200)  # Generate 200 points for a smooth circle
		circle_x = CENTER_X + radius * np.cos(theta)
		circle_y = CENTER_Y + radius * np.sin(theta)
		circle_points = np.column_stack((circle_x, circle_y))
		
		# Draw it as a faint blue line
		self.boundary_circle = scene.Line(pos=circle_points, color=(0.3, 0.5, 1.0, 0.7), width=2,
		                                  parent=self.view.scene)
		
		# 3. Stage Path History (A faint trailing line showing where the stage has been)
		self.path_history = []
		self.path_line = scene.Line(parent=self.view.scene, color=(1, 0.3, 0.3, 0.6), width=2)
		
		# 4. Current Stage Position (The moving Red Dot)
		self.scatter = scene.Markers(parent=self.view.scene)
		
		self.update_vispy_plot()
		self.m_panel2.Bind(wx.EVT_SIZE, self.on_panel_resize)
	
	def update_vispy_plot(self):
		if self.vispy_canvas:
			pos = np.array([[self.current_stage_x, self.current_stage_y]])
			
			# Update the red dot's current position
			self.scatter.set_data(pos, edge_color='white', face_color='red', size=15, symbol='o')
			
			# Update the trailing line history to track movement
			if not self.path_history or self.path_history[-1] != [self.current_stage_x, self.current_stage_y]:
				self.path_history.append([self.current_stage_x, self.current_stage_y])
				
				# Keep only the last 200 coordinates to prevent memory lag over long sessions
				if len(self.path_history) > 200:
					self.path_history.pop(0)
				
				# Vispy Line requires at least 2 points to draw
				if len(self.path_history) > 1:
					self.path_line.set_data(np.array(self.path_history))
			
			self.vispy_canvas.update()
	
	def on_panel_resize(self, event):
		if self.vispy_canvas:
			self.vispy_canvas.native.SetSize(self.m_panel2.GetSize())
		event.Skip()
	
	# ---------------------------------------------------------
	#                     UTILITY & DISPLAY LOGIC
	# ---------------------------------------------------------
	
	def get_status_text(self):
		status_map = {
			BUSY: "BUSY", READY: "READY", HOME: "HOMED", UNKNOWN: "UNKNOWN",
			ERROR: "ERROR", OVERFLOW: "OVERFLOW"
		}
		return status_map.get(self.device_status, f"CODE: {self.device_status}")
	
	def update_output_display(self, status_message=None, filter_status=None):
		
		# --- Output Text Fields ---
		self.m_textCtrl3.SetValue(f"{self.current_stage_x:.2f}")
		self.m_textCtrl7.SetValue(f"{self.current_stage_y:.2f}")
		
		if filter_status:
			self.m_textCtrl5.SetValue(filter_status)
		
		# --- Update the Main Window Status Bar ---
		# If a new action happened, save it and show it
		if status_message:
			self.last_action_message = status_message
			self.m_statusBar1.SetStatusText(status_message)
		# If this is just a 500ms background update, keep the old message alive!
		elif hasattr(self, 'last_action_message'):
			self.m_statusBar1.SetStatusText(self.last_action_message)
		else:
			self.m_statusBar1.SetStatusText("Ready")
		
		port_status = "OPEN" if self.serial_port and self.serial_port.is_open else "CLOSED"
		self.m_textCtrl8.SetValue(port_status)
		
		# --- Status Panel LEDs (Panel 3) ---
		if self.serial_port and self.serial_port.is_open:
			self.LED_COMStatus.SetState(1)
		else:
			self.LED_COMStatus.SetState(2)
		
		# Since your PIC relies on limits and manual stops, we keep the main status Green unless there's an explicit serial error
		if self.device_status == ERROR or self.device_status == OVERFLOW:
			self.LED_CommandStatus.SetState(0)
			self.LED_FilterWheelStatus.SetState(0)
		else:
			self.LED_FilterWheelStatus.SetState(1)
		
		# --- Motor Control Limit Switch LEDs (Panel 1) ---
		self.LED_LimitNorth.SetState(0 if self.limit_switch_status['N'] == '1' else 1)
		self.LED_LimitSouth.SetState(0 if self.limit_switch_status['S'] == '1' else 1)
		self.LED_LimitEast.SetState(0 if self.limit_switch_status['E'] == '1' else 1)
		self.LED_LimitWest.SetState(0 if self.limit_switch_status['W'] == '1' else 1)
	
	def get_input_value(self, text_ctrl):
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
		self.close_serial_port()
		wx.MessageBox(f"Serial Communication Error: {error_msg}", "Error", wx.OK | wx.ICON_ERROR)
	
	# ---------------------------------------------------------
	#                      HOUSEKEEPING
	# ---------------------------------------------------------
	
	def on_close_window(self, event):
		self.on_save_settings(None)
		self.close_serial_port()
		if self.serial_thread:
			self.serial_thread.stop()
		self.Destroy()


# =========================================================
#                    APPLICATION ENTRY POINT
# =========================================================

if __name__ == '__main__':
	app.use_app('wx')
	
	wx_app = wx.App(False)
	
	frame = WFCController(None)
	frame.Show(True)
	
	wx_app.MainLoop()