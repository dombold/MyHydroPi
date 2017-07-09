#!/usr/bin/env python

##############################################################################
#
# Written by Dominic Bolding for The Raspberry Pi - 2017
#
# Website: myhydropi.com
# Contact: admin@myhydropi.com
#
# This program will recognise a button push on GPIO pin 27 and take a photo.
# If the button is held down then it will continue to take photo's every second
# until the button is relased. Images are stored in order to the specified
# folder, if the folder does not exist then the program will create it.
#
# GPIO pins use the Broadcom numbering scheme
#
##############################################################################

import os.path
from time import sleep
import RPi.GPIO as GPIO
from picamera import PiCamera


# Configures pin numbering to Broadcom reference
GPIO.setmode(GPIO.BCM)

# Set GPIO pin to input and activate pull_down resistor to reference pin to ground
gpio_pin = 27
GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

camera = PiCamera()
image_no = 1

# Set where you want the image saved
image_folder = ('/home/pi/myprojects/Cam_Images')


# Check that the directory to save the images exists, if not create one
if not os.path.exists(image_folder):
    print ("Making Directory")  # Not required testing only
    os.makedirs(image_folder)

camera.start_preview()
sleep(5) #  Allow camera to set light levels

print ("Ready")  # Not required testing only

try:
    while True:
        if GPIO.input(gpio_pin):  # Check for PIR sensor trigger
            print ("Button Pushed")  # Not required testing only
            # Check file name so that you don't overwrite an existing image
            while os.path.isfile('/home/pi/myprojects/Cam_Images/image%s.jpg' %image_no):
                image_no += 1
            # Take and save picture
            camera.capture('/home/pi/myprojects/Cam_Images/image%s.jpg' %image_no)
            sleep(1)  # Time between shots if button is held down
            print ("Picture Captured")  # Not required testing only
except KeyboardInterrupt:
    print ("Shutting Down")  # Not required testing only
    camera.stop_preview()
    GPIO.cleanup()
