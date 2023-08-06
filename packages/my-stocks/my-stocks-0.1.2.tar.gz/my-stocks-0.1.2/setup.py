# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['my_stocks']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.1,<4.0.0', 'typer>=0.4.0,<0.5.0', 'yfinance>=0.1.70,<0.2.0']

entry_points = \
{'console_scripts': ['my-stocks = my_stocks.main:app']}

setup_kwargs = {
    'name': 'my-stocks',
    'version': '0.1.2',
    'description': 'Easy way to access financial data in .csv format and make historical data plot',
    'long_description': '# Analyze financial data quick and easy with via CLI\n\n### Run my-stock --help to get all available options\n',
    'author': 'markus',
    'author_email': 'datamastery87@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
