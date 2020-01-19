from PyQt5 import QtCore, QtGui, QtWidgets
import socket
import sys
from ssl import wrap_socket
import time
import base64
import mailparser

ENCODING = 'utf-8'
TIMEOUT = 20
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

    window.listWidgetEmails.show()
    window.listWidgetEmails.addItem(header)

def sendDataHeader(sock, data, window, number):
    """Sends data to a given socket."""
    try:
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

    except:
        print('Error while requesting mail headers')

# Send RETR command to retrieve mail
def sendDataMail(sock, data, window):
    try:
        sock.send((data).encode(ENCODING))
        print('Client sent: ' + str(data))
        error = 0
        response = ''
        while True:
            buff = sock.recv(4096)
            buff = (str(buff, 'utf-8'))
            response += buff

            if '\n.\r' in response:
                break

        start = response.find('+OK')
        tempData = response[start : ]
        start = tempData.find(CRLF)
        receivedData = tempData[start + len(CRLF) :]
        extractEmailContent(receivedData, window)

    except:
        print('Error while requesting mail data')

def extractEmailContent(email, window):
    message = email
    mailContent = ''
    mail = mailparser.parse_from_string(message)

    # Mail headers
    header = mail.headers
    try: 
        mDate = header["Date"]
    except:
        mDate = 'Error'
    try:
        mFrom = header["From"]
    except:
        mFrom = 'Error'
    try:
        mTo = header["To"]
    except: 
        mTo = mFrom
    try:
        mSubject = header["Subject"]
    except: 
        mSubject = 'Error'

    mailContent += 'Date: ' + mDate + CRLF
    mailContent += 'From: ' + mFrom + CRLF
    mailContent += 'To: ' + mTo + CRLF
    mailContent += 'Subject: ' +mSubject + CRLF
    mailContent += '\nMail content:\n'
    # Mail body
    mBody = mail.text_plain
    try:
        mailContent += mBody[0]
    except:
        mailContent = 'Something went wrong'

    # Checking email attachments
    attachments = mail.attachments
    if attachments:
        for i in range(len(attachments)):
            attachment = attachments[i]
            attachmentData = attachment["payload"]
            filename = attachment["filename"]
            mailContent += CRLF + CRLF + 'Attachment: ' + filename
            # Save attachments
            try:
                imgdata = base64.b64decode(attachmentData)
                with open(filename, 'wb') as f:
                    f.write(imgdata)
            except:
                print('Error while saving attachment')
   

    window.textBrowserShowMail.setText(mailContent)

# Get number of mails in the maildrop - STAT command
def numOfMails(sock):
    num = sendData(sock, 'STAT' + CRLF)
    print('STAT response:', num)
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


def retranslateUILoggedIn(QMainWindow, username):
    QMainWindow.loginButton.hide()
    #QMainWindow.statusBar().showMessage('Logged in pop3' + username)


# Checks connection state with NOOP f.e Yandex POP returns -ERR for all commands after RETR command       
def checkConnectionState(sock, window):
    try:
        while True:
            check = sendData(sock, 'NOOP' + CRLF)
            if b'OK' in check:
                return True
    except:
        print('Connection is already closed')
        QtWidgets.QMessageBox.warning(window, 'Error', 'Bad user or password') 
    
    


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
            return True 

    def relogin(self):
        self.quit()
        self.loggedIn = self.login(self.accInfo["popServer"], self.accInfo["popPort"], self.accInfo["smtpServer"], self.accInfo["smtpPort"], self.accInfo["login"], self.accInfo["password"])
        if self.loggedIn:
            self.getEmails()
        else:
            QtWidgets.QMessageBox.warning(self.QMainWindow, 'Error', 'Can not refresh emails')
 




    def getEmails(self):
        try:
            if self.loggedIn:
                self.QMainWindow.listWidgetEmails.clear()
                self.numberOfMails = numOfMails(self.ssl_sock)
                self.QMainWindow.textBrowserNumEmails.setText(self.numberOfMails)
                self.QMainWindow.textBrowserNumEmails.show()
                self.QMainWindow.labelNumEmails.show()
                retranslateUILoggedIn(self.QMainWindow, self.username)
                listEmails(self.ssl_sock, self.QMainWindow)
        except:
            QMainWindow.loginButton.show()

       
    def retrieveMail(self, mailNum, window):
        sendDataMail(self.ssl_sock, 'RETR ' + mailNum+CRLF, window)

    # Deletes email
    def deleteEmail(self, mailNumber): 
        end = mailNumber.find('\n')
        mailNumber = mailNumber[ : end]
        while True:
            # if marked to be deleted
            connection = checkConnectionState(self.ssl_sock, self.QMainWindow)
            if connection:
                return self.deleteMailCheckOK(mailNumber)
#            if connection == False: 
#                loginCheck = self.login(self.accInfo["popServer"], self.accInfo["popPort"], self.accInfo["smtpServer"], self.accInfo["smtpPort"], self.accInfo["login"], self.accInfo["password"])
#                if loginCheck:
#                    return self.deleteMailCheckOK(mailNumber)

    def deleteMailCheckOK(self, mailNumber):
        time.sleep(2)
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
        try:
            connection = checkConnectionState(self.ssl_sock, self.QMainWindow)
            if connection:
                self.quitCheckOK()
        except: 
            print('Error while quitting')

    def quitCheckOK(self):
        data = sendData(self.ssl_sock, 'QUIT' + CRLF)
        if(data.startswith(b'+OK')):
            self.ssl_sock.close()
            self.ssl_sock = None
            self.loggedIn = False

    # Resets deletion marks
    def resetDeletion(self):
        connection = checkConnectionState(self.ssl_sock, self.QMainWindow)
        if connection:
            sendData(self.ssl_sock, 'RSET' + CRLF)


      



