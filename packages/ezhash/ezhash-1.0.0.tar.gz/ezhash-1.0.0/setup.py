# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ezhash']

package_data = \
{'': ['*']}

install_requires = \
['tqdm>=4.62.3,<5.0.0', 'typer[all]>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['ezh = ezhash.main:app']}

setup_kwargs = {
    'name': 'ezhash',
    'version': '1.0.0',
    'description': 'CLI tool which computes and compares file hash.',
    'long_description': '# EzHash\nCLI tool which computes and compares file hash.\n\n## Usage\n\nBasic:\n```\nezh sha256 ~/Downloads/image.iso \n```\n\nWith comparison:\n```\nezh sha256 ~/Downloads/image.iso 85dcd0455f6bb643c4ddd819a0b0c4737d850f6df3b9ec2686bc6b7cd71791f7\n```\n',
    'author': 'Naffah Abdulla Rasheed',
    'author_email': 'mail@naffah.me',
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
