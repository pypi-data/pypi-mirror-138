# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['ipython_profile']
install_requires = \
['click>=8.0.3,<9.0.0',
 'ipython-autoimport>=0.3,<0.4',
 'ipython>=8.0.1,<9.0.0',
 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['ipython-profile = ipython_profile:run']}

setup_kwargs = {
    'name': 'ipython-profile',
    'version': '0.1.0',
    'description': 'An opinionated iPython profile for interactive development',
    'long_description': None,
    'author': 'Seva Zhidkov',
    'author_email': 'zhidkovseva@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
