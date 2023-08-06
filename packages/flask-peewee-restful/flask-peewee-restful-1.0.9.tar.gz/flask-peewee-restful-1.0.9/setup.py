# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_peewee_restful']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.0.2,<3.0.0',
 'loguru>=0.5.3,<0.6.0',
 'peewee>=3.14.4,<4.0.0',
 'requests>=2.26.0,<3.0.0',
 'typing_extensions>=4.0.0,<5.0.0']

setup_kwargs = {
    'name': 'flask-peewee-restful',
    'version': '1.0.9',
    'description': 'Generate Flask Restful API from Peewee Models',
    'long_description': None,
    'author': 'Binh Vu',
    'author_email': 'binh@toan2.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
