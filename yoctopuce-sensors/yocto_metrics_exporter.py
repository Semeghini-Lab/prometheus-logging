# metrics_exporter.py

import asyncio
import logging
from prometheus_client import start_http_server, Gauge
from yocto_sensor_manager import SensorManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Define Prometheus metrics with labels
def create_metric(sensor_type):
    return Gauge(
        f'meteo_{sensor_type}',
        f'{sensor_type.capitalize()} reading from Yoctopuce sensors',
        ['hardware_id']
    )

# Create Prometheus metrics dynamically based on sensor types
SENSOR_TYPES = ['temperature', 'pressure', 'humidity']
metrics = {sensor_type: create_metric(sensor_type) for sensor_type in SENSOR_TYPES}

async def read_sensor_data(sensors):
    """
    Asynchronously reads data from all sensors and updates Prometheus metrics.
    """
    while True:
        for hw_id, sensor_info in sensors.items():
            sensor = sensor_info['sensor']
            sensor_type = sensor_info['type']

            if sensor.isOnline():
                try:
                    value = sensor.get_currentValue()
                    metrics[sensor_type].labels(hardware_id=hw_id).set(value)
                    # logging.info(f"[{sensor_type.capitalize()}] {hw_id}: {value}")
                except Exception as e:
                    logging.error(f"Error reading {sensor_type} from {hw_id}: {e}")
            else:
                logging.warning(f"Sensor {hw_id} is offline.")

        await asyncio.sleep(1)  # Wait for 1 second before next read

async def main():
    """
    Main asynchronous function to initialize sensors and start data reading.
    """
    sensor_manager = SensorManager()

    try:
        sensor_manager.initialize_sensors()
        sensors = sensor_manager.get_sensors()

        if not sensors:
            logging.warning("No sensors found. Exiting.")
            return

        # Start the sensor data reading task
        sensor_task = asyncio.create_task(read_sensor_data(sensors))

        # Run indefinitely until interrupted
        await sensor_task

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    finally:
        sensor_manager.cleanup()

if __name__ == "__main__":
    # Start Prometheus HTTP server on port 8000
    start_http_server(8000)
    logging.info("Prometheus metrics are now being served on http://localhost:8000/metrics")

    try:
        # Run the main async function
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("USB metrics exporter stopped by user.")