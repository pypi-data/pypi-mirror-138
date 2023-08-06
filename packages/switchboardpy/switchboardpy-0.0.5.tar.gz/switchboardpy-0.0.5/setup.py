# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['switchboardpy']

package_data = \
{'': ['*']}

install_requires = \
['OSlash==0.6.3',
 'PyNaCl==1.4.0',
 'anchorpy==0.7.0',
 'anyio==3.4.0',
 'apischema==0.16.6',
 'attrs==21.2.0',
 'base58==2.1.1',
 'borsh-construct==0.1.0',
 'cachetools==4.2.4',
 'certifi==2021.10.8',
 'cffi==1.15.0',
 'charset-normalizer==2.0.9',
 'construct-typing==0.5.2',
 'construct==2.10.67',
 'h11==0.12.0',
 'httpcore==0.13.7',
 'httpx==0.18.2',
 'idna==3.3',
 'inflection==0.5.1',
 'iniconfig==1.1.1',
 'jsonrpcclient==4.0.2',
 'jsonrpcserver==5.0.5',
 'jsonschema==3.2.0',
 'more-itertools==8.12.0',
 'packaging==21.3',
 'pluggy==1.0.0',
 'protobuf>=3.5.0.post1',
 'psutil==5.8.0',
 'py==1.11.0',
 'pycparser==2.21',
 'pyparsing==3.0.6',
 'pyrsistent==0.18.0',
 'requests==2.26.0',
 'rfc3986==1.5.0',
 'six==1.16.0',
 'sniffio==1.2.0',
 'solana==0.21.0',
 'sumtypes==0.1a6',
 'toml==0.10.2',
 'toolz==0.11.2',
 'types-cachetools==4.2.6',
 'typing-extensions==3.10.0.2',
 'urllib3==1.26.7',
 'websockets==10.1',
 'zstandard==0.16.0']

setup_kwargs = {
    'name': 'switchboardpy',
    'version': '0.0.5',
    'description': 'Switchboard V2 API',
    'long_description': None,
    'author': 'Albert Hermida',
    'author_email': 'albert@switchboard.xyz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/switchboard-xyz/switchboardv2-py-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
