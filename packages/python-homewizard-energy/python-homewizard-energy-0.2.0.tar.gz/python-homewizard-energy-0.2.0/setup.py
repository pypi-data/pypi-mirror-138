# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['homewizard_energy']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.0.0']

setup_kwargs = {
    'name': 'python-homewizard-energy',
    'version': '0.2.0',
    'description': 'Asynchronous Python client for the HomeWizard Energy',
    'long_description': '# python-homewizard-energy\n\nAsyncio package to communicate with HomeWizard Energy devices\nThis package is aimed at basic control of the device. Initial setup and configuration is assumed to done with the official HomeWizard Energy app.\n\n## Disclaimer\n\nThis package is not developed, nor supported by HomeWizard.\n\n## Installation\n```bash\npython3 -m pip install python-homewizard-energy\n```\n\n# Usage\nInstantiate the HWEnergy class and access the API.\n\nFor more details on the API see the official API documentation on\nhttps://homewizard-energy-api.readthedocs.io\n\n# Example\nThe example below is available as a runnable script in the repository.\n\n```python\nfrom homewizard_energy import HomeWizardEnergy\n\n# Make contact with a energy device\ndevice = HomeWizardEnergy(args.host)\n\n# Update device value\nawait device.update()\n\n# Use the data\nprint(device.device.product_name)\nprint(device.device.serial)\nprint(device.data.wifi_ssid)\n\n# Close connection\nawait device.close()\n```\n',
    'author': 'DCSBL',
    'author_email': None,
    'maintainer': 'DCSBL',
    'maintainer_email': None,
    'url': 'https://github.com/dcsbl/python-homewizard-energy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
