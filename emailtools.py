
######################################################

import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr

######################################################

class EMailSender:

    ######################################################

    def __init__(self, smtp, user, pawd = ''):
        result = None
        self.user = None
        self.session = None

        try:
            self.session = smtplib.SMTP(smtp)
            if len(pawd) > 0:
                self.session.login(user, pawd)

            result = True
            return

        finally:
            if result:
                self.user = user

    ######################################################

    def sendmail(self, toaddr, subject, body):
        result = None

        try:
            if not self.user:
                return

            msg = MIMEText(body, 'plain', 'utf-8')
            msg['From'] = formataddr((Header('EMailSender', 'utf-8').encode(), self.user))
            msg['To'] = ', '.join(toaddr)
            msg['Subject'] = Header(subject, 'utf-8').encode()
            self.session.sendmail(self.user, toaddr, msg.as_string())

            result = True
            return

        finally:
            return result

    ######################################################

    def close(self):
        try:
            self.session.quit()

        finally:
            return True

    ######################################################

######################################################
