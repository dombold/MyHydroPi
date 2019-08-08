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
# This program is designed to send an email with an attachment, sender,
# receiver and a subject line along with a short message in the body of
# the email
#
##############################################################################

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

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

# Open the attachment and join it to the message
filename = "Attachment_File_With_Extension"
attachment = open("Path_To_File", "rb")

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= {}".
    format(filename))
msg.attach(part)

# Establish connection with the email server
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "FromUser_Email_Password")

# Join all parts of the email and send
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()