# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_tvseries']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.21.3,<0.22.0',
 'lxml>=4.6.4,<5.0.0',
 'nonebot-adapter-onebot==2.0.0-beta.1',
 'nonebot-plugin-htmlrender>=0.0.4.2,<0.0.5.0',
 'nonebot2==2.0.0-beta.1']

setup_kwargs = {
    'name': 'nonebot-plugin-tvseries',
    'version': '0.0.2.3',
    'description': '',
    'long_description': '# nonebot-plugin-tvseries\n\n获取美剧\n\n# 安装\n\n## 环境(dockerfile)\n\n```\nENV TZ=Asia/Shanghai\nENV LANG zh_CN.UTF-8\nENV LANGUAGE zh_CN.UTF-8\nENV LC_ALL zh_CN.UTF-8\nENV TZ Asia/Shanghai\nENV DEBIAN_FRONTEND noninteractive\n```\n\n## 本体\n\n`pip install nonebot-plugin-tvseries`\n\n## 依赖\n\n```bash\napt install -y locales locales-all fonts-noto\n\napt-get install -y libnss3-dev libxss1 libasound2 libxrandr2 \\\n    libatk1.0-0 libgtk-3-0 libgbm-dev libxshmfence1\n\nplaywright install chromium && playwright install-deps\n```\n\n# 使用\n\n`剧集` `tvseries`\n\n# 有问题 提issue 最好pr\n',
    'author': 'kexue',
    'author_email': 'xana278@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
