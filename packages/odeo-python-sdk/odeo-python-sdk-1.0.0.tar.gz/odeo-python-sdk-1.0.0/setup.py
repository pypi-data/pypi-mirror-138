# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['odeo', 'odeo.models', 'odeo.services']

package_data = \
{'': ['*']}

install_requires = \
['requests-oauthlib>=1.3.0,<2.0.0', 'requests>=2.27.1,<3.0.0']

extras_require = \
{'docs': ['Sphinx>=4.4.0,<5.0.0', 'sphinx-rtd-theme>=1.0.0,<2.0.0']}

setup_kwargs = {
    'name': 'odeo-python-sdk',
    'version': '1.0.0',
    'description': 'Python library for Odeo For Business API',
    'long_description': '# Odeo Python SDK\n\n[![PyPI version](https://badge.fury.io/py/odeo-python-sdk.svg)](https://pypi.org/project/odeo-python-sdk)\n[![Documentation Status](https://readthedocs.org/projects/odeo-python-sdk/badge/?version=latest)](https://odeo-python-sdk.readthedocs.io/en/latest/?badge=latest)\n[![PyPI - License](https://img.shields.io/pypi/l/odeo-python-sdk)](https://opensource.org/licenses/MIT)\n\nPython library for calling Odeo For Business API, such as _Disbursement_, _Payment Gateway_, _Cash_, and _Sub Users_\nservices.\n\n## Installation\n\nThe SDK currently supports Python 3.9 and later.\n\nTo use Odeo Python SDK, install the latest version with `pip`:\n\n```shell\npip install odeo-python-sdk\n```\n\n## Documentation\n\nFor more detailed guides of how to use and set up the SDK please go to https://odeo-python-sdk.readthedocs.io',
    'author': 'Rudi',
    'author_email': 'rudi@odeo.co.id',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://docs.odeo.co.id',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
