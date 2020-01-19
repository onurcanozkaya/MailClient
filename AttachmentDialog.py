import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QVBoxLayout, QMessageBox


class AttachmentDialog(QDialog):
    def __init__(self, parent=None, filename=None):
        super(AttachmentDialog, self).__init__(parent)
        self.filename = filename

        self.setWindowTitle('Attachment: ' + self.filename)

        self.labelImage = QtWidgets.QLabel(self)
        image = QtGui.QPixmap(filename)
        self.labelImage.setPixmap(image)
   
        self.resize(image.width(), image.height())
        self.show()
