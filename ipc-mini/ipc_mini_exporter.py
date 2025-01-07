from ipc_mini_manager import *
from prometheus_client import start_http_server, Gauge
import logging
import asyncio

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Define Prometheus gauges
ipc_pressure_gauge = Gauge(
        f'ipc_mini_pressure',
        f'Pressure readings from IPC Mini',
        ['device'])
ipc_voltage_gauge = Gauge(
        f'ipc_mini_voltage',
        f'Voltage readings from IPC Mini',
        ['device'])
ipc_current_gauge = Gauge(
        f'ipc_mini_current',
        f'Current readings from IPC Mini',
        ['device'])

async def main():
    
    devices = ['SAES TOP', 'SAES BOTTOM']
    device_ips = ['192.168.0.104', '192.168.0.103']
    device_managers = [IPCMiniManager(ip) for ip in device_ips]

    while True:
        for i in range(len(devices)):
            ipc_pressure_gauge.labels(device=devices[i]).set(device_managers[i].get_pressure())
            ipc_current_gauge.labels(device=devices[i]).set(device_managers[i].get_current())
            ipc_voltage_gauge.labels(device=devices[i]).set(device_managers[i].get_voltage())
            logging.info(f'{devices[i]} reads pressure {device_managers[i].get_pressure()}')
        await asyncio.sleep(5)


if __name__ == "__main__":
    # Start Prometheus HTTP server on port 8001
    start_http_server(8002)
    logging.info("Prometheus metrics are now being served on http://localhost:8002/metrics")

    try:
        # Run the main async function
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Thermocouple Logger metrics exporter stopped by user.")
