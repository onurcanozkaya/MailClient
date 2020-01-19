from PyQt5 import QtCore, QtGui, QtWidgets

import smtplib
import socket
import sys
import time
import base64
from socket import gaierror

class SmtpClient():
    def __init__(self, QMainWindow):
        self.QMainWindow = QMainWindow

    def send_email(self, smtpServer, smtpPort, login, password, toUser, subject, msg):
        try: 
            server=smtplib.SMTP_SSL(smtpServer + ':' + str(smtpPort))
            server.ehlo()
            server.login(login, password)
            message ='Subject: {}\n\n{}'.format (subject,msg)
            server.sendmail(login, toUser, message)
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


