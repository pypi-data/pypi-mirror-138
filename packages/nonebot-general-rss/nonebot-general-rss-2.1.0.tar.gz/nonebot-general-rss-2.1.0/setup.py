# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src\\plugins'}

packages = \
['nonebot-general-rss',
 'nonebot-general-rss.RSS',
 'nonebot-general-rss.RSS.routes',
 'nonebot-general-rss.RSS.routes.Parsing']

package_data = \
{'': ['*']}

install_requires = \
['ImageHash>=4.2.0,<5.0.0',
 'Pillow>=9.0.0,<10.0.0',
 'arrow>=1.2.0,<2.0.0',
 'bbcode>=1.1.0,<2.0.0',
 'emoji>=0.5.4,<0.6.0',
 'feedparser>=6.0.0,<7.0.0',
 'google-trans-new>=1.1.9,<2.0.0',
 'httpx>=0.18.0,<0.19.0',
 'magneturi>=1.3,<2.0',
 'nonebot-adapter-onebot==2.0.0b1',
 'nonebot-plugin-apscheduler>=0.1.2,<0.2.0',
 'nonebot2==2.0.0b1',
 'pydantic>=1.9.0,<2.0.0',
 'pyquery>=1.4.3,<2.0.0',
 'python-qbittorrent>=0.4.2,<0.5.0',
 'tenacity>=7.0.0,<8.0.0',
 'tinydb>=4.6.1,<5.0.0',
 'typing-extensions>=3.10.0.2,<4.0.0.0']

setup_kwargs = {
    'name': 'nonebot-general-rss',
    'version': '2.1.0',
    'description': 'nonebot-general-rss',
    'long_description': '# nonebot-general-rss\n\n基于 [ELF_RSS](https://github.com/Quan666/ELF_RSS) 修改的 Nonebot2 机器人插件，支持子频道订阅。\n\n**当前版本v2.x适用于 `nonebot2 2.0.0b1` 及以上，若使用 `nonebot2 2.0.0a16` 请移步 alpha 分支。**\n\n## 功能介绍\n\n* 发送QQ消息来动态增、删、查、改 RSS 订阅\n* 订阅内容翻译（使用谷歌机翻，可设置为百度翻译）\n* 个性化订阅设置（更新频率、翻译、仅标题、仅图片等）\n* 多平台支持\n* 图片压缩后发送\n* 种子下载并上传到群文件\n* 消息支持根据链接、标题、图片去重\n* 可设置只发送限定数量的图片，防止刷屏\n* 可设置从正文中要移除的指定内容，支持正则\n\n## 文档目录\n\n> * [部署教程](docs/部署教程.md)\n> * [使用教程](docs/使用教程.md)\n> * [更新日志](docs/更新日志.md)\n\n## 效果预览\n\n![效果1](https://cdn.jsdelivr.net/gh/mobyw/images@main/Screenshots/Screenshot_2.jpg)\n\n![效果2](https://cdn.jsdelivr.net/gh/mobyw/images@main/Screenshots/Screenshot_3.jpg)\n\n![效果3](https://cdn.jsdelivr.net/gh/mobyw/images@main/Screenshots/Screenshot_4.jpg)\n\n![效果4](https://cdn.jsdelivr.net/gh/mobyw/images@main/Screenshots/Screenshot_5.jpg)\n\n![效果5](https://cdn.jsdelivr.net/gh/mobyw/images@main/Screenshots/Screenshot_6.jpg)\n',
    'author': 'mobyw',
    'author_email': 'mobyw66@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mobyw/nonebot-general-rss',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.3,<4.0.0',
}


setup(**setup_kwargs)
