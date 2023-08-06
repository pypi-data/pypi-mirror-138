# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['filesystem', 'filesystem.fmt']

package_data = \
{'': ['*']}

install_requires = \
['PyExcelerate',
 'PyYAML',
 'XlsxWriter',
 'chardet',
 'h5py',
 'iniconfig',
 'openpyxl',
 'optext-python==0.1.1',
 'toml',
 'untangle',
 'xlrd==1.2.0',
 'xmltodict']

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

setup_kwargs = {
    'name': 'filesystem-python',
    'version': '0.2.0',
    'description': 'FileSystem for Python',
    'long_description': '# Filesystem Python\n\n[![Python package](https://github.com/kagemeka/filesystem-python/actions/workflows/python-package.yml/badge.svg)](https://github.com/kagemeka/filesystem-python/actions/workflows/python-package.yml)\n[![Documentation Status](https://readthedocs.org/projects/filesystem-python/badge/?version=latest)](https://filesystem-python.readthedocs.io/en/latest/?badge=latest)\n[![PyPI version](https://badge.fury.io/py/filesystem-python.svg)](https://badge.fury.io/py/filesystem-python)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n',
    'author': 'Hiroshi Tsuyuki',
    'author_email': 'kagemeka1@gmail.com',
    'maintainer': 'Hiroshi Tsuyuki',
    'maintainer_email': 'kagemeka1@gmail.com',
    'url': 'https://github.com/kagemeka/filesystem-python/#readme',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
