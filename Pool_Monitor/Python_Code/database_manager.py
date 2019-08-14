#!/usr/bin/env python

# Import Python Modules

import logging
import mysql.connector as mariadb

# Import Custom Modules

import hydropi_variables as var


# Create required database in the MySQL if it doesn't' already exist


def create_database():

    try:
        conn = mariadb.connect(user=var.username,
                            password=var.password,
                            host=var.servername)
        curs = conn.cursor()
        curs.execute("SET sql_notes = 0; ")  # Hide Warnings
        curs.execute("CREATE DATABASE IF NOT EXISTS {}".format(var.dbname))
        curs.execute("SET sql_notes = 1; ")  # Show Warnings
    except mariadb.Error as error:
        logging.warning("Create Database Error: {}".format(error))
        pass
    conn.commit()
    conn.close()
    return


def open_database_connection():

    try:    
        conn = mariadb.connect(user=var.username,
                                password=var.password,
                                host=var.servername,
                                database=var.dbname)
        curs = conn.cursor()
        curs.execute("SET sql_notes = 0; ")  # Hide Warnings
    except mariadb.Error as error:
        logging.warning("Database Open Connection Error: {}".format(error))
        pass
    return conn, curs


def execute_query(curs, dbquery):
    try:
        curs.execute(dbquery)
    except mariadb.Error as error:
        logging.warning("Database Query Execution Error: {}".format(error))
        pass
    return curs


def close_database_connection(conn, curs):

    try:
        curs.execute("SET sql_notes = 1; ")  # Show Warnings
    except mariadb.Error as error:
        logging.warning("Database Close Connection Error: {}".format(error))
        pass
    conn.commit()
    conn.close()


#  Create all the tables required in the database

def create_database_tables():

    # Create the relays table and add default data

    conn, curs = open_database_connection()

    dtcount = 0

    for tablename in var.relay_timer_names:
        execute_query(curs, "CREATE TABLE IF NOT EXISTS {} "
                    "(pk INT UNSIGNED PRIMARY KEY,"
                    "starttime DATETIME DEFAULT NULL, "
                    "stoptime DATETIME DEFAULT "
                    "NULL);".format(tablename))

    # Add default "NULL" data to each relay_timer table

        for pairs in range(1, (var.numdtpairs[dtcount] + 1)):

            execute_query(curs, "INSERT IGNORE INTO {} (pk,starttime,stoptime)"
                        " VALUES({},NULL,NULL)".format(tablename, pairs))
        dtcount += 1

    # Create the timer_override table
 
    execute_query(curs, "CREATE TABLE IF NOT EXISTS timer_override "
                                "(pk INT UNSIGNED PRIMARY KEY);")
    execute_query(curs, "INSERT IGNORE INTO timer_override (pk) VALUES(1)")
    execute_query(curs, "INSERT IGNORE INTO timer_override (pk) VALUES(2)")

    # Add relay columns and default to "off" in the timer_override table

    for number in var.relaycount:
        relayname = ("relay_" + str(number))

        i = execute_query(curs, "SELECT {} FROM timer_override WHERE pk = 1"
                        .format(relayname))
        result = i.fetchone()
        if result is None:
            execute_query(curs, "ALTER TABLE timer_override ADD {} VARCHAR(5)"
                            .format(relayname))
            execute_query(curs, "UPDATE IGNORE timer_override SET {} = 'off' "
                        "WHERE pk = 1;".format(relayname))

        i = execute_query(curs, "SELECT {} FROM timer_override WHERE pk = 2"
                        .format(relayname))
        result = i.fetchone()
        if result is None:
            curs.execute("UPDATE IGNORE timer_override SET {} = 'False' "
                        "WHERE pk = 2;".format(relayname))


    # Create the sensors table

    execute_query(curs, "CREATE TABLE IF NOT EXISTS sensors (timestamp DATETIME);")

    for key, value in list(var.sensors.items()):
        if value["is_connected"] is True:
            i = execute_query(curs, "SELECT {} FROM sensors LIMIT 1"
                        .format(value["name"]))
            result = i.fetchone()
            if result is None:
                execute_query(curs, "ALTER TABLE sensors ADD {} DECIMAL(10,2);"
                .format(value["name"]))

    # Create the settings table and add configured data

    execute_query(curs, "CREATE TABLE IF NOT EXISTS settings "
                "(pk TINYINT(1) UNSIGNED PRIMARY"
                " KEY);")
    i = execute_query(curs, "SELECT pk FROM settings LIMIT 1")
    result = i.fetchone()
    if result is None:
        execute_query(curs, "INSERT IGNORE INTO settings (pk) VALUES(1)")

    for key, value in list(var.sensors.items()):
        i = execute_query(curs, "SELECT {} FROM settings LIMIT 1"
                        .format(value["upper_alert_name"]))
        result = i.fetchone()
        if result is None:
            execute_query(curs, "ALTER TABLE settings ADD ({} DECIMAL(10,2), "
            "{} DECIMAL(10,2));".format(value["upper_alert_name"],
                                        value["lower_alert_name"]))
            execute_query(curs, "UPDATE IGNORE settings SET {} = {}, {} = {} "
                    "WHERE pk=1;".format(value["upper_alert_name"],
                                        value["upper_alert_value"],
                                        value["lower_alert_name"],
                                        value["lower_alert_value"]))

    for key, value in list(var.misc_setting.items()):
        if key == "to_email":
            i = execute_query(curs, "SELECT {} FROM settings LIMIT 1"
                            .format(key))
            result = i.fetchone()
            if result is None:
                execute_query(curs, "ALTER TABLE settings ADD {} VARCHAR(254);"
                                    .format(key))
                execute_query(curs, "UPDATE IGNORE settings SET {} = '{}' "
                        "WHERE pk=1;".format(key, value))

        elif key == "pause_readings":
            i = execute_query(curs, "SELECT {} FROM settings LIMIT 1"
                            .format(key))
            result = i.fetchone()
            if result is None:
                execute_query(curs, "ALTER TABLE settings ADD {} BOOLEAN;"
                                    .format(key))
                execute_query(curs, "UPDATE IGNORE settings SET {} = {} "
                        "WHERE pk=1;".format(key, value))

        elif key == "offset_percent":
            i = execute_query(curs, "SELECT {} FROM settings LIMIT 1"
                            .format(key))
            result = i.fetchone()
            if result is None:
                execute_query(curs, "ALTER TABLE settings ADD {} DECIMAL(10,2);"
                                    .format(key))
                execute_query(curs, "UPDATE IGNORE settings SET {} = {} "
                        "WHERE pk=1;".format(key, value))

        else:
            i = execute_query(curs, "SELECT {} FROM settings LIMIT 1"
                            .format(key))
            result = i.fetchone()
            if result is None:
                execute_query(curs, "ALTER TABLE settings ADD {} INT(10);"
                                    .format(key))
                execute_query(curs, "UPDATE IGNORE settings SET {} = {} "
                        "WHERE pk=1;".format(key, value))

    close_database_connection(conn, curs)
    return


