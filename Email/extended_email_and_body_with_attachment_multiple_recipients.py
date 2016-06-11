#!/usr/bin/env python

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

fromaddr = "FromUser@gmail.com"
toaddr = "ToUser1@gmail.com,ToUser2@gmail.com"
ccaddr = "ToUser3@gmail.com,ToUser4@gmail.com,ToUser5@gmail.com"
bccaddr = "ToUser6@gmail.com"
alladdr = toaddr.split(",") + ccaddr.split(",") + [bccaddr]

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
server.sendmail(fromaddr, alladdr, text)
server.quit()