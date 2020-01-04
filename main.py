import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import (QWidget, QLabel, QMessageBox, QLineEdit, QTextEdit, QGridLayout, QApplication, QPushButton, QAction, qApp, QMenu, QToolTip, QDesktopWidget)
from PyQt5.QtGui import QIcon, QFont
from SendMailDialog import SendMailDialog as SendMailDialog
from LoginDialog import LoginDialog as LoginDialog
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
    
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
        loginButton = QPushButton('Login', self)
        loginButton.setToolTip('Click to login')
        loginButton.move(0,25)

        loginButton.clicked.connect(self.login)     

        # Send Mail Button
        sendMailButton = QPushButton('Send Mail', self)
        sendMailButton.setToolTip('Click to send mail')
        sendMailButton.move(125,25)
        sendMailButton.clicked.connect(self.sendMail)            

        # Main window configurations
        self.resize(1024, 768)
        self.center()
        self.setWindowTitle('Mail Client')
        self.setWindowIcon(QIcon('test.png'))        
        self.show()

    def login(self):
      
        sender = self.sender()
        login = LoginDialog()
        if not login.exec_(): 
            self.statusBar().showMessage('Login cancelled')

    def sendMail(self):
        sendMail = SendMailDialog()
        sendMail.exec_()
        sendMail.show()

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