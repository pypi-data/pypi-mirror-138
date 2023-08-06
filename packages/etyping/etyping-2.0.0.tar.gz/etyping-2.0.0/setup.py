# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['etyping']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML', 'selenium', 'webdriver-manager']

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
{'console_scripts': ['etyping = etyping.cli:main']}

setup_kwargs = {
    'name': 'etyping',
    'version': '2.0.0',
    'description': 'Sushida API for Python',
    'long_description': '# Etyping Python\nA etyping tool for Python\n\n\n\n',
    'author': 'Hiroshi Tsuyuki',
    'author_email': 'kagemeka1@gmail.com',
    'maintainer': 'Hiroshi Tsuyuki',
    'maintainer_email': 'kagemeka1@gmail.com',
    'url': 'https://github.com/kagemeka/etyping-python#readme',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
