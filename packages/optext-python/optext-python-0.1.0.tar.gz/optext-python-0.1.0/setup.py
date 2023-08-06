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
    'version': '0.1.0',
    'description': 'Extension of Optional type inspired by Rust Option<T>.',
    'long_description': "# Optext\n\n\n## CI/CD\n[![Python package](https://github.com/kagemeka/optext/actions/workflows/python-package.yml/badge.svg)](https://github.com/kagemeka/optext/actions/workflows/python-package.yml)\n[![readthedocs build status](https://readthedocs.org/projects/python-project-templates/badge/?version=latest)](https://python-project-templates.readthedocs.io/en/latest/?badge=latest)\n\n[`Optext`'s documentation](https://python-project-templates.readthedocs.io/)\n---\n\n## publish package to Pypi\n[![PyPI version](https://badge.fury.io/py/optext.svg)](https://badge.fury.io/py/optext)\n\n\n## license\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n",
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
