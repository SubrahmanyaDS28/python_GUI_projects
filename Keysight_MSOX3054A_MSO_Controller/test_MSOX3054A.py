import pyvisa
import matplotlib.pyplot as plt
import numpy as np


MSOX3054A_RESOURCE_STRING = 'USB0::0x0957::0x17A2::MY53100120::0::INSTR'
rm = pyvisa.ResourceManager()
osc = rm.open_resource(MSOX3054A_RESOURCE_STRING)
print(osc.query('*IDN?'))
print(osc.query('*ESR?'))

v_scale = float(osc.query(':CHANnel1:SCALe?').rstrip())
h_scale = float(osc.query(':TIMebase:SCALe?').rstrip())
print(osc.query(':MEASure:PERIod? CHANnel1'))
print(osc.query(':MEASure:VAVerage? CHANnel1'))
print(osc.query(':MEASure:FREQuency? CHANnel1'))
osc.write(":MEASure:CLEar")
print("COUNTER = ", osc.query(':MEASure:COUNter? CHANnel1'))
print("math = ", osc.query(":MEASure:VPP? MATH"))
print(osc.query(":MEASure:VPP? CHANnel4"))

# osc.write(":DIGitize CHANnel2")
osc.write('WAVeform:SOUrce MATH')
osc.write(':WAVeform:FORMat ASCii')
osc.write(":WAVeform:POINts 21844")
c = osc.query(':WAVeform:DATA?')

v_math_scale = float(osc.query(':FUNCtion:SCALe?').rstrip())
# h_math_scale = float(osc.query(':TIMebase:SCALe?').rstrip())

c = c.split(',')
volts=np.array([float(v) for v in c[1:]])
t = np.linspace(0, h_scale*10, 20832)
plt.plot(t, volts, '-o')
plt.ylim([-v_math_scale*4, v_math_scale*4])
plt.show()