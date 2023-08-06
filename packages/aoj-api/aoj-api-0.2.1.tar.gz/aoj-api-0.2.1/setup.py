# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aoj']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp',
 'beautifulsoup4',
 'optext-python==0.1.1',
 'requests',
 'selenium',
 'selext==0.2.1']

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
{'console_scripts': ['add-1-2 = package_1.__main__:main',
                     'sample-command = package_2.__main__:main'],
 'pseudo_package.plugin': ['sample-plugin = package_1.plugins:plugin_call']}

setup_kwargs = {
    'name': 'aoj-api',
    'version': '0.2.1',
    'description': 'This is a template for python projects.',
    'long_description': '# AOJ\n\nAOJ API for Python\n\n[![Python package](https://github.com/kagemeka/aoj/actions/workflows/python-package.yml/badge.svg)](https://github.com/kagemeka/aoj/actions/workflows/python-package.yml)\n[![CodeQL](https://github.com/kagemeka/aoj/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/kagemeka/aoj/actions/workflows/codeql-analysis.yml)\n[![Documentation Status](https://readthedocs.org/projects/aoj/badge/?version=latest)](https://aoj.readthedocs.io/en/latest/?badge=latest)\n[![PyPI version](https://badge.fury.io/py/aoj-api.svg)](https://badge.fury.io/py/aoj-api)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n',
    'author': 'Hiroshi Tsuyuki',
    'author_email': 'kagemeka1@gmail.com',
    'maintainer': 'Hiroshi Tsuyuki',
    'maintainer_email': 'kagemeka1@gmail.com',
    'url': 'https://github.com/kagemeka/aoj/#readme',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
