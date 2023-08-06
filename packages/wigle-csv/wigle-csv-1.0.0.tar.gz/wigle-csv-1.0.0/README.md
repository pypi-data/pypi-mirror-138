# wigle-csv

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/wigle-csv)](https://pypi.org/project/wigle-csv/)
[![PyPI](https://img.shields.io/pypi/v/wigle-csv)](https://pypi.org/project/wigle-csv/)
[![Downloads](https://pepy.tech/badge/wigle-csv)](https://pepy.tech/project/wigle-csv)
[![ci](https://github.com/jyooru/wigle-csv/actions/workflows/ci.yml/badge.svg)](https://github.com/jyooru/wigle-csv/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/jyooru/wigle-csv/branch/main/graph/badge.svg?token=SRK5RPLHN0)](https://codecov.io/gh/jyooru/wigle-csv)
[![License](https://img.shields.io/github/license/jyooru/wigle-csv)](LICENSE)

Python module to parse the [WiGLE CSV format](https://api.wigle.net/csvFormat.html).

## Installation

wigle-csv is available on PyPI:

```bash
pip install wigle-csv
```

## Usage

wigle-csv provides a `read` function that can be used to easily parse files in the WiGLE CSV format:

```py
import wigle_csv


filename = "WigleWifi.csv"

with open(filename) as file:
    preheader, reader = wigle_csv.read(file)
    print(f"Loaded {filename} using {preheader.format_version}.")

    wpa2_wifi_count = 0
    wifi_count = 0
    for radio in reader:
        if radio.type == "WIFI":
            wifi_count += 1
            if "WPA2" in radio.capabilities:
                wpa2_wifi_count += 1

    print(f"There are {wifi_count} WiFi networks in {filename}.")
    print(f"{wpa2_wifi_count} use WPA2.")
```

```
$ python example.py
Loaded WigleWifi.csv using WigleWifi-1.4.
There are 6360 WiFi networks in WigleWifi.csv.
5345 use WPA2.
```

wigle-csv presents all data in the provided CSV file using dataclasses. All dataclasses are statically typed and based on the [WiGLE CSV Format Specification](https://api.wigle.net/csvFormat.html):

```py
class Preheader:
    format_version: str
    app_release: Optional[str]
    model: Optional[str]
    release: Optional[str]
    device: Optional[str]
    display: Optional[str]
    board: Optional[str]
    brand: Optional[str]


class Radio:
    address: str
    capabilities: str
    timestamp: datetime
    channel: int
    rssi: int
    latitude: float
    longitude: float
    altitude: float
    accuracy: float
    type: str
    name: Optional[str]
```

## License

See [LICENSE](LICENSE) for details.
