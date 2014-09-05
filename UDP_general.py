import socket
import time
import struct
import re
import sys


def process_data(in_message):
    print("st:", repr(in_message))
    if not isinstance(in_message, str):
        message = in_message.decode("iso-8859-1")
    else:
        message = in_message
    stuff = re.search(r"(\w+):(\w+):([\w\W]*)", message)
    if stuff is None:
        raise IOError
    name = stuff.group(1)
    dtype = stuff.group(2)
    data = in_message[len(name) + len(dtype) + 2:]
    data = struct.unpack(dtype, data)
    return name, data

class UDP_receiver(object):
    def __init__(self, ip, port):
        try:
            self.socket.close()
        except AttributeError:
            pass
        self._ip, self._port = ip, port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((ip, port))

    def init(self, *args):
        self.__init__(*args)

    def receive_data(self, size=255):
        message, addr = self.socket.recvfrom(size)
        print('got', repr(message))
        return process_data(message)

def main():
    UDP_IP = "0.0.0.0"
    UDP_PORT = 5099
    udp = UDP_receiver(UDP_IP, UDP_PORT)
    print("Server started")
    while True:
        print(udp.receive_data(1024))
        time.sleep(0.001)

if __name__ == "__main__":
    main()
