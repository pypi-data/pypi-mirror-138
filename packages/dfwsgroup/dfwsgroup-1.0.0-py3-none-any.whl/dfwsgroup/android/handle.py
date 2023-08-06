#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/8 17:37
# @Author  : Lifeng
# @Site    : 
# @File    : handle.py
# @Software: PyCharm

import json
import yaml
from pathlib import Path
from jinja2 import Template


class Handle:
    def __init__(self, devices: str, packages: str):
        self.devices = devices
        self.packages = packages
        self.path = Path(__file__).parent.parent.joinpath("data", "command.yml")

    def read_yml(self, tier):
        with open(self.path, "r", encoding="utf-8") as r:
            data = yaml.safe_load(r)[tier]
            results = Template(json.dumps(data)).render(contents=[self.devices, self.packages])
            return json.loads(results)

    def handle_argv(self, *, argv: str):
        try:
            if isinstance(argv, str):
                data = {"--10": 10, "--15": 15, "--20": 20, "--25": 25, "--30": 30}
                for i in data.keys():
                    if argv == i:
                        return self.read_yml(tier=f"adb_{data[i]}")
            if argv is None:
                return self.read_yml(tier=f"adb_5")
        except Exception as e:
            raise e