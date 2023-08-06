# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cosmoplots']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cosmoplots',
    'version': '0.1.2',
    'description': 'Routines to get a sane default configuration for production quality plots.',
    'long_description': '# cosmoplots\nRoutines to get a sane default configuration for production quality plots. Used by complex systems modelling group at UiT.\n\n# Installation\n```\npip install cosmoplots\n```\n# Use\nSet your `rcparams` before plotting in your code, for example:\n```Python\nimport cosmoplots\n\naxes_size = cosmoplots.set_rcparams_aip(plt.rcParams, num_cols=1, ls="thin")\n```\n\n## `change_log_axis_base`\n\n```python\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport cosmoplots\n\naxes_size = cosmoplots.set_rcparams_aip(plt.rcParams, num_cols=1, ls="thin")\na = np.exp(np.linspace(-3, 5, 100))\n# 1 --- Semilogx\nfig = plt.figure()\nax = fig.add_axes(axes_size)\nbase = 2  # Default is 10, but 2 works equally well\ncosmoplots.change_log_axis_base(ax, "x", base=base)\n# Do plotting ...\n# If you use "plot", the change_log_axis_base can be called at the top (along with add_axes\n# etc.), but using loglog, semilogx, semilogy will re-set, and the change_log_axis_base\n# function must be called again.\nax.plot(a)\nplt.show()\n\n# 2 --- Semilogy\nfig = plt.figure()\nax = fig.add_axes(axes_size)\ncosmoplots.change_log_axis_base(ax, "y")\n# Do plotting ...\n# If you use "plot", the change_log_axis_base can be called at the top (along with add_axes\n# etc.), but using loglog, semilogx, semilogy will re-set, and the change_log_axis_base\n# function must be called again.\nax.semilogy(a)\ncosmoplots.change_log_axis_base(ax, "y")  # Commenting out this result in the default base10 ticks\nplt.show()\n```\n\n',
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
