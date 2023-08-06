import os


def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):    # 判断是否为windows系统
        command = 'cls'
    os.system(command)