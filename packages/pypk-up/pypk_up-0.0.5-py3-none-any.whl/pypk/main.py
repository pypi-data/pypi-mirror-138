from pypk.pypi_update import pypi_update
from pypk.pypi_upload import pypi_upload
import os
from pypk.clear_console import clearConsole

def run():
    while True:
        step = input('1、更新python包\n2、上传项目至pypi\n0、退出程序\n请选择需要的操作：')
        if step == '1':
            clearConsole()
            pypi_update()
        elif step == '2':
            clearConsole()
            pypi_upload()
        elif step == '0':
            clearConsole()
            break
        else:
            print('输入信息有误')


if __name__ == '__main__':
    run()

