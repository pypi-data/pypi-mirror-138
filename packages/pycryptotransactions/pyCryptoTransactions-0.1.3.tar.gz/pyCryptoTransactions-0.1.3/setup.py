# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyCryptoTransactions',
 'pyCryptoTransactions.exchanges',
 'pyCryptoTransactions.exchanges.binance',
 'pyCryptoTransactions.exchanges.coinbase',
 'pyCryptoTransactions.exchanges.coinbase.coinbaseApiWrapper.coinbase',
 'pyCryptoTransactions.exporters',
 'pyCryptoTransactions.manual',
 'pyCryptoTransactions.networks',
 'pyCryptoTransactions.networks.binanceChain',
 'pyCryptoTransactions.networks.bitcoin',
 'pyCryptoTransactions.networks.bitcoin.Archive',
 'pyCryptoTransactions.networks.bsc',
 'pyCryptoTransactions.networks.cosmos',
 'pyCryptoTransactions.networks.eth',
 'pyCryptoTransactions.networks.iota',
 'pyCryptoTransactions.networks.litecoin',
 'pyCryptoTransactions.networks.osmos',
 'pyCryptoTransactions.networks.persistence',
 'pyCryptoTransactions.networks.thorchain']

package_data = \
{'': ['*'], 'pyCryptoTransactions.exchanges.coinbase': ['coinbaseApiWrapper/*']}

install_requires = \
['blockcypher>=1.0.93,<2.0.0',
 'pandas>=1.4.0,<2.0.0',
 'pycoin>=0.91.20210515,<0.92.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'pycryptotransactions',
    'version': '0.1.3',
    'description': 'Python Package to query crpyto transactions from various blockchains and exchanges through public APIs',
    'long_description': '# py-Crypto-Transactions\n\n[![PyPI](https://badge.fury.io/py/pycryptotransactions.svg)](https://badge.fury.io/py/pycryptotransactions)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/pycryptotransactions)\n![GitHub](https://img.shields.io/github/license/pcko1/pycryptotransactions)\n[![Python 3.8](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-310/)\n![GitHub Issues](https://img.shields.io/github/issues/jensb89/py-Crypto-Transactions)\n\n\nA python package to query crypto transaction from various blockchains and exchanges\nto build your own portfolio app!\n\npyCryptoTransactions also supports a few exporters, such that data can be imported e.g. at Koinly or Accointing.\n\nNote: Very elary alpha version!\n\n## Install\nUse pip:\n * pip install pyCryptoTransactions (NOTE: make sure to use camelCase name like this and not pycryptotransactions)\nOr use poetry \nOr install directly by cloning the git repo\n## Supported Blockchains\n * Bitcoin\n * Litecoin\n * Cosmos\n * Thorchain\n * Osmos\n * Iota\n * Persistence\n * Ethereum (soon)\n * Bsc (soon)\n\n## Supported exchanges\n * Binance (support for exported CSVs, no API yet)\n * Coinbase (Oauth Api)\n * Coinbase Pro (soon)\n\n## Examples\n```\nt = LitecoinImport("xpub...")\nt.getTransactions()`\n```\n\n```\nt = CosmosChain("cosmos....")\ntxs = t.getTransactions()\nprint(txs)\ndf = txs.toPandasDataframe()\ndf.to_csv("atom_test.csv")\nprint(txs.calculateBalance())\na = AccointingExporter(txs)\na.exportToExcel("atom_accointing.xlsx")\n```',
    'author': 'Jens Brauer',
    'author_email': 'jensb89@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jensb89/py-Crypto-Transactions',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
