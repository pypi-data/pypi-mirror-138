# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypgstac']

package_data = \
{'': ['*'], 'pypgstac': ['migrations/*']}

install_requires = \
['asyncpg>=0.25.0,<0.26.0',
 'orjson>=3.5.2',
 'python-dateutil>=2.8.2,<3.0.0',
 'smart-open>=4.2.0,<5.0.0',
 'typer>=0.4.0']

entry_points = \
{'console_scripts': ['pypgstac = pypgstac.pypgstac:app']}

setup_kwargs = {
    'name': 'pypgstac',
    'version': '0.4.5',
    'description': '',
    'long_description': 'Python tools for working with PGStac\n',
    'author': 'David Bitner',
    'author_email': 'bitner@dbspatial.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stac-utils/pgstac',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
