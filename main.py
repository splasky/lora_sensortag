#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# Last modified: 2018-10-12 15:58:01

from serial import Serial


class Mdot(Serial):

    """Mdot communcation"""

    def __init__(self, device: str, baudrate: int, timeout: int = 10):
        """Class object initialize

        :device:str: device
        :baudrate:int: baudrate
        :timeout:int: timeout

        """
        super(Mdot, self).__init__()
        self.port = device
        self.baudrate = baudrate
        self.timeout = timeout
        self._is_join = False

    def connect(self):
        self.open()

    def join(self):
        if self._is_join:
            return
        self.write("at+join\n".encode("ascii"))
        ret = self.read(100)
        if 'OK' not in ret.decode('ascii'):
            raise Exception("Join error")
        self._is_join = True

    def send(self, message: str):
        if self._is_join:
            self.write('at+send="{}"\n'.format(message).encode("ascii"))
        else:
            print("Must join first!")

    def __del__(self):
        self.close()


if __name__ == "__main__":
    from sensortag import Sensortag
    import time
    tag = Sensortag("B0:B4:48:ED:D7:85")
    data = tag.get_sensor_data()
    mdot = Mdot("/dev/ttyXRUSB0", 115200, 20)
    mdot.connect()
    mdot.join()
    data = str(data)
    for d in range(0, len(data), 8):
        mdot.send(data[d:d + 8])
        time.sleep(1)
        print(data[d:d + 10])

    del mdot
    del tag
