# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['restfy', 'restfy.http']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'restfy',
    'version': '0.1.0',
    'description': 'A small rest framework',
    'long_description': None,
    'author': 'Manasses Lima',
    'author_email': 'manasseslima@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
