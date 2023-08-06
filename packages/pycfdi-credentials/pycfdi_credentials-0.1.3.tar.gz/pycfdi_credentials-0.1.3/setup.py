# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycfdi_credentials']

package_data = \
{'': ['*']}

install_requires = \
['pyOpenSSL>=22.0.0,<23.0.0']

setup_kwargs = {
    'name': 'pycfdi-credentials',
    'version': '0.1.3',
    'description': 'Library to manage CSD and FIEL files from SAT. Use this to sign, verify and get certificate data.',
    'long_description': None,
    'author': 'Moises Navarro',
    'author_email': 'moisalejandro@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
