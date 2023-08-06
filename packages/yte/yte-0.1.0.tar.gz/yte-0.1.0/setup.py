# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yte']

package_data = \
{'': ['*']}

install_requires = \
['plac>=1.3.4,<2.0.0', 'pyyaml>=6.0,<7.0']

entry_points = \
{'console_scripts': ['yte = yte:main']}

setup_kwargs = {
    'name': 'yte',
    'version': '0.1.0',
    'description': 'A YAML template engine with Python expressions',
    'long_description': None,
    'author': 'Johannes Köster',
    'author_email': 'johannes.koester@tu-dortmund.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
