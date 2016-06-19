#!/usr/bin/python

import MySQLdb
from time import sleep
import datetime
import RPi.GPIO as GPIO


servername = "localhost"
username = "root"
password = "hsv240etc"
dbname = "hydropi"

# Set up GPIO ports

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(22, GPIO.OUT)
GPIO.output(22, True)
GPIO.setup(23, GPIO.OUT)
GPIO.output(23, True)
GPIO.setup(24, GPIO.OUT)
GPIO.output(24, True)
GPIO.setup(25, GPIO.OUT)
GPIO.output(25, True)

#Check the timer data from SQL and see if all the conditions
#are met to activate the Relay


def timercheck(timer_data, relay):
    if timer_data[1] == "NULL" or timer_data[1] is None:
        return  "False"
    cdt = datetime.datetime.now()
    starttimer = timer_data[1]
    starttimer = starttimer.replace(year=cdt.year)
    stoptimer = timer_data[2]
    stoptimer = stoptimer.replace(year=cdt.year)

    if cdt.date() >= starttimer.date() and cdt.date() <= stoptimer.date():
        if cdt.time() >= starttimer.time() and cdt.time() <= stoptimer.time():
            return "True"
        else:
            return "False"
    else:
        return "False"

#Get the data from the SQL database


def get_relay_timer_data(tablename, row):

    conn = MySQLdb.connect(servername, username, password, dbname)
    conn.text_factory = str
    curs = conn.cursor()
    curs.execute("SELECT * FROM {0} WHERE pk={1}".format(tablename, row))
    relay_timer_values = curs.fetchone()
    conn.close()

    return relay_timer_values


def read_override_data():

    conn = MySQLdb.connect(servername, username, password, dbname)
    #conn.text_factory = str
    curs = conn.cursor()
    curs.execute("SELECT * FROM timeoverride WHERE pk=(1)")
    override_timer_values = curs.fetchone()
    conn.close()

    return override_timer_values

# Main Program


def main():
    while True:  # Repeat the code indefinitely
        override = read_override_data()
        # Check the gpo1 relay
        if override[1] == 2:
            relay = 22
            relayon = "False"
            relayrow = 1
            while relayon == "False" and relayrow <= 4:
                timer_data = get_relay_timer_data("gpo1", relayrow)
                relayon = timercheck(timer_data, relay)
                if relayon == "True":
                    GPIO.output(relay, False)
                    break
                elif relayon == "False":
                    relayrow += 1
                if relayrow == 5:
                    GPIO.output(relay, True)

        elif override[1] == 1:
            GPIO.output(22, False)  # turn relay on
        elif override[1] == 0:
            GPIO.output(22, True)  # turn relay off

    # Check the gpo2 relay
        if override[2] == 2:
            relay = 23
            relayon = "False"
            relayrow = 1
            while relayon == "False" and relayrow <= 4:
                timer_data = get_relay_timer_data("gpo2", relayrow)
                relayon = timercheck(timer_data, relay)
                if relayon == "True":
                    GPIO.output(relay, False)
                    break
                elif relayon == "False":
                    relayrow += 1
                if relayrow == 5:
                    GPIO.output(relay, True)

        elif override[2] == 1:
            GPIO.output(23, False)  # turn relay on
        elif override[2] == 0:
            GPIO.output(23, True)  # turn relay off

    # Check the gpo3 relay
        if override[3] == 2:
            relay = 24
            relayon = "False"
            relayrow = 1
            while relayon == "False" and relayrow <= 4:
                timer_data = get_relay_timer_data("gpo3", relayrow)
                relayon = timercheck(timer_data, relay)
                if relayon == "True":
                    GPIO.output(relay, False)
                    break
                elif relayon == "False":
                    relayrow += 1
                if relayrow == 5:
                    GPIO.output(relay, True)

        elif override[3] == 1:
            GPIO.output(24, False)  # turn relay on
        elif override[3] == 0:
            GPIO.output(24, True)  # turn relay off

    # Check the gpo4 relay
        if override[4] == 2:
            relay = 25
            relayon = "False"
            relayrow = 1
            while relayon == "False" and relayrow <= 4:
                timer_data = get_relay_timer_data("gpo4", relayrow)
                relayon = timercheck(timer_data, relay)
                if relayon == "True":
                    GPIO.output(relay, False)
                    break
                elif relayon == "False":
                    relayrow += 1
                if relayrow == 5:
                    GPIO.output(relay, True)

        elif override[4] == 1:
            GPIO.output(25, False)  # turn relay on
        elif override[4] == 0:
            GPIO.output(25, True)  # turn relay off

        sleep(5)
main()














