#!/usr/bin/env python

#Required modules for Temperature Sensor

import os
import time

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
        time.sleep(0.2)
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
    print"Temperature Sensor 1 = ", read_temp(temp_sensor_1)
    #Insert data file name for attitional sensors below and remove the "#"
    #print"Temperature Sensor 2 = ", read_temp(temp_sensor_2)
    #print"Temperature Sensor 3 = ", read_temp(temp_sensor_3)
    time.sleep(2)   # Read every 2 seconds
