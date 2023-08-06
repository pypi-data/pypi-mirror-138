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
['blockmatrix>=0.2.0,<0.3.0', 'numpy>=1.22.1,<2.0.0', 'scikit-learn>=1.0,<2.0']

extras_require = \
{'neuro': ['pandas>=1.4.0,<2.0.0',
           'mne>=0.24.1,<0.25.0',
           'moabb>=0.4.4,<0.5.0',
           'seaborn>=0.11.2,<0.12.0'],
 'solver': ['toeplitz==0.3.2']}

setup_kwargs = {
    'name': 'toeplitzlda',
    'version': '0.2.2',
    'description': 'Implementation of LDA using a block-Toeplitz structured covariance matrix for stationary spatiotemporal data.',
    'long_description': "# ToeplitzLDA\n\nCode for the ToeplitzLDA classifier proposed in [here](https://arxiv.org/abs/2202.02001).\nThe classifier conforms sklearn and can be used as a drop-in replacement for other LDA\nclassifiers. For usage refer to the learning from label proportions (LLP) example or the\nexample script.\n\nNote we used Ubuntu 20.04 with python3.8 to generate our results.\n\n## Getting Started / User Setup\n\nIf you only want to use this library, you can use the following setup. Note that this\nsetup is based on a fresh Ubuntu 20.04 installation.\n\n### Getting fresh ubuntu ready\n\n```bash\napt install python3-pip python3-venv\n```\n\n### Python package installation\n\nIn this setup, we assume you want to run the examples that actually make use of real EEG\ndata or the actual unsupervised speller replay. If you only want to employ `ToeplitzLDA`\nin your own spatiotemporal data / without `mne` and `moabb` then you can remove the\npackage extra `neuro`, i.e. `pip install toeplitzlda` or `pip install toeplitzlda[solver]`\n\n0. (Optional) Install fortran Compiler. On ubuntu: `apt install gfortran`\n1. Create virtual environment: `python3 -m venv toeplitzlda_venv`\n2. Activate virtual environment: `source toeplitzlda_venv/bin/activate`\n3. Update pip: `pip install --upgrade pip`\n4. Install numpy: `pip install numpy`\n5. Install toeplitzlda: `pip install toeplitzlda[neuro,solver]`, if you dont have a\n   fortran compiler: `pip install toeplitzlda[neuro]`\n\n### Check if everything works\n\nEither clone this repo or just download the `scripts/example_toeplitz_lda_bci_data.py`\nfile and run it: `python example_toeplitz_lda.py`. Note that this will automatically\ndownload EEG data with a size of around 650MB.\n\nAlternatively, you can use the `scripts/example_toeplitz_lda_generated_data.py` where\nartificial data is generated. Note however, that only stationary background noise is\nmodeled and no interfering artifacts as is the case in, e.g., real EEG data. As a result,\nthe 'overfit' effect of traditional slda on these artifacts is reduced.\n\n## Development Setup\n\nWe use a fortran compiler to provide speedups for solving block-Toeplitz linear equation\nsystems. If you are on ubuntu you can install `gfortran`.\n\nWe use `poetry` for dependency management. If you have it installed you can simply use\n`poetry install` to set up the virtual environment with all dependencies.\n\nIf setup does not work for you, please open an issue. We cannot guarantee support for many\ndifferent platforms, but could provide a singularity image.\n\n## Learning from label proportions\n\nUse the run_llp.py script to apply ToeplitzLDA in the LLP scenario and create results file\nthat can then be visualized using visualize_llp.py to create the plots shown in our\npublication. Note that the two datasets will be downloaded automatically and are\napproximately 16GB in size.\n\n## ERP benchmark\n\nThis is not yet available.\n\nNote this benchmark will take quite a long time if you do not have access to a computing\ncluster. The public datasets (including the LLP datasets) total a size of approximately\n120GB.\n\nBLOCKING TODO: How should we handle the private datasets?\n\n## FAQ\n\n### Why is my classification performance for my stationary spatiotemporal data really bad?\n\nCheck if your data is in _channel-prime_ order, i.e., in the flattened feature vector, you\nfirst enumerate over all channels (or some other spatially distributed sensors) for the\nfirst time point and then for the second time point and so on. If this is not the case,\ntell the classifier: e.g. `ToeplitzLDA(n_channels=16, data_is_channel_prime=False)`\n",
    'author': 'Jan Sosulski',
    'author_email': 'mail@jan-sosulski.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jsosulski/toeplitzlda',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
