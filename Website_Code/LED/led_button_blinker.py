#!/usr/bin/env python

import RPi.GPIO as GPIO  # Import GPIO Module
from time import sleep  # Import sleep Module for timing

GPIO.setmode(GPIO.BCM)  # Configures pin numbering to Broadcom reference
GPIO.setwarnings(False)  # Disable Warnings
GPIO.setup(17, GPIO.OUT)  #Set our GPIO pin to output 
GPIO.output(17, False)  #Set output to off
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Set GPIO to input with a  pull-down resistor
GPIO.add_event_detect(27, GPIO.RISING, bouncetime=200)  # Monitor GPIO pin for a rising edge and debounce for 200mS

try:
    while (True):
        if GPIO.event_detected(27):  # Check to see if button has been pushed
            activate = True
            while (activate is True):  # Execute this code until the button is pushed again
                GPIO.output(17, True)  # Turn LED on
                sleep(0.5)
                GPIO.output(17, False) # Turn LED off
                sleep(0.5)
                if GPIO.event_detected(27):  # Check for a 2nd button push
                    activate = False
        else:
            GPIO.output(17, False)  # Turn LED off
except KeyboardInterrupt:
    # catches the ctrl-c command, breaks the loop above 
    # and resets the GPIO's
    GPIO.cleanup()