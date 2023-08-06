# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['my_stocks']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.1,<4.0.0',
 'numpy>=1.22.2,<2.0.0',
 'pandas>=1.4.1,<2.0.0',
 'prompt-toolkit>=3.0.28,<4.0.0',
 'typer>=0.4.0,<0.5.0',
 'yfinance>=0.1.70,<0.2.0']

entry_points = \
{'console_scripts': ['my-stocks = my_stocks.main:app']}

setup_kwargs = {
    'name': 'my-stocks',
    'version': '0.1.3',
    'description': 'Easy way to access financial data in .csv format and make historical data plot',
    'long_description': '# Analyze financial data quick and easy via CLI\n\nRun my-stock --help to get all available options\n\n`get-stock-data`: Get historical data for a stock of your choice\n\n`get-dividends`: Get historical dividend data for a stock of your choice\n',
    'author': 'markus',
    'author_email': 'datamastery87@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
