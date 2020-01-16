import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QPushButton, QToolTip, qApp, QMenu, QDialog,QAction, QDialogButtonBox, QFormLayout, QLabel, QLineEdit, QWidget, QVBoxLayout, QMessageBox

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
        loginLayout.addRow("POP3 Server", self.popServer)
        loginLayout.addRow("POP3 Server Port", self.popServerPort)
        loginLayout.addRow("SMTP Server", self.smtpServer)
        loginLayout.addRow("SMTP Server Port", self.smtpServerPort)
        loginLayout.addRow("Username", self.username)
        loginLayout.addRow("Password", self.password)

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
        try:
            loginStatus = self.pop3client.login(self.popServer.text(), self.popServerPort.text(), self.smtpServer.text(), self.smtpServerPort.text(), self.username.text(), self.password.text()) 

            if loginStatus: 
                self.pop3client.getEmails(self.mainWindow)

                self.mainWindow.statusBar().showMessage('Logged in as ' + self.username.text())
                self.mainWindow.logoutButton.show()

                self.mainWindow.accountInfo = {
                    "popServer": self.popServer.text(),
                    "popPort": self.popServerPort.text(),
                    "smtpServer": self.smtpServer.text(),
                    "smtpPort": self.smtpServerPort.text(),
                    "login": self.username.text(),
                    "password": self.password.text()
                }

                self.accept()
            else:
                QMessageBox.warning(
                    self, 'Error', 'Bad user or password')
                pass 
        except:
            QMessageBox.warning(self, 'Error', 'Bad user or password') 
            

    def exception(exctype, value, traceback):
        # Print the error and traceback
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)

    sys._excepthook = sys.excepthook
    sys.excepthook = exception

