import socket
import time
import struct
import re


def process_data(message):
    stuff = re.match(r"(\w+):(\w+):([\w\W]*)", message)
    if stuff is None:
        raise IOError
    name = stuff.group(1)
    dtype = stuff.group(2)
    data = stuff.group(3)
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
