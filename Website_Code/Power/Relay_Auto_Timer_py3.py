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
# For Python 3 I have used mysql-connector module to connect to the database.
# To add the module you need to enter the following commands
#
# sudo apt install python3-pip
# sudo pip3 install mysql-connector-python
#
##############################################################################

import mysql.connector as mariadb
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

# Set the GPIO pin numbers that are required
outputpins = [22, 23, 24, 25]
# Relay names in MySQL
relaynum = ["relay_1_timer", "relay_2_timer", "relay_3_timer", "relay_4_timer"]
 # Number of relays to be controlled
relaycount = range(1, 5)
# Number of Start/Stop pairs per relay
numdtpairs = 4


#Set our GPIO pins to outputs and set them to off then wait 2 seconds

for i in outputpins:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, False)
sleep(2)

# Read the manual setting from the database


def read_override_data():
    conn = mariadb.connect(user=username,
                           password=password,
                           host=servername,
                           database=dbname)
    curs = conn.cursor()
    try:
        curs.execute("SELECT * FROM timer_override WHERE pk=(1)")
    except mariadb.Error as error:
        print("Error: {}".format(error))
    override_timer_values = curs.fetchone()
    conn.close()
    return override_timer_values

#Get the start/stop pairs from the SQL database


def get_relay_timer_data(tablename, row):
    conn = mariadb.connect(user=username,
                           password=password,
                           host=servername,
                           database=dbname)
    curs = conn.cursor()
    try:
        curs.execute("SELECT * FROM {0} WHERE pk={1}".format(tablename, row))
    except mariadb.Error as error:
        print("Error: {}".format(error))
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

try:
    while True:  # Repeat the code indefinitely
        override = read_override_data()
        for i, j, z in zip(relaycount, outputpins, relaynum):
            if override[i] == "auto":
                relay = j
                relayon = "False"
                dtpair = 1
                while relayon == "False" and dtpair <= numdtpairs:
                    timer_data = get_relay_timer_data(z, dtpair)
                    relayon = timercheck(timer_data, relay)
                    if relayon == "True":
                        GPIO.output(relay, True)
                        break
                    elif relayon == "False":
                        dtpair += 1
                    if dtpair == (numdtpairs + 1):
                        GPIO.output(relay, False)
            elif override[i] == "on":
                GPIO.output(j, True)  # turn relay on
            elif override[i] == "off":
                GPIO.output(j, False)  # turn relay off
        sleep(1)
except KeyboardInterrupt:
    # catches the ctrl-c command, breaks the loop above
    # and turns off the relays
        for i in outputpins:
            GPIO.output(i, False)