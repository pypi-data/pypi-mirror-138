# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yaml2devops']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'azure-devops>=6.0.0-beta.4,<7.0.0', 'click>=8.0.3,<9.0.0']

entry_points = \
{'console_scripts': ['yaml2devops = yaml2devops.command_line:cli']}

setup_kwargs = {
    'name': 'yaml2devops',
    'version': '0.1.0',
    'description': 'yaml2devops-cli は yaml に記載したテストスイートの実行タスクを azure devops に起票できるツールです',
    'long_description': '使い方は [GitHub](https://github.com/nnashiki/yaml2devops-cli) を参照してください。',
    'author': 'Niten Nashiki',
    'author_email': 'n.nashiki.work@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nnashiki/yaml2devops-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
