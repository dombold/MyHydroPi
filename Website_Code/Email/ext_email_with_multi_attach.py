#!/usr/bin/env python

##############################################################################
#
# Written by Dominic Bolding for the Raspberry Pi - 2019
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
import os.path

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
body = 'This is an extended email test with multiple attachments'
msg.attach(MIMEText(body, 'plain'))

# Define the attachments and their location
dir_path = "PathToAttachmentFolder" # eg. /home/pi/documents
files = ["FileName1.ext", "FileName2.ext", "FileName3.ext"]

part = MIMEBase('application', 'octet-stream')

# add multiple files to the message
for f in files:  
    file_path = os.path.join(dir_path, f)
    part.set_payload((open(file_path, "rb")).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',"attachment, filename={}".
        format(f))
    msg.attach(part)

# Establish connection with the email server
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "FromUser_Email_Password")

# Join all parts of the email and send
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()