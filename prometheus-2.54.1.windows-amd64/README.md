# prometheus-tools

A collection of tools, scripts, and configurations for working with Prometheus. This repository currently includes:

- Prometheus configuration files (prometheus.yml) for setting up and managing Prometheus instances.
- A custom Python client for querying time-series data from Prometheus, with support for flexible time range queries and data analysis using pandas.
- A python script for backing up Prometheus data onto our NAS.
- A batch script calling on the Prometheus backup to be used with Windows Task Scheduler

Use these tools to streamline your interaction with Prometheus, when setting up a new instance, querying metrics, or performing data analysis.

---

Minimal example for calling the PrometheusClient class:

```python

from prometheus_client import PrometheusClient
from datetime import datetime, timedelta, timezone

# Define metric and time range

metric_name = 'meteo_temperature'
end_time = datetime.now(timezone.utc)
start_time = end_time - timedelta(hours=12)

# Query Prometheus

client = PrometheusClient(prometheus_url='http://localhost:9090')

df = client.query_range(metric=metric_name, start_time=start_time, end_time=end_time, step='5s')
```
---

Notes on Prometheus backup.

```prometheus_data_backup.py``` is designed to copy any files that have been modified within the last 24 hours onto the NAS. There is no overwrite protection and changes are only copied from local to the NAS.
```prometheus_data_backup.bat``` exists to facilitate scheduling with Windows Task Scheduler. The backup occurs every day at 23:59:59.
