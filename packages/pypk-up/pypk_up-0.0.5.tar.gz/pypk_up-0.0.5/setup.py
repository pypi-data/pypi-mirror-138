import setuptools
with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()
setuptools.setup(
    name="pypk_up",    # 包名
    version="0.0.5",  # 版本
    author="测码范晔",   # 作者
    author_email="1538379200@qq.com",    # 邮箱
    description="一个管理python包和上传程序的扩展工具",
    long_description=long_description,  # 长介绍，为编写的README
    long_description_content_type="text/markdown",  # 使用介绍文本
    url="",     # github等项目地址
    packages=setuptools.find_packages(),    # 自动查找包，手动写也可
    install_requires=['setuptools>=60.8.1', 'wheel>=0.37.1', 'twine>=3.8.0'],    # 安装此包所需的依赖
    entry_points={
        'console_scripts': [        # 命令行运行代码
            'pypk_up=pypk.main:run'
        ],
    },
    classifiers=(       # 其他的配置项
        "Programming Language :: Python :: 3",      # 限制pytest编程语言，版本为3
        "License :: OSI Approved :: MIT License",   # 使用MIT的开源协议(手动添加协议后修改此项)
        "Operating System :: OS Independent",   # 系统要求
    ),
)