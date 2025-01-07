# yoctopuce-sensors

This project allows you to monitor Yoctopuce sensors and export sensor readings (temperature, pressure, humidity) as Prometheus metrics via an HTTP server. The readings can then be scraped by Prometheus for real-time monitoring.

## Features

- Supports multiple sensor types (temperature, pressure, humidity) from Yoctopuce.
- Prometheus metrics integration to expose sensor readings via a web endpoint.
- Asynchronous sensor data collection for non-blocking I/O.
- Detailed logging for sensor status, including errors and offline sensors.

## Requirements

- Python 3.8+
- Yoctopuce Python Library
- Prometheus Python Client Library

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Semeghini-Lab/yoctopuce-sensors.git
    cd yoctopuce-sensors
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Install the Yoctopuce Python libraries:

    - Download the [Yoctopuce Python libraries](https://www.yoctopuce.com/EN/libraries.php) and add the `yoctopuce` package to your environment.
  
4. Verify that Prometheus is running and if it is not, start scraping data by executing the following command:

   ```bash
   ./prometheus --config.file=path/to/prometheus.yml
   ```
   The `prometheus.yml` configuration file can be found in the *prometheus-tools* repository on the Semeghini-Lab github.

5. Run the Prometheus exporter:

    ```bash
    python3 yocto_metrics_exporter.py
    ```

6. View the Prometheus metrics:

    The metrics are exposed at `http://localhost:8000/metrics` by default. You can change the port by modifying the `yocto_metrics_exporter.py` file.

## Configuration

To change the sensor types or the port number for the Prometheus server, you can modify the constants in the code or create a `config.ini` file (optional).

### Sample `config.ini`

```ini
[prometheus]
port = 8000

[sensors]
types = temperature, pressure, humidity
```

---

## Usage

1.	Ensure the Yoctopuce sensors are connected via USB.
2.	The program will automatically discover all sensors and expose their readings via the Prometheus HTTP server.
3.	In your Prometheus configuration file (prometheus.yml), add a new job to scrape the exporter:

  ```yaml
  scrape_configs:
  - job_name: 'yoctopuce_sensors'
    static_configs:
      - targets: ['localhost:8000']
  ```
4. Restart Prometheus and verify that the sensor metrics are available in the Prometheus UI.

---

## Logging

The logs provide information about sensor status, errors, and sensor readings. Logging is configured in `yocto_metrics_exporter.py`. You can customize the logging level (e.g., DEBUG, INFO, WARNING, ERROR) to control the verbosity of the logs.

---

## Cleanup

The SensorManager class automatically frees up Yoctopuce resources when the program exits. To stop the exporter, use Ctrl + C.
