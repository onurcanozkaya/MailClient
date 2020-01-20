# Send mail window

import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import (QWidget, QMessageBox, QLabel, QLineEdit, QTextEdit, QGridLayout, QApplication, QPushButton, QFileDialog)


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

        # Button to add attachment
        self.addAttachmentButton = QPushButton('Attachment', self)
        self.addAttachmentButton.clicked.connect(self.addAttachment)
        self.addAttachmentButton.show()

        # Attachment names
        self.attachmentFirst = QLabel('')
        self.attachmentFirst.hide()

        self.attachLabel = QLabel('Attachment names:')
        self.attachLabel.hide()

        self.attachmentCountLabel = QLabel('Added attachments: ')
        self.attachmentCountLabel.hide()

        self.attachmentCount = QLabel('')
        self.attachmentCount.hide()


        # Attachment filename
        self.attachmentFileName = []
        self.attachmentCountN = 0

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(sender, 1, 0)
        grid.addWidget(self.senderAddr, 1, 1)

        grid.addWidget(to, 2, 0)
        grid.addWidget(self.toEdit, 2, 1)

        grid.addWidget(subject, 3, 0)
        grid.addWidget(self.subjectEdit, 3, 1)

        grid.addWidget(mailContent, 4, 0, 1, 2)
        grid.addWidget(self.mailContentEdit, 5, 0, 1, 2)

        grid.addWidget(self.addAttachmentButton, 6, 0)

        grid.addWidget(self.attachLabel, 7, 0)
        grid.addWidget(self.attachmentFirst, 7, 1)
        grid.addWidget(self.attachmentCountLabel, 8, 0)
        grid.addWidget(self.attachmentCount, 8, 1)


        sendButton = QPushButton('Send', self)
        sendButton.setToolTip('Are you sure to send this mail?')
        grid.addWidget(sendButton, 0, 1)

        sendButton.clicked.connect(self.sendEmail)            

        self.setLayout(grid) 
        self.setWindowTitle('Send Mail')    
        self.resize(600, 400)
        self.show()

    def sendEmail(self):
        #self.smtpClient.login(self.parentWindow.accountInfo["smtpServer"], self.parentWindow.accountInfo["smtpPort"], self.parentWindow.accountInfo["login"], self.parentWindow.accountInfo["password"] )
        #self.smtpClient.sendEmail(self.senderAddr.text(), self.toEdit.text(), self.subjectEdit.text(), self.mailContentEdit.toPlainText())
        response = self.smtpClient.send_email(
                    self.parentWindow.accountInfo["smtpServer"], 
                    self.parentWindow.accountInfo["smtpPort"], 
                    self.parentWindow.accountInfo["login"], 
                    self.parentWindow.accountInfo["password"],
                    self.toEdit.text(), 
                    self.subjectEdit.text(), 
                    self.mailContentEdit.toPlainText(),
                    self.attachmentFileName)

        if response:
            self.hide()
            self.parentWindow.statusBar().showMessage('Sent mail successfuly. Logged in as ' + self.parentWindow.accountInfo["login"])

        else:
            QMessageBox.warning(self, 'Error', 'Error while sending the email') 
            self.parentWindow.statusBar().showMessage('Error while sending the email. Logged in as ' + self.parentWindow.accountInfo["login"])

    def addAttachment(self):
        self.openFileNameDialog()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
            self.attachmentFileName.append(fileName)
            self.attachmentFirst.setText(str(self.attachmentFileName))
            self.attachmentFirst.show()
            self.attachmentCountLabel.show()
            self.attachmentCountN += 1
            self.attachmentCount.setText(str(self.attachmentCountN))
            self.attachmentCount.show()
            self.attachLabel.show()

            
    

    
    
    def exception(exctype, value, traceback):
        # Print the error and traceback
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)

    sys._excepthook = sys.excepthook
    sys.excepthook = exception
        
        
