# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ftfy', 'ftfy.bad_codecs']

package_data = \
{'': ['*']}

install_requires = \
['wcwidth>=0.2.5']

entry_points = \
{'console_scripts': ['ftfy = ftfy.cli:main']}

setup_kwargs = {
    'name': 'ftfy',
    'version': '6.1.0',
    'description': 'Fixes mojibake and other problems with Unicode, after the fact',
    'long_description': None,
    'author': 'Robyn Speer',
    'author_email': 'rspeer@arborelia.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
