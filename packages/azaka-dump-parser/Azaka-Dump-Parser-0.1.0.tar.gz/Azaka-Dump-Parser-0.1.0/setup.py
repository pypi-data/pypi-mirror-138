# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['azaka_dump_parser']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'azaka-dump-parser',
    'version': '0.1.0',
    'description': 'A dump parser utility for VNDB, made for Azaka.',
    'long_description': '# Azaka-Dump-Parser\nA dump parser utility for VNDB.\n',
    'author': 'mooncell07',
    'author_email': 'mooncell07@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
