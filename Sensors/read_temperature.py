#!/usr/bin/env python

##############################################################################
# Written by Dominic Bolding for myhydropi.com - 2016
#
# Feel free to use and modify this code for you own use in any way.
#
# This program is designed to read the temperature in Celcius or Fahrenheit
# from a DS18B20 waterproof temperature sensor. To read more than one
# temperature sensor remove the # symbol from lines 27,28 and 63,64
# and update as required.
#
# For Python 3.x compatibility comment out line 64 and uncomment line 66
##############################################################################

#Required modules for Temperature Sensor

import os
from time import sleep  # Import sleep module for timing

# Load Raspberry Pi Drivers

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# Define data file for temperature sensors

temp_sensor_1 = '/sys/bus/w1/devices/28-01157127dfff/w1_slave'
#Insert data file name for attitional sensors below and remove the "#"
#temp_sensor_2 = '/sys/bus/w1/devices/28-xxxxxxxxxxxx/w1_slave'
#temp_sensor_3 = '/sys/bus/w1/devices/28-xxxxxxxxxxxx/w1_slave'


#Read the 2 raw lines of data from the temperature sensor


def read_temp_raw(temp_sensor):

    f = open(temp_sensor, 'r')
    lines = f.readlines()
    f.close()
    return lines

# Check the Temp Sensor file for errors and convert to Celcius or Fahrenheit


def read_temp(temp_sensor):

    lines = read_temp_raw(temp_sensor)
    while lines[0].strip()[-3:] != 'YES':
        sleep(0.2)
        lines = read_temp_raw(temp_sensor)
    temp_result = lines[1].find('t=')
    if temp_result != -1:
        temp_string = lines[1][temp_result + 2:]
        # Use line below for Celsius
        temp = float(temp_string) / 1000.0
        #Use line below for Fahrenheit
        #temp = ((float(temp_string) / 1000.0) * (9.0 / 5.0)) + 32
        return temp

# Get Temperature
while True:
    print "Temperature Sensor 1 = ", read_temp(temp_sensor_1)
    #Python 3.x print command syntax below
    #print("Temperature Sensor 1 = ", read_temp(temp_sensor_1))
    #Insert data file name for attitional sensors below
    #print"Temperature Sensor 2 = ", read_temp(temp_sensor_2)
    #print"Temperature Sensor 3 = ", read_temp(temp_sensor_3)
    sleep(2)   # Read every 2 seconds
