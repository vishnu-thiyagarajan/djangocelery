from __future__ import absolute_import, unicode_literals
import requests
import zipfile
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from django.conf import settings
from celery import shared_task


@shared_task
def downloadandemail(data):
    list_of_files = []
    list_of_urls = data['urls']
    msg = MIMEMultipart()
    msg['From'] = settings.EMAIL_HOST_USER
    msg['To'] = data['email']
    msg['Subject'] = 'Html files attached for listed urls'
    body = 'Hi there, sending this email from Python!'
    msg.attach(MIMEText(body, 'plain'))
    for item in range(0, len(list_of_urls)):
        file = requests.get(list_of_urls[item])
        f = open(str(item + 1) + ".html", "w")
        f.write(file.text)
        f.close()
        list_of_files.append(str(item + 1) + ".html")
    with zipfile.ZipFile('out.zip', 'w') as zipMe:
        for file in list_of_files:
            zipMe.write(file, compress_type=zipfile.ZIP_DEFLATED)
    filename = 'out.zip'
    attachment = open(filename, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename=" + filename)
    msg.attach(part)
    text = msg.as_string()
    server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    server.starttls()
    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    server.sendmail(settings.EMAIL_HOST_USER, data['email'], text)
    server.quit()
