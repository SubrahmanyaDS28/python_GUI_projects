import threading
import pyvisa
from pydispatch import dispatcher
import time

COMMAND_FREQUENCY = ":MEASure:COUNter? CHANnel1"

MSOX3054A_RESOURCE_STRING = 'USB0::0x0957::0x17A2::MY53100120::0::INSTR'

class MSOX3054A_OSC(threading.Thread):
	def __init__(self, readCallbackFunction=None, start = False):
		threading.Thread.__init__(self)
		self.rm = pyvisa.ResourceManager()
		self.device = None
		self.readExitFlag = False
		self.freq_response = None
		
		if readCallbackFunction:
			dispatcher.connect(readCallbackFunction, signal="DataReceive", sender=dispatcher.Any)
			self.readCallbackFunction = True
			
		if start:
			self.open()
		
	def open(self):
		try:
			self.device = self.rm.open_resource(MSOX3054A_RESOURCE_STRING)
		except Exception as e:
			print(f"Connection Failed: {e}")
			return e
		
		# print(self.device.query("*IDN?"))
		self.device.timeout = 5000
		return "Success"
	
	def send_command(self, command):
		self.device.write(command)
	
	def read_data(self):
		data = self.device.read()
		dispatcher.send("DataReceive", message=data)
		
	def query_command(self, command):
		data = self.device.query(command)
		dispatcher.send("DataReceive", message=data)
		
	def get_id(self):
		# print(self.rm.list_resources())
		data = self.device.query("*IDN?")
		return data
	
	def run(self):
		self.__start_read_thread()
		
	def __start_read_thread(self):
		while not self.readExitFlag:
			try:
				
				# 1. Get Data from Oscilloscope
				# Using the specific command you requested
				self.send_command(":MEASure:CLEar")
				counts = self.device.query(':MEASure:COUNter? CHANnel1')
				# freq_response = self.MSOX3054A.query(':MEASure:FREQuency? CHANnel1')
				# self.freq_response = int(float(raw_response))
				math_vpp = self.device.query(":MEASure:VPP? MATH")
				math_rms = self.device.query(":MEASure:VRMS? MATH")
				math_freq = self.device.query(":MEASure:FREQuency? MATH")
				n2e_vavg = self.device.query(":MEASure:VAVerage? CHANnel4")
				
				
				data = f"{counts.rstrip()},{math_vpp.rstrip()},{math_rms.rstrip()},{math_freq.rstrip()},{n2e_vavg.rstrip()}"
				print(data)
				if data is not None:
					dispatcher.send(signal="DataReceive", sender=self, message=data)
					self.freq_response = None
				
			except Exception as e:
				print("Error reading data: ", str(e))
				return str(e)
			
				
			time.sleep(1)
			
			
	def stop(self):
		self.readExitFlag = True