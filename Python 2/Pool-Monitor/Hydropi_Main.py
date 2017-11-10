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
# Due to the fact that it takes the sensors approx. 2 sec to take a reading and
# that all the other delays are calculated based on the time between readings
# value there are some rounding errors which means that a 30 minute pause may
# actually turn out to be closer to 35 minutes in reality and the delay between
# emails is similarly affected, so don't expect your timings to be perfect.
# For the same reasons if you set a relay to on or off at the same time that
# sensor readings are being taken there may be up to a 2 second delay for each
# connected sensor before the relay is changed.
#
##############################################################################

import io
import os
import sys
import fcntl
import smtplib
import MySQLdb
import datetime
import RPi.GPIO
import MySQLdb.cursors
from time import sleep
from collections import OrderedDict
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart

# Uncomment sleep if running program at startup with crontab

#sleep(10)

# Load Raspberry Pi Drivers for 1-Wire Temperature Sensor

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# Define Atlas Scientific Sensor Class


class atlas_i2c:

    long_timeout = 1.5  # the timeout needed to query readings & calibrations
    short_timeout = .5  # timeout for regular commands
    default_bus = 1  # the default bus for I2C on the newer Raspberry Pis,
                     # certain older boards use bus 0
    default_address = 102  # the default address for the Temperature sensor

    def __init__(self, address=default_address, bus=default_bus):
        # open two file streams, one for reading and one for writing
        # the specific I2C channel is selected with the bus
        # it is usually 1, except for older revisions where its 0
        # wb and rb indicate binary read and write
        self.file_read = io.open("/dev/i2c-" + str(bus), "rb", buffering=0)
        self.file_write = io.open("/dev/i2c-" + str(bus), "wb", buffering=0)

        # initializes I2C to either a user specified or default address
        self.set_i2c_address(address)

    def set_i2c_address(self, addr):
        # set the I2C communications to the slave specified by the address
        # The commands for I2C dev using the ioctl functions are specified in
        # the i2c-dev.h file from i2c-tools
        I2C_SLAVE = 0x703
        fcntl.ioctl(self.file_read, I2C_SLAVE, addr)
        fcntl.ioctl(self.file_write, I2C_SLAVE, addr)

    def write(self, string):
        # appends the null character and sends the string over I2C
        string += "\00"
        self.file_write.write(string)

    def read(self, num_of_bytes=31):
        # reads a specified number of bytes from I2C,
        # then parses and displays the result
        res = self.file_read.read(num_of_bytes)  # read from the board
        # remove the null characters to get the response
        response = filter(lambda x: x != '\x00', res)

        if(ord(response[0]) == 1):  # if the response isnt an error
            # change MSB to 0 for all received characters except the first
            # and get a list of characters
            char_list = map(lambda x: chr(ord(x) & ~0x80), list(response[1:]))
            # NOTE: having to change the MSB to 0 is a glitch in the
            # raspberry pi, and you shouldn't have to do this!
            # convert the char list to a string and returns it
            return ''.join(char_list)
        else:
            return "Error " + str(ord(response[0]))

    def query(self, string):
        # write a command to the board, wait the correct timeout,
        # and read the response
        self.write(string)

        # the read and calibration commands require a longer timeout
        if((string.upper().startswith("R")) or
           (string.upper().startswith("CAL"))):
            sleep(self.long_timeout)
        elif((string.upper().startswith("SLEEP"))):
            return "sleep mode"
        else:
            sleep(self.short_timeout)
        return self.read()

    def close(self):
        self.file_read.close()
        self.file_write.close()


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

# Check that only one Primary Temperature sensor is defined


def check_for_only_one_reference_temperature():

    ref_check = 0

    for key, value in sensors.items():
        if (value["is_connected"]) is True:
            if value["sensor_type"] == "1_wire_temp":
                if value["is_ref"] is True:
                    ref_check += 1
            if value["sensor_type"] == "atlas_temp":
                if value["is_ref"] is True:
                    ref_check += 1
    if ref_check > 1:
        os.system('clear')
        print ("\n\n                     !!!! WARNING !!!!\n\n"
        "You can only have one Primary Temperature sensor, Please set the\n"
        "Temperature sensor that is in the liquid you are testing to True\n"
        "and the other to False\n\n                     !!!! WARNING !!!!\n\n")
        sys.exit()  # Stop program
    return

