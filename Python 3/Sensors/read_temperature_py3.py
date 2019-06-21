#!/usr/bin/env python

##############################################################################
#
# Written by Dominic Bolding for the Raspberry Pi - 2016
#
# Website: myhydropi.com
# Contact: admin@myhydropi.com
#
# Feel free to use and modify this code for you own use in any way.
#
# This program is designed to read the temperature in Celcius or Fahrenheit
# from a DS18B20 waterproof temperature sensor. To read more than one
# temperature sensor remove the # symbol from lines 30,31 and 63,64
# and update as required.
#
##############################################################################

import os
from time import sleep  #  Import sleep function for timing
from math import trunc  #  Import trunc function to set accuracy

#  Load Raspberry Pi Drivers
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

#  Define data file for temperature sensors
temp_sensor_1 = '/sys/bus/w1/devices/28-xxxxxxxxxxxx/w1_slave'

#  Uncomment and insert data file name for attitional sensors
#temp_sensor_2 = '/sys/bus/w1/devices/28-xxxxxxxxxxxx/w1_slave'
#temp_sensor_3 = '/sys/bus/w1/devices/28-xxxxxxxxxxxx/w1_slave'


def read_temp_raw(temp_sensor):
#  Read the 2 raw lines of data from the temperature sensor
    f = open(temp_sensor, 'r')
    lines = f.readlines()
    f.close()
    return lines

#  This definition truncates the number of digits after the decimal point
#  The sensor normally outputs Celcius values to 3 decimal points 
def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return trunc(stepper * number) / stepper

def read_temp(temp_sensor):
#  Check the Temp Sensor file for errors and convert to Celcius or Fahrenheit
    lines = read_temp_raw(temp_sensor)
    while lines[0].strip()[-3:] != 'YES':
        sleep(0.2)
        lines = read_temp_raw(temp_sensor)
    temp_result = lines[1].find('t=')
    if temp_result != -1:
        temp_string = lines[1][temp_result + 2:]
        #  Use line below for Celsius
        #  The last number (2 shown here) sets the number of digits after the
        #  decimal point or accuracy
        temp = truncate((float(temp_string) / 1000.0),2)
        #  Uncomment line below for Fahrenheit
        #  The last number (2 shown here) sets the number of digits after the
        #  decimal point or accuracy
        #temp = truncate((((float(temp_string) / 1000.0) * (9.0 / 5.0)) + 32),2)
        return temp

#  Get Temperature
while True:
    print("Temperature Sensor 1 = ", read_temp(temp_sensor_1))

#  Uncomment below for attitional sensors
    #print"Temperature Sensor 2 = ", read_temp(temp_sensor_2)
    #print"Temperature Sensor 3 = ", read_temp(temp_sensor_3)
    sleep(2)   #  Read every 2 seconds
