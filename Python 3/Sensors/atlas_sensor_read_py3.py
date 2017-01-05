#!/usr/bin/env python

##############################################################################
#
# Written by Dominic Bolding for the Raspberry Pi - 2017
#
# Website: myhydropi.com
# Contact: admin@myhydropi.com
#
# Feel free to use and modify this code for you own use in any way.
# atlas_i2c class code written by Atlas Scientific
#
##############################################################################

import io
import fcntl
from time import sleep


# Define Atlas Scientific Sensor Class


class atlas_i2c:

    long_timeout = 1.5  # the timeout needed to query readings & calibrations
    short_timeout = .5  # timeout for regular commands
    default_bus = 1  # the default bus for I2C on the newer Raspberry Pis,
                     # certain older boards use bus 0
    default_address = 99  # the default address for the Temperature sensor

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


def main():
    while True:  # Repeat the code indefinitely
        try:
            device = atlas_i2c(98)  # Oxidation Resuction Sensor
            orp_reading = device.query("R")
            print (orp_reading)
            #publish.single("ORP", orp_reading, hostname="your_server")
        except IOError:
            print ("Query failed")
        try:
            device = atlas_i2c(99)  # pH Sensor
            ph_reading = device.query("R")
            print (ph_reading)
            #publish.single("pH", ph_reading, hostname="your_server")
        except IOError:
            print ("Query failed")
        try:
            device = atlas_i2c(100)  # Electrical Conductivity Sensor
            ec_reading = device.query("R")
            print (ec_reading)
            #publish.single("EC", ec_reading, hostname="your_server")
        except IOError:
            print ("Query failed")
        try:
            device = atlas_i2c(102)  # Temperature Sensor
            temp_reading = device.query("R")
            print (temp_reading)
            #publish.single("Temp", temp_reading, hostname="your_server")
        except IOError:
            print ("Query failed")

        sleep(300)  # read sensor circuit every 300 sec (5 min)