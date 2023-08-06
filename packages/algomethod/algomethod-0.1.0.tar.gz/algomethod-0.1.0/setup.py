# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['algomethod']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp',
 'beautifulsoup4',
 'optext-python==0.1.1',
 'requests',
 'selenium',
 'selext==0.2.0']

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
    'name': 'algomethod',
    'version': '0.1.0',
    'description': 'This is a template for python projects.',
    'long_description': '# Algomethod\n\nalgo-method API for Python\n',
    'author': 'Hiroshi Tsuyuki',
    'author_email': 'kagemeka1@gmail.com',
    'maintainer': 'Hiroshi Tsuyuki',
    'maintainer_email': 'kagemeka1@gmail.com',
    'url': 'https://github.com/kagemeka/algomethod/#readme',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
