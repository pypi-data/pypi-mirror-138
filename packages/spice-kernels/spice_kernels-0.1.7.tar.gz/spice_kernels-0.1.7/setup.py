# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spice_kernels']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=4.3,<5.0',
 'cmapy>=0.6,<0.7',
 'matplotlib>=3.4,<4.0',
 'numpy>=1.20,<2.0',
 'opencv-python>=4.5.3,<5.0.0',
 'scipy>=1.6,<2.0',
 'spiceypy>=4.0.2,<5.0.0']

entry_points = \
{'console_scripts': ['get_pointing = spice_kernels.spice_kernels:main']}

setup_kwargs = {
    'name': 'spice-kernels',
    'version': '0.1.7',
    'description': '',
    'long_description': None,
    'author': 'Steve Guest',
    'author_email': 'steve.guest@stfc.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://test.pypi.org/project/spice-kernels/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
