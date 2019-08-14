#!/usr/bin/env python

##############################################################################
#
# Written by Dominic Bolding for the Raspberry Pi - 2016
# Updated 2019
#
# Website: myhydropi.com
# Contact: admin@myhydropi.com
#
# Feel free to use and modify this code for you own use in any way.
#
# This program is designed to provide the following features:
#
# 1. Read Multiple Sensors - DS18B20 1-wire type Temperature sensors, Atlas
# Scientific Temperature, pH, Oxidation Reduction Potential (ORP) and
# Electrical Conductivity sensors and save the results to a MySQL database at
# a set interval with a set level of accuracy. Multiple sensors of the same
# type can also be used by configuring the "sensors" variable with the correct
# sensor type. A reference temperature reading will be set by one of the
# temperature sensors if any are connected, if not a value of 25C will be
# applied. This is necessary to ensure accurate readings from the other
# sensors as the liquid being tested changes temperature.
# The electrical conductivity reading is also converted to parts per million.
# There is also a customizible "pause" setting included to stop readings while
# chemicals are being added, this prevents spikes in the readings for more
# accurate results.
#
# 2. Check that the sensor readings fall within a set range and if not then
# send an alert email. The email will only be sent once and will not send
# another until all the readings are back within range or a set time period
# has passed. Which sensors are included in the alert test can also be set on
# a sensor by sensor basis.
#
# 3. Turn relays on and off at set times stored in a MySql database. You can
# set a different number of Start/Stop pairs for each relay. The timers can
# be overridden to force the Relays either on or off by changing the values in
# the database. The database is checked every second for changes.
#
# 4. The program will also create the initial database and tables if they do
# not already exist in MySQL, it sets the relays to Off and the timers to NULL.
# Email alert default values are also added to the settings table. In addition
# if you change the number of relays, sensors or date/time pairs being used
# the software will reconfigure the database to reflect these changes after
# restarting the program.
#
# 5. The program will also continue to run in the event of minor errors such as
# failed sensor readings or email server login failures. These errors will be
# logged to a file named hydropi_error.log. The initial setup checks will also
# be output to this file.
#
# Note: If you change the sensor names or alert value names after you have run
# the program once, these new names will create a new column in the table
# leaving the old columns in place. If these are no longer required then they
# will have to be removed manually. If you want to completely start over then
# "DROP" the database and with the new settings in place restart the program.
#
# Finally a word on the time between readings, pause delay and the email resend
# delays. These have been setup with default values to read the sensors every
# 5 minutes, stop taking readings for 30 minutes when the pause delay is
# invoked and to resend an email every 2 days if the readings have not returned
# within the limits.
#
##############################################################################

# Import Python Modules

import sys
import datetime
import logging
from time import sleep

# Import Custom Modules

import hydropi_variables as var
import sensor_manager as sensors
import database_manager as dbman
import email_manager as emman
import power_manager as pman

# Uncomment sleep if running program at startup with crontab

#sleep(10)

# Check the the number of GPIO ports equals the number of Start/Stop pairs


def check_number_of_relays_equals_start_stop_pairs():

    if len(var.outputpins) != len(var.numdtpairs):
        logging.error("\nThe number of GPIO ports you have listed does not match the\n"
        "number of Start/Stop pairs you have set for each relay.\n\n"
        "Please update the variables \"outputpins\" or \"numdtpairs\"\n"
        "so that they have the same number of entries.\n")
        sys.exit()  # Stop program
    return


# Check that only one Primary Temperature sensor is defined


def check_for_only_one_reference_temperature():

    ref_check = 0

    for key, value in list(var.sensors.items()):
        if (value["is_connected"]) is True:
            if value["sensor_type"] == "1_wire_temp":
                if value["is_ref"] is True:
                    ref_check += 1
            if value["sensor_type"] == "atlas_temp":
                if value["is_ref"] is True:
                    ref_check += 1
    if ref_check > 1:
        logging.error("\n\"You can only have one Primary Temperature sensor,\n"
                    "Please set the Temperature sensor that is in the liquid\n"
                    "you are testing to True and the other to False\n")
        sys.exit()  # Stop program
    return


#################
#               #
# Main Program  #
#               #
#################

# Start Logging

logging.basicConfig(filename = 'hydropi_error.log',
        format = '%(asctime)s -  %(levelname)s - %(message)s',
        datefmt = '%d/%m/%Y %I:%M:%S %p', 
        level = logging.INFO)

# Sanity Checks

check_number_of_relays_equals_start_stop_pairs()
check_for_only_one_reference_temperature()

# Configure relay GPIO ports

pman.set_GPIO_pins()

# Build/Remove MySQL Database Entries

dbman.create_database()
dbman.create_database_tables()
dbman.remove_excess_database_entries()

try:
    while True:  # Repeat the code indefinitely

        # Control the relays

        pman.activate_deactivate_relays()

        sleep(1)

        # Check if sensor readings have been paused, if not then read and store
        # sensor values and check against alert values, send an email if required

        if datetime.datetime.now() >= (var.sensor_ref_time + 
           datetime.timedelta(seconds=var.time_between_readings)):
            var.sensor_ref_time = datetime.datetime.now()

            # Read delay values from settings table

            delays = dbman.get_settings_table_values()
            var.time_between_readings = delays["read_sensor_delay"]
            email_time_delay = delays["email_reset_delay"]
            pause_time = delays["pause_reset_delay"]

            if delays["pause_readings"] == 0:
                alert_readings = sensors.read_sensors()

                if var.alert_check is True and var.email_sent is True:
                    var.email_sent = emman.reset_email_sent_flag_if_alerts_clear(alert_readings, var.email_sent)
                    if var.email_sent is False:
                        var.alert_check is False
                        email_sent_time = datetime.datetime.now()

                elif var.alert_check is False:
                    var.alert_check = emman.check_sensor_alert_limits(alert_readings, var.alert_check)
                    if var.alert_check is True:
                        all_settings = dbman.get_settings_table_values()
                        emman.send_email(alert_readings, all_settings)
                        logging.info("Email has been sent")
                        var.email_sent = True
                        email_sent_time = datetime.datetime.now()

            elif delays["pause_readings"] == 1:
                if var.new_pause is True:
                    logging.info("Readings have been paused")
                    pause_start_time = datetime.datetime.now()
                    var.new_pause = False
                if datetime.datetime.now() >= (pause_start_time + 
                   datetime.timedelta(seconds=pause_time)):
                    dbman.reset_pause_readings()
                    var.new_pause = True
                    logging.info("Reading sensors again")

            if var.email_sent is True:
                if datetime.datetime.now() >= (email_sent_time + 
                   datetime.timedelta(seconds=email_time_delay)):
                    var.alert_check = False
                    email_sent_time = datetime.datetime.now()

except KeyboardInterrupt:
    # catches the ctrl-c command, breaks the loop above 
    # and turns the relays off
    pman.set_relays_off()
