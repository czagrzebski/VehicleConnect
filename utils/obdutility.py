"""
obdutility.py
Class to fetch information from ELM Adapter using OBD Module

Creed Zagrzebski
"""

import logging
import os
import time

import numpy as np
import obd
from obd import OBDStatus


class OBDUtility():
    """Uses OBD Module To Fetch Diagnostic Information From ELM Adapter Using On-board Diagnostics"""

    def __init__(self):
        obd.logger.removeHandler(obd.console_handler)
        self.run = True
        self.connection = None
        self.connectionWait = False
        self.port = None
        self.obdData = {"speed": '0', "rpm": '0', "coolant_temp": '0',
                        "throttle_position": '0', "intake_pressure": '0', "timing_advance": '0', "maf": '0'}

    def connect_to_obd(self, **kwargs):
        """Connects to OBD Port"""
        self.port = kwargs["connection"]
        self.obd_mac_address = kwargs["obd_mac"]
        print("Connecting to port on {0}".format(self.obd_mac_address))
        try:
            self.connection = obd.OBD(kwargs["connection"])
        except:
            logging.debug("Failed to connect to " + kwargs["connection"])
        try:
            os.system(
                'sudo rfcomm bind /dev/rfcomm1 %s'.format(self.obd_mac_address))
        except:
            logging.debug("Failed to bind OBD Adapter to RFCOMM1")

    def is_connection_alive(self):
        """Verifies the connection is valid by checking if RPM is active"""
        rpmResponse = self.connection.query(obd.commands.RPM)
        if rpmResponse.is_null():
            return False
        else:
            return True

    def wait_for_connection(self):
        """Waits for OBD Connection"""
        self.connectionWait = True
        print("Waiting for Connection on {0}".format(self.port))

        while self.connectionWait:
            self.connect_to_obd(connection=self.port,
                                obd_mac=self.obd_mac_address)
            if self.is_connection_alive():
                logging.debug("Connection now successful")
                self.connectionWait = False
                break
            else:
                self.obdData = {"speed": '0', "rpm": '0', "coolant_temp": '0',
                                "throttle_position": '0', "intake_pressure": '0', "timing_advance": '0', "maf": '0'}
                time.sleep(3)

    def get_obd_data(self):
        return self.obdData

    def refresh_obd_data(self):
        """Returns Dictionary of OBD Data. Gets OBD Data (Speed, RPM, Coolant Temperature, Throttle Position, Intake Pressure, and Mass Air Flow) from OBD Port"""
        # NOTE: GEAR INFORMATION IS NOT AVAILABLE FROM OBD, thus its not included in this class. Gear is a calculated value, and can
        # be calculated through the Vehicle Class.

        # Check if connection is setup
        # If unavailable, it will pass
        if self.connection is not None:
            try:
                # Checks if connection is valid
                if(self.is_connection_alive() is False):
                    self.wait_for_connection()

                # Get Speed
                # Default Unit: Miles Per Hour
                if self.connection.supports(obd.commands.SPEED):
                    speedResponse = self.connection.query(obd.commands.SPEED)
                    speed = round(speedResponse.value.to("mph"))
                else:
                    speed = '0'

                # Get RPM
                if self.connection.supports(obd.commands.RPM):
                    rpmResponse = self.connection.query(obd.commands.RPM)
                    rpm = rpmResponse.value
                else:
                    rpm = '0'

                # Get Coolant Temperature
                # Default Unit: Celsius
                if self.connection.supports(obd.commands.COOLANT_TEMP):
                    coolantTemperatureResponse = self.connection.query(
                        obd.commands.COOLANT_TEMP)
                    coolantTemperature = coolantTemperatureResponse.value
                else:
                    coolantTemperature = '0'

                # Get Throttle Position
                if self.connection.supports(obd.commands.THROTTLE_POS):
                    throttlePositionResponse = self.connection.query(
                        obd.commands.THROTTLE_POS)
                    throttlePosition = throttlePositionResponse.value
                else:
                    throttlePosition = '0'

                # Get Intake Pressure
                if self.connection.supports(obd.commands.INTAKE_PRESSURE):
                    intakePressureResponse = self.connection.query(
                        obd.commands.INTAKE_PRESSURE)
                    intakePressure = intakePressureResponse.value
                else:
                    intakePressure = '0'

                # Get Timing Advance
                if self.connection.supports(obd.commands.TIMING_ADVANCE):
                    timingAdvanceResponse = self.connection.query(
                        obd.commands.TIMING_ADVANCE)
                    timingAdvance = timingAdvanceResponse.value
                else:
                    timingAdvance = '0'

                # Get Mass Air Flow
                if self.connection.supports(obd.commands.MAF):
                    mafResponse = self.connection.query(obd.commands.MAF)
                    maf = mafResponse.value
                else:
                    maf = '0'

                self.obdData = {"speed": speed, "rpm": rpm, "coolant_temp": coolantTemperature, "throttle_position": throttlePosition,
                                "intake_pressure": intakePressure, "timing_advance": timingAdvance, "maf": maf}
                return self.obdData
            except Exception as E:
                logging.debug(E)