# Create required database in the MySQL if it doesn't' already exist


def create_database():

    conn = MySQLdb.connect(servername, username, password)
    curs = conn.cursor()
    curs.execute("SET sql_notes = 0; ")  # Hide Warnings

    curs.execute("CREATE DATABASE IF NOT EXISTS {}".format(dbname))

    curs.execute("SET sql_notes = 1; ")  # Show Warnings
    conn.commit()
    conn.close()
    return


def open_database_connection():

    conn = MySQLdb.connect(servername, username, password, dbname)
    curs = conn.cursor()
    curs.execute("SET sql_notes = 0; ")  # Hide Warnings

    return conn, curs


def close_database_connection(conn, curs):

    curs.execute("SET sql_notes = 1; ")
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
        curs.execute("CREATE TABLE IF NOT EXISTS {} "
                    "(pk INT UNSIGNED PRIMARY KEY,"
                    "starttime DATETIME DEFAULT NULL, "
                    "stoptime DATETIME DEFAULT "
                    "NULL);".format(tablename))

    # Add default "NULL" data to each relay_timer table

        for pairs in range(1, (numdtpairs[dtcount] + 1)):
            curs.execute("INSERT IGNORE INTO {} (pk,starttime,stoptime)"
                        " VALUES({},NULL,NULL)".format(tablename, pairs))
        dtcount += 1

    close_database_connection(conn, curs)

    return relaytimer


def create_timer_override_table():

    conn, curs = open_database_connection()

    curs.execute("CREATE TABLE IF NOT EXISTS timer_override "
                "(pk INT UNSIGNED PRIMARY KEY);")
    curs.execute("INSERT IGNORE INTO timer_override (pk) VALUES(1)")
    curs.execute("INSERT IGNORE INTO timer_override (pk) VALUES(2)")

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
        except:
            pass

    close_database_connection(conn, curs)

    return


def create_sensors_table():

    conn, curs = open_database_connection()

    curs.execute("CREATE TABLE IF NOT EXISTS sensors (timestamp DATETIME);")

    for key, value in sensors.items():
        if value["is_connected"] is True:
            try:
                curs.execute("ALTER TABLE sensors ADD {} DECIMAL(10,2);"
                .format(value["name"]))
            except:
                pass

    close_database_connection(conn, curs)

    return


def create_settings_table():

    conn, curs = open_database_connection()

    curs.execute("CREATE TABLE IF NOT EXISTS settings "
                "(pk TINYINT(1) UNSIGNED PRIMARY"
                " KEY);")
    try:
        curs.execute("INSERT IGNORE INTO settings (pk) VALUES(1)")
    except:
        pass
    for key, value in sensors.items():
        try:
            curs.execute("ALTER TABLE settings ADD ({} DECIMAL(10,2), "
            "{} DECIMAL(10,2));".format(value["upper_alert_name"],
                                        value["lower_alert_name"]))
            curs.execute("UPDATE IGNORE settings SET {} = {}, {} = {} "
                    "WHERE pk=1;".format(value["upper_alert_name"],
                                        value["upper_alert_value"],
                                        value["lower_alert_name"],
                                        value["lower_alert_value"]))
        except:
            pass

    for key, value in misc_setting.items():
        if key == "to_email":
            try:
                curs.execute("ALTER TABLE settings ADD {} VARCHAR(254);"
                .format(key))
                curs.execute("UPDATE IGNORE settings SET {} = '{}' "
                        "WHERE pk=1;".format(key, value))
            except:
                pass

        elif key == "pause_readings":
            try:
                curs.execute("ALTER TABLE settings ADD {} BOOLEAN;"
                .format(key))
                curs.execute("UPDATE IGNORE settings SET {} = {} "
                        "WHERE pk=1;".format(key, value))
            except:
                pass

        elif key == "offset_percent":
            try:
                curs.execute("ALTER TABLE settings ADD {} DECIMAL(10,2);"
                .format(key))
                curs.execute("UPDATE IGNORE settings SET {} = {} "
                        "WHERE pk=1;".format(key, value))
            except:
                pass

        else:
            try:
                curs.execute("ALTER TABLE settings ADD {} INT(10);"
                .format(key))
                curs.execute("UPDATE IGNORE settings SET {} = {} "
                        "WHERE pk=1;".format(key, value))
            except:
                pass

    close_database_connection(conn, curs)

    return

    # Remove excess columns from tables in the database


