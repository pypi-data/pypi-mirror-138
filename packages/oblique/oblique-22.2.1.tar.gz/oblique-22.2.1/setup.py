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
    'version': '22.2.1',
    'description': 'Show koans from Oblique Strategies',
    'long_description': '# Oblique Strategies for Python\n\nShows koans from [Oblique Strategies](https://en.wikipedia.org/wiki/Oblique_Strategies).\n\nYou can get the official [physical card set](https://www.enoshop.co.uk/product/oblique-strategies) as well.\n\n```\n❯ pip install oblique\n❯ python -m oblique --help\nUsage: python -m oblique [OPTIONS]\n\nOptions:\n  --edition TEXT   Which OS editions to include?  [default: 1,2,3,4]\n  --extra          Include additional koans found online  [default: False]\n  --python         Include Monty Python quotes  [default: False]\n  --count INTEGER  How many koans to show  [default: 3]\n  --help           Show this message and exit.\n\n❯ oblique\nFaced with a choice, do both (from Dieter Rot)\nDo something sudden, destructive and unpredictable\nMove towards the unimportant\n```\n\n## License\n\nCode is BSD-3 licensed. Koans attributed to Brian Eno and Peter Schmidt. ',
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
