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
# This program is designed to provide the following features and should be run
# initially from the command line so that a couple of configuration errors can
# be tested for and warnings provided on screen:
#
# 1. Turn relays on and off at set times stored in a MySql database. You can
# set a different number of Start/Stop pairs for each relay. The timers can
# be overridden to force the Relays either on or off by changing the values in
# the database. The database is checked every second for changes.
#
# 2. The program will also create the initial database and tables if they do
# not already exist in MySQL, it sets the relays to Off and the timers to NULL.
# If you change the number of relays, sensors or date/time pairs being used
# the software will reconfigure the database to reflect these changes after
# restarting the program.
#
#
# For Python 3 I have used python-mysqldb module to connect to the database.
# To add the module you need to enter the following commands
#
# sudo apt install python-mysqldb
#
##############################################################################


import os
import sys
import mysql.connector as mariadb
import datetime
import RPi.GPIO
from time import sleep


# Uncomment sleep if running program at startup with crontab

#sleep(10)

# Check the the number of GPIO ports equals the number of Start/Stop pairs


def check_number_of_relays_equals_start_stop_pairs():

    if len(outputpins) != len(numdtpairs):
        os.system('clear')
        print("\nThe number of GPIO ports you have listed does not match the\n"
        "number of Start/Stop pairs you have set for each relay.\n\n"
        "Please update the variables \"outputpins\" or \"numdtpairs\"\n"
        "so that they have the same number of entries.\n")
        sys.exit()  # Stop program
    return


def set_GPIO_pins():

    RPi.GPIO.setmode(RPi.GPIO.BCM)
    RPi.GPIO.setwarnings(False)

    for relay in outputpins:
        RPi.GPIO.setup(relay, RPi.GPIO.OUT)
        RPi.GPIO.output(relay, False)
    sleep(2)

# Create required database in the MySQL if it doesn't' already exist


def create_database():

    conn = mariadb.connect(user=username,
                           password=password,
                           host=servername)
    curs = conn.cursor()
    try:
        curs.execute("SET sql_notes = 0; ")  # Hide Warnings
        curs.execute("CREATE DATABASE IF NOT EXISTS {}".format(dbname))
        curs.execute("SET sql_notes = 1; ")  # Show Warnings
    except mariadb.Error as error:
        print("Error: {}".format(error))
        pass
    conn.commit()
    conn.close()
    return


def open_database_connection():

    conn = mariadb.connect(user=username,
                           password=password,
                           host=servername,
                           database=dbname)
    curs = conn.cursor()
    try:
        curs.execute("SET sql_notes = 0; ")  # Hide Warnings
    except mariadb.Error as error:
        print("Error: {}".format(error))
        pass

    return conn, curs


def close_database_connection(conn, curs):

    try:
        curs.execute("SET sql_notes = 1; ")  # Show Warnings
    except mariadb.Error as error:
        print("Error: {}".format(error))
        pass
    conn.commit()
    conn.close()


def create_relay_tables():

    conn, curs = open_database_connection()

    relaytimer = []
    dtcount = 0

    for number in relaycount:
        relay = ("relay_" + str(number) + "_timer")
        relaytimer.append(relay)

    for tablename in relaytimer:
        try:
            curs.execute("CREATE TABLE IF NOT EXISTS {} "
                        "(pk INT UNSIGNED PRIMARY KEY,"
                        "starttime DATETIME DEFAULT NULL, "
                        "stoptime DATETIME DEFAULT "
                        "NULL);".format(tablename))
        except mariadb.Error as error:
            print("Error: {}".format(error))
            pass

    # Add default "NULL" data to each relay_timer table

        for pairs in range(1, (numdtpairs[dtcount] + 1)):
            try:
                curs.execute("INSERT IGNORE INTO {} (pk,starttime,stoptime)"
                            " VALUES({},NULL,NULL)".format(tablename, pairs))
            except mariadb.Error as error:
                print("Error: {}".format(error))
                pass
        dtcount += 1

    close_database_connection(conn, curs)

    return relaytimer


