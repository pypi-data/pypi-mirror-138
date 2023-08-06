# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyrinth',
 'pyrinth.internal',
 'pyrinth.model',
 'pyrinth.model.v1',
 'pyrinth.model.v2']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'pyrinth',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'ENDERZOMBI102',
    'author_email': 'enderzombi102.end@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
