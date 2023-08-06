# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['macad']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['macad = macad.mac_changer:main']}

setup_kwargs = {
    'name': 'macad',
    'version': '1.0.0',
    'description': '"Change your system\'s mac-address"',
    'long_description': None,
    'author': 'Deepak Patidar',
    'author_email': 'info.deepakpatidar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
