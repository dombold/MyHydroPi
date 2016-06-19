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
# This program is designed to send an email with a sender, receiver and
# a subject line along with a short message in the body of the email
#
##############################################################################

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Create email header
fromaddr = "FromUser@gmail.com"
toaddr = "ToUser@gmail.com"
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Test Alert"

# Create email body text
body = 'This is an extended email test'
msg.attach(MIMEText(body, 'plain'))

# Establish connection with the email server
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "FromUser_Email_Password")

# Join all parts of the email and send
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()