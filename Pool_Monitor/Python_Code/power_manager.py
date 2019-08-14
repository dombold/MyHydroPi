#!/usr/bin/env python

# Import Python Modules

import datetime
import RPi.GPIO

#  Import Custom Modules

import hydropi_variables as var
import database_manager as dbman

def set_GPIO_pins():

    RPi.GPIO.setmode(RPi.GPIO.BCM)
    RPi.GPIO.setwarnings(False)

    for relay in var.outputpins:
        RPi.GPIO.setup(relay, RPi.GPIO.OUT)
        RPi.GPIO.output(relay, False)

    return

def set_relays_off():

    for relay in var.outputpins:
        RPi.GPIO.output(relay, False)

    return

#Check the start/stop pairs retrieved from the database and see if all the
#conditions are met to activate the Relay


def check_each_start_stop_timer(timer_data):

    # If the relay is set to auto then check all start/stop times for that
    # relay and based on current time turn relay on or off

    if timer_data[1] is None:  # Python reads a "NULL" value as None
        return  False

    else:
        cdt = datetime.datetime.now()
        starttimer = timer_data[1]
        starttimer = starttimer.replace(year=cdt.year)
        stoptimer = timer_data[2]
        stoptimer = stoptimer.replace(year=cdt.year)

        if (cdt.date() >= starttimer.date()  # Check month and day
            and cdt.date() <= stoptimer.date()):

            if (cdt.time() >= starttimer.time()  # Check hour and minute
                and cdt.time() <= stoptimer.time()):
                return True
            else:
                return False
        else:
            return False


def activate_deactivate_relays():

    # Read settings of On, Off or Auto for each relay and execute required
    # relay state

    override = dbman.read_timer_override_data()

    for rct, opp, ndtp, rts in zip(var.relaycount, var.outputpins,
                                   var.numdtpairs, var.relay_timer_names):
        if override[rct] == "auto":
            relayon = False
            dtpair = 1
            while relayon is False and dtpair <= ndtp:
                timer_data = dbman.get_relay_timer_start_stop_data(rts, dtpair)
                relayon = check_each_start_stop_timer(timer_data)
                if relayon is True:
                    RPi.GPIO.output(opp, True)
                    relayname = ("relay_" + str(rct))
                    dbman.current_relay_state(relayname, relayon)
                    break
                elif relayon is False:
                    dtpair += 1
                if dtpair == (ndtp + 1):
                    RPi.GPIO.output(opp, False)
                    relayname = ("relay_" + str(rct))
                    dbman.current_relay_state(relayname, relayon)
        elif override[rct] == "on":
            RPi.GPIO.output(opp, True)  # turn relay on
            relayname = ("relay_" + str(rct))
            dbman.current_relay_state(relayname, True)
        elif override[rct] == "off":
            RPi.GPIO.output(opp, False)  # turn relay off
            relayname = ("relay_" + str(rct))
            dbman.current_relay_state(relayname, False)
    return