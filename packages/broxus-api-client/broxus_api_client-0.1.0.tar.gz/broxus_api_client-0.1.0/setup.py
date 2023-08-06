# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['broxus_api_client',
 'broxus_api_client.explorer',
 'broxus_api_client.token_indexer']

package_data = \
{'': ['*']}

install_requires = \
['httpx[http2]>=0.22.0,<0.23.0',
 'pydantic>=1.9.0,<2.0.0',
 'ujson>=5.1.0,<6.0.0']

setup_kwargs = {
    'name': 'broxus-api-client',
    'version': '0.1.0',
    'description': 'Set of API clients for Broxus APIs in Everscale',
    'long_description': '# Set of API clients for Broxus APIs in Everscale\n\n[![PyPI version shields.io](https://img.shields.io/pypi/v/broxus_api_client.svg)](https://pypi.python.org/pypi/broxus_api_client/)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/broxus_api_client.svg)](https://pypi.python.org/pypi/broxus_api_client/)\n[![PyPI license](https://img.shields.io/pypi/l/broxus_api_client.svg)](https://pypi.python.org/pypi/broxus_api_client/)\n\nAll models and requests automatically generated from Broxus swagger schemas:\n\n* Token indexer - http://token-indexer.broxus.com/v1/swagger.yaml\n* Explorer - https://explorer-api.broxus.com/v1/swagger.yaml\n\n## LICENSE\n\nThis project is licensed under the terms of the [MIT](https://github.com/MIREX/broxus_api_client/blob/master/LICENSE)\nlicense.',
    'author': 'MIREX',
    'author_email': 'lifincevkirill@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MIREX/broxus_api_client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
