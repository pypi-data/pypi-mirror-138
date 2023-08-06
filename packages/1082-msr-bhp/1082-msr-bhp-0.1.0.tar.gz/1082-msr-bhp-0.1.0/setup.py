# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['1082_msr_bhp']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0']

setup_kwargs = {
    'name': '1082-msr-bhp',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Lucas Selfslagh',
    'author_email': 'lucas.selfslagh@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
