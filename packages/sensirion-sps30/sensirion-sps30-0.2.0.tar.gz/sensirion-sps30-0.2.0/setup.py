# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sensirion_sps30']

package_data = \
{'': ['*']}

install_requires = \
['pyserial>=3.5,<4.0']

setup_kwargs = {
    'name': 'sensirion-sps30',
    'version': '0.2.0',
    'description': 'Sensirion SPS30 Python library',
    'long_description': '# Sensirion SPS30 PM Sensor\n\n![PyPI](https://img.shields.io/pypi/v/sensirion-sps30?style=flat-square)\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/MMartin09/sensirion-sps30/lint?style=flat-square)\n![GitHub](https://img.shields.io/github/license/MMartin09/sensirion-sps30?style=flat-square)\n[![style black](https://img.shields.io/badge/Style-Black-black.svg?style=flat-square)](https://github.com/ambv/black)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat-square&labelColor=ef8336)](https://pycqa.github.io/isort/)\n\n## Short description\n\n<a href="https://sensirion.com/images/scale/1200x750/com-sensirion-master/portfolio/series/image/4df6fc7a-b697-493b-aa0f-f203ba562e11.png">\n    <img src="https://sensirion.com/images/scale/1200x750/com-sensirion-master/portfolio/series/image/4df6fc7a-b697-493b-aa0f-f203ba562e11.png" align="left" height="73" width="145" >\n</a>  \n\nThis is a simple library to communicate with a [Sensirion SPS30](https://sensirion.com/products/catalog/SPS30/) sensor via Serial communication. \nThe SPS30 is an MCERTS-certified particulate matter sensor based on laser scattering measurement principles. \nIt can classify particles within PM1.0, PM2.5, PM4 and PM10 categories. \n\nFor further details refer to the official [documentation](https://sensirion.com/media/documents/8600FF88/616542B5/Sensirion_PM_Sensors_Datasheet_SPS30.pdf) of the sensor.\n\n## Usage\n\nExample Python script to read and print a single measurement.\n\n```python\nfrom time import sleep\n\nfrom sensirion_sps30 import SPS30\n\nport: str = "COM3"\nsps30 = SPS30(port)\n\nsps30.start_measurement()\nsleep(5)\n\ndata = sps30.read_values()\nprint(data)\n\nsps30.stop_measurement()\n```\n\n## Contributions\n\nCommunity contributions are a welcome addition to the project. \nBefore introducing any major features or changes to the existing API please consider opening an [issue](https://github.com/MMartin09/sensirion-sps30/issues) to outline your proposal.\n\nBug reports are also welcome on the [issue page](https://github.com/MMartin09/sensirion-sps30/issues).\n',
    'author': 'MMartin09',
    'author_email': 'mmartin09@outlook.at',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MMartin09/sensirion-sps30',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
