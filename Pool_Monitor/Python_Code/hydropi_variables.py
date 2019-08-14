#!/usr/bin/env python

#  Import Python Modules

from datetime import datetime
from collections import OrderedDict

# Define MySQL database login settings

servername = "localhost"
username = "yourDatabbaseUsername"
password = "yourdatabasePassword"
dbname = "hydropidb"

# Define Email Server login settings

fromaddress = "yourFromEmailAddress"
emailpassword = "yourFromEmailPassword"
emailserver = 'smtp.gmail.com'
emailserverport = 587
textfile = "path/ToEmail/Textfile.txt"
htmlfile = "path/ToEmail/Htmlfile.html"

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
                            "/sys/bus/w1/devices/28-XXXXXXXXXXXX/w1_slave",
                            "accuracy": 1,
                            "test_for_alert": False,
                            "upper_alert_name": "ds18b20_temp_hi",
                            "upper_alert_value": 50,
                            "lower_alert_name": "ds18b20_temp_low",
                            "lower_alert_value": 10}),

                         #("temp_2", {  # DS18B20 Temperature Sensor
                              #"sensor_type": "1_wire_temp",
                              #"name": "ds18b20_temp_2",
                              #"is_connected": True,
                              #"is_ref": False,
                              #"ds18b20_file":
                              #"/sys/bus/w1/devices/28-yyyyyyyyyyyy/w1_slave",
                              #"accuracy": 1,
                              #"test_for_alert": False,
                              #"upper_alert_name": "ds18b20_temp_hi_2",
                              #"upper_alert_value": 100,
                              #"lower_alert_name": "ds18b20_temp_low_2",
                              #"lower_alert_value": 75}),

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

# Define Relay Settings

outputpins = [22, 23, 24, 25]  # Specifiy a RPi GPIO Pin for each relay
numdtpairs = [4, 3, 2, 1]  # Number of Start/Stop pairs for each relay
relaycount = list(range(1, (len(outputpins) + 1)))

# Generate database column relay names

relay_timer_names = []

for number in relaycount:
    relay = ("relay_" + str(number) + "_timer")
    relay_timer_names.append(relay)

# Define other settings

misc_setting = {"offset_percent": 2,  # Stop toggling when close to alert value
                "pause_readings": False, # Initially set to False on startup
                "email_reset_delay": 172800,  # in seconds 60x60x24x2 = 2 Days
                "read_sensor_delay": 300,  # in seconds 60x5 = 5 Minutes
                "pause_reset_delay": 1800,  # in seconds 60x30 = 30 Minutes
                "to_email": "yourToEmailAddress", # destination email address
                "pool_size" : 27000} # pool volume in litres

# Define other True/False flags and timing

# Sets the delay equivalent to the "read sensor delay" before the first reading
time_between_readings = misc_setting["read_sensor_delay"]
main_pump_relay = outputpins[0]  # Stops email alert check if the pump is "off"
alert_check = False #  Is False if all sensors are within the set limits 
sensor_ref_time = datetime.now()  # Set starting time
email_sent = False #  Is False if an email has not been sent in "email reset delay" time
new_pause = True # Is True if sensor readings are currently not paused