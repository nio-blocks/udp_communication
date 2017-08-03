from six import string_types
import socket
import struct
import sys

UDP_DATA_FORMAT = "{name}:{format}:"
ALL_POS = [255, 65535, 4294967295]
STD_POS = [127, 32767, 2147483647]
STD_NEG = [-(n + 1) for n in STD_POS]

DTYPES = {
        (STD_NEG[0], STD_POS[0]):  'b',
        (0, ALL_POS[0]):           'B',
        (STD_NEG[1], STD_POS[1]):  'h',
        (0, ALL_POS[1]):           'H',
        (STD_NEG[2], STD_POS[2]):  'l',
        (0, ALL_POS[2]):           'L',
         }


def find_dtype(tup, dtype):
    '''finds and returns the data type according to
    https://docs.python.org/2/library/struct.html'''
    if dtype is float:
        return "f"
    if dtype == "double":
        return "d"
    if dtype is not int:
        raise ValueError("invalid data type")
    dmin = min(tup)
    dmax = max(tup)
    if dmin >= 0:
        dmin = 0
        try:
            dmax = next((n for n in enumerate(ALL_POS) if n[1] >= dmax))
            dmax = dmax[1]
        except StopIteration:
            return 'f'
    else:
        try:
            dmin = next((n for n in enumerate(STD_NEG) if n[1] <= dmin))[0]
            dmax = next((n for n in enumerate(STD_POS) if n[1] >= dmax))[0]
        except StopIteration:
            return 'f'
        # get the largest index
        i = max(dmin, dmax)
        dmax, dmin = STD_POS[i], STD_NEG[i]

    return str(len(tup)) + DTYPES[(dmin, dmax)]


def convert_data(name, iterable, dtype):
    data = tuple(iterable)
    dtype = find_dtype(data, dtype)
    packed_data = struct.pack(dtype, *data)
    header = UDP_DATA_FORMAT.format(name=name, format=dtype)
    if sys.version_info[0] >= 3:
        header = header.encode()
    return header + packed_data


class UDP(object):
    def __init__(self, ip, port):
        self._ip = ip
        self._port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.connect((ip, port))

    def send_data(self, name, data, dtype):
        message = convert_data(name, data, dtype)
        print(repr(message))
        return self.socket.sendall(message)


def main():
    import time
    IP = "192.168.100.111"
    PORT = 5099
    udp = UDP(IP, PORT)
    n = 0

    while(True):
        udp.send_data('test', range(n, n + 8), int)
        time.sleep(0.1)
        n += 8
        if(n > 800):
            n = 0

if __name__ == "__main__":
    main()
