# sensor_manager.py

import logging
from yoctopuce.yocto_api import YAPI, YRefParam
from yoctopuce.yocto_temperature import YTemperature
from yoctopuce.yocto_pressure import YPressure
from yoctopuce.yocto_humidity import YHumidity

class SensorManager:
    """
    Manages the initialization and discovery of Yoctopuce sensors.
    """
    
    SENSOR_TYPES = {
        'temperature': YTemperature,
        'pressure': YPressure,
        'humidity': YHumidity
    }

    def __init__(self):
        self.sensors = {}
        self.setup_hub()

    def setup_hub(self):
        """
        Registers the Yoctopuce USB hub.
        """
        errmsg = YRefParam()
        YAPI.RegisterHub("usb", errmsg)
        if errmsg.value:
            logging.error(f"Error registering Yoctopuce hub: {errmsg.value}")
            raise RuntimeError(f"Yoctopuce hub registration failed: {errmsg.value}")
        logging.info("Yoctopuce hub registered successfully.")

    def initialize_sensors(self):
        """
        Discovers and initializes all connected sensors.
        Populates the self.sensors dictionary with sensor information.
        """
        for sensor_type, sensor_class in self.SENSOR_TYPES.items():
            # Dynamically get the first sensor method, e.g., FirstTemperature, FirstPressure
            first_sensor_method = getattr(sensor_class, f'First{sensor_type.capitalize()}', None)
            if not first_sensor_method:
                logging.warning(f"No method found for initializing {sensor_type} sensors.")
                continue

            sensor = first_sensor_method()
            while sensor:
                hw_id = sensor.get_hardwareId()
                self.sensors[hw_id] = {'sensor': sensor, 'type': sensor_type}
                logging.info(f"Found {sensor_type.capitalize()} Sensor: {hw_id}")

                # Dynamically get the next sensor method, e.g., nextTemperature, nextPressure
                next_sensor_method = getattr(sensor, f'next{sensor_type.capitalize()}', None)
                if not next_sensor_method:
                    logging.warning(f"No method found to iterate {sensor_type} sensors.")
                    break

                sensor = next_sensor_method()

    def get_sensors(self):
        """
        Returns the dictionary of initialized sensors.
        """
        return self.sensors

    def cleanup(self):
        """
        Frees Yoctopuce API resources.
        """
        YAPI.FreeAPI()
        logging.info("Yoctopuce API resources freed.")