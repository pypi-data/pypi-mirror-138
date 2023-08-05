# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blockmatrix']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.1,<4.0.0', 'seaborn>=0.11.2,<0.12.0', 'vg>=2.0.0,<3.0.0']

extras_require = \
{'channels': ['mne>=0.24.1,<0.25.0'], 'solver': ['toeplitz>=0.3.2,<0.4.0']}

setup_kwargs = {
    'name': 'blockmatrix',
    'version': '0.2.0',
    'description': 'Utilities to handle blockmatrices, especially covariance matrices.',
    'long_description': None,
    'author': 'Jan Sosulski',
    'author_email': 'mail@jan-sosulski.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
