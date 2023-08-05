# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rich_demo']

package_data = \
{'': ['*']}

install_requires = \
['rich>=11.2.0,<12.0.0']

entry_points = \
{'console_scripts': ['rich-demo = rich_demo.__main__:run'],
 'pipx.run': ['rich-demo = rich_demo.__main__:run']}

setup_kwargs = {
    'name': 'rich-demo',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Chema Cortés',
    'author_email': 'dextrem@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chemacortes/rich-demo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
