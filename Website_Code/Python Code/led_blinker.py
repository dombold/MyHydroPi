#!/usr/bin/env python

import RPi.GPIO as GPIO  # Import RPi.GPIO Module
from time import sleep  # Import sleep Module for timing

GPIO.setmode(GPIO.BCM)  # Configures pin numbering to Broadcom reference
GPIO.setwarnings(False)  # Disable Warnings
GPIO.setup(17, GPIO.OUT)  #Set our GPIO pin to output 
GPIO.output(17, False)  #Set output to off

while (True):
        GPIO.output(17, True)  # Turn LED on
        sleep(0.01)
        GPIO.output(17, False) # Turn LED off
        sleep(0.01)