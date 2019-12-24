import os
import re
import threading
import time
from datetime import datetime
from math import cos, sin
import logging
import traceback
import platform
import argparse
from kivymd.uix.bottomnavigation import MDBottomNavigation
from kivymd.uix.bottomnavigation import MDBottomNavigationBar
from kivymd.uix.bottomnavigation import MDBottomNavigationHeader
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.label import MDLabel
from kivymd.theming import ThemeManager


import kivy
import numpy as np
import obd
from kivy.app import App
from kivy.clock import Clock, mainthread
from kivy.config import Config
from kivy.lang import Builder
from kivy.properties import (ListProperty, NumericProperty, ObjectProperty,
                             StringProperty)
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.stacklayout import StackLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.settings import SettingsWithSidebar
from kivy.core.window import Window

from utils.obdutility import OBDUtility
from utils.vehicle import Vehicle
from settings.settings_json import obd_json, vehicle_json
from utils.gauges import Gauge, GaugeSmall
from kivymd.app import MDApp

global developermode
developermode = False

global obd_mac_address
obd_mac_address = "8C:DE:52:C4:E5:84"

####===Configuration===####
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
Config.set('graphics', 'resizable', False)
Config.set('kivy', 'keyboard_mode', 'systemanddock')
Window.size = (800, 480)
###########################



class ImageButton(ButtonBehavior, Image):
    pass


