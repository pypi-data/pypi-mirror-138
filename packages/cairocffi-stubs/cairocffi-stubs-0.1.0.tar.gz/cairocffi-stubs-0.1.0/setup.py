# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cairocffi-stubs']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cairocffi-stubs',
    'version': '0.1.0',
    'description': 'Stubs for cairocffi. ',
    'long_description': None,
    'author': '忘忧北萱草',
    'author_email': 'wybxc@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
