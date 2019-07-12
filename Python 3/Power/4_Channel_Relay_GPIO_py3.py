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
# This program is designed to turn 4 GPIO ports or relays on and off
# every 5 seconds.
#
#
##############################################################################


import RPi.GPIO as GPIO  # Import GPIO Module
from time import sleep  # Import sleep Module for timing

GPIO.setmode(GPIO.BCM)  # Configures how we are describing our pin numbering
GPIO.setwarnings(False)  # Disable Warnings
OutputPins = [22, 23, 24, 25]  # Set the GPIO pins that are required

# Set our GPIO pins to outputs and set them to off

for i in OutputPins:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, False)

try:
    while (True):
    # Step through each GPIO pin and set On
        for i in OutputPins:
            GPIO.output(i, True)
    # Sleep for 5 seconds
            sleep(5)
            GPIO.output(i, False)
except KeyboardInterrupt:
    # catches the ctrl-c command, breaks the loop above
    # and turns off the relays
        for i in OutputPins:
            GPIO.output(i, False)

