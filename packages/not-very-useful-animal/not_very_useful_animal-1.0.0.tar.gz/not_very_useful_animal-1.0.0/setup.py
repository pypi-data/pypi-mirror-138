# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['not_very_useful_animal']

package_data = \
{'': ['*'], 'not_very_useful_animal': ['dist/*']}

setup_kwargs = {
    'name': 'not-very-useful-animal',
    'version': '1.0.0',
    'description': 'a not very useful animal',
    'long_description': None,
    'author': 'Fatemejahanni',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
