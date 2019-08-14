#!/usr/bin/env python

# Import Python Modules

import smtplib
import logging
import RPi.GPIO
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#  Import Custom Modules

import hydropi_variables as var
import database_manager as dbman

#Generate an email when there is a problem with the pool

def send_email(alert_readings, address):

    # Create a string of "out of linmit" sensors and values for the email body

    out_of_limit_sensors_text = ""
    out_of_limit_sensors_html = "<br>"

    for k, v in alert_readings:
        out_of_limit_sensors_text = (out_of_limit_sensors_text + "\n" + k + "  -  " +
                                    str(v) + "\n\n")
        out_of_limit_sensors_html = (out_of_limit_sensors_html + 
                                    "<tr style=\"text-align: center;\"><td><h2>" + 
                                    k + " Sensor " + "  -  " + str(v) + 
                                    "</h2></td></tr><br>")

    # Build email and send

    fromaddr = var.fromaddress
    toaddr = address["to_email"]
    alladdr = toaddr.split(",")
    msg = MIMEMultipart("alternative")
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Pool Alert"

    # Open the body text file and join it to the message
    ftext = open(var.textfile)
    bodytext = ftext.read()
    bodytext = bodytext.format(out_of_limit_sensors_text.upper())
    msg.attach(MIMEText(bodytext, 'plain'))

    # Open the body html file and join it to the message
    fhtml = open(var.htmlfile)
    bodyhtml = fhtml.read()
    bodyhtml = bodyhtml.format(out_of_limit_sensors_html.upper())
    msg.attach(MIMEText(bodyhtml, 'html'))

    server = smtplib.SMTP(var.emailserver, var.emailserverport)
    try:
        server.starttls()
        server.login(fromaddr, var.emailpassword)
        text = msg.as_string()
        server.sendmail(fromaddr, alladdr, text)
        server.quit()
    except:
        logging.warning("Email Server Connection Error")
        pass
    return

def reset_email_sent_flag_if_alerts_clear(alert_results, email_sent):

    check = []

    # Get all the limit settings for the alert

    all_settings = dbman.get_settings_table_values()

    for reading in alert_results:
        for key, value in list(var.sensors.items()):
            if reading[0] == value["name"]:

                if  (reading[1] >
                    (all_settings[value["lower_alert_name"]] *
                    (1 + all_settings["offset_percent"])) and
                    (reading[1] <
                    (all_settings[value["upper_alert_name"]] *
                    (1 - all_settings["offset_percent"])))):
                    check.append("OK")

    # Check if all the sensor readings are now OK, if so reset email_sent flag

    if len(alert_results) == len(check):
        var.email_sent = False

    return (var.email_sent)

def check_sensor_alert_limits(alert_results, alert_flag):

    # Get all the limit settings for the email alert

    all_settings = dbman.get_settings_table_values()

    # The IF statement below checks that the main pump relay is active before
    # checking the sensor alert limits. Comment out this line for 24hr
    # monitoring.

    if RPi.GPIO.input(var.main_pump_relay) == 1:

        # check the limits for each sensor to trigger the alert email

        for reading in alert_results:
            for key, value in list(var.sensors.items()):
                if reading[0] == value["name"]:
                    if  ((reading[1] <
                        all_settings[value["lower_alert_name"]])or
                        (reading[1] >
                        all_settings[value["upper_alert_name"]])):
                        alert_flag = True
                    else:
                        alert_flag = False

    return alert_flag