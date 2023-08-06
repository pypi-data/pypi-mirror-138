# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lawsql_utils',
 'lawsql_utils.files',
 'lawsql_utils.general',
 'lawsql_utils.html',
 'lawsql_utils.trees']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'arrow>=1.2,<2.0',
 'beautifulsoup4>=4.10.0,<5.0.0',
 'html5lib>=1.1,<2.0',
 'markdown2>=2.4.0,<3.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'python-dotenv>=0.19.2,<0.20.0',
 'types-PyYAML>=6.0,<7.0',
 'types-python-dateutil>=2.8.0,<3.0.0']

setup_kwargs = {
    'name': 'lawsql-utils',
    'version': '0.0.1',
    'description': 'lawsql helper functions',
    'long_description': 'None',
    'author': 'Marcelino G. Veloso III',
    'author_email': 'mars@veloso.one',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
