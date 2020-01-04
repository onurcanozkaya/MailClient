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
def send_data(sock, data):
    
    sock.send((data).encode(ENCODING))
    buff = sock.recv(4096)
    print(buff)
    return buff

class Pop3Client():

    def login(email,port,login,password):
        print("Logging in")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_sock = wrap_socket(sock)
        ssl_sock.settimeout(TIMEOUT)
        ssl_sock.connect((email, int(port)))
        data = ssl_sock.recv()
        print(data)
        send_data(ssl_sock, 'USER ' + login + CRLF)
        data=send_data(ssl_sock, 'PASS ' + password + CRLF)
        if(data.startswith(b'+OK')):
            return 1 

