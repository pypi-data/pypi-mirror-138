# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['superturtle', 'superturtle.documentation.source']

package_data = \
{'': ['*'],
 'superturtle': ['documentation/*',
                 'documentation/build/doctrees/*',
                 'documentation/build/html/*',
                 'documentation/build/html/_modules/*',
                 'documentation/build/html/_sources/*',
                 'documentation/build/html/_static/*']}

setup_kwargs = {
    'name': 'superturtle',
    'version': '0.0.1',
    'description': "Extensions to Python's turtle",
    'long_description': None,
    'author': 'Chris Proctor',
    'author_email': 'chris@chrisproctor.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
