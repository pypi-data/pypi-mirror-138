# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xarray_cube']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=4.3,<5.0',
 'numpy>=1.19,<2.0',
 'spectral-cube>=0.6,<0.7',
 'typing-extensions>=3.10,<4.0',
 'xarray-dataclasses>=0.9,<0.10',
 'xarray>=0.18,<0.30']

setup_kwargs = {
    'name': 'xarray-cube',
    'version': '0.3.0',
    'description': 'xarray extension for spectral cube analysis',
    'long_description': '# xarray-cube\n\n[![PyPI](https://img.shields.io/pypi/v/xarray-cube.svg?label=PyPI&style=flat-square)](https://pypi.org/project/xarray-cube/)\n[![Python](https://img.shields.io/pypi/pyversions/xarray-cube.svg?label=Python&color=yellow&style=flat-square)](https://pypi.org/project/xarray-cube/)\n[![Test](https://img.shields.io/github/workflow/status/a-lab-nagoya/xarray-cube/Test?logo=github&label=Test&style=flat-square)](https://github.com/a-lab-nagoya/xarray-cube/actions)\n[![License](https://img.shields.io/badge/license-MIT-blue.svg?label=License&style=flat-square)](LICENSE)\n\nxarray extension for spectral cube analysis\n\n## Installation\n\n```shell\npip install xarray-cube\n```\n',
    'author': 'Akio Taniguchi',
    'author_email': 'taniguchi@a.phys.nagoya-u.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/a-lab-nagoya/xarray-cube/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
