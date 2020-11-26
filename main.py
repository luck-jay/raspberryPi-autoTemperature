# -*- coding: utf-8 -*-
#!/usr/bin/python3
# 导入temp.py 模块
from control import control
# 导入time模块，使用sleep函数
from time import sleep
# 导入datetime模块，获取系统时间
from datetime import datetime

import os

# 预设高温散热温度
Pre_temp = 50
# 设置日志文件大小
log_size = 102400 # 100k
# 设置日志文件名字
logfile = 'log'
# 获取cpu温度信息
def temp_cpu():
    # 设置cpu温度初始值
    cpu = 0
    # 求出10秒内cpu温度平均值
    for i in range(10):
        # 打开cpu温度文件
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            data = f.read()
            cpu += int(data) / 1000
        # 每次查看温度后暂停一秒
        sleep(1)
    # 返回10秒内温度的平均值
    return cpu / 10

def main(t):
    sig = True
    # 初始化引脚
    t.local_gpio()
    # 循环判断温度是否达到指定值
    while True:
        # 获取当前系统时间
        now_time = datetime.now().strftime('%F %T')
        t_temp = temp_cpu()
        # 获取日志文件大小
        logfile_size = os.path.getsize(logfile)
        # 判断是否第一次打开程序
        if sig:
            with open(logfile, 'w') as f: f.write('{}\tCPU当前温度：{:.3f}\n'.format(now_time, t_temp))
            sig = False
        else:
            # 判断日志文件是否超标
            if logfile_size < log_size:
                with open(logfile, 'a') as f: f.write('{}\tCPU当前温度：{:.3f}\n'.format(now_time, t_temp))
            else:
                with open(logfile, 'w') as f: f.write('{}\tCPU当前温度：{:.3f}\n'.format(now_time, t_temp))

        # 如果温度达到预设值
        if t_temp >= Pre_temp:
            t.set_open()
            with open(logfile, 'a') as f: f.write('散热被打开!\n')

        elif 0 < t_temp < Pre_temp :
            # 如果温度没有达到预设值
            t.set_down()
            with open(logfile, 'a') as f: f.write('散热被关闭!\n')

        else:
            #如果都不满足，则是出现了错误
            print('程序出现异常！')
            break



if __name__ == "__main__":
    # 创建一个control类的实例
    t = control()

    try:
        main(t)
    except KeyboardInterrupt:
        # 程序强制退出，则释放引脚
        print("程序强制退出！")
    finally:
        # 无论程序出现什么情况，都必须释放引脚
        t.clear_gpio()
    

