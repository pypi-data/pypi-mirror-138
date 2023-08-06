#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/8 13:48
# @Author  : Lifeng
# @Site    : 
# @File    : androidScript.py
# @Software: PyCharm

import os
from pathlib import Path
from colorama import Fore
from dfwsgroup.android.handle import Handle

__all__ = ["StabilityTestAndroid"]


class StabilityTestAndroid:
    def __init__(self, packages: str):
        results = os.popen('adb devices', "r").readlines()
        self._devices = results[1].split("\t")[0]
        self._path = Path(__file__).parent.joinpath("Fastbot_Android")
        self._handle = Handle(self._devices, packages)

    def _jar_package_push(self):
        if self._devices:
            os.system(f"adb push {self._path.joinpath('framework.jar')} /sdcard")
            os.system(f"adb push {self._path.joinpath('monkeyq.jar')} /sdcard")
            os.system(f"adb push {self._path.joinpath('fastbot-thirdpart.jar')} /sdcard")
        else:
            raise Exception(f"检查是否连接有问题或adb环境是否正常！")

    def execute(self, *, parameter: str):
        if not self._devices:
            raise Exception(f"请检查设备号：{self._devices}")

        self._jar_package_push()

        return os.system(self._handle.handle_argv(argv=parameter))
