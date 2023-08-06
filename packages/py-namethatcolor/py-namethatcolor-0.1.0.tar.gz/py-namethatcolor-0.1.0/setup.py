# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['py_namethatcolor']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'py-namethatcolor',
    'version': '0.1.0',
    'description': 'A small tool to get the closest known color to any given one and also generates its general shade (like Blue, Red, Black, etc)',
    'long_description': 'py-namethatcolor\n================\n\n\nAbout\n-----\n\nThe script allows to get the closest known color to any given one and also generates its general shade (like Blue, Red, Black, etc)\n\n.. code ::\n\n    >>> from py_namethatcolor import get_color\n    >>> color = get_color("#336699")\n    >>> color.name\n    \'Lochmara\'\n    >>> color.shade.name\n    \'Blue\'\n\n\nCredits\n-------\n\nIt\'s a Python port of the "`Name that Color <https://chir.ag/projects/name-that-color/#6195ED>`_"\nscript that was originally written by Chirag Mehta and also its improved\nversion developed for "`Color Name & Hue <https://www.color-blindness.com/color-name-hue/>`_"\nby Daniel Flueck\n',
    'author': 'Mikhail Porokhovnichenko',
    'author_email': 'marazmiki@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/marazmiki/py-namethatcolor',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
