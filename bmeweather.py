# -*- coding: utf-8 -*-
import sys
import time
import bme280
import rrdtool
import requests
import feedparser
import os
import shutil
import datetime

def zambretti():
    # Filtering the pressure change by using the average from different periods should give better, more stable results
    # Read the pressure values for now/t=0, t=-0.5h, t=-1.0h, t=-1.5h, t=-2.0h, t=-2.5h, t=-3.0h, t=-3.5h, t=-4.0h, t=-4.5h, t=-5.0h, t=-5.5h and t=-6.0h
    press0 = rrdtool.fetch("/home/dietpi/pyweather/climate_data.rrd", 'AVERAGE', '-s -1800')
    press1 = rrdtool.fetch("/home/dietpi/pyweather/climate_data.rrd", 'AVERAGE', '-s -3600', '-e -3600')
    press2 = rrdtool.fetch("/home/dietpi/pyweather/climate_data.rrd", 'AVERAGE', '-s -5400', '-e -5400')
    press3 = rrdtool.fetch("/home/dietpi/pyweather/climate_data.rrd", 'AVERAGE', '-s -7200', '-e -7200')
    press4 = rrdtool.fetch("/home/dietpi/pyweather/climate_data.rrd", 'AVERAGE', '-s -9000', '-e -9000')
    press5 = rrdtool.fetch("/home/dietpi/pyweather/climate_data.rrd", 'AVERAGE', '-s -10800', '-e -10800')
    press6 = rrdtool.fetch("/home/dietpi/pyweather/climate_data.rrd", 'AVERAGE', '-s -12600', '-e -12600')
    press7 = rrdtool.fetch("/home/dietpi/pyweather/climate_data.rrd", 'AVERAGE', '-s -14400', '-e -14400')
    press8 = rrdtool.fetch("/home/dietpi/pyweather/climate_data.rrd", 'AVERAGE', '-s -16200', '-e -16200')
    press9 = rrdtool.fetch("/home/dietpi/pyweather/climate_data.rrd", 'AVERAGE', '-s -18000', '-e -18000')
    press10 = rrdtool.fetch("/home/dietpi/pyweather/climate_data.rrd", 'AVERAGE', '-s -19800', '-e -19800')
    press11 = rrdtool.fetch("/home/dietpi/pyweather/climate_data.rrd", 'AVERAGE', '-s -21600', '-e -21600')
    press12 = rrdtool.fetch("/home/dietpi/pyweather/climate_data.rrd", 'AVERAGE', '-s -23400', '-e -23400')
    # Calculate the single differences and normalize them to a change in pressure over 1h
    pressurerdiff1 = (press0[2][0][3] - press1[2][0][3])*2
    pressurerdiff2 = (press0[2][0][3] - press2[2][0][3])
    pressurerdiff3 = (press0[2][0][3] - press3[2][0][3])/1.5
    pressurerdiff4 = (press0[2][0][3] - press4[2][0][3])/2
    pressurerdiff5 = (press0[2][0][3] - press5[2][0][3])/2.5
    pressurerdiff6 = (press0[2][0][3] - press6[2][0][3])/3
    pressurerdiff7 = (press0[2][0][3] - press7[2][0][3])/3.5
    pressurerdiff8 = (press0[2][0][3] - press8[2][0][3])/4
    pressurerdiff9 = (press0[2][0][3] - press9[2][0][3])/4.5
    pressurerdiff10 = (press0[2][0][3] - press10[2][0][3])/5
    pressurerdiff11 = (press0[2][0][3] - press11[2][0][3])/5.5
    pressurerdiff12 = (press0[2][0][3] - press12[2][0][3])/6
     
    # Calculate the average of the differences
    pressurerdiff = (pressurerdiff1 + pressurerdiff2 + pressurerdiff3 + pressurerdiff4 + pressurerdiff5 + pressurerdiff6 + pressurerdiff7 + pressurerdiff8 + pressurerdiff9 + pressurerdiff10 + pressurerdiff11 + pressurerdiff12)/12
    # Get the current pressure
    currentpress = press0[2][0][3]
    # Calculate the trend
    # The internet says for the UK 1.25 may work better
    if pressurerdiff < -0.25:
        trend = -1
    elif pressurerdiff >= -0.25 and pressurerdiff <= 0.25:
        trend = 0
    elif pressurerdiff > 0.25:
        trend = 1
    # Get the current month
    today = datetime.date.today()
    date = datetime.datetime.strptime(str(today), "%Y-%m-%d")
    month = int(date.month)
    # Use the Zambretti-algorithm to finally make the forecast
    # --------------------------------------------------------
    # Falling Conditions
    # ------------------
    if trend == -1:
        #shutil.copyfile('/home/pi/pressure_info/DownRight.png', '/var/www/html/Arrow.png')
        zambretti = 0.0009746*currentpress*currentpress-2.1068*currentpress+1138.7019
        if month < 4 | month > 9:
            zambretti = zambretti + 1
        zambretti = int(round(zambretti))
        forecast = 'Error getting forecast'
        if zambretti <= 0:
            forecast = 'Settled Fine'
            #shutil.copyfile('/home/pi/pressure_info/Sun.png', '/var/www/html/Forecast.png')
        elif zambretti == 1:
            forecast = 'Settled Fine'
            #shutil.copyfile('/home/pi/pressure_info/Sun.png', '/var/www/html/Forecast.png')
        elif zambretti == 2:
            forecast = 'Fine Weather'
            #shutil.copyfile('/home/pi/pressure_info/Sun.png', '/var/www/html/Forecast.png')
        elif zambretti == 3:
            forecast = 'Fine Becoming Less Settled'
            #shutil.copyfile('/home/pi/pressure_info/SunCloud.png', '/var/www/html/Forecast.png')
        elif zambretti == 4:
            forecast = 'Fairly Fine Showers Later'
            #shutil.copyfile('/home/pi/pressure_info/SunCloud.png', '/var/www/html/Forecast.png')
        elif zambretti == 5:
            forecast = 'Showery Becoming unsettled'
            #shutil.copyfile('/home/pi/pressure_info/SunCloud.png', '/var/www/html/Forecast.png')
        elif zambretti == 6:
            forecast = 'Unsettled, Rain later'
            #shutil.copyfile('/home/pi/pressure_info/Rain.png', '/var/www/html/Forecast.png')
        elif zambretti == 7:
            forecast = 'Rain at times, worse later'
            #shutil.copyfile('/home/pi/pressure_info/Rain.png', '/var/www/html/Forecast.png')
        elif zambretti == 8:
            forecast = 'Rain at times, becoming very unsettled'
            #shutil.copyfile('/home/pi/pressure_info/Rain.png', '/var/www/html/Forecast.png')
        elif zambretti == 9:
            forecast = 'Very Unsettled, Rain'
            #shutil.copyfile('/home/pi/pressure_info/Rain.png', '/var/www/html/Forecast.png')
        return forecast
    # Steady Conditions
    # -----------------
    elif trend == 0:
        #shutil.copyfile('/home/pi/pressure_info/Right.png', '/var/www/html/Arrow.png')
        zambretti = 138.24-0.133*currentpress
        zambretti = int(round(zambretti))
        forecast = 'Error getting forecast'
        if zambretti <= 0:
            forecast = 'Settled Fine'
            #shutil.copyfile('/home/pi/pressure_info/Sun.png', '/var/www/html/Forecast.png')
        elif zambretti == 1:
            forecast = 'Settled Fine'
            #shutil.copyfile('/home/pi/pressure_info/Sun.png', '/var/www/html/Forecast.png')
        elif zambretti == 2:
            forecast = 'Fine Weather'
            #shutil.copyfile('/home/pi/pressure_info/Sun.png', '/var/www/html/Forecast.png')
        elif zambretti == 3:
            forecast = 'Fine, Possibly showers'
            #shutil.copyfile('/home/pi/pressure_info/SunCloud.png', '/var/www/html/Forecast.png')
        elif zambretti == 4:
            forecast = 'Fairly Fine, Showers likely'
            #shutil.copyfile('/home/pi/pressure_info/SunCloud.png', '/var/www/html/Forecast.png')
        elif zambretti == 5:
            forecast = 'Showery Bright Intervals'
            #shutil.copyfile('/home/pi/pressure_info/SunCloud.png', '/var/www/html/Forecast.png')
        elif zambretti == 6:
            forecast = 'Changeable some rain'
            #shutil.copyfile('/home/pi/pressure_info/SunCloud.png', '/var/www/html/Forecast.png')
        elif zambretti == 7:
            forecast = 'Unsettled, rain at times'
            #shutil.copyfile('/home/pi/pressure_info/Rain.png', '/var/www/html/Forecast.png')
        elif zambretti == 8:
            forecast = 'Rain at Frequent Intervals'
            #shutil.copyfile('/home/pi/pressure_info/Rain.png', '/var/www/html/Forecast.png')
        elif zambretti == 9:
            forecast = 'Very Unsettled, Rain'
            #shutil.copyfile('/home/pi/pressure_info/Rain.png', '/var/www/html/Forecast.png')
        elif zambretti == 10:
            forecast = 'Stormy, much rain'
           # shutil.copyfile('/home/pi/pressure_info/Storm.png', '/var/www/html/Forecast.png'))
        return forecast
    # Rising Conditions
    # -----------------
    elif trend == 1:
        #shutil.copyfile('/home/pi/pressure_info/UpRight.png', '/var/www/html/Arrow.png')
        zambretti = 142.57-0.1376*currentpress
        if month < 4 | month > 9:
            zambretti = zambretti + 1
        zambretti = int(round(zambretti))
        forecast = 'Error getting forecast'
        if zambretti <= 0:
            forecast = 'Settled Fine'
            #shutil.copyfile('/home/pi/pressure_info/Sun.png', '/var/www/html/Forecast.png')
        elif zambretti == 1:
            forecast = 'Settled Fine'
            #shutil.copyfile('/home/pi/pressure_info/Sun.png', '/var/www/html/Forecast.png')
        elif zambretti == 2:
            forecast = 'Fine Weather'
            #shutil.copyfile('/home/pi/pressure_info/Sun.png', '/var/www/html/Forecast.png')
        elif zambretti == 3:
            forecast = 'Becoming Fine'
            #shutil.copyfile('/home/pi/pressure_info/Sun.png', '/var/www/html/Forecast.png')
        elif zambretti == 4:
            forecast = 'Fairly Fine, Improving'
            #shutil.copyfile('/home/pi/pressure_info/Sun.png', '/var/www/html/Forecast.png')
        elif zambretti == 5:
            forecast = 'Fairly Fine, Possibly showers, early'
            #shutil.copyfile('/home/pi/pressure_info/SunCloud.png', '/var/www/html/Forecast.png')
        elif zambretti == 6:
            forecast = 'Showery Early, Improving'
            #shutil.copyfile('/home/pi/pressure_info/SunCloud.png', '/var/www/html/Forecast.png')
        elif zambretti == 7:
            forecast = 'Changeable, Improving'
            #shutil.copyfile('/home/pi/pressure_info/SunCloud.png', '/var/www/html/Forecast.png')
        elif zambretti == 8:
            forecast = 'Rather Unsettled Clearing Later'
            #shutil.copyfile('/home/pi/pressure_info/SunCloud.png', '/var/www/html/Forecast.png')
        elif zambretti == 9:
            forecast = 'Unsettled, Probably Improving'
            #shutil.copyfile('/home/pi/pressure_info/SunCloud.png', '/var/www/html/Forecast.png')
        elif zambretti == 10:
            forecast = 'Unsettled, short fine Intervals'
            #shutil.copyfile('/home/pi/pressure_info/SunCloud.png', '/var/www/html/Forecast.png')
        elif zambretti == 11:
            forecast = 'Very Unsettled, Finer at times'
            #shutil.copyfile('/home/pi/pressure_info/SunCloud.png', '/var/www/html/Forecast.png')
        elif zambretti == 12:
            forecast = 'Stormy, possibly improving'
            #shutil.copyfile('/home/pi/pressure_info/Storm.png', '/var/www/html/Forecast.png')
        elif zambretti == 13:
            #shutil.copyfile('/home/pi/pressure_info/Storm.png', '/var/www/html/Forecast.png')
            forecast = 'Stormy, much rain'
        return forecast
    
