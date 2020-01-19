import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QVBoxLayout, QMessageBox

# Some known POP3 and SMTP servers
A = ['pop.gmail.com', 995, 'smtp.gmail.com', 465]
B = ['pop.yandex.com', 995, 'smtp.yandex.com', 465]

class LoginDialog(QDialog):
    def __init__(self, parent=None, pop3=None, parentWindow=None):
        super(LoginDialog, self).__init__(parent)
        self.pop3client = pop3
        self.mainWindow = parentWindow

        self.setWindowTitle('Login')
        # Get login information
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.popServer = QLineEdit()
        self.popServerPort = QLineEdit()
        self.smtpServer = QLineEdit()
        self.smtpServerPort = QLineEdit()
        loginLayout = QFormLayout()
        loginLayout.addRow("Username", self.username)
        loginLayout.addRow("Password", self.password)
        loginLayout.addRow("POP3 Server", self.popServer)
        loginLayout.addRow("POP3 Server Port", self.popServerPort)
        loginLayout.addRow("SMTP Server", self.smtpServer)
        loginLayout.addRow("SMTP Server Port", self.smtpServerPort)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.check)
        self.buttons.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(loginLayout)
        layout.addWidget(self.buttons)
        self.resize(400, 100)
        self.setLayout(layout)
    

    def check(self):
        # Login check
        self.loginStatus = 0

        # To match with stored servers
        start = self.username.text().find('@')
        mailAddr = self.username.text()
        domain = mailAddr[start + 1: ]
        
        if not self.popServer.text() and not self.popServerPort.text() and not self.smtpServer.text() and not self.smtpServerPort.text():
            if domain == 'gmail.com':
                popServer, popPort, smtpServer, smtpPort = A
            if domain == 'yandex.com':
                popServer, popPort, smtpServer, smtpPort = B
        else:
            popServer = self.popServer.text()
            popPort = self.popServerPort.text()
            smtpServer = self.smtpServer.text()
            smtpPort = self.smtpServerPort.text()

        try:
            self.loginStatus = self.pop3client.login(popServer, popPort, smtpServer, smtpPort, self.username.text(), self.password.text()) 

            if self.loginStatus: 
                self.accept()
            else:
                QMessageBox.warning(
                    self, 'Error', 'Bad user or password')
                pass 
        except:
            e = sys.exc_info()[0]
            print(e)
            QMessageBox.warning(self, 'Error', 'Bad user or password') 

        # If login successful request emails
        if self.loginStatus:
            self.pop3client.getEmails()
            self.mainWindow.statusBar().showMessage('Logged in as ' + self.username.text())
            self.mainWindow.sendMailButton.show()
            self.mainWindow.logoutButton.show()
            self.mainWindow.refreshButton.show()
            self.mainWindow.resetMailButton.show()

            # Save login configuration to use with smtp
            self.mainWindow.accountInfo = {
                "popServer": popServer,
                "popPort": popPort,
                "smtpServer": smtpServer,
                "smtpPort": smtpPort,
                "login": self.username.text(),
                "password": self.password.text()
            }
    # If the user rejects log in
    def reject(self):
        self.mainWindow.loginButton.show()
        self.hide()

    def exception(exctype, value, traceback):
        # Print the error and traceback
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)

    sys._excepthook = sys.excepthook
    sys.excepthook = exception

