#!/usr/bin/env python

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

fromaddr = "FromUser@gmail.com"
toaddr = "ToUser@gmail.com"
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Test Alert"
f = open("PathToEmailBodyTextWithExtension")

body = f.read()
msg.attach(MIMEText(body, 'plain'))

filename = "AttachmentFileWithExt"
attachment = open("PathToFile", "rb")

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

msg.attach(part)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "FromUserEmailPassword")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
