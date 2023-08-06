# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cyberpunk', 'cyberpunk.storage', 'cyberpunk.transformations']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.0.2,<3.0.0',
 'PyYAML>=6.0,<7.0',
 'boto3>=1.20.54,<2.0.0',
 'gunicorn>=20.1.0,<21.0.0',
 'pydub>=0.25.1,<0.26.0',
 'python-dotenv>=0.19.2,<0.20.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'cyberpunk',
    'version': '0.1.0',
    'description': 'Audio Processing Server',
    'long_description': None,
    'author': 'Johannes Naylor',
    'author_email': 'jonaylor89@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
