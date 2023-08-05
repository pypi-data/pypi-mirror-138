import os
from pathlib import Path
from pypk.clear_console import clearConsole


def pypi_upload():
    while True:
        try:
            control_type = input('1、生成配置文件结构\n2、打包程序\n3、上传程序\n0、退出程序\n请通过序号选择需要的操作：')
            if int(control_type) == 1:
                changepath = input('一般这种文件都会放在根目录中,程序默认使用上一级目录进行创建，是否手动指定根目录？Y为重新指定，其他任意字符为不指定：')
                if changepath.lower() == 'y':
                    filepath = input('请输入文件路径：')+'/'
                else:
                    filepath = '../'
                mkfileList = ['setup.py', 'LICENSE.txt', 'README.md']
                for filename in mkfileList:
                    Path(filepath+filename).touch(exist_ok=True)
                    if filename == 'setup.py':
                        with open(filepath+filename, 'w', encoding='utf-8') as f:
                            f.write('''import setuptools
with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()
setuptools.setup(
    name="xxx",    # 包名
    version="0.1",  # 版本
    author="hzz",   # 作者
    author_email="1538379200@qq.com",    # 邮箱
    description="项目介绍",
    long_description=long_description,  # 长介绍，为编写的README
    long_description_content_type="text/markdown",  # 使用介绍文本
    url="",     # github等项目地址
    packages=setuptools.find_packages(),    # 自动查找包，手动写也可
    install_requires=['setuptools>=60.8.1', 'wheel>=0.37.1', 'twine>=3.8.0'],    # 安装此包所需的依赖
    entry_points={
        'console_scripts': [        # 命令行运行代码
            'pypi-up=pypk.main:run'
        ],
    },
    classifiers=(       # 其他的配置项
        "Programming Language :: Python :: 3",      # 限制pytest编程语言，版本为3
        "License :: OSI Approved :: MIT License",   # 使用MIT的开源协议(手动添加协议后修改此项)
        "Operating System :: OS Independent",   # 系统要求
    ),
)''')
                    elif filename == 'LICENSE.txt':
                        with open(filepath + filename, 'w', encoding='utf-8') as f:
                            f.write('''MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.''')
                    else:
                        pass
                print('文件创建完成，请修改配置项和开源协议等')
            elif int(control_type) == 2:
                basepath = input('指定程序根目录,不输入则默认上一级目录：')
                print('正在打包文件……')
                if ':' in basepath:
                    sdisk = basepath.split(':')[0]
                    os.system(f'cd {sdisk}: && cd {basepath} &&　python setup.py sdist bdist_wheel')
                elif basepath == '':
                    os.system('cd .. && python setup.py sdist bdist_wheel')
                else:
                    os.system(f'cd {basepath} && python setup.py sdist bdist_wheel')
                print('文件打包操作已完成')
            elif int(control_type) == 3:
                workpath = input('请输入当前文件根目录,不输入则默认上一级目录：')
                username = input('请输入用户名：')
                password = input('请输入密码：')
                print('准备进行文件上传')
                if ':' in workpath:
                    sdisk = workpath.split(':')[0]
                    os.system(f'cd {sdisk}: && cd {workpath} && py -m twine upload -u {username} -p {password}  dist/*')
                elif workpath == '':
                    os.system(f'cd .. && py -m twine upload -u {username} -p {password}  dist/*')
                else:
                    os.system(f'cd {workpath} && py -m twine upload -u {username} -p {password}  dist/*')
                print('已完成文件上传程序')
            elif int(control_type) == 0:
                clearConsole()
                break
        except:
            print('输入的序号有误，请重新输入')

# if __name__ == '__main__':
#     pypi_upload()



