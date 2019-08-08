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
# receiver and a subject line. In addition it will also read a pre prepared
# text and html file and use it's contents to create the body of the email
#
##############################################################################

#!/usr/bin/env python

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Create email header
fromaddr = "FromUser@gmail.com"
toaddr = "ToUser1@gmail.com,ToUser2@gmail.com,ToUser3@gmail.com"
alladdr = toaddr.split(",")

msg = MIMEMultipart("alternative")
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Test Alert"

# Open the body text file and join it to the message
ftext = open("FullPathToEmailBodyText/FileName.Extension")
bodytext = ftext.read()
msg.attach(MIMEText(bodytext, 'plain'))

# Open the body html file and join it to the message
fhtml = open("FullPathToEmailBodyHTML/FileName.Extension")
bodyhtml = fhtml.read()
msg.attach(MIMEText(bodyhtml, 'html'))

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
server.login(fromaddr, "FromUserEmailPassword")

# Join all parts of the email and send
text = msg.as_string()
server.sendmail(fromaddr, alladdr, text)
server.quit()