# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xseis2']

package_data = \
{'': ['*'], 'xseis2': ['h5cpp/.git', 'include/gsl/*', 'include/xseis2/*']}

install_requires = \
['obspy>=1.2.2,<2.0.0', 'setuptools>=59.6.0,<60.0.0']

setup_kwargs = {
    'name': 'xseis2',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.11',
}
from setup import *
build(setup_kwargs)

setup(**setup_kwargs)
