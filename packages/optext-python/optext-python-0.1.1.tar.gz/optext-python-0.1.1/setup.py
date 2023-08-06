# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['optext']

package_data = \
{'': ['*']}

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
    'name': 'optext-python',
    'version': '0.1.1',
    'description': 'Extension of Optional type inspired by Rust Option<T>.',
    'long_description': "# Optext\n\n[![Python package](https://github.com/kagemeka/optext/actions/workflows/python-package.yml/badge.svg)](https://github.com/kagemeka/optext/actions/workflows/python-package.yml)\n[![readthedocs build status](https://readthedocs.org/projects/optext/badge/?version=latest)](https://optext.readthedocs.io/en/latest/?badge=latest)\n[![PyPI version](https://badge.fury.io/py/optext.svg)](https://badge.fury.io/py/optext)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\n\n[`Optext`'s documentation](https://optext.readthedocs.io/)\n---\n",
    'author': 'Hiroshi Tsuyuki',
    'author_email': 'kagemeka1@gmail.com',
    'maintainer': 'Hiroshi Tsuyuki',
    'maintainer_email': 'kagemeka1@gmail.com',
    'url': 'https://github.com/kagemeka/optext',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