def remove_excess_timer_override_and_relay_database_entries():

    conn, curs = open_database_connection()

    curs.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE "
                "TABLE_NAME = 'timer_override';")
    colnum = curs.fetchone()
    colnum = (int(colnum[0])) - 1

    while colnum > len(outputpins):
        curs.execute("ALTER TABLE timer_override DROP {};"
                    .format("relay_" + str(colnum)))
        curs.execute("DROP TABLE {};"
                    .format("relay_" + str(colnum) + "_timer"))
        curs.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE "
                    "TABLE_NAME = 'timer_override';")
        colnum = curs.fetchone()
        colnum = (int(colnum[0])) - 1

    close_database_connection(conn, curs)

    return


def remove_excess_datetime_pairs():

    conn, curs = open_database_connection()

    dtcount = 0

    for relay in relay_timer_names:
        curs.execute("DELETE FROM {} WHERE pk > {};"
                    .format(relay, numdtpairs[dtcount]))
        dtcount += 1

    close_database_connection(conn, curs)

    return


def remove_unused_sensors():

    conn, curs = open_database_connection()

    for key, value in sensors.items():
        if value["is_connected"] is False:
            try:
                curs.execute("ALTER TABLE sensors DROP {};"
                            .format(value["name"]))
            except:
                pass

    close_database_connection(conn, curs)

    return


def remove_unused_sensors_settings():

    conn, curs = open_database_connection()

    for key, value in sensors.items():
        if value["is_connected"] is False:
            try:
                curs.execute(("ALTER TABLE settings DROP COLUMN {}, "
                "DROP COLUMN {};")
                .format(value["upper_alert_name"],
                        value["lower_alert_name"]))
            except:
                pass

    close_database_connection(conn, curs)

    return

# Read in the data from the Temp Sensor file


def read_1_wire_temp_raw(temp_num):

        f = open(sensors[temp_num]["ds18b20_file"], 'r')
        lines = f.readlines()
        f.close()

        return lines

# Process the Temp Sensor file for errors and convert to degrees C


def read_1_wire_temp(temp_num):

    lines = read_1_wire_temp_raw(temp_num)

    while lines[0].strip()[-3:] != 'YES':
        sleep(0.2)
        lines = read_1_wire_temp_raw()
    equals_pos = lines[1].find('t=')

    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        # Use line below for Celsius
        temp_curr = float(temp_string) / 1000.0
        #Uncomment line below for Fahrenheit
        #temp_curr = ((float(temp_string) / 1000.0) * (9.0 / 5.0)) + 32

        return temp_curr

# read and log each sensor if it is set to True in the sensors list


def log_sensor_readings(all_curr_readings):

    # Create a timestamp and store all readings on the MySQL database

    conn, curs = open_database_connection()

    curs.execute("INSERT INTO sensors (timestamp) VALUES(now());")
    curs.execute("SELECT MAX(timestamp) FROM sensors")
    last_timestamp = curs.fetchone()
    last_timestamp = last_timestamp[0].strftime('%Y-%m-%d %H:%M:%S')

    for readings in all_curr_readings:
        try:
            curs.execute(("UPDATE sensors SET {} = {} WHERE timestamp = '{}'")
                        .format(readings[0], readings[1], last_timestamp))
        except:
            pass

    close_database_connection(conn, curs)

    return


