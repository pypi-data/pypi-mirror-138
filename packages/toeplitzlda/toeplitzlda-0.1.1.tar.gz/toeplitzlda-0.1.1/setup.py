# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['toeplitzlda',
 'toeplitzlda.benchmark',
 'toeplitzlda.classification',
 'toeplitzlda.usup_replay']

package_data = \
{'': ['*']}

install_requires = \
['blockmatrix>=0.1.0,<0.2.0',
 'mne>=0.24.1,<0.25.0',
 'moabb>=0.4.4,<0.5.0',
 'numpy>=1.22.1,<2.0.0',
 'pandas>=1.4.0,<2.0.0',
 'scikit-learn>=1.0,<2.0']

extras_require = \
{'solver': ['toeplitz>=0.3.2,<0.4.0']}

setup_kwargs = {
    'name': 'toeplitzlda',
    'version': '0.1.1',
    'description': 'Implementation of LDA using a block-Toeplitz structured covariance matrix for stationary spatiotemporal data.',
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
