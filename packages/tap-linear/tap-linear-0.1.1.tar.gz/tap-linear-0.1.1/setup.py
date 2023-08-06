# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_linear', 'tap_linear.queries', 'tap_linear.schemas', 'tap_linear.tests']

package_data = \
{'': ['*']}

install_requires = \
['black>=21.9b0,<22.0', 'requests>=2.25.1,<3.0.0', 'singer-sdk>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['tap-linear = tap_linear.tap:TapLinear.cli']}

setup_kwargs = {
    'name': 'tap-linear',
    'version': '0.1.1',
    'description': '`tap-linear` is a Singer tap for Linear, built with the Meltano SDK for Singer Taps.',
    'long_description': None,
    'author': 'Harisaran G',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<3.11',
}


setup(**setup_kwargs)
