import socket
import time
import numpy as np
from debugmessages import *

HOST = '127.0.0.1'
PORT = 50007


class MessageSender:
    def __init__(self):
        self.badMsg = DebugMessages(self)
        self.badMsg.info("Message Sende initialized")

        def send(self,chars):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                for i in range(64):
                    msg = chars.encode('utf-8')
                    s.sendall(msg)
                    time.sleep(1)
                s.close()
