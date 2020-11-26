# -*- coding: utf-8 -*-
"""
1、智能识别温度，通过温度调节散热，使效率最大化
"""
# 导入GPIO处理模块
import RPi.GPIO as GPIO
# 定义散热控制类
class control:
    # 定义使用的树莓派
    gpio = 18
    
    # 设置初始值
    def __init__(self, gpio=18):
        self.gpio = gpio
    
    # 打开散热
    def set_open(self):
        '''这个函数没有参数，用于打开散热'''
        GPIO.output(self.gpio, GPIO.LOW)

    # 关闭散热
    def set_down(self):
        '''这个函数没有参数，用于关闭散热'''
        GPIO.output(self.gpio, GPIO.HIGH)

    # 初始化引脚
    def local_gpio(self):
        '''这个函数没有参数，用于初始化引脚'''
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio, GPIO.OUT)

    # 释放引脚
    def clear_gpio(self):
        '''这个函数没有参数，用于释放引脚'''
        GPIO.cleanup()

