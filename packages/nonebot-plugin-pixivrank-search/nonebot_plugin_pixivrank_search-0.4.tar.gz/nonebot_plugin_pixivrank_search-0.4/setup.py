# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_pixivrank_search']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.8.0,<0.9.0',
 'aiohttp>=3.8.1,<4.0.0',
 'beautifulsoup4>=4.10.0,<5.0.0',
 'feedparser>=6.0.8,<7.0.0',
 'lxml>=4.7.1,<5.0.0',
 'nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
 'nonebot2>=2.0.0-beta.2,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-pixivrank-search',
    'version': '0.4',
    'description': '基于RSSHUB阅读器实现的获取P站排行和P站搜图',
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
