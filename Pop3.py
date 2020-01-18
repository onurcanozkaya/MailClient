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
def sendData(sock, data):
    
    sock.send((data).encode(ENCODING))
    buff = sock.recv(4096)
    print(buff)
    return buff


def extractHeaders(message, number, window):
    header = str(number)
    header += ' '

    start = message.find('\nFrom:') 
    end = message.find('\n', start+1)
    header += message[start : end]

    start = message.find('\nDate:') 
    end = message.find('\n', start+1)
    header += message[start : end]

    start = message.find('\nSubject:') 
    end = message.find('\n', start+1)
    header += message[start : end]

    start = message.find('\nTo:') 
    end = message.find('\n', start+1)
    header += message[start : end]

    print("Mail Header: " + header)
    window.listWidgetEmails.show()
    window.listWidgetEmails.addItem(header)

def sendDataHeader(sock, data, window, number):
    """Sends data to a given socket."""
    sock.send((data).encode(ENCODING))
    print("Client sent: " + str((data).encode(ENCODING)))
     
    response = ''
   
    while True:
        buff = sock.recv(4096)
        buff = (str(buff, 'utf-8'))
        response += buff
        
        #print("TOP command response: " + str(response))
        
        # End of message
        if '\n.\r' in response:
            break
   
    extractHeaders(response, number, window)

# Send RETR command to retrieve mail
def sendDataMail(sock, data, window):
    sock.send((data).encode(ENCODING))
    print('Client sent: ' + str(data))

    response = ''
    while True:
        buff = sock.recv(4096)
        buff = (str(buff, 'utf-8'))
        response += buff

        if '\n.\r' in response:
            break

    extractEmailContent(response, window)

def extractEmailContent(email, window):
    message = email
    mailContent = ''

    start = message.find('\nDate:') 
    end = message.find('\n', start+1)
    mailContent += message[start : end]

    start = message.find('\nFrom:') 
    end = message.find('\n', start+1)
    mailContent += message[start : end]

    start = message.find('\nTo:') 
    end = message.find('\n', start + 1)
    mailContent += message[start : end]

    start = message.find('\nSubject:') 
    end = message.find('\n', start + 1)
    mailContent += message[start : end]

    mailContent += '\n===================================='

    # If the mail is sent from Gmail
    if '\nContent-Type: text/plain; charset="UTF-8"' in message:
        start = message.find('\nContent-Type: text/plain; charset="UTF-8"') 
        end = message.find('\n--', start + 1)
        length = len('\nContent-Type: text/plain; charset="UTF-8"')
        mailContent += message[start + length : end]
        window.textBrowserShowMail.setText(mailContent)
    # TODO HTML
    # TODO ATTACHMENTS 

    # If the mail is sent from iOS Mail
    elif '\nContent-Type: text/plain; charset=utf-8' in message:
        if '\nX-Mailer: iPhone Mail (17C54)' in message:
            start = message.find('\nX-Mailer: iPhone Mail (17C54)')
            end = message.find('\n.', start + 1)

            length = len('\nX-Mailer: iPhone Mail (17C54)')
            mailContent += message[start + length : end]
            window.textBrowserShowMail.setText(mailContent)
        else: 
            print(message)


    # If the mail is sent from Windows Mail
    elif '\nContent-Type: text/plain; charset="us-ascii"' in message:
        start = message.find('\nContent-Type: text/plain; charset="us-ascii"') 
        end = message.find('\n--', start + 1)

        if '\nContent-Transfer-Encoding: quoted-printable' in message[start : end]:
            start = message.find('\nContent-Transfer-Encoding: quoted-printable')
            length = len('\nContent-Transfer-Encoding: quoted-printable')
            mailContent += message[start + length : end]
            window.textBrowserShowMail.setText(mailContent)

    else:
        print(message)


# Get number of mails in the maildrop - STAT command
def numOfMails(sock):
    num = sendData(sock, 'STAT' + CRLF)
    #print('STAT response:', num)
    num = (str(num, 'utf-8'))
    start = num.find(' ')
    end = num.find(' ', start + 1)
    num = num[start + 1: end]
    return num

# List emails LIST command    
def listEmails(sock, window):
    sock.send(('LIST' + CRLF).encode(ENCODING))

    listMailResponse = ''

    while True: 
        buff = sock.recv(4096)
        
        print(buff)
        buff = (str(buff, 'utf-8'))
        listMailResponse += buff
        if '\n.\r' in listMailResponse:
            break

    listHeaders(sock, listMailResponse, window)


