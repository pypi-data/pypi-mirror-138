# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oblique']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0']

entry_points = \
{'console_scripts': ['oblique = oblique:main']}

setup_kwargs = {
    'name': 'oblique',
    'version': '22.2.0',
    'description': 'Show koans from Oblique Strategies',
    'long_description': None,
    'author': 'Łukasz Langa',
    'author_email': 'lukasz@langa.pl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ambv/oblique',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