def read_sensors():

    all_curr_readings = []
    alert_readings = []
    ref_temp = 25

    # Get the readings from any 1-Wire temperature sensors

    for key, value in sensors.items():
        if value["is_connected"] is True:
            if value["sensor_type"] == "1_wire_temp":
                try:
                    sensor_reading = (round(float(read_1_wire_temp(key)),
                                 value["accuracy"]))
                except:
                    sensor_reading = 50
                    
                all_curr_readings.append([value["name"], sensor_reading])

                if value["test_for_alert"] is True:
                    alert_readings.append([value["name"], sensor_reading])
                if value["is_ref"] is True:
                    ref_temp = sensor_reading

    # Get the readings from any Atlas Scientific temperature sensors

            if value["sensor_type"] == "atlas_scientific_temp":
                device = atlas_i2c(value["i2c"])
                try:
                    sensor_reading = round(float(device.query("R")),
                                value["accuracy"])
                except:
                    sensor_reading = 50
                    
                all_curr_readings.append([value["name"], sensor_reading])
                if value["test_for_alert"] is True:
                    alert_readings.append([value["name"], sensor_reading])
                if value["is_ref"] is True:
                    ref_temp = sensor_reading
                    
    # Get the readings from any Atlas Scientific Elec Conductivity sensors

            if value["sensor_type"] == "atlas_scientific_ec":
                device = atlas_i2c(value["i2c"])
                # Set reference temperature value on the sensor
                device.query("T," + str(ref_temp))
                try:
                    sensor_reading = (round(((float(device.query("R"))) *
                        value["ppm_multiplier"]), value["accuracy"]))
                except:
                    sensor_reading = 10000
                    
                all_curr_readings.append([value["name"], sensor_reading])
                
                if value["test_for_alert"] is True:
                    alert_readings.append([value["name"], sensor_reading])

    # Get the readings from any other Atlas Scientific sensors

            if value["sensor_type"] == "atlas_scientific":
                device = atlas_i2c(value["i2c"])
                # Set reference temperature value on the sensor
                device.query("T," + str(ref_temp))
                try:
                    sensor_reading = round(float(device.query("R")),
                                value["accuracy"])
                except:
                    if value["name"] == "ph":
                        sensor_reading = 2
                    elif value["name"] == "orp":
                        sensor_reading = 1000
                        
                all_curr_readings.append([value["name"], sensor_reading])
                if value["test_for_alert"] is True:
                    alert_readings.append([value["name"], sensor_reading])

    log_sensor_readings(all_curr_readings)

    # Alert_Readings will return just the readings from sensors you want
    # tested for the email alert

    return alert_readings


def get_settings_table_values():

    # Get the current alert limit settings from the database

    conn = MySQLdb.connect(servername, username, password, dbname,
                            cursorclass=MySQLdb.cursors.DictCursor)
    curs = conn.cursor()
    curs.execute("SET sql_notes = 0; ")

    curs.execute("SELECT * FROM settings WHERE pk = 1")
    setting_values = curs.fetchone()

    # divide offset percent by 100 to convert to decimal
    setting_values["offset_percent"] = (setting_values["offset_percent"] / 100)

    close_database_connection(conn, curs)

    return setting_values


def send_email(alert_readings):

    #Generate an email when there is a problem with the pool

    # Get the email addresses to send the alert to

    all_settings = get_settings_table_values()

    out_of_limit_sensors = ""

    for k, v in alert_readings:
        out_of_limit_sensors = (out_of_limit_sensors + "\n" + k + "  -  " +
                                str(v) + "\n")

    # Build email and send

    fromaddr = "FromEmail@gmail.com"
    toaddr = all_settings["to_email"]
    alladdr = toaddr.split(",")
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Pool Alert"

    body = ("Hi\n\nThis is your Pool\n\nYou should know that the following "
    "sensor(s) are indicating that there is a problem that needs your "
    "attention\n{}\nPlease check this by logging into\n\nwww.yourwebsite.com"
    "\n\n Regards\n\nYour HydroPi").format(out_of_limit_sensors.upper())

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    try:
        server.starttls()
        server.login(fromaddr, "YourFromEmailPassword")
        text = msg.as_string()
        server.sendmail(fromaddr, alladdr, text)
        server.quit()
    except:
        pass
    return


def check_sensor_alert_limits(alert_check):

    # Get all the limit settings for the email alert

    all_settings = get_settings_table_values()

    # The IF statement below checks that the main pump relay is active before
    # checking the sensor alert limits. Comment out this line for 24hr
    # monitoring.

    if RPi.GPIO.input(main_pump_relay) == 1:

        # check the limits for each sensor to trigger the alert email

        for reading in alert_readings:
            for key, value in sensors.items():
                if reading[0] == value["name"]:
                    if  ((reading[1] <
                        all_settings[value["lower_alert_name"]])or
                        (reading[1] >
                        all_settings[value["upper_alert_name"]])):
                        alert_check = True
                    else:
                        alert_check = False

    return alert_check


