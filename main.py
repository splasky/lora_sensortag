#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# Last modified: 2018-10-11 16:14:34

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
            print("Join error")
            return
        self._is_join = True

    def send(self, message: str):
        if self._is_join:
            self.write('at+send="{}"\n'.format(message).encode("ascii"))
        else:
            print("Must join first!")

    def __del__(self):
        self.close()


if __name__ == "__main__":
    mdot = Mdot("/dev/ttyXRUSB0", 115200, 20)
    mdot.connect()
    mdot.join()
    mdot.send("Test!")
    del(mdot)
