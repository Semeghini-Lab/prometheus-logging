from prometheus_client import start_http_server, Gauge
from tc_logger_manager import TCLogger
import logging
import asyncio

# TO EDIT
# USB COM port of the TC Logger linker
port = "COM7"
tclogger = TCLogger(port)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Define Prometheus gauge
temp_gauge = Gauge(
        f'tc_logger_temp_celcius',
        f'Readings from thermocouple logger',
        ['channel']
    )

async def main():
    channels_to_read = list(range(0,8)) + [24,25]
    while True:
        for i in channels_to_read:
                temp = tclogger.read_channel(i)
                # If the tc logger can not read a temperature, it returns None (set temp to something nonsensical)
                if temp == None:
                     temp = -500
                temp_gauge.labels(channel=i).set(temp)
                # logging.info(f'Chan {i} reads temp {temp}')
        await asyncio.sleep(1)

if __name__ == "__main__":
    # Start Prometheus HTTP server on port 8001
    start_http_server(8001)
    logging.info("Prometheus metrics are now being served on http://localhost:8001/metrics")

    try:
        # Run the main async function
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Thermocouple Logger metrics exporter stopped by user.")
    finally:
         tclogger.close()