def reset_email_sent_flag_if_alerts_clear(email_sent):

    check = []

    # Get all the limit settings for the alert

    all_settings = get_settings_table_values()

    for reading in alert_readings:
        for key, value in sensors.items():
            if reading[0] == value["name"]:

                if  (reading[1] >
                    (all_settings[value["lower_alert_name"]] *
                    (1 + all_settings["offset_percent"])) and
                    (reading[1] <
                    (all_settings[value["upper_alert_name"]] *
                    (1 - all_settings["offset_percent"])))):
                    check.append("OK")

    # Check if all the sensor readings are now OK, if so reset email_sent flag

    if len(alert_readings) == len(check):
        email_sent = False

    return (email_sent)


def reset_pause_readings():

    # Reset pause flag to restart sensor readings

    conn, curs = open_database_connection()

    curs.execute("UPDATE IGNORE settings SET pause_readings = False "
                 "WHERE pk=1;")

    close_database_connection(conn, curs)

    return


def read_timer_override_data():

    # Read whether the Relay should be On, Off or using the timer

    conn, curs = open_database_connection()

    curs.execute("SELECT * FROM timer_override WHERE pk=(1)")
    override_timer_values = curs.fetchone()

    close_database_connection(conn, curs)

    return override_timer_values

#Get the start/stop pairs from the database


def get_relay_timer_start_stop_data(tablename, row):

    conn, curs = open_database_connection()

    curs.execute("SELECT * FROM {} WHERE pk={}".format(tablename, row))
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


def current_relay_state(currrelay, relaystate):

    conn, curs = open_database_connection()

    curs.execute("UPDATE IGNORE timer_override SET {} = {} WHERE pk = 2"
                .format(currrelay, relaystate))

    close_database_connection(conn, curs)

    return


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
                    relayname = ("relay_" + str(rct))
                    current_relay_state(relayname, relayon)
                    break
                elif relayon is False:
                    dtpair += 1
                if dtpair == (ndtp + 1):
                    RPi.GPIO.output(opp, False)
                    relayname = ("relay_" + str(rct))
                    current_relay_state(relayname, relayon)
        elif override[rct] == "on":
            RPi.GPIO.output(opp, True)  # turn relay on
            relayname = ("relay_" + str(rct))
            current_relay_state(relayname, True)
        elif override[rct] == "off":
            RPi.GPIO.output(opp, False)  # turn relay off
            relayname = ("relay_" + str(rct))
            current_relay_state(relayname, False)
    return

# Configuration Settings

# Define the sensor names, what sensors are connected, the sensor type, the
# atlas scientific sensor I2C addresses and define a primary temperature sensor.
# In the case shown below that would be either "temp_1" or "atlas_sensor_1".
# This is the sensor that is in the liquid that is being sampled and is used
# as a reference by the other sensors. If there are no temperature sensors
# connected a default value of 25C will be applied.
#
# Note: The temperature sensors cannot both be set to "is_ref: True", also
# "temp_1" must always be a DS18B20 type sensor and "atlas_sensor_1" must
# always be an Atlas Scientific type temperature sensor so that the reference
# temperature is always set before the other Atlas Scientific sensors are read.

sensors = OrderedDict([("temp_1", {  # DS18B20 Temperature Sensor
                            "sensor_type": "1_wire_temp",
                            "name": "ds18b20_temp",
                            "is_connected": True,
                            "is_ref": False,
                            "ds18b20_file":
                            "/sys/bus/w1/devices/28-xxxxxxxxxxxx/w1_slave",
                            "accuracy": 1,
                            "test_for_alert": False,
                            "upper_alert_name": "ds18b20_temp_hi",
                            "upper_alert_value": 50,
                            "lower_alert_name": "ds18b20_temp_low",
                            "lower_alert_value": 10}),

                       ("atlas_sensor_1", {  # Atlas Scientific Temp Sensor
                            "sensor_type": "atlas_scientific_temp",
                            "name": "atlas_temp",
                            "is_connected": True,
                            "is_ref": True,
                            "i2c": 102,
                            "accuracy": 1,
                            "test_for_alert": False,
                            "upper_alert_name": "atlas_temp_hi",
                            "upper_alert_value": 40,
                            "lower_alert_name": "atlas_temp_low",
                            "lower_alert_value": 25}),

                       ("atlas_sensor_3", {  # Atlas Scientific EC Sensor
                            "sensor_type": "atlas_scientific_ec",
                            "name": "ec",
                            "is_connected": True,
                            "is_ref": False,
                            "i2c": 100,
                            "accuracy": 0,
                            "ppm_multiplier": 0.67,  # Convert EC to PPM
                            "test_for_alert": True,
                            "upper_alert_name": "ec_hi",
                            "upper_alert_value": 6000,
                            "lower_alert_name": "ec_low",
                            "lower_alert_value": 4500}),

                       ("atlas_sensor_4", {  # pH/ORP Atlas Scientific Sensor
                            "sensor_type": "atlas_scientific",
                            "name": "ph",
                            "is_connected": True,
                            "is_ref": False,
                            "i2c": 99,
                            "accuracy": 2,
                            "test_for_alert": True,
                            "upper_alert_name": "ph_hi",
                            "upper_alert_value": 7.4,
                            "lower_alert_name": "ph_low",
                            "lower_alert_value": 7}),

                       ("atlas_sensor_5", {  # pH/ORP Atlas Scientific Sensor
                            "sensor_type": "atlas_scientific",
                            "name": "orp",
                            "is_connected": True,
                            "is_ref": False,
                            "i2c": 98,
                            "accuracy": 0,
                            "test_for_alert": True,
                            "upper_alert_name": "orp_hi",
                            "upper_alert_value": 700,
                            "lower_alert_name": "orp_low",
                            "lower_alert_value": 550})])

