from setuptools import setup, find_packages
setup(
    name='nonebot_plugin_pixiv', # pip安装时候的名字
    version="1.0.1", # 版本号 
    description=(
        'pixiv.net查图(支持动图)' # 描述
    ), 
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown", 
    author='anlen123', #作者
    author_email='1761512493@qq.com',
    maintainer='anlen123', #维护人员
    maintainer_email='1761512493@qq.com',
    packages=find_packages(), # 需要处理的包目录(通常为包含 __init__.py 的文件夹)
    platforms=["all"], # 程序适用的软件平台列表
    url='https://github.com/anlen123/nonebot_plugin_pixiv', # github地址
    install_requires=[
        'aiohttp',
        'nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
        'nonebot2>=2.0.0-beta.1,<3.0.0',
    ]
)
