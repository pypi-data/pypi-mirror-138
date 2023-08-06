# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['odeo', 'odeo.models', 'odeo.services']

package_data = \
{'': ['*']}

install_requires = \
['requests-oauthlib>=1.3.0,<2.0.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'odeo-python-sdk',
    'version': '0.0.1',
    'description': 'Python library for Odeo For Business API',
    'long_description': '# Odeo Python SDK\n\nPython library for calling Odeo For Business API with [Requests](https://docs.python-requests.org/en/latest/).',
    'author': 'Rudi',
    'author_email': 'rudi@odeo.co.id',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://docs.odeo.co.id',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
