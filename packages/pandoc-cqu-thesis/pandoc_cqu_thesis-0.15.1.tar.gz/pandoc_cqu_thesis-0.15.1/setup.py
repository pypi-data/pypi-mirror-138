# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pandoc_cqu_thesis']

package_data = \
{'': ['*']}

install_requires = \
['panflute>=2.0', 'regex>=2021.4.4,<2022.0.0']

entry_points = \
{'console_scripts': ['pandoc_cqu_thesis = pandoc_cqu_thesis:main']}

setup_kwargs = {
    'name': 'pandoc-cqu-thesis',
    'version': '0.15.1',
    'description': '用于重庆大学毕业论文的 pandoc filter',
    'long_description': '# 用于重庆大学毕业论文的 pandoc filter\n\n配合 [cqu-thesis-markdown](https://github.com/ilcpm/cqu-thesis-markdown) 使用。\n\n## 安装\n\n``` shell\npip3 install .\n```\n\n## TODO\n\n目前代码很混乱（各种意义上），质量也不好，待重构。不过能跑起来（逃）。\n\n其他 TODO 见于 [cqu-thesis-markdown](https://github.com/ilcpm/cqu-thesis-markdown).\n',
    'author': 'Hagb Green',
    'author_email': 'hagb@hagb.name',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Hagb/pandoc_cqu_thesis',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