# Define other alert settings

misc_setting = {"offset_percent": 2,  # Stop toggling when close to alert value
                "pause_readings": False,
                "email_reset_delay": 172800,  # 60x60x24x2 = 2 Days
                "read_sensor_delay": 290,  # 60x5 = 5 Minutes
                "pause_reset_delay": 1800,  # 60x30 = 30 Minutes
                "to_email": "ToEmail@Address.com"}

# Define MySQL database login settings

servername = "localhost"
username = "YourMysqlUsername"
password = "YourMysqlPassword"
dbname = "YourMysqlDatabaseName"

# Define Relay Settings

outputpins = [22, 23, 24, 25]  # Specifiy a RPi GPIO Pin for each relay
numdtpairs = [4, 3, 2, 1]  # Number of Start/Stop pairs for each relay
relaycount = range(1, (len(outputpins) + 1))

# Define other settings

# number of seconds between sensor readings
time_between_readings = misc_setting["read_sensor_delay"]
main_pump_relay = outputpins[0]  # Stops email alert check if the pump is "off"
alert_check = False
loops = 0  # Set starting loops count for timing relay and sensor readings
email_sent = False
email_sent_reset = 0
pause_loops = 0


#################
#               #
# Main Program  #
#               #
#################


# Sanity Checks

check_number_of_relays_equals_start_stop_pairs()
check_for_only_one_reference_temperature()

# Configure relay GPIO ports

set_GPIO_pins()

# Build/Remove MySQL Database Entries

create_database()

relay_timer_names = create_relay_tables()
create_timer_override_table()
create_sensors_table()
create_settings_table()

remove_excess_timer_override_and_relay_database_entries()
remove_excess_datetime_pairs()
remove_unused_sensors()

while True:  # Repeat the code indefinitely

    # Control the relays

    activate_deactivate_relays()

    sleep(1)

    # Check if sensor readings have been paused, if not then read and store
    # sensor values and check against alert values, send an email if required

    if loops == time_between_readings:
        loops = 0

        # Read delay values from settings table

        delays = get_settings_table_values()
        time_between_readings = delays["read_sensor_delay"]
        email_reset_loop = (delays["email_reset_delay"] //
                                    time_between_readings)
        pause_reset_loop = (delays["pause_reset_delay"] //
                                    time_between_readings)

        if delays["pause_readings"] == 0:
            alert_readings = read_sensors()

            if alert_check is True and email_sent is True:
                email_sent = reset_email_sent_flag_if_alerts_clear(email_sent)
                if email_sent is False:
                    alert_check is False
                    email_sent_reset = 0

            elif alert_check is False:
                alert_check = check_sensor_alert_limits(alert_check)
                if alert_check is True:
                    email_sent = send_email(alert_readings)
                    email_sent = True
                    email_sent_reset = 0

        elif delays["pause_readings"] == 1:
            pause_loops += 1
            if pause_loops == pause_reset_loop:
                reset_pause_readings()
                pause_loops = 0

        if email_sent is True:
            email_sent_reset += 1
            if email_sent_reset == email_reset_loop:
                alert_check = False
                email_sent_reset = 0

    loops += 1