class VehicleConnect(MDApp):

    ###########===Kivy Binded Variables==##################
    speedOBD = StringProperty('0')
    speedOBDValue = NumericProperty(0)

    rpmOBD = StringProperty('0')
    rpmOBDValue = NumericProperty(0)

    coolantTemperatureOBD = StringProperty('0')
    coolantTemperatureOBDValue = NumericProperty(0)

    throttlePositionOBD = StringProperty('0')
    throttlePositionOBDValue = NumericProperty(0)

    intakePressureOBD = StringProperty('0')
    intakePressureOBDValue = NumericProperty(0)

    timingAdvanceOBD = StringProperty('0')
    timingAdvanceOBDValue = NumericProperty(0)

    mafOBD = StringProperty('0')
    mafOBDValue = NumericProperty(0)

    gear = StringProperty('0')

    obdStatus = StringProperty('0')


    #######################################################

    def build(self):
        self.settings_cls = SettingsWithSidebar
        main = Builder.load_file("data/main_ui.kv")
        theme_cls = ThemeManager()
        self.theme_cls.theme_style = "Dark"
        self.sm = MyScreenManager()
        return main

    def build_config(self, config):
        config.setdefaults('OBD', {
            'obdport': '/dev/rfcomm1',
            'obdmacaddress': '00:00:00:00:00:00'}

        )

        config.setdefaults('Vehicle', {
            'firstGear': 0.00,
            'secondGear': 0.00,
            'thirdGear': 0.00,
            'fourthGear': 0.00,
            'fifthGear': 0.00,
            'sixthGear': 0.00,
            'axelRatio':
            0.00,
            'tireDiamater': 0.00,
            'maxRPM': 7000

        })

    def build_settings(self, settings):
        # OBD Panel
        settings.add_json_panel('OBD', self.config, data=obd_json)

        # Vehicle Panel
        settings.add_json_panel('Vehicle', self.config, data=vehicle_json)

    def on_config_change(self, config, section, key, value):
        if key == "maxRPM":
            self.vehicle.setup_vehicle(max_rpm=self.config.get(
                'Vehicle', 'maxRPM'))
        if key == "obdport":
            # change obd port
            obdUtility.connect_to_obd(connection=self.config.get(
                'OBD', 'obdport'))

        if key == "firstGear" or "secondGear" or "thirdGear" or "fourthGear" or "fifthGear" or "sixthGear":
            try:
                # get gear settings
                first_gear = float(self.config.get('Vehicle', 'firstGear'))
                second_gear = float(self.config.get('Vehicle', 'secondGear'))
                third_gear = float(self.config.get('Vehicle', 'thirdGear'))
                fourth_gear = float(self.config.get('Vehicle', 'fourthGear'))
                fifth_gear = float(self.config.get('Vehicle', 'fifthGear'))
                sixth_gear = float(self.config.get('Vehicle', 'sixthGear'))

                # build list of gears with gear ratio
                transmission_ratio_list = {
                    1: first_gear, 2: second_gear, 3: third_gear, 4: fourth_gear, 5: fifth_gear, 6: sixth_gear}

                # set transmission ratios
                self.vehicle.setup_vehicle(
                    transmission_ratios=transmission_ratio_list)
                self.vehicle.generate_gear_data()
            except:
                logging.warning("Error while loading the vehicle information")
        if key == "axelRatio":
            axel_ratio = float(self.config.get('Vehicle', 'axelRatio'))
            self.vehicle.setup_vehicle(axel_ratio=axel_ratio)
            self.vehicle.generate_gear_data()
        if key == "tireDiamater":
            tire_diamater = float(self.config.get('Vehicle', 'tireDiameter'))
            self.vehicle.setup_vehicle(tire_diamater=tire_diamater)
            self.vehicle.generate_gear_data()
        if key == "obdmacaddress":
            athread = threading.Thread(target=obdUtility.set_rfcomm, args=((self.config.get('OBD', 'obdmacaddress'))))
            athread.start()

    def on_start(self):
        #bind rfcomm1 to bluetooth OBD adapter
        if developermode == False:
            obdUtility.set_rfcomm(self.config.get('OBD', 'obdmacaddress'))
       

        # Initialize Vehicle Class
        self.vehicle = Vehicle()
        try:
            #Import Saved Settings
            first_gear = float(self.config.get('Vehicle', 'firstGear'))
            second_gear = float(self.config.get('Vehicle', 'secondGear'))
            third_gear = float(self.config.get('Vehicle', 'thirdGear'))
            fourth_gear = float(self.config.get('Vehicle', 'fourthGear'))
            fifth_gear = float(self.config.get('Vehicle', 'fifthGear'))
            sixth_gear = float(self.config.get('Vehicle', 'sixthGear'))
            axel_ratio = float(self.config.get('Vehicle', 'axelRatio'))
            tire_diamater = float(self.config.get('Vehicle', 'tireDiamater'))
            max_rpm = float(self.config.get('Vehicle', 'maxRPM'))
            transmission_ratio_list = {1: first_gear, 2: second_gear,
                                       3: third_gear, 4: fourth_gear, 5: fifth_gear, 6: sixth_gear}

            # Setup Vehicle (for Gear Calculation and General Vehicle Information)
            self.vehicle.setup_vehicle(
                axel_ratio=axel_ratio, tire_size=tire_diamater, transmission_ratios=transmission_ratio_list, max_rpm=max_rpm)
        except:
            logging.error("Failed to load vehicle information from settings")

        # Generate Gear Data to be used for Gear Calculation
        self.vehicle.generate_gear_data()

        if developermode == True:
            self.basic_popup("System", "Developer Mode Has Been Enabled!", "Ok", lambda x: self.close_current_popup())
        
        #!!!!!!!!!!
        #Experimental Version WARNING...REMOVE BEFORE MERGING TO MASTER!!!

        self.basic_popup("System", "This is an experimental build! Expect Bugs", "Ok", lambda x: self.close_current_popup())
        
        self.current_dtc_codes = {}
        
        #obd connection thread
        self.update_obd_data = threading.Thread(target=self.refresh_obd)
        self.update_obd_data.setDaemon(True)
        self.update_obd_data.start()

        self.update_ui_obd = False
        #update obd data
        Clock.schedule_interval(lambda x: self.update_obd(), .1)

        #check for diagnostics
        check_diagnostic_codes_thread = threading.Thread(target=self.check_for_diagnostics)
        check_diagnostic_codes_thread.setDaemon(False)
        check_diagnostic_codes_thread.start()
        

    def check_for_diagnostics(self):
            diagnostic_codes = obdUtility.get_diagnostic_codes()
            if diagnostic_codes is not None:
                for dtc in diagnostic_codes:
                    if dtc[0] not in self.current_dtc_codes:
                        logging.info("Found check engine code {0}".format(dtc[0]))
                        code = {dtc}
                        self.current_dtc_codes.update(code)
                        self.basic_popup("Alert", "{0}\n{1}".format(dtc[0], dtc[1]), "Ok", lambda x: self.close_current_popup())

    def refresh_obd(self):
        obdUtility.connect_to_obd(connection=self.config.get(
            'OBD', 'obdport'), obd_mac=obd_mac_address)

        # constantly refreshes obd data
        while True:
            obdUtility.refresh_obd_data()
            self.check_for_diagnostics()
            time.sleep(.2)

    
    @mainthread
    def update_obd(self):
        try:
            if self.update_ui_obd == True:
                # Get Dict of fetched OBD Data
                obd_data = obdUtility.get_obd_data()
                
            
               
                # Get OBD Values from Returned Dict
                # Convert Values to Percent (For Gauges)
                # Set binded StringProperty and NumericProperty values (kivy) to obd data

                speedValue = (re.findall('\d+', str(obd_data["speed"])))
                self.speedOBDValue = int(speedValue[0])/140
                self.speedOBD = str(speedValue[0])

                rpmValue = (re.findall('\d+', str(obd_data["rpm"])))
                self.rpmOBDValue = int(rpmValue[0])/int(self.vehicle.max_rpm)
                self.rpmOBD = str(rpmValue[0])

                coolantTemperatureValue = (re.findall(
                    '\d+', str(obd_data["coolant_temp"])))
                self.coolantTemperatureOBDValue = int(
                    coolantTemperatureValue[0])/160
                self.coolantTemperatureOBD = str(coolantTemperatureValue[0])

                throttlePositionValue = (re.findall(
                    '\d+', str(obd_data["throttle_position"])))
                self.throttlePositionOBDValue = int(
                    throttlePositionValue[0])/100
                self.throttlePositionOBD = str(throttlePositionValue[0])

                intakePressureValue = (re.findall(
                    '\d+', str(obd_data["intake_pressure"])))
                self.intakePressureOBDValue = int(intakePressureValue[0])/150
                self.intakePressureOBD = str(intakePressureValue[0])

                timingAdvanceValue = (re.findall(
                    '\d+', str(obd_data["timing_advance"])))
                self.timingAdvanceOBDValue = int(timingAdvanceValue[0])/100
                self.timingAdvanceOBD = str(timingAdvanceValue[0])

                mafValue = (re.findall('\d+', str(obd_data["maf"])))
                self.mafOBDValue = int(mafValue[0])/100
                self.mafOBD = str(mafValue[0])


             
                self.gear = self.vehicle.get_gear(
                    int(speedValue[0]), int(rpmValue[0]))


                

        except Exception as uiUpdateError:
                logging.error(
                    "An error occurred while attempting to push obd data to the interface: {0}".format(uiUpdateError))
                traceback.print_exc()

    def enable_obd_ui_updates(self):
        """Enables OBD UI Updating"""
        self.update_ui_obd = True

    def change_screen(self):
        pass

    def disable_obd_ui_updates(self):
        """Disables OBD UI Updating (Saves RPi Resources)"""
        self.update_ui_obd = False

    @mainthread
    def basic_popup(self, title, message, button_text, action):
        box = BoxLayout(orientation="vertical")
        box.add_widget(Label(text="{0}".format(message), pos_hint={'center_y': .5}))
        btn1 = Button(text=button_text, size_hint = (1,.3))
        btn1.bind(on_release=action)
        box.add_widget(btn1)
        popup = Popup(title=title,
                            content=box,
                            size_hint=(None, None), size=(380, 240))
        popup.open()

    def one_button_popup(self, title, message, button_one_title, button_one_action):
        pass
    
    def close_current_popup(self):
         if isinstance(App.get_running_app().root_window.children[0], Popup):
            App.get_running_app().root_window.children[0].dismiss()

    def advanced_popup(self, title, message, button_one_title, button_one_action, button_two_title, button_two_action):
        box = BoxLayout(orientation="vertical")
        box2 = BoxLayout(orientation="horizontal")
        box.add_widget(Label(text='Hello world'))
        box2.add_widget(Button(text='Hi'))
        box2.add_widget(Button(text='Cool'))
        box.add_widget(box2)
        popup = Popup(title=title,
                            content=box,
                            size_hint=(None, None), size=(400, 300))
        popup.open()



#######===SCREENS===#######


class MyScreenManager(ScreenManager):
    HomeScreen = ObjectProperty(None)
    PerformanceHomeScreen = ObjectProperty(None)
    NavBar = ObjectProperty(None)


class HomeScreen(Screen):
  

    
    def print_test(self):
        print("hithere")


class PerformanceHomeScreen(Screen):
    pass



###########################


class NavBar(FloatLayout):
    pass


class AppDashboard(FloatLayout):
    pass


if __name__ == "__main__":
    LOG_FILE = datetime.now().strftime('logs/vclog_%H_%M_%S_%d_%m_%Y.log')
    logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG,
                        format='VehicleConnect: %(message)s')
    logging.debug("Vehicle Connect")
    
    if platform.system() == "Windows":
        developermode=True
        logging.debug("DEBUG MODE ENABLED FOR WINDOWS ENVIRONMENT")
    
 
    obdUtility = OBDUtility()
    vehicleConnect = VehicleConnect()
    vehicleConnect.run()
