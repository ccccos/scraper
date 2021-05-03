import smtplib
import datetime
from email.mime.text import MIMEText
import random

'''This module is used to send notification email'''
class Notification_Sender():
    def __init__(self, data):
        self.smtp = smtplib.SMTP_SSL
        self.sender = 'miniteckmonitor@gmail.com'
        self.receiver = 'miniteckmonitor@gmail.com'
        self.password = 'Tea4five'
        self.date = datetime.datetime.now().strftime(r'%Y-%m-%d')
        self.message = MIMEText(str(data))
        self.message['From'] = self.sender
        self.message['To'] = self.receiver
        self.message['Subject'] = 'Notification Email for ' + self.date

    def send_email(self):
        try:
            smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp.ehlo()
            smtp.login(self.sender, self.password)
            smtp.sendmail(self.sender, self.receiver, self.message.as_string())
            print("Email Sent to {} at {}".format(self.receiver, self.date))
        except smtplib.SMTPAuthenticationError as e:
            print("SMTP Error: ", e)


if __name__ == '__main__':
    notification = Notification_Sender(data=random.sample(range(0,500), 30))
    notification.send_email()