#!/usr/bin/env python

##############################################################################
#
# Written by Dominic Bolding for the Raspberry Pi - 2016
#
# Website: myhydropi.com
# Contact: admin@myhydropi.com
#
# Please feel free to use and modify this code for you own use.
#
# This program is designed to send a simple email with just a basic message
# in the body of the email and who it is from.
#
##############################################################################

import smtplib

# Establish connection with the email server
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("FromUser@gmail.com", "FromUserPassword")

# Create email body text and send
msg = "This is a simple email test!"
server.sendmail("FromUser@gmail.com", "ToUser@gmail.com", msg)
server.quit()