def listHeaders(sock, message, window):
    # Looking for numbers message id and byte, example response from the socket b'+OK 3 messages (18432 bytes)\r\n1 6843\r\n2 6843\r\n3 4746\r\n.\r\n'
    start = message.find(' ') 
    end = message.find(' ', start+1)
    # Number of mails in maildrop
    msgCount = int(message[start + 1 : end])
    # Skips CRLF (next line) also deletes read parts
    message = message[message.find(CRLF) + 1 : ]
    for x in range (0, msgCount):
        # After message number there is single space looking for it example: \r\n1 6843
        messageNumber = int(message[ : message.find(' ')])
        # Sending message number with TOP command to get mail headers
        sendDataHeader(sock, 'TOP ' + str(messageNumber) + ' 0' + CRLF, window, messageNumber)
        # Removes read number going for next message number
        message = message[message.find(' ') : ]
        message = message[message.find('\n') : ]


# TODO Changes in the UI while logged in
def retranslateUILoggedIn(QMainWindow, username):
    QMainWindow.loginButton.hide()
    #QMainWindow.statusBar().showMessage('Logged in pop3' + username)
    print(' ')



# for test purposes 
def saveAccountInfo(QMainWindow, accInfo):
    QMainWindow.accountInfo = accInfo

# Checks connection state with NOOP f.e Yandex POP returns -ERR for all commands after RETR command       
def checkConnectionState(sock):
    check = sendData(sock, 'NOOP' + CRLF)
    if b'OK' in check:
        return True
    else: 
        return False


class Pop3Client():
    def __init__(self, QMainWindow):
        self.QMainWindow = QMainWindow
        # SSL Socket
        self.ssl_sock = ''
        self.loggedIn = False

    def login(self, popServer, popPort, smtpServer, smtpPort, login, password):
        print("Logging in")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ssl_sock = wrap_socket(sock)
        self.ssl_sock.settimeout(TIMEOUT)

  

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
        self.loggedIn = True
        print(data)
        sendData(self.ssl_sock, 'USER ' + login + CRLF)
        data=sendData(self.ssl_sock, 'PASS ' + password + CRLF)
        if(data.startswith(b'+OK')):
            return 1 

    def getEmails(self):
        if self.loggedIn:
            self.QMainWindow.listWidgetEmails.clear()
            self.numberOfMails = numOfMails(self.ssl_sock)
            self.QMainWindow.textBrowserNumEmails.setText(self.numberOfMails)
            self.QMainWindow.textBrowserNumEmails.show()
            self.QMainWindow.labelNumEmails.show()
            # delete following line when tests are done
            saveAccountInfo(self.QMainWindow, self.accInfo)
            retranslateUILoggedIn(self.QMainWindow, self.username)
            listEmails(self.ssl_sock, self.QMainWindow)
       
    def retrieveMail(self, mailNum, window):
        sendDataMail(self.ssl_sock, 'RETR ' + mailNum+CRLF, window)

    # Deletes email
    def deleteEmail(self, mailNumber): 
        end = mailNumber.find('\n')
        mailNumber = mailNumber[ : end]
        print('mail number: ' + str(mailNumber))
        while True:
            # if marked to be deleted
            connection = checkConnectionState(self.ssl_sock)
            if connection:
                return self.deleteMailCheckOK(mailNumber)
            if connection == False: 
                loginCheck = self.login(self.accInfo["popServer"], self.accInfo["popPort"], self.accInfo["smtpServer"], self.accInfo["smtpPort"], self.accInfo["login"], self.accInfo["password"])
                if loginCheck:
                    return self.deleteMailCheckOK(mailNumber)

    def deleteMailCheckOK(self, mailNumber):
        time.sleep(2)
        print('DELE '+ mailNumber + CRLF)
        deleteAttemptSuccess = sendData(self.ssl_sock, 'DELE ' + mailNumber + CRLF)
        if deleteAttemptSuccess:
            tempNum = int(self.numberOfMails)
            tempNum -= 1
            self.numberOfMails = str(tempNum)
            self.QMainWindow.textBrowserNumEmails.setText(self.numberOfMails)
            return True
        return False

    # Quits POP3 session
    def quit(self):
        print('Client sent: NOOP')
        quitTest = checkConnectionState(self.ssl_sock)
        if quitTest:
            self.quitCheckOK()
        else:
            self.login(self.accInfo["popServer"], self.accInfo["popPort"], self.accInfo["smtpServer"], self.accInfo["smtpPort"], self.accInfo["login"], self.accInfo["password"])
            self.quitCheckOK()

    def quitCheckOK(self):
        print('Client sent: QUIT')
        data = sendData(self.ssl_sock, 'QUIT' + CRLF)
        if(data.startswith(b'+OK')):
            self.ssl_sock.close()
            self.ssl_sock = None
            self.loggedIn = False


      



