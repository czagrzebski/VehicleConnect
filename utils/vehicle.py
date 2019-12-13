import numpy as np


class Vehicle():
    def __init__(self):
        self.year = 1996
        self.vin = "NONE"
        self.max_rpm = 7000
        self.axel_ratio = 0
        self.tire_diameter = 0
        self.transmission_ratios = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        self.rpm_list = [500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000, 3250, 3500,
                        3750, 4000, 4250, 4500, 4750, 5000, 5250, 5500, 5750, 6000, 6250, 6500, 6750, 7000]
        self.gear_data = {}

    def setup_vehicle(self, **kwargs):
        if("year" in kwargs):
            self.year = kwargs["year"]
        if("vin" in kwargs):
            self.vin = kwargs["vin"]
        if("axel_ratio" in kwargs):
            self.axel_ratio = kwargs["axel_ratio"]
        if("transmission_ratios" in kwargs):
            self.transmission_ratios = kwargs["transmission_ratios"]
        if("tire_size" in kwargs):
            self.tire_diameter = kwargs["tire_size"]
        if("max_rpm" in kwargs):
            self.max_rpm = kwargs["max_rpm"]

    def generate_gear_data(self):
        """Generates Gear Data used to Determine the Gear based on RPM and Speed."""
        for rpm in self.rpm_list:
            self.temp_data = {}

            for transmission_ratio in self.transmission_ratios:

                # Skip if Transmission Ratio, Tire Diamater, or Axel Ratio is Zero
                if self.transmission_ratios[transmission_ratio] != 0 and self.tire_diameter != 0 and self.axel_ratio != 0:
                    speed = rpm / \
                        ((self.axel_ratio *
                          self.transmission_ratios[transmission_ratio]*336.13)/self.tire_diameter)
                    data = {round(speed): transmission_ratio}
                    self.temp_data.update(data)
                    self.gear_data.update({rpm: self.temp_data})
                else:
                    continue

    def get_gear(self, speed, rpm):
        try:
            if (int(rpm) == 0 and int(speed) == 0):
                gear = "N"
                return gear
            elif (int(rpm) == 0):
                gear = "N"
                return gear
            else:
                # Convert RPM List to NP Array
                rpm_np = np.asarray(self.rpm_list)

                # Find Index of RPM that is nearest to given RPM
                idx_RPM = (np.abs(rpm_np - rpm)).argmin()

                # Nearest RPM
                nearest_RPM = rpm_np[idx_RPM]

                # Get Speed Values from nearest RPM from generated RPM data

                speed_np = np.array([])
                for mph in self.gear_data[nearest_RPM]:
                    speed_np = np.append(speed_np, mph)

                idx_Speed = (np.abs(speed_np-speed)).argmin()

                nearest_Speed = speed_np[idx_Speed]

                # Retrieve Gear based on nearest RPM and speed from Generated Gear List
                gear = self.gear_data[nearest_RPM][nearest_Speed]

                return str(gear)
        except Exception as F:
            return 'N'
