# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sinian_test']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sinian-test',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'ph.yu',
    'author_email': 'sinian.yu@tuya.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