def create_timer_override_table():

    conn, curs = open_database_connection()
    try:
        curs.execute("CREATE TABLE IF NOT EXISTS timer_override "
                    "(pk INT UNSIGNED PRIMARY KEY);")
        curs.execute("INSERT IGNORE INTO timer_override (pk) VALUES(1)")
    except mariadb.Error as error:
        print("Error: {}".format(error))
        pass

    # Add columns and default "off" data to timer_override table

    for number in relaycount:
        relayname = ("relay_" + str(number))
        try:
            curs.execute("ALTER TABLE timer_override ADD {} VARCHAR(5)"
                            .format(relayname))
            curs.execute("UPDATE IGNORE timer_override SET {} = 'off' "
                        "WHERE pk = 1;".format(relayname))
            curs.execute("UPDATE IGNORE timer_override SET {} = 'False' "
                        "WHERE pk = 2;".format(relayname))
        except mariadb.Error as error:
            print("Error: {}".format(error))
            pass

    close_database_connection(conn, curs)

    return

    # Remove excess columns from tables in the database


def remove_excess_timer_override_and_relay_database_entries():

    conn, curs = open_database_connection()
    try:
        curs.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE "
                    "TABLE_NAME = 'timer_override';")
    except mariadb.Error as error:
        print("Error: {}".format(error))
        pass
    colnum = curs.fetchone()
    colnum = (int(colnum[0])) - 1

    while colnum > len(outputpins):
        try:
            curs.execute("ALTER TABLE timer_override DROP {};"
                        .format("relay_" + str(colnum)))
            curs.execute("DROP TABLE {};"
                        .format("relay_" + str(colnum) + "_timer"))
            curs.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE "
                        "TABLE_NAME = 'timer_override';")
        except mariadb.Error as error:
            print("Error: {}".format(error))
            pass
        colnum = curs.fetchone()
        colnum = (int(colnum[0])) - 1

    close_database_connection(conn, curs)

    return


def remove_excess_datetime_pairs():

    conn, curs = open_database_connection()

    dtcount = 0

    for relay in relay_timer_names:
        try:
            curs.execute("DELETE FROM {} WHERE pk > {};"
                        .format(relay, numdtpairs[dtcount]))
        except mariadb.Error as error:
            print("Error: {}".format(error))
            pass
        dtcount += 1

    close_database_connection(conn, curs)

    return


def read_timer_override_data():

    # Read whether the Relay should be On, Off or using the timer

    conn, curs = open_database_connection()
    try:
        curs.execute("SELECT * FROM timer_override WHERE pk=(1)")
    except mariadb.Error as error:
        print("Error: {}".format(error))
        pass
    override_timer_values = curs.fetchone()

    close_database_connection(conn, curs)

    return override_timer_values

#Get the start/stop pairs from the database


def get_relay_timer_start_stop_data(tablename, row):

    conn, curs = open_database_connection()
    try:
        curs.execute("SELECT * FROM {} WHERE pk={}".format(tablename, row))
    except mariadb.Error as error:
        print("Error: {}".format(error))
        pass
    relay_timer_values = curs.fetchone()

    close_database_connection(conn, curs)

    return relay_timer_values

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

    override = read_timer_override_data()

    for rct, opp, ndtp, rts in zip(relaycount, outputpins,
                                   numdtpairs, relay_timer_names):
        if override[rct] == "auto":
            relayon = False
            dtpair = 1
            while relayon is False and dtpair <= ndtp:
                timer_data = get_relay_timer_start_stop_data(rts, dtpair)
                relayon = check_each_start_stop_timer(timer_data)
                if relayon is True:
                    RPi.GPIO.output(opp, True)
                    break
                elif relayon is False:
                    dtpair += 1
                if dtpair == (ndtp + 1):
                    RPi.GPIO.output(opp, False)
        elif override[rct] == "on":
            RPi.GPIO.output(opp, True)  # turn relay on
        elif override[rct] == "off":
            RPi.GPIO.output(opp, False)  # turn relay off
    return


# Define MySQL database login settings

servername = "localhost"
username = "YourMysqlUsername"
password = "YourMysqlPassword"
dbname = "YourMysqlDatabaseName"

# Define Relay Settings

outputpins = [22, 23, 24, 25]  # Specifiy a RPi GPIO Pin for each relay
numdtpairs = [4, 3, 2, 1]  # Number of Start/Stop pairs for each relay
relaycount = list(range(1, (len(outputpins) + 1)))

#################
#               #
# Main Program  #
#               #
#################


# Sanity Checks

check_number_of_relays_equals_start_stop_pairs()

# Configure relay GPIO ports

set_GPIO_pins()

# Build/Remove MySQL Database Entries

create_database()

relay_timer_names = create_relay_tables()
create_timer_override_table()

remove_excess_timer_override_and_relay_database_entries()
remove_excess_datetime_pairs()

while True:  # Repeat the code indefinitely

    # Control the relays

    activate_deactivate_relays()

    sleep(1)
