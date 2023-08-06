# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['statute_matcher_regex', 'statute_matcher_regex.formula']

package_data = \
{'': ['*']}

install_requires = \
['statute-serial-number>=0.0.1,<0.0.2']

setup_kwargs = {
    'name': 'statute-matcher-regex',
    'version': '0.0.1',
    'description': 'Raw regex strings and constructors to create Philippine statutory labels.',
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
