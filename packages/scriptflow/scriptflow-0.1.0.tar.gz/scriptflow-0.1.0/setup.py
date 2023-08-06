# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scriptflow']

package_data = \
{'': ['*']}

install_requires = \
['asyncssh>=2.9.0,<3.0.0',
 'click>=8.0.3,<9.0.0',
 'numpy>=1.22.2,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'rich>=11.0.0,<12.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['scriptflow = scriptflow.scriptflow_cli:hello']}

setup_kwargs = {
    'name': 'scriptflow',
    'version': '0.1.0',
    'description': 'Like a makefile but in python, a stripped-down system of Airflow or Luigi',
    'long_description': None,
    'author': 'Thibaut Lamadon',
    'author_email': 'thibaut.lamadon@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
