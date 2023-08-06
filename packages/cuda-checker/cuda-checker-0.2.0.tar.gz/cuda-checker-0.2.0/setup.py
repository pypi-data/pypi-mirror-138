# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cuda_checker']

package_data = \
{'': ['*']}

install_requires = \
['tensorflow', 'torch']

extras_require = \
{'docs': ['furo',
          'myst-parser',
          'pdoc3',
          'pydata-sphinx-theme',
          'python-docs-theme',
          'sphinx',
          'sphinx-book-theme',
          'sphinx-theme-pd',
          'sphinx_rtd_theme<=2.0.0',
          'sphinxcontrib-mermaid']}

entry_points = \
{'console_scripts': ['cuda-checker = cuda_checker.cli:check']}

setup_kwargs = {
    'name': 'cuda-checker',
    'version': '0.2.0',
    'description': 'NVIDIA CUDA checker for pythonn deeplearning project.',
    'long_description': "# Cuda Checker\n\n[![Python package](https://github.com/kagemeka/cuda-checker/actions/workflows/python-package.yml/badge.svg)](https://github.com/kagemeka/cuda-checker/actions/workflows/python-package.yml)\n[![readthedocs build status](https://readthedocs.org/projects/cuda-checker/badge/?version=latest)](https://cuda-checker.readthedocs.io/en/latest/?badge=latest)\n[![PyPI version](https://badge.fury.io/py/cuda-checker.svg)](https://badge.fury.io/py/cuda-checker)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\n[`Cuda Checker`'s documentation](https://cuda-checker.readthedocs.io/)\n---\n",
    'author': 'Hiroshi Tsuyuki',
    'author_email': 'kagemeka1@gmail.com',
    'maintainer': 'Hiroshi Tsuyuki',
    'maintainer_email': 'kagemeka1@gmail.com',
    'url': 'https://github.com/kagemeka/cuda-checker#readme',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
