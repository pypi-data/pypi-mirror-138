# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lol_id_tools']

package_data = \
{'': ['*'], 'lol_id_tools': ['local_data/*']}

install_requires = \
['rapidfuzz>=2.0.2,<3.0.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'lol-id-tools',
    'version': '1.8.0',
    'description': '',
    'long_description': None,
    'author': 'mrtolkien',
    'author_email': 'gary.mialaret@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
