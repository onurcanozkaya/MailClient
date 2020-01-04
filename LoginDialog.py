import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QPushButton, QToolTip, qApp, QMenu, QDialog,QAction, QDialogButtonBox, QFormLayout, QLabel, QLineEdit, QWidget, QVBoxLayout, QMessageBox
from Pop3 import Pop3Client

class LoginDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)

        self.setWindowTitle('Login')
        # Get login information
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.popServer = QLineEdit()
        self.popServerPort = QLineEdit()
        loginLayout = QFormLayout()
        loginLayout.addRow("POP3 Server", self.popServer)
        loginLayout.addRow("POP3 Server Port", self.popServerPort)
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
            loginStatus = Pop3Client.login(self.popServer.text(), self.popServerPort.text(), self.username.text(), self.password.text()) 

            if loginStatus: 
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