# Remove excess columns from tables in the database


def remove_excess_database_entries():

    conn, curs = open_database_connection()

    # remove excess timer override and relay database entries

    execute_query(curs, "SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE "
                "TABLE_NAME = 'timer_override';")
    colnum = curs.fetchone()
    colnum = (int(colnum[0])) - 1

    while colnum > len(var.outputpins):
        execute_query(curs, "ALTER TABLE timer_override DROP {};"
                    .format("relay_" + str(colnum)))
        execute_query(curs, "DROP TABLE {};"
                    .format("relay_" + str(colnum) + "_timer"))
        execute_query(curs, "SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE "
                    "TABLE_NAME = 'timer_override';")
        colnum = curs.fetchone()
        colnum = (int(colnum[0])) - 1

    # remove excess datetime pairs

    dtcount = 0

    for relay in var.relay_timer_names:
        execute_query(curs, "DELETE FROM {} WHERE pk > {};"
                    .format(relay, var.numdtpairs[dtcount]))
        dtcount += 1

    # remove unused sensors

    for key, value in list(var.sensors.items()):
        if value["is_connected"] is False:
            execute_query(curs, "ALTER TABLE sensors DROP {};"
                        .format(value["name"]))

    # remove unused sensors settings

    for key, value in list(var.sensors.items()):
        if value["is_connected"] is False:
            execute_query(curs, "ALTER TABLE settings DROP COLUMN {}, "
            "DROP COLUMN {};"
            .format(value["upper_alert_name"],
                    value["lower_alert_name"]))

    close_database_connection(conn, curs)

    return

    # read and log each sensor if it is set to True in the sensors list


def log_sensor_readings(all_curr_readings):

    # Create a timestamp and store all readings on the MySQL database

    conn, curs = open_database_connection()
    execute_query(curs, "INSERT INTO sensors (timestamp) VALUES(now());")
    execute_query(curs, "SELECT MAX(timestamp) FROM sensors")
    last_timestamp = curs.fetchone()
    last_timestamp = last_timestamp[0].strftime('%Y-%m-%d %H:%M:%S')

    for readings in all_curr_readings:
        execute_query(curs, "UPDATE sensors SET {} = {} WHERE timestamp = '{}'"
                        .format(readings[0], readings[1], last_timestamp))

    close_database_connection(conn, curs)

    return

def get_settings_table_values():

    # Get the current alert limit settings from the database

    conn, curs = open_database_connection()
    curs = conn.cursor(dictionary=True)
    execute_query(curs, "SELECT * FROM settings WHERE pk = 1")
    setting_values = curs.fetchone()

    # divide offset percent by 100 to convert to decimal
    setting_values["offset_percent"] = (setting_values["offset_percent"] / 100)

    close_database_connection(conn, curs)

    return setting_values

def reset_pause_readings():

    # Reset pause flag to restart sensor readings

    conn, curs = open_database_connection()

    execute_query(curs, "UPDATE IGNORE settings SET pause_readings = False "
                "WHERE pk=1;")

    close_database_connection(conn, curs)

    return

def read_timer_override_data():

    # Read whether the Relay should be On, Off or using the timer

    conn, curs = open_database_connection()

    execute_query(curs, "SELECT * FROM timer_override WHERE pk=(1)")
    override_timer_values = curs.fetchone()

    close_database_connection(conn, curs)

    return override_timer_values

#Get the start/stop pairs from the database

def get_relay_timer_start_stop_data(tablename, row):

    conn, curs = open_database_connection()

    execute_query(curs, "SELECT * FROM {} WHERE pk={}".format(tablename, row))
    relay_timer_values = curs.fetchone()

    close_database_connection(conn, curs)

    return relay_timer_values


def current_relay_state(currrelay, relaystate):

    conn, curs = open_database_connection()

    execute_query(curs, "UPDATE IGNORE timer_override SET {} = {} WHERE pk = 2"
                    .format(currrelay, relaystate))

    close_database_connection(conn, curs)

    return