#!/usr/bin/python

import os
import rrdtool
import bmeall

 
try:
    # Read the current temperature
    #temp = sensor.read_temperature()
    # Read the current barometric pressure level
    #pressure = sensor.read_pressure()
	# added in my own code to read temp, press and humid via customer bmeall code
	reads = []
	reads = bmeall.readall()
	temp = reads['t']
	pressure = reads['p']
	humidity = reads['h']
	
except:
    sys.exit(-1)
 
# Calculate the ambient temperature
#cpu_temp = os.popen('vcgencmd measure_temp').readline()
#cpu_temp = cpu_temp.replace("temp=","")
#cpu_temp = cpu_temp.replace("'C\n","")
#cpu = float(cpu_temp)
#ambient = temp-((cpu-temp)/1.425)
 
# Set the altitude of your current location in meter
altitude = 68
psea = pressure / pow(1.0 - altitude/44330.0, 5.255)
psea = psea/100.0
 
# insert data into round-robin-database
#data = "N:%.2f:%.2f" % (ambient, psea)
#rrdtool.update("%s/pressure.rrd" % (os.path.dirname(os.path.abspath(__file__))), data)
print(temp)
print(pressure)
print(humidity)