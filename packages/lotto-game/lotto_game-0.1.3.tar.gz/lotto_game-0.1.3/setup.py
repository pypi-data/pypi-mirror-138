# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lotto_game']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'lotto-game',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'czasoprzestrzenny',
    'author_email': 'jaroslawold@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/czasoprzestrzenny/lotto_game',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
