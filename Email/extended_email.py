#!/usr/bin/env python

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


fromaddr = "FromUser@gmail.com"
toaddr = "ToUser@gmail.com"
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Test Alert"

body = 'This is an extended email test'
msg.attach(MIMEText(body, 'plain'))

server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo
server.starttls()
server.login(fromaddr, "FromUserEmailPassword")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
