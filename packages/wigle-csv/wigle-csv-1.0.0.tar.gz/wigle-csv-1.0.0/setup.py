# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wigle_csv']

package_data = \
{'': ['*']}

install_requires = \
['dataclass-csv>=1.4.0,<2.0.0']

setup_kwargs = {
    'name': 'wigle-csv',
    'version': '1.0.0',
    'description': 'WiGLE CSV format parser',
    'long_description': '# wigle-csv\n\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/wigle-csv)](https://pypi.org/project/wigle-csv/)\n[![PyPI](https://img.shields.io/pypi/v/wigle-csv)](https://pypi.org/project/wigle-csv/)\n[![Downloads](https://pepy.tech/badge/wigle-csv)](https://pepy.tech/project/wigle-csv)\n[![ci](https://github.com/jyooru/wigle-csv/actions/workflows/ci.yml/badge.svg)](https://github.com/jyooru/wigle-csv/actions/workflows/ci.yml)\n[![codecov](https://codecov.io/gh/jyooru/wigle-csv/branch/main/graph/badge.svg?token=SRK5RPLHN0)](https://codecov.io/gh/jyooru/wigle-csv)\n[![License](https://img.shields.io/github/license/jyooru/wigle-csv)](LICENSE)\n\nPython module to parse the [WiGLE CSV format](https://api.wigle.net/csvFormat.html).\n\n## Installation\n\nwigle-csv is available on PyPI:\n\n```bash\npip install wigle-csv\n```\n\n## Usage\n\nwigle-csv provides a `read` function that can be used to easily parse files in the WiGLE CSV format:\n\n```py\nimport wigle_csv\n\n\nfilename = "WigleWifi.csv"\n\nwith open(filename) as file:\n    preheader, reader = wigle_csv.read(file)\n    print(f"Loaded {filename} using {preheader.format_version}.")\n\n    wpa2_wifi_count = 0\n    wifi_count = 0\n    for radio in reader:\n        if radio.type == "WIFI":\n            wifi_count += 1\n            if "WPA2" in radio.capabilities:\n                wpa2_wifi_count += 1\n\n    print(f"There are {wifi_count} WiFi networks in {filename}.")\n    print(f"{wpa2_wifi_count} use WPA2.")\n```\n\n```\n$ python example.py\nLoaded WigleWifi.csv using WigleWifi-1.4.\nThere are 6360 WiFi networks in WigleWifi.csv.\n5345 use WPA2.\n```\n\nwigle-csv presents all data in the provided CSV file using dataclasses. All dataclasses are statically typed and based on the [WiGLE CSV Format Specification](https://api.wigle.net/csvFormat.html):\n\n```py\nclass Preheader:\n    format_version: str\n    app_release: Optional[str]\n    model: Optional[str]\n    release: Optional[str]\n    device: Optional[str]\n    display: Optional[str]\n    board: Optional[str]\n    brand: Optional[str]\n\n\nclass Radio:\n    address: str\n    capabilities: str\n    timestamp: datetime\n    channel: int\n    rssi: int\n    latitude: float\n    longitude: float\n    altitude: float\n    accuracy: float\n    type: str\n    name: Optional[str]\n```\n\n## License\n\nSee [LICENSE](LICENSE) for details.\n',
    'author': 'Joel',
    'author_email': 'joel@joel.tokyo',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jyooru/wigle-csv',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
