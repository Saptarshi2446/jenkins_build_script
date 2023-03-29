import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Your Mailjet API credentials
#mailjet_api_key = 'e907b2941debdb6e56a9db0e350fd07f'
#mailjet_api_secret = '32c01d1b750667c0591b7585d1d67540'
mailjet_api_key = '547fa6ae837634b0e2260b5d95aaf795'
mailjet_api_secret = 'bc6be0bbf4faa323e695313e7340a0a1'

# Recipient email
receivers_mail = ['saptarshi.r@paramaah.com', 'sachin.jp@paramaah.com']
to_email = ", ".join(receivers_mail)

# Create message
msg = MIMEMultipart()
msg['From'] = 'sachinjayaprakash07@gmail.com'
msg['To'] = to_email
msg['Subject'] = 'Test Email with Attachment'

body = 'Hello, this is a test email from Python using Mailjet with an attachment!'
msg.attach(MIMEText(body, 'plain'))

# Attach file
filename = '/tmp/Daily/report.csv'
attachment_path = os.path.join(os.getcwd(), filename)
with open(attachment_path, 'rb') as attachment:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={filename}')
    msg.attach(part)

# Connect to Mailjet SMTP server and send email
smtp_server = 'in-v3.mailjet.com'
smtp_port = 587
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.login(mailjet_api_key, mailjet_api_secret)
text = msg.as_string()
server.sendmail(msg['From'], to_email, text)
server.quit()

print('Email sent successfully with attachment!')
