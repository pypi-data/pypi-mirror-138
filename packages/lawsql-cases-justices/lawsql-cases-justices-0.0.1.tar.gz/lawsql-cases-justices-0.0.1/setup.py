# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lawsql_cases_justices']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'Unidecode>=1.2.0,<2.0.0',
 'httpx>=0.22.0,<0.23.0',
 'lawsql_utils>=0.0.1,<0.0.2',
 'python-dotenv>=0.19.2,<0.20.0',
 'sqlite-utils>=3.22,<4.0']

setup_kwargs = {
    'name': 'lawsql-cases-justices',
    'version': '0.0.1',
    'description': 'Get justices from yaml file; updates local database.',
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
