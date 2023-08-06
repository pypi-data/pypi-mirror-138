# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['placeholder']

package_data = \
{'': ['*']}

install_requires = \
['cairo-nile>=0.3.0,<0.4.0']

setup_kwargs = {
    'name': 'cairo-placeholder',
    'version': '0.0.2',
    'description': 'Example project for cairo-glyph',
    'long_description': '# cairo-placeholder\n\nAn example library published to demonstrate the [cairo-glyph](https://github.com/sambarnes/cairo-glyph) package manager. See that repo for instructions/details.\n\n`pip install cairo-placeholder`\n',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
