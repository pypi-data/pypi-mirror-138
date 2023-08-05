# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyrigami', 'pyrigami.engraver', 'pyrigami.units']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9,<2.0', 'qahirah>=1.1,<2.0']

setup_kwargs = {
    'name': 'pyrigami',
    'version': '0.1.0',
    'description': 'A library to draw declaratively on PDF/SVG/PNG.',
    'long_description': '# pyrigami\n\nA library to draw declaratively on PDF/SVG/PNG.\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n\n',
    'author': 'Ananth P',
    'author_email': 'ananth.pattabiraman@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/ananthp/pyrigami',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
