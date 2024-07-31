import smtplib
from config import *
import ssl
from applogging import logger
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

class Mailer():
    def __init__(self, email: str, password: str):
        self.email: str = email
        self.password: str = password
        self.message: MIMEMultipart = None
        self.recipient = ""
        self.server = None
        self.connect()

    def __reset(self):
        self.message = None
        self.recipient = ""

    def __build_message(
        self, 
        recipient: str, 
        subject: str, 
        body: MIMEText, 
        attachmets: list[str] = []):
        try:
            self.recipient = recipient
            message = MIMEMultipart()
            message['Subject'] = subject
            message['From'] = self.email
            message['To'] = self.recipient
            message.attach(body)

            for path in attachmets:
                with open(path,'rb') as file:
                    filename = path.split('/')[-1]
                    mime = MIMEApplication(file.read(), Name=filename)
                    message.attach(mime) 

            self.message = message
        except Exception as e:
            self.message = None
            logger.exception(e)
    
    def connect(self):
        try:
            logger.info("[Mailer] Connecting to server")
            context = ssl.create_default_context()
            self.server = smtplib.SMTP_SSL(smtp_server, smtp_port, context=context)
            self.server.connect(smtp_server, smtp_port)
            logger.info(f"[Mailer] Login with {self.email}")
            self.server.login(self.email, self.password)
            logger.info("[Mailer] Connected to server")
        except Exception as e:
            logger.exception(e)

    def reconnect(self):
        try:
            logger.info("[Mailer] Reconnecting to server")
            self.server.connect(smtp_server, smtp_port)
            self.server.login(self.email, self.password)
            logger.info("[Mailer] Connected to server")
        except Exception as e:
            logger.exception(e)

    def check_connection(self):
        try:
            status = self.server.noop()[0]
            if status == 250:
                return True
            else:
                return False
        except Exception:
            return False
        
    def close(self):
        try:
            self.server.quit()
            logger.info("[Mailer] Connection closed")
        except Exception as e:
            logger.exception(e)
        
    def build_plain_message(
        self, 
        recipient: str, 
        subject: str, 
        body: str, 
        attachmets: list[str] = []
    ):
       plain_body = MIMEText(body, 'plain')
       self.__build_message(
           recipient,
           subject,
           plain_body,
           attachmets)
       
    def build_html_message(
        self, 
        recipient: str, 
        subject: str, 
        body: str, 
        attachmets: list[str] = []
    ):
       html_body = MIMEText(body, 'html')
       self.__build_message(
           recipient,
           subject,
           html_body,
           attachmets)

    def send(self):
        try:
            if (self.message):
                recipient = self.recipient
                message = self.message
                logger.info(f"[Mailer] Sending email to {recipient}")
                
                for i in range(3):
                    if self.check_connection():
                        self.server.sendmail(sender_email, recipient, message.as_string())
                        break
                    else:
                        self.reconnect()
                    
                self.__reset()
                logger.info(f"[Mailer] Email sent to {recipient}")
                return True
            else:
                logger.warn("[Mailer] Message not built yet")
                return False
        except Exception:
            logger.error(f"[Mailer] Failed send email to {recipient}")
            return False
