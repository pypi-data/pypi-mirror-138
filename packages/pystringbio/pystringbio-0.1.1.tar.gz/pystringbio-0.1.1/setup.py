# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pystringbio', 'pystringbio.api', 'pystringbio.io', 'pystringbio.store']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6.2,<0.7.0',
 'fastapi>=0.65.1,<0.66.0',
 'marshmallow>=3.12.1,<4.0.0',
 'progressbar2>=3.53.1,<4.0.0',
 'prompt-toolkit>=3.0.18,<4.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'pyrediscore>=0.2.5,<0.3.0',
 'requests>=2.25.1,<3.0.0',
 'uvicorn>=0.13.4,<0.14.0']

entry_points = \
{'console_scripts': ['start = pystringbio.server:start']}

setup_kwargs = {
    'name': 'pystringbio',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'glaunay',
    'author_email': 'pitooon@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
