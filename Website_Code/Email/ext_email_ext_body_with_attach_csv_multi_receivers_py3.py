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
# receivers and a subject line. In addition it will also read a pre prepared
# text and html file and use it's contents to create the body of the email.
# Finally it will use a CSV file to get the receivers and send them a
# personalised email.
#
##############################################################################

#!/usr/bin/env python

import smtplib
import csv

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Create email header
fromaddr = "FromUser@gmail.com"

msg = MIMEMultipart("mixed")
msg['From'] = fromaddr
msg['Subject'] = "Final Results"

msgAlternative = MIMEMultipart('alternative')
msg.attach(msgAlternative)

# Open the body text file and join it to the message
ftext = open("FullPathToEmailBodyText/FileName.Extension")
bodytext = ftext.read()
msgAlternative.attach(MIMEText(bodytext, 'plain'))

# Open the body html file and join it to the message
fhtml = open("FullPathToEmailBodyHTML/FileName.Extension")
bodyhtml = fhtml.read()
msgAlternative.attach(MIMEText(bodyhtml, 'html'))

# Open the attachment and join it to the message
filename = "AttachmentFileName"
attachment = open("FullPathToFile/AttachmentFileName.Extension", "rb")

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
with open("FullPathToCsvFile/FileName.Extension") as file:
    reader = csv.reader(file)
    next(reader)
    # Read the CSV file to get receiver emails and personalise
    # the body of the email
    for User, Email, Score, Result in reader:
        text = msg.as_string()
        text = text.format(User=User,Score=Score,Result=Result)
        server.sendmail(fromaddr, Email, text,)
server.quit()
