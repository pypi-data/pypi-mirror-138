# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['lambdo']
install_requires = \
['PyYAML>=6.0,<7.0', 'boto3>=1.20.52,<2.0.0', 'glob2>=0.7,<0.8']

entry_points = \
{'console_scripts': ['lambdo = lambdo:just_lambdo_it']}

setup_kwargs = {
    'name': 'lambdo',
    'version': '6.2.4',
    'description': 'Humor is the only test of gravity, and gravity of humor; for a subject which will not bear raillery is suspicious, and a jest which will not bear serious examination is false wit.',
    'long_description': None,
    'author': 'Jan van Hellemond',
    'author_email': 'jan@jvhellemond.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jvhellemond/lambdo',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
