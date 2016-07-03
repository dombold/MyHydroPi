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
# at set times stored in a MySql database. The timers can be overridden
# to force the Relays either on or off.
#
# While the code looks counter intuitive by setting the GPIO pin to true
# to turn off the relay this is actually correct due to the fact that the
# relay that I am using is configured as active low.
#
# If you have a relay that is active high or are using LED's then reverse the
# True and False settings'
#
# For Python 3 I have used cymysql module to connect to the database
# to add the module you need to enter the following commands
#
# sudo apt-get install python3-pip
# sudo pip-3.2 install cymysql
#
##############################################################################

import cymysql
from time import sleep
import datetime
import RPi.GPIO as GPIO


servername = "localhost"
username = "YourMySQLusername"
password = "YourMySQLpassword"
dbname = "YourDatabaseName"

# Set up GPIO ports

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Global Variables

outputpins = [22, 23, 24, 25]  # Set the GPIO pin numbers that are required
gponum = ["gpo1", "gpo2", "gpo3", "gpo4"]  # List of relay names in MySQL
relaycount = range(1, 5)  # Number of relays to be controlled
numdtpairs = 4  # Number of Start/Stop pairs per relay

#Set our GPIO pins to outputs and set them to off then wait 2 seconds

for i in outputpins:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, True)
sleep(2)

# Read the manual setting from the database


def read_override_data():
    conn = cymysql.connect(servername, username, password, dbname)
    curs = conn.cursor()
    curs.execute("SELECT * FROM timeoverride WHERE pk=(1)")
    override_timer_values = curs.fetchone()
    conn.close()
    return override_timer_values

#Get the start/stop pairs from the SQL database


def get_relay_timer_data(tablename, row):
    conn = cymysql.connect(servername, username, password, dbname)
    curs = conn.cursor()
    curs.execute("SELECT * FROM {0} WHERE pk={1}".format(tablename, row))
    relay_timer_values = curs.fetchone()
    conn.close()
    return relay_timer_values

#Check the timer data from SQL and see if all the conditions
#are met to activate the Relay


def timercheck(timer_data, relay):
    if timer_data[1] is None:  # Python reads a "NULL" value as None
        return  "False"
    else:
        cdt = datetime.datetime.now()
        starttimer = timer_data[1]
        starttimer = starttimer.replace(year=cdt.year)
        stoptimer = timer_data[2]
        stoptimer = stoptimer.replace(year=cdt.year)
        if (cdt.date() >= starttimer.date()
            and cdt.date() <= stoptimer.date()):
            if (cdt.time() >= starttimer.time()
                and cdt.time() <= stoptimer.time()):
                return "True"
            else:
                return "False"
        else:
            return "False"

# Main Program

while True:  # Repeat the code indefinitely
    override = read_override_data()
    for i, j, z in zip(relaycount, outputpins, gponum):
        if override[i] == "auto":
            relay = j
            relayon = "False"
            dtpair = 1
            while relayon == "False" and dtpair <= numdtpairs:
                timer_data = get_relay_timer_data(z, dtpair)
                relayon = timercheck(timer_data, relay)
                if relayon == "True":
                    GPIO.output(relay, False)
                    break
                elif relayon == "False":
                    dtpair += 1
                if dtpair == (numdtpairs + 1):
                    GPIO.output(relay, True)
        elif override[i] == "on":
            GPIO.output(j, False)  # turn relay on
        elif override[i] == "off":
            GPIO.output(j, True)  # turn relay off
    sleep(1)