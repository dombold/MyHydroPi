#!/usr/bin/env python

#  Import Python Modules

import io
import os
import fcntl
import logging
from time import sleep

#  Import Custom Modules

import hydropi_variables as var
import database_manager as dbman

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
            return "Error: " + str(ord(response[0]))

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


# Load Raspberry Pi Drivers for 1-Wire Temperature Sensor


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


# Read in the data from the Temp Sensor file


def read_1_wire_temp_raw(temp_num):

        f = open(var.sensors[temp_num]["ds18b20_file"], 'r')
        lines = f.readlines()
        f.close()

        return lines


# Process the Temp Sensor file for errors and convert to degrees C or F


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
        # Uncomment line below for Fahrenheit
        #temp_curr = ((float(temp_string) / 1000.0) * (9.0 / 5.0)) + 32

        return temp_curr

# read and log each sensor if it is set to True in the sensors list


def read_sensors():

    all_curr_readings = []
    alert_readings = []
    ref_temp = 25

    # Get the readings from any 1-Wire temperature sensors

    for key, value in var.sensors.items():
        if value["is_connected"] is True:
            if value["sensor_type"] == "1_wire_temp":
                try:
                    sensor_reading = (round(float(read_1_wire_temp(key)),
                                 value["accuracy"]))
                except:
                    logging.warning("{} - {} Error: {}".format(key, value["sensor_type"], sensor_reading))
                    sensor_reading = 0
                    
                all_curr_readings.append([value["name"], sensor_reading])

                if sensor_reading != 0:   
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
                    logging.warning("{} - {} {}".format(key, value["sensor_type"], sensor_reading))
                    sensor_reading = 0
                    
                all_curr_readings.append([value["name"], sensor_reading])

                if sensor_reading != 0: 
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
                    logging.warning("{} - {} {}".format(key, value["sensor_type"], sensor_reading))
                    sensor_reading = 0
                    
                all_curr_readings.append([value["name"], sensor_reading])

                if value["test_for_alert"] is True and sensor_reading != 0:
                    alert_readings.append([value["name"], sensor_reading])

    # Get the readings from any other Atlas Scientific sensors

            if value["sensor_type"] == "atlas_scientific":
                device = atlas_i2c(value["i2c"])
                # Set reference temperature value on the sensor
                # if statement added for latest Atlas firmware, no temp reference required
                # for the ORP sensor
                if value["name"] == "ph":
                    device.query("T," + str(ref_temp))
                try:
                    sensor_reading = round(float(device.query("R")),
                                value["accuracy"])
                except:
                    if value["name"] == "ph":
                        logging.warning("{} - {}_{} {}".format(key, value["sensor_type"], value["name"], sensor_reading))
                        sensor_reading = 0
                    elif value["name"] == "orp":
                        logging.warning("{} - {}_{} {}".format(key, value["sensor_type"], value["name"], sensor_reading))
                        sensor_reading = 0
                        
                all_curr_readings.append([value["name"], sensor_reading])

                if value["test_for_alert"] is True and sensor_reading != 0:
                    alert_readings.append([value["name"], sensor_reading])

    dbman.log_sensor_readings(all_curr_readings)

    # Alert_Readings will return just the readings from sensors you want
    # tested for the email alert

    return alert_readings