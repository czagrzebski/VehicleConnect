import time
import json
import logging

class SettingsManager():
    """VehicleConnect Settings Manager"""

    def __init__(self):
        self.config = None

    def get_setting(self, section, key):
        """
        Returns Setting Value
        """
        
        try:
            return self.config[section][key] 
        except KeyError as Error:
            logging.debug("Unable to find key")
            return None

    def set_setting(self, section, key, value):
        """
        Sets a setting for VehicleConnect Configuration
        """
        if self.config[section][key] != value:
            self.config[section][key] = value
            self.write_config()
        else:
            logging.debug("Value already exists in {0}".format(key))
       
    def get_all_settings(self):
        """Returns dictionary of Current VehicleConnect Settings"""
        return self.config

    def restore_default_config(self):
        """
        Restores VehicleConnect Configuration to the default configuration

        """
        pass
    
    def read_config(self):
        """
        Reads Configuration File to SettingsManager().config
        """

        with open('settings\\config.json') as json_file:
            self.config = json.load(json_file)
            logging.debug("Reading Configuration File")

    def write_config(self):
        """
        Writes SettingsManager().config Configuration to File
        """
        with open('settings\\config.json', 'w') as outfile:
            json.dump(self.config, outfile)
            logging.debug("Writing Configuration File")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='SettingsManager: %(message)s')
    manager = SettingsManager()
    manager.read_config()
    manager.get_setting("vehicle", "max_rpm")
    manager.set_setting("vehicle", "max_rpm", 4000)
    manager.get_setting("vehicle", "max_rpm")