def writeTmp():
    ret = rrdtool.graph("/home/dietpi/pyweather/html/graph1.png",
                  '--color', 'CANVAS#000000',
                  '--color', 'FONT#07FFFE',
                  '--color', 'BACK#000000',
                  '--color', 'MGRID#0066FF',
                  '--right-axis', '1:0',
                  '--right-axis-format', '%2.1lf',
                  '--imgformat', 'PNG',
                  '--width', '790',
                  '--height', '300',
                  '--start', "-64800",
                  '--end', "now",
                  '--vertical-label', '°Celsius',
                  '--title', 'Temperature',
                  #'--lower-limit', '0',
                  'DEF:temperature=/home/dietpi/pyweather/climate_data.rrd:temperature:MAX',
                  'LINE1:temperature#8700af:temperature')
def writeWnd():
    ret = rrdtool.graph("/home/dietpi/pyweather/html/graph3.png",
                  '--color', 'CANVAS#000000',
                  '--color', 'FONT#07FFFE',
                  '--color', 'BACK#000000',
                  '--color', 'MGRID#0066FF',
                  '--right-axis', '1:0',
                  '--right-axis-format', '%2.1lf',
                  '--imgformat', 'PNG',
                  '--width', '790',
                  '--height', '300',
                  '--start', "-64800",
                  '--end', "now",
                  '--vertical-label', 'mph',
                  '--title', 'Wind Speed',
                  #'--lower-limit', '0',
                  'DEF:windspeed=/home/dietpi/pyweather/climate_data.rrd:wind:MAX',
                  'LINE1:windspeed#8700af:windspeed')

