# Send mail window

import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QApplication, QPushButton)


class SendMailDialog(QtWidgets.QDialog):
    
    def __init__(self, smtp=None, parent=None):
        super(SendMailDialog, self).__init__(parent)
        self.parentWindow = parent

        self.smtpClient = smtp
        
        sender = QLabel('From:')
        self.senderAddr = QLabel('')
        self.senderAddr.setText(self.parentWindow.accountInfo["login"])
        to = QLabel('To:')
        subject = QLabel('Subject:')
        mailContent = QLabel('Message:')

        self.toEdit = QLineEdit()
        self.subjectEdit = QLineEdit()
        self.mailContentEdit = QTextEdit()

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(sender, 1, 0)
        grid.addWidget(self.senderAddr, 1, 1)

        grid.addWidget(to, 2, 0)
        grid.addWidget(self.toEdit, 2, 1)

        grid.addWidget(subject, 3, 0)
        grid.addWidget(self.subjectEdit, 3, 1)

        grid.addWidget(mailContent, 4, 0)
        grid.addWidget(self.mailContentEdit, 4, 1, 5, 1)

        sendButton = QPushButton('Send', self)
        sendButton.setToolTip('Are you sure to send this mail?')
        grid.addWidget(sendButton, 0, 1)

        sendButton.clicked.connect(self.sendEmail)            

        self.setLayout(grid) 
        self.setWindowTitle('Send Mail')    
        self.resize(600, 400)
        self.show()

    def sendEmail(self):
        sender = self.sender()
        self.parentWindow.statusBar().showMessage('Sending mail.')
        self.smtpClient.login(self.parentWindow.accountInfo["smtpServer"], self.parentWindow.accountInfo["smtpPort"], self.parentWindow.accountInfo["login"], self.parentWindow.accountInfo["password"] )
        self.smtpClient.sendEmail(self.senderAddr.text(), self.toEdit.text(), self.subjectEdit.text(), self.mailContentEdit.toPlainText())
    def exception(exctype, value, traceback):
        # Print the error and traceback
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)

    sys._excepthook = sys.excepthook
    sys.excepthook = exception
        
        
