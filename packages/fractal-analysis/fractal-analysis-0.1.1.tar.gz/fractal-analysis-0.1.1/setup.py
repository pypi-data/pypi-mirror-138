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
    'version': '0.1.1',
    'description': '',
    'long_description': '# Fractal Analysis\nFractal and multifractal methods, including\n\n- fractional Brownian motion (FBM) tester\n- multifractional Brownian motion (MBM) tester\n\n## To install\nTo get started, simply do:\n```\npip install fractal-analysis\n```\nor check out the code from out GitHub repository.\n\nYou can now use the package in Python with:\n```\nfrom fractal_analysis import tester\n```\n\n## Examples\nImport:\n```\nfrom fractal_analysis.tester.series_tester import SeriesTester\n```\nTo test a series ```series```:\n```\ntester = SeriesTester(x=series)\n```\n\nTo test if the series is FBM with holder exponent 0.3 and use auto estimated sigma square:\n\n```\nis_fbm, sig2, h = tester.is_fbm(h=0.3, sig2=None)\n```\nIf the output contains, for example:\n> Bad auto sigma square calculated with error 6.239236333681868. Suggest to give sigma square and rerun.\n\nThe auto sigma square estimated is not accurate. One may want to manually choose a sigma square and rerun. For example:\n```\nis_fbm, sig2, h = tester.is_fbm(h=0.3, sig2=1)\n```\nOne can also test the series without specified holder exponent through either setting ```None``` to ```h``` that searches the correct holder exponent from 0.1 to 1 with step 0.1, or entering customized values. I.e.,\n```\nis_fbm, sig2, h = tester.is_fbm(h=None, sig2=None)\n```\nor\n```\nis_fbm, sig2, h = tester.is_fbm(h=[0,1, 0.2, 0.3], sig2=None)\n```\nTo test if the series is MBM with a given holdr exponent series ```h_mbm``` and use auto estimated sigma square:\n```\nret, sig2 = tester.is_mbm(h=h_mbm, sig2=None)\n```\nIf the following appears:\n>Bad estimated sigma square: 0.0. Suggest to give sigma square and rerun.\n\nOne may want to manually choose a sigma square and rerun. For example:\n```\nret, sig2 = tester.is_mbm(h=h_mbm, sig2=1)\n```\n',
    'author': 'yujiading',
    'author_email': 'yujia.ding@cgu.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yujiading/fractals',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
