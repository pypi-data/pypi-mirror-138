# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cosmoplots']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cosmoplots',
    'version': '0.1.0',
    'description': 'Routines to get a sane default configuration for production quality plots.',
    'long_description': '# cosmoplots\nRoutines to get a sane default configuration for production quality plots. Used by complex systems modelling group at UiT.\n\n# Use\nSet your `rcparams` before plotting in your code, for example:\n```Python\nfrom cosmoplots import figure_defs\n\naxes_size = figure_defs.set_rcparams_aip(plt.rcParams, num_cols=1, ls="thin")\n```',
    'author': 'gregordecristoforo',
    'author_email': 'gregor.decristoforo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/uit-cosmo/cosmoplots',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
