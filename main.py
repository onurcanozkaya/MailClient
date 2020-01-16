import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import (QTextBrowser, QDialog, QWidget, QLabel, QMessageBox, QLineEdit, QTextEdit, QGridLayout, QApplication, QPushButton, QAction, qApp, QMenu, QToolTip, QDesktopWidget)
from PyQt5.QtGui import QIcon, QFont
from SendMailDialog import SendMailDialog as SendMailDialog
from LoginDialog import LoginDialog as LoginDialog
from Pop3 import Pop3Client


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.accountInfo = '' # mail adress : self.accountInfo["login"]  password : self.accountInfo["password"]
    
        # Shortcut to exit Ctrl + Q
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        self.statusbar = self.statusBar()

        # Menu Bar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        # Sub Menu
        importMenu = QMenu('Import', self)
        importFileAction = QAction('Import file', self) 
        importMenu.addAction(importFileAction)
        
        newMailAction = QAction('New Mail', self)        
        
        fileMenu.addAction(newMailAction)
        fileMenu.addMenu(importMenu)
        
        viewMenu = menubar.addMenu('View')
        
        viewStatAct = QAction('View statusbar', self, checkable=True)
        viewStatAct.setStatusTip('View statusbar')
        viewStatAct.setChecked(True)
        viewStatAct.triggered.connect(self.toggleMenu)
        
        viewMenu.addAction(viewStatAct)

        # Status Bar
        self.statusBar().showMessage('Ready')

        # Login Button
        self.loginButton = QPushButton('Log in', self)
        self.loginButton.setToolTip('Click to log in')
        self.loginButton.setObjectName("loginButton")
        self.loginButton.move(0,25)

        self.loginButton.clicked.connect(self.login)    

        # Number of mails
        self.labelNumEmails = QLabel(self)
        self.labelNumEmails.move(900, 0)
        self.labelNumEmails.hide()
        self.labelNumEmails.setText("Number of Mails") 
 
        self.textBrowserNumEmails = QTextBrowser(self)
        self.textBrowserNumEmails.move(900,25)
        self.textBrowserNumEmails.setObjectName("textBrowserNumEmails")
        self.textBrowserNumEmails.hide()

        # Send Mail Button
        self.sendMailButton = QPushButton('Send Mail', self)
        self.sendMailButton.setToolTip('Click to send mail')
        self.sendMailButton.move(100,25)
        self.sendMailButton.clicked.connect(self.sendMail)      

        # Logout button
        self.logoutButton = QPushButton('Log out', self)
        self.logoutButton.move(200,25)
        self.logoutButton.setObjectName("logoutButton")
        self.logoutButton.hide()
        self.logoutButton.clicked.connect(self.logout)  

        # Main window configurations
        self.resize(1024, 768)
        self.center()
        self.setWindowTitle('Mail Client')
        self.setWindowIcon(QIcon('test.png'))        
        self.show()

    # Log in POP3
    def login(self):
        sender = self.sender()
        pop = Pop3Client(main)
        login = LoginDialog(parent=self, pop3=pop, parentWindow=main)
        login.show()
        if not login.exec_(): 
            self.statusBar().showMessage('Log in cancelled')
    
    # Shows send mail dialog
    def sendMail(self):
        sendMail = SendMailDialog()
        # SMTP
        sendMail.exec_()
        sendMail.show()

    # TODO Log out
    def logout(self):
        self.logoutButton.hide()
        self.loginButton.setText('Log in')
        self.statusBar().showMessage('Logged out')

    # Asking to quit
    def closeEvent(self, event):
        # Message box
        reply = QMessageBox.question(self, 'Exit',"Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()    

    # To center window on start
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def toggleMenu(self, state):
        if state:
            self.statusbar.show()
        else:
            self.statusbar.hide()
        


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main = MainWindow()

    main.show()

    sys.exit(app.exec_())