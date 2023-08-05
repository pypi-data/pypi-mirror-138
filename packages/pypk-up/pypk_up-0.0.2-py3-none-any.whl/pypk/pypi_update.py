import subprocess
import os
from clear_console import clearConsole


def pypi_update():
    print('使用pip更新程序前，请确保已设置pip环境变量')
    qinghua = 'https://pypi.tuna.tsinghua.edu.cn/simple'
    kexuejishu = 'https://pypi.mirrors.ustc.edu.cn/simple'
    douban = 'http://pypi.doubanio.com/simple/'
    tengxun = 'https://mirrors.cloud.tencent.com/pypi/simple/'
    ali = 'https://mirrors.aliyun.com/pypi/simple/'
    mirrorList = [qinghua, kexuejishu, douban, tengxun, ali]
    print('使用镜像源安装：\n1、清华镜像源\n2、科学大学镜像源\n3、豆瓣镜像源\n4、腾讯镜像源\n5、阿里镜像源\n0、自定义镜像源\n如果不需要镜像源，可以选择自定义，直接回车')
    useMirror = ''
    while True:
        mirror = input('请输入镜像源：')
        try:
            if int(mirror) == 0:
                a = input('请输入自定义镜像源：')
                useMirror = a
            elif int(mirror) > 0:
                useMirror = mirrorList[int(mirror)-1]
            break
        except:
            print('输入有误，请重新输入')
    print('正在查找可更新数据源……')
    get_pakeages = os.popen('pip list --outdate')
    listPakeages = list(get_pakeages)
    # show_updatePk = [listPakeages[x].split(' ')[0] for x in range(2, len(listPakeages)-1)]
    show_updatePk = []

    for i in range(2, len(listPakeages) - 1):
        pk = listPakeages[i].split(' ')[0]
        show_updatePk.append(pk)
        print(i - 1, '、', pk)

    print('输入序号可以更新单个包\n输入0更新全部\n输入-x为过滤第x项(x为前置的序号)\n输入任意非数字退出程序')
    while True:
        try:
            userOrder = input('请输入需要的操作：')
            print('')
            if int(userOrder) == 0:
                if useMirror == '':
                    for pakeage in show_updatePk:
                        subprocess.call('pip install --upgrade ' + pakeage, shell=True)
                else:
                    for pakeage in show_updatePk:
                        subprocess.call('pip install --upgrade ' + pakeage + ' -i '+useMirror, shell=True)
                print('操作完成')
                clearConsole()
                break
            elif int(userOrder) > 0:
                try:
                    if useMirror == '':
                        subprocess.call('pip install --upgrade ' + show_updatePk[int(userOrder) - 1], shell=True)
                    else:
                        subprocess.call('pip install --upgrade ' + show_updatePk[int(userOrder) - 1] + ' -i ' + useMirror, shell=True)
                    print('已操作：', show_updatePk[int(userOrder)-1])
                    print('更新数据：')
                    for pIndex, p in enumerate(show_updatePk):
                        print(pIndex+1, '、', p)
                except:
                    print('输入的数字有误，可能没有此序号')
            elif int(userOrder) < 0:
                try:
                    removeList = userOrder.split('-')[1]
                    pakeNum = int(removeList)
                    del show_updatePk[pakeNum-1]
                    print('更新数据：')
                    for pakeIndex, pakeage in enumerate(show_updatePk):
                        print(pakeIndex+1, '、', pakeage)
                except:
                    print('输入的序号有误或者符号错误')
        except:
            print('取消更新')
            clearConsole()
            break

# if __name__ == '__main__':
#     pypi_update()