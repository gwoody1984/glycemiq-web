import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .config import config_as_dict


def send_mail(to_address, message_subject, message_body):
    config = config_as_dict('APP')

    user = config['MAIL_USER']
    password = config['MAIL_PASSWORD']

    msg = MIMEMultipart()
    msg['From'] = user
    msg['To'] = to_address
    msg['Subject'] = message_subject
    msg.attach(MIMEText(message_body, 'html'))

    mail_server = smtplib.SMTP(config['MAIL_SERVER'], config['MAIL_PORT'])
    mail_server.ehlo()
    mail_server.starttls()
    mail_server.ehlo()
    mail_server.login(user, password)
    mail_server.sendmail(user, to_address, msg.as_string())
    mail_server.close()
