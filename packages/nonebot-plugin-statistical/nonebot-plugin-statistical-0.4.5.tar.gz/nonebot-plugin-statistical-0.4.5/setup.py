# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_statistical']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.1,<4.0.0',
 'nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
 'nonebot2>=2.0.0-beta.2,<3.0.0',
 'ujson>=5.1.0,<6.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-statistical',
    'version': '0.4.5',
    'description': '基于 run_postprocessor 实现的功能调用统计以及可视化，且可为插件设置别名和显示白名单',
    'long_description': None,
    'author': 'HibiKier',
    'author_email': '775757368@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
