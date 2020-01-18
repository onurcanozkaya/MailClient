from PyQt5 import QtCore, QtGui, QtWidgets

import smtplib
import socket
import sys
from ssl import wrap_socket
import time
import base64

ENCODING = 'utf-8'
TIMEOUT = 2
CRLF = "\r\n"

# Sends data to a given socket.
def sendData(sock, data):
    
    sock.send((data).encode(ENCODING))
    buff = sock.recv(4096)
    print(buff)
    return buff




class SmtpClient():
    def __init__(self, QMainWindow):
        self.QMainWindow = QMainWindow
        # SSL Socket
        self.ssl_sock = ''
        self.loggedIn = False

    def login(self, smtpServer, smtpPort, login, password):
        print("Smtp login")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ssl_sock = wrap_socket(sock)
        self.ssl_sock.settimeout(TIMEOUT)

        self.ssl_sock.connect((smtpServer, int(smtpPort)))
        data = self.ssl_sock.recv()
        print(data)
        if data.startswith(b'220'):
            sendData(self.ssl_sock, 'EHLO ' + login + CRLF)
            
        
            self.loggedIn = 1

    def sendEmail(self, fromUser, toUser, subject, mailContent):
        print('from user' + fromUser + toUser + subject + mailContent)

    def send_email(self, smtpServer, smtpPort, login, password, toUser, subject, msg):
        try: 
            server=smtplib.SMTP(smtpServer + ':' + smtpPort)
            server.ehlo()
            server.starttls()
            server.login(login, password)
            message ='Subject: {}\n\n{}'.format (subject,msg)
            server.sendmail(login, toUser, message)
            server.quit()
            print('success')
            return 1
        except:
            print('Fail')
            return 0
