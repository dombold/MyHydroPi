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
# 2. The program will also create the initial database and tables if they do
# not already exist in MySQL.
#
# For Python 3 I have used python-mysqldb module to connect to the database.
# to add the module you need to enter the following commands
#
# sudo apt install python-mysqldb
#
##############################################################################

import io
import os
import sys
import fcntl
import mysql.connector as mariadb
from time import sleep
from collections import OrderedDict


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
        self.file_write.write(bytes(string, 'UTF-8'))

    def read(self, num_of_bytes=31):
        # reads a specified number of bytes from I2C,
        # then parses and displays the result
        res = self.file_read.read(num_of_bytes)  # read from the board
        # remove the null characters to get the response
        response = list([x for x in res])

        if(response[0] == 1):  # if the response isnt an error
            # change MSB to 0 for all received characters except the first
            # and get a list of characters
            char_list = [chr(x & ~0x80) for x in list(response[1:])]
            # NOTE: having to change the MSB to 0 is a glitch in the
            # raspberry pi, and you shouldn't have to do this!
            # convert the char list to a string and returns it
            result = ''.join(char_list)
            return result.split('\x00')[0]
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


# Check that only one Primary Temperature sensor is defined


def check_for_only_one_reference_temperature():

    ref_check = 0

    for key, value in list(sensors.items()):
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


def create_sensors_table():

    conn, curs = open_database_connection()
    try:
        curs.execute("CREATE TABLE IF NOT EXISTS sensors (timestamp DATETIME);")
    except mariadb.Error as error:
        print("Error: {}".format(error))
        pass

    for key, value in list(sensors.items()):
        if value["is_connected"] is True:
            try:
                curs.execute("ALTER TABLE sensors ADD {} DECIMAL(10,2);"
                .format(value["name"]))
            except mariadb.Error as error:
                print("Error: {}".format(error))
                pass

    close_database_connection(conn, curs)

    return


def remove_unused_sensors():

    conn, curs = open_database_connection()

    for key, value in list(sensors.items()):
        if value["is_connected"] is False:
            try:
                curs.execute("ALTER TABLE sensors DROP {};"
                            .format(value["name"]))
            except mariadb.Error as error:
                print("Error: {}".format(error))
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
        lines = read_1_wire_temp_raw(temp_num)
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
    try:
        curs.execute("INSERT INTO sensors (timestamp) VALUES(now());")
        curs.execute("SELECT MAX(timestamp) FROM sensors")
    except mariadb.Error as error:
        print("Error: {}".format(error))
        pass
    last_timestamp = curs.fetchone()
    last_timestamp = last_timestamp[0].strftime('%Y-%m-%d %H:%M:%S')

    for readings in all_curr_readings:
        try:
            curs.execute(("UPDATE sensors SET {} = {} WHERE timestamp = '{}'")
                        .format(readings[0], readings[1], last_timestamp))
        except mariadb.Error as error:
            print("Error: {}".format(error))
            pass

    close_database_connection(conn, curs)

    return


def read_sensors():

    all_curr_readings = []
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

    log_sensor_readings(all_curr_readings)

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
                            "/sys/bus/w1/devices/28-01157127dfff/w1_slave",
                            "accuracy": 1}),

                       ("atlas_sensor_1", {  # Atlas Scientific Temp Sensor
                            "sensor_type": "atlas_scientific_temp",
                            "name": "atlas_temp",
                            "is_connected": True,
                            "is_ref": True,
                            "i2c": 102,
                            "accuracy": 1}),

                       ("atlas_sensor_2", {  # pH/ORP Atlas Scientific Sensor
                            "sensor_type": "atlas_scientific",
                            "name": "ph",
                            "is_connected": True,
                            "is_ref": False,
                            "i2c": 99,
                            "accuracy": 2}),

                       ("atlas_sensor_3", {  # pH/ORP Atlas Scientific Sensor
                            "sensor_type": "atlas_scientific",
                            "name": "orp",
                            "is_connected": True,
                            "is_ref": False,
                            "i2c": 98,
                            "accuracy": 0}),

                       ("atlas_sensor_4", {  # Atlas Scientific EC Sensor
                            "sensor_type": "atlas_scientific_ec",
                            "name": "ec",
                            "is_connected": True,
                            "is_ref": False,
                            "i2c": 100,
                            "accuracy": 0,
                            "ppm_multiplier": 0.67})])  # Convert EC to PPM

# Define MySQL database login settings

servername = "localhost"
username = "YourMysqlUsername"
password = "YourMysqlPassword"
dbname = "YourMysqlDatabaseName"

loops = 0  # Set starting loops count sensor readings


#################
#               #
# Main Program  #
#               #
#################


# Sanity Checks

check_for_only_one_reference_temperature()

# Build/Remove MySQL Database Entries

create_database()
create_sensors_table()
remove_unused_sensors()

while True:  # Repeat the code indefinitely

    if loops == 300:
        loops = 0

        read_sensors()

    loops += 1
    sleep(1)
