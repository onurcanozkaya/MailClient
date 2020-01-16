from PyQt5 import QtCore, QtGui, QtWidgets
import socket
import sys
from ssl import wrap_socket
import time
import base64

ENCODING = 'utf-8'
TIMEOUT = 2
CRLF = "\r\n"

# Sends data to a given socket.
def send_data(sock, data):
    
    sock.send((data).encode(ENCODING))
    buff = sock.recv(4096)
    print(buff)
    return buff

# Get number of mails in the maildrop - STAT command
def numOfMails(sock):
    num = send_data(sock, 'STAT' + CRLF)
    #print('STAT response:', num)
    num = (str(num, 'utf-8'))
    start = num.find(' ')
    end = num.find(' ', start + 1)
    num = num[start + 1: end]
    return num

# List emails LIST command    
def listEmails(sock):
    sock.send(('LIST' + CRLF).encode(ENCODING))

    listMailResponse = ''

    while True: 
        buff = sock.recv(4096)
        
        print(buff)
        buff = (str(buff, 'utf-8'))
        listMailResponse += buff
        if CRLF in listMailResponse:
            break

# TODO Changes in the UI while logged in
def retranslateUILoggedIn(QMainWindow, username):
    QMainWindow.loginButton.setText("Change account")
    #QMainWindow.statusBar().showMessage('Logged in pop3' + username)
    print(' ')



# for test purposes 
def saveAccountInfo(QMainWindow, accInfo):
    QMainWindow.accountInfo = accInfo


class Pop3Client():
    def __init__(self, QMainWindow):
        self.QMainWindow = QMainWindow

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ssl_sock = wrap_socket(sock)
        self.ssl_sock.settimeout(TIMEOUT)

    def login(self, popServer, popPort, smtpServer, smtpPort, login, password):
        print("Logging in")

        # to test UI
        self.accInfo = {
            "popServer": popServer,
            "popPort": popPort,
            "smtpServer": smtpServer,
            "smtpPort": smtpPort,
            "login": login,
            "password": password
        }

        self.username = login

        self.ssl_sock.connect((popServer, int(popPort)))
        data = self.ssl_sock.recv()
        print(data)
        send_data(self.ssl_sock, 'USER ' + login + CRLF)
        data=send_data(self.ssl_sock, 'PASS ' + password + CRLF)
        if(data.startswith(b'+OK')):
            return 1 

    def getEmails(self, QMainWindow):
        self.numberOfMails = numOfMails(self.ssl_sock)
        QMainWindow.textBrowserNumEmails.setText(self.numberOfMails)
        QMainWindow.textBrowserNumEmails.show()
        QMainWindow.labelNumEmails.show()
        #saveAccountInfo(QMainWindow, self.accInfo)
        retranslateUILoggedIn(QMainWindow, self.username)
        listEmails(self.ssl_sock)
       



