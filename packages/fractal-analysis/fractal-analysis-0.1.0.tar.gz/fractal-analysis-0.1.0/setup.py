# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fractal_analysis', 'fractal_analysis.tester']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.4.0,<2.0.0', 'scipy>=1.8.0,<2.0.0', 'tqdm>=4.62.3,<5.0.0']

setup_kwargs = {
    'name': 'fractal-analysis',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'yujiading',
    'author_email': 'yujia.ding@cgu.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
