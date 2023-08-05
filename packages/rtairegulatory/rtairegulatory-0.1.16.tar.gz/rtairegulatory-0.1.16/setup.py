# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rtairegulatory']

package_data = \
{'': ['*']}

install_requires = \
['jupyter-book>=0.12.1,<0.13.0', 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['rtairegulatory = rtairegulatory.__main__:app']}

setup_kwargs = {
    'name': 'rtairegulatory',
    'version': '0.1.16',
    'description': "Radiotherapy AI's Regulatory Documentation Manager",
    'long_description': None,
    'author': 'Simon Biggs',
    'author_email': 'simon.biggs@radiotherapy.ai',
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
