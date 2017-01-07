#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GPIOCtrl这个工具主要是为了方便进行Linux下的GPIOCtrl的操作
"""

from shell.ShellCmd import ShellCmd

import os

class GPIOCtrl(object):

    baseDir = "/sys/class/gpio/"

    NONE    = "none"
    RISING  = "rising"
    FALLING = "falling"
    BOTH    = "both"

    @staticmethod
    def setBasePath(dir):
        GPIOCtrl.baseDir = dir;

    @staticmethod
    def directionPath(pinNumber):
        return GPIOCtrl.baseDir + "gpio" + str(pinNumber) + "/direction"

    @staticmethod
    def valuePath(pinNumber):
        return GPIOCtrl.baseDir + "gpio" + str(pinNumber) + "/value"

    @staticmethod
    def requestGpio(pinNumber):
        if os.path.exists(GPIOCtrl.baseDir + "gpio" + str(pinNumber)) :
            return
        cmd = "echo " + str(pinNumber) + " > " + GPIOCtrl.baseDir + "export"
        ShellCmd.execute(cmd)

    @staticmethod
    def freeGpio(pinNumber):
        if os.path.exists(GPIOCtrl.baseDir + "gpio" + str(pinNumber)) :
            cmd = "echo " + str(pinNumber) + " > " + GPIOCtrl.baseDir + "unexport"
            ShellCmd.execute(cmd)

    @staticmethod
    def setIn(pinNumber):
        cmd = "echo in > " + GPIOCtrl.directionPath(pinNumber)
        ShellCmd.execute(cmd)

    @staticmethod
    def setOut(pinNumber):
        cmd = "echo out > " + GPIOCtrl.directionPath(pinNumber)
        ShellCmd.execute(cmd)

    @staticmethod
    def setValue(pinNumber, value):
        cmd = "echo " + str(value) + " > " + GPIOCtrl.valuePath(pinNumber)
        ShellCmd.execute(cmd)

    @staticmethod
    def setOutValue(pinNumber, value):
        if value == 0:
            cmd = "echo low > " + GPIOCtrl.directionPath(pinNumber)
            ShellCmd.execute(cmd)
        else :
            cmd = "echo high > " + GPIOCtrl.directionPath(pinNumber)
            ShellCmd.execute(cmd)

    @staticmethod
    def getValue(pinNumber):
        cmd = "cat " + GPIOCtrl.valuePath(pinNumber)
        return ShellCmd.execute(cmd)[0].strip('\n')

    """
     *  none    表示引脚为输入，不是中断引脚
     *  rising  表示引脚为中断输入，上升沿触发
     *  falling 表示引脚为中断输入，下降沿触发
     *  both    表示引脚为中断输入，边沿触发
    """
    @staticmethod
    def setEdge(pinNumber, type):
        cmd = "echo " + type + " > " + GPIOCtrl.baseDir + "gpio" + str(pinNumber) + "/edge"
        ShellCmd.execute(cmd)

