#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GPIO这个工具主要是为了方便进行Linux下的GPIO的操作
"""

from GPIOCtrl import GPIOCtrl
import select
import os

class GPIO(object):

    @staticmethod
    def initGPIOOut(pinNumber, value):
        GPIOCtrl.requestGpio(pinNumber)
        GPIOCtrl.setOutValue(pinNumber, value)

    @staticmethod
    def initGPIOIN(pinNumber):
        GPIOCtrl.requestGpio(pinNumber)
        GPIOCtrl.setIn(pinNumber)

    @staticmethod
    def freeGPIO(pinNumber):
        GPIOCtrl.freeGpio(pinNumber)

    @staticmethod
    def getValue(pinNumber):

        return GPIOCtrl.getValue(pinNumber)


    @staticmethod
    def setValue(pinNumber, value):

        GPIOCtrl.setValue(pinNumber, value)

    @staticmethod
    def getIMXPinNumber(group, num):
        return (group-1)*32 + num

    @staticmethod
    def irq(pinNumber, edgeType):

        GPIOCtrl.requestGpio(pinNumber)

        # 设置对应的pin脚为输入，并设置触发方式
        GPIOCtrl.setIn(pinNumber)
        GPIOCtrl.setEdge(pinNumber, edgeType)

        # 打开文件
        fd = os.open(GPIOCtrl.baseDir + GPIOCtrl.valuePath(pinNumber), os.O_RDWR)

        # 设置epoll触发方式
        epoll = select.epoll()
        epoll.register(fd, select.EPOLLPRI | select.EPOLLERR)

        while(True):

            # 等待事件发生
            events = epoll.poll(1)

            # 处理对应的事务
            for fileno , event in events:
                if event & select.EPOLLPRI:

                    value = os.read(fd, 512)

                    os.close(fd)

                    GPIOCtrl.setOut(pinNumber)
                    GPIOCtrl.setValue(pinNumber, 1)

                    GPIOCtrl.freeGpio(pinNumber)

                    return value
