#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GPIO这个工具主要是为了方便进行Linux下的GPIO的操作
"""

from GPIOCtrl import GPIOCtrl
import select
import os
import threading

class GPIO(object):

    mutex = threading.Lock()

    @staticmethod
    def initGPIOOut(pinNumber, value):
        GPIO.mutex.acquire()
        GPIOCtrl.requestGpio(pinNumber)
        GPIOCtrl.setOutValue(pinNumber, value)
        GPIO.mutex.release()

    @staticmethod
    def initGPIOIN(pinNumber):
        GPIO.mutex.acquire()
        GPIOCtrl.requestGpio(pinNumber)
        GPIOCtrl.setIn(pinNumber)
        GPIO.mutex.release()

    @staticmethod
    def freeGPIO(pinNumber):
        GPIO.mutex.acquire()
        GPIOCtrl.freeGpio(pinNumber)
        GPIO.mutex.release()

    @staticmethod
    def getValue(pinNumber):
        GPIO.mutex.acquire()
        val = GPIOCtrl.getValue(pinNumber)
        GPIO.mutex.release()

        return val


    @staticmethod
    def setValue(pinNumber, value):
        GPIO.mutex.acquire()
        GPIOCtrl.setValue(pinNumber, value)
        GPIO.mutex.release()

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
