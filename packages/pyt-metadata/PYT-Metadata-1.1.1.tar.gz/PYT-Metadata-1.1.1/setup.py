# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyt_metadata']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.3,<4.0.0', 'Markdown>=3.3.6,<4.0.0']

setup_kwargs = {
    'name': 'pyt-metadata',
    'version': '1.1.1',
    'description': 'Metadata generator from python toolboxes',
    'long_description': None,
    'author': 'Cody Scott',
    'author_email': 'jcodyscott+PYTMETA@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
