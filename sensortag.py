#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# Last modified: 2018-10-12 15:09:18

from bluepy.sensortag import SensorTag
from bluepy.sensortag import KeypressDelegate
import time


class Sensortag(SensorTag):

    """Texaus sensortag cc2650/cc1350"""

    def __init__(self, addr):
        """Initialize sensortag """
        super().__init__(addr)
        self.IRtemperature.enable()
        self.humidity.enable()
        self.barometer.enable()
        self.accelerometer.enable()
        self.magnetometer.enable()
        self.gyroscope.enable()
        self.battery.enable()
        self.keypress.enable()
        self.setDelegate(KeypressDelegate())
        self.lightmeter.enable()
        # wait until sensor initialize finish
        time.sleep(1)

    def get_sensor_data(self):
        self.waitForNotifications(5)
        return {"Temp": self.IRtemperature.read(),
                "Humidity": self.humidity.read(),
                "Barometer": self.barometer.read(),
                "Acceleraometer": self.accelerometer.read(),
                "Magnetometer": self.magnetometer.read(),
                "Gyroscope": self.gyroscope.read(),
                "Lightmeter": self.lightmeter.read(),
                "Battery": self.battery.read(),
                }

    def __del__(self):
        self.disconnect()


if __name__ == "__main__":
    print("connecting ...")
    tag = Sensortag("B0:B4:48:ED:D7:85")
    print(tag.get_sensor_data())
    del tag
