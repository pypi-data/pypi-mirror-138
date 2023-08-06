# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_petpet']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>8.2.0',
 'aiocache>=0.11.0',
 'httpx>=0.19.0',
 'imageio>=2.12.0,<3.0.0',
 'nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
 'nonebot2>=2.0.0-beta.1,<3.0.0',
 'numpy>=1.20.0,<2.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-petpet',
    'version': '0.2.2.1',
    'description': 'Nonebot2 plugin for making fun pictures',
    'long_description': '# nonebot-plugin-petpet\n\n[Nonebot2](https://github.com/nonebot/nonebot2) 插件，制作头像相关的表情包\n\n### 使用\n\n发送“头像表情包”显示下图的列表：\n\n<div align="left">\n  <img src="https://s2.loli.net/2022/01/04/A3OWEtNcjygxPIf.jpg" width="400" />\n</div>\n\n\n每个表情包首次使用时会下载对应的图片和字体，可以手动下载 `resources` 下的 `images` 和 `fonts` 文件夹，放置于机器人运行目录下的 `data/petpet/` 文件夹中\n\n\n#### 触发方式\n- 指令 + @user，如： /爬 @小Q\n- 指令 + qq号，如：/爬 123456\n- 指令 + 自己，如：/爬 自己\n- 指令 + 图片，如：/爬 [图片]\n\n前三种触发方式会使用目标qq的头像作为图片\n\n#### 支持的指令\n\n- 摸\n\n<div align="left">\n  <img src="./examples/petpet.gif" width="200" />\n</div>\n\n\n- 亲\n\n<div align="left">\n  <img src="./examples/kiss.gif" width="200" />\n</div>\n\n\n- 贴/蹭\n\n<div align="left">\n  <img src="./examples/rub.gif" width="200" />\n</div>\n\n\n- 顶/玩\n\n<div align="left">\n  <img src="./examples/play.gif" width="200" />\n</div>\n\n\n- 拍\n\n<div align="left">\n  <img src="./examples/pat.gif" width="200" />\n</div>\n\n\n- 撕\n\n<div align="left">\n  <img src="./examples/rip.jpg" width="200" />\n</div>\n\n\n- 丢\n\n<div align="left">\n  <img src="./examples/throw.jpg" width="200" />\n</div>\n\n\n- 爬\n\n<div align="left">\n  <img src="./examples/crawl.jpg" width="200" />\n</div>\n\n\n- 精神支柱\n\n<div align="left">\n  <img src="./examples/support.jpg" width="200" />\n</div>\n\n\n- 一直\n\n<div align="left">\n  <img src="./examples/always.gif" width="200" />\n</div>\n\n\n- 加载中\n\n<div align="left">\n  <img src="./examples/loading.gif" width="200" />\n</div>\n\n\n- 转\n\n<div align="left">\n  <img src="./examples/turn.gif" width="200" />\n</div>\n\n\n- 小天使\n\n<div align="left">\n  <img src="./examples/littleangel.jpg" width="200" />\n</div>\n\n\n- 不要靠近\n\n<div align="left">\n  <img src="./examples/dont_touch.jpg" width="200" />\n</div>\n\n\n- 一样\n\n<div align="left">\n  <img src="./examples/alike.jpg" width="200" />\n</div>\n\n\n- 滚\n\n<div align="left">\n  <img src="./examples/roll.gif" width="200" />\n</div>\n\n\n- 玩游戏\n\n<div align="left">\n  <img src="./examples/play_game.png" width="200" />\n</div>\n\n\n- 膜\n\n<div align="left">\n  <img src="./examples/worship.gif" width="200" />\n</div>\n',
    'author': 'meetwq',
    'author_email': 'meetwq@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MeetWq/nonebot-plugin-petpet',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
