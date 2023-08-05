# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['helm_upgrade']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML==6.0', 'bs4==0.0.1', 'numpy==1.22.2', 'requests==2.27.1']

entry_points = \
{'console_scripts': ['helm-upgrade = helm_upgrade.cli:main']}

setup_kwargs = {
    'name': 'helm-upgrade',
    'version': '0.1.0',
    'description': 'A Python CLI to manage Helm Chart dependencies',
    'long_description': None,
    'author': 'Sarah Gibson',
    'author_email': 'drsarahlgibson@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
