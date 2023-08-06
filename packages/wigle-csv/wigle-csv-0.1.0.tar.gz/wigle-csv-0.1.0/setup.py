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
    'version': '0.1.0',
    'description': 'WiGLE CSV format parser',
    'long_description': None,
    'author': 'Joel',
    'author_email': 'joel@joel.tokyo',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
