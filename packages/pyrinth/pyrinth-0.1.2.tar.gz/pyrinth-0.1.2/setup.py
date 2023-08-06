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
    'version': '0.1.2',
    'description': '',
    'long_description': "PyRinth\n-\nA library to interact with modrinth's v1 and v2 APIs\n\nFeatures:\n - Compatible with both v1 and v2 APIs\n - Automatic request caching and refreshing with configurable interval\n - Lazy population of objects to minimize API calls\n\n[Documentation](https://enderzombi102.gitlab.io/pyrinth)\n\n### Installing\nFrom PyPi\n```bash\n$ pip install pyrinth\n```\nFrom source\n```bash\n$ pip install git+https://gitlab.com/ENDERZOMBI102/pyrinth.git\n```\n",
    'author': 'ENDERZOMBI102',
    'author_email': 'enderzombi102.end@gmail.com',
    'maintainer': 'ENDERZOMBI102',
    'maintainer_email': 'enderzombi102.end@gmail.com',
    'url': 'https://gitlab.com/ENDERZOMBI102/pyrinth',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
