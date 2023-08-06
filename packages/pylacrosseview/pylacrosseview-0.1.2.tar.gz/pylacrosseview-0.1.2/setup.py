# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylacrosseview']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'pylacrosseview',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'regulad',
    'author_email': 'regulad@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