def writeHumPrs():
    ret = rrdtool.graph("/home/dietpi/pyweather/html/graph2.png",
                  '--color', 'CANVAS#000000',
                  '--color', 'FONT#07FFFE',
                  '--color', 'BACK#000000',
                  '--color', 'MGRID#0066FF',
                  '--right-axis', '1:950',
                  '--right-axis-format', '%4.0lf',
                  '--imgformat', 'PNG',
                  '--width', '790',
                  '--height', '300',
                  '--start', "-64800",
                  '--end', "now",
                  '--vertical-label', 'rel.% \ hPa',
                  '--title', 'Pressure Humidity',
                  'DEF:humidity=/home/dietpi/pyweather/climate_data.rrd:humidity:MAX',
                  'DEF:pressure=/home/dietpi/pyweather/climate_data.rrd:pressure:MAX',
                  "CDEF:scaled_pressure=pressure,950,-",
                  'LINE1:humidity#ffff87:humidity',
                  'LINE2:scaled_pressure#ffaf00:pressure')
				  
				  

while True:
    temperature,pressure,humidity = bme280.readBME280All()
    temperature -= 1.65
    pressure += 13.3
    humidity += 6.4
    d = feedparser.parse('https://weather-broker-cdn.api.bbci.co.uk/en/observation/rss/bs16')
    entry = d.entries[0]
    windir = entry.summary.split("Wind Direction: ", 1)[-1].split(",")[0]
    windspeed = float(entry.summary.split("Wind Speed: ", 1)[-1].split("mph,")[0])
    print(windir)
    #ret = rrdtool.update('/home/dietpi/pyweather/climate_data.rrd','N:' + `temperature` + ':' + `humidity` + ':' + `pressure`)
    ret = rrdtool.update('/home/dietpi/pyweather/climate_data.rrd','N:' + `windspeed` + ':' + `temperature` + ':' + `humidity` + ':' + `pressure`)
    #r = requests.post("http://192.168.1.13:8080/api/add", data={'sensorname': 'dietpizerowsensor', 'temperature': temperature, 'air_pressure': pressure, 'humidity':  humidity})
    print "Wind : ", windspeed, "mph ---","Temperature : ", temperature, "°C ---", " Pressure : ", pressure, "hPa ---", " Humidity : ", humidity
    #print(r.status_code, r.reason)
    #print(r.text[:300] + '...')
    sys.stdout.flush()
    writeTmp()
    writeHumPrs()
    writeWnd()
    forecastnow = zambretti()
    print(forecastnow)
    now = datetime.datetime.now()
    currtime = str(now.strftime("%H:%M"))
    currentcond = "Wind: %s mph --- Temperature: %s°C --- Forecast @ %s is %s" % (windspeed, temperature, currtime, forecastnow)
    text_file = open("/home/dietpi/pyweather/html/forecast.txt", "w")
    n = text_file.write(currentcond)
    print(currentcond)
    text_file.close()
    text1_file = open("/var/www/html/weather.txt", "w")
    n = text1_file.write(currentcond)
    text1_file.close()
    time.sleep(1800)
