# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nib_save_wrapper']

package_data = \
{'': ['*']}

install_requires = \
['nibabel>=3.2.2,<4.0.0', 'numpy>=1.22.2,<2.0.0']

setup_kwargs = {
    'name': 'nib-save-wrapper',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Joshua Teves',
    'author_email': 'joshua.teves@nih.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
