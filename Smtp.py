from PyQt5 import QtCore, QtGui, QtWidgets

import smtplib
import socket
import sys
import time
import base64
from os.path import basename
from socket import gaierror
import imghdr 

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.utils import formatdate
from email import encoders
from socket import gaierror

class SmtpClient():
    def __init__(self, QMainWindow):
        self.QMainWindow = QMainWindow

    def send_email(self, smtpServer, smtpPort, login, password, toUser, subject, content, attachmentFileLocation):
        
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = login
        msg['To'] = toUser
        
    
        fileType = ''

        msg.attach(MIMEText(content, 'plain'))
        
        if attachmentFileLocation:
            #files=['hi.jpg']
            # Content-Type: image/jpeg
            for f in attachmentFileLocation or []:
                if '.jpg' in f:
                    fileType = 'jpeg'
                    with open(f, "rb") as fil:
                        part = MIMEImage(
                        fil.read(),
                        _subtype=fileType,
                        Name=basename(f)
                        )
                if '.png' in f:
                    fileType = 'png'
                    with open(f, "rb") as fil:
                        part = MIMEImage(
                        fil.read(),
                        _subtype=fileType,
                        Name=basename(f)
                        )
                else:
                    with open(f, "rb") as fil:
                        part = MIMEApplication(
                        fil.read(),
                        _subtype=fileType,
                        Name=basename(f)
                        )
                part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
                msg.attach(part)

        try: 
            server=smtplib.SMTP_SSL(smtpServer + ':' + str(smtpPort))
            server.ehlo()
            recipients = toUser.split(',')
            server.login(login, password)
            server.sendmail(login, recipients,msg.as_string())
            server.quit()
            print('success')
            return 1
        
        except (gaierror, ConnectionRefusedError):
            # tell the script to report if your message was sent or which errors need to be fixed
            print('Failed to connect to the server. Bad connection settings?')
            QtWidgets.QMessageBox.warning(self.QMainWindow, 'Error','Failed to connect to the server. Bad connection settings?')

           
        except smtplib.SMTPServerDisconnected:
            print('Failed to connect to the server. Wrong user/password?')
            QtWidgets.QMessageBox.warning(self.QMainWindow, 'Error','Failed to connect to the server. Wrong user/password?' )

          
        except smtplib.SMTPException as e:
            print('SMTP error occurred: '+ str(e))
            QtWidgets.QMessageBox.warning(self.QMainWindow, 'Error','SMTP error occurred: '+ str(e) )


