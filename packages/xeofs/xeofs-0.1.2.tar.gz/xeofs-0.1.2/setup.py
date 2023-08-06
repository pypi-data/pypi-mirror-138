# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xeofs', 'xeofs.models', 'xeofs.pandas', 'xeofs.xarray']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.2,<2.0.0',
 'pandas>=1.4.1,<2.0.0',
 'pooch>=1.6.0,<2.0.0',
 'scikit-learn>=1.0.2,<2.0.0',
 'xarray>=0.21.1,<0.22.0']

setup_kwargs = {
    'name': 'xeofs',
    'version': '0.1.2',
    'description': 'Collection of EOF analysis and related techniques for climate science',
    'long_description': '.. image:: https://img.shields.io/github/v/tag/nicrie/xeofs?label=Release\n   :alt: GitHub tag (latest SemVer)\n\n.. image:: https://img.shields.io/github/workflow/status/nicrie/xeofs/CI\n  :alt: GitHub Workflow Status (event)\n\n.. image:: https://readthedocs.org/projects/xeofs/badge/?version=latest\n   :target: https://xeofs.readthedocs.io/en/latest/?badge=latest\n   :alt: Documentation Status\n\n.. image:: https://codecov.io/gh/nicrie/xeofs/branch/main/graph/badge.svg?token=8040ZDH6U7\n  :target: https://codecov.io/gh/nicrie/xeofs\n\n\n=================================\nxeofs: EOF analysis and variants\n=================================\nEmpirical orthogonal function (EOF) analysis, commonly referred to as\nprincipal component analysis (PCA), is a popular decomposition\ntechnique in climate science. Over the years, a variety of variants\nhave emerged but the lack of availability of these different methods\nin the form of easy-to-use software seems to unnecessarily hinder the\nacceptance and uptake of these EOF variants by the broad climate science\ncommunity.\n\n************************\nGoal (work in progress)\n************************\nCreate a Python package that provides simple access to a variety of different\nEOF-related techniques through the popular interfaces of NumPy_, pandas_\nand xarray_.\n\n************************\nDocumentation\n************************\nDocumentation_ is work in progress.\n\n.. _Documentation: https://xeofs.readthedocs.io/en/latest/\n\n************************\nCredits\n************************\n\n- General project structure: yngvem_\n- Testing data: xarray_ \\& pooch_\n\n\n\n.. _NumPy: https://www.numpy.org\n.. _pandas: https://pandas.pydata.org\n.. _xarray: https://xarray.pydata.org\n.. _yngvem: https://github.com/yngvem/python-project-structure\n.. _pooch: https://github.com/fatiando/pooch\n',
    'author': 'Niclas Rieger',
    'author_email': 'niclasrieger@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nicrie/xeofs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
