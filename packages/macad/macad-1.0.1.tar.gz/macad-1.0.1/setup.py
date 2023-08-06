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
    'version': '1.0.1',
    'description': 'The Tool For Changing Your MAC Address for Any Interface',
    'long_description': '# Macad\nThe Tool For Changing Your MAC Address for Any Interface\n\nTo install this package, use\n\n```bash\nsudo pip install macad\n```\n> Note: `this library requires root privileges, you need to use sudo`\n\n## RUN\n\nWant to contribute? Great!\n\nOpen your favorite Terminal and run these commands.\n\nSee All Arguments and Options for more information:\n\n```sh\nsudo macad -h\n```\n\nFind your interface and put cammand\n\n```sh\nsudo macad -i <interface> -m <new mac address>\nOR \nsudo macad --interface <interface> --mac <new mac address>\n```\n\nExample:\n\n```sh\nsudo macad -i wp2s1 -m 00:11:22:33:44:55\n```\n> Note: `sometimes assigned mac not be available so for that start mac from 00:XX:XX:XX:XX:XX`\n\nThe output  look like this\n\n```sh\n[+] MAC Address was Successfully Changed to 00:XX:XX:XX:XX:XX\n\n```\n\n## License\n\nMIT\n\n**Free Software, Hell Yeah!**\n\n## Author\n\n[Deepak Patidar](https://github.com/DeepakDarkiee/great-text)',
    'author': 'Deepak Patidar',
    'author_email': 'info.deepakpatidar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DeepakDarkiee/macad.git',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6.0',
}


setup(**setup_kwargs)
