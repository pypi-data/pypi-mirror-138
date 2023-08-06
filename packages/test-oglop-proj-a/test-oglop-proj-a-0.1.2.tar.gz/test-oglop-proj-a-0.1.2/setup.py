# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['test_oglop_proj_a']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'test-oglop-proj-a',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Jan Gazda',
    'author_email': '7480694+1oglop1@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
