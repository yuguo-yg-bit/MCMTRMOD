# -*- coding: utf-8 -*-
from __future__ import print_function
# CRT6 客户端系统
# 参照官方文档：System.md, 实体/渲染.md

import mod.client.extraClientApi as clientApi

ClientSystem = clientApi.GetClientSystemCls()
engine_namespace = clientApi.GetEngineNamespace()
engine_system = clientApi.GetEngineSystemName()


class CRT6ClientSystem(ClientSystem):
    def __init__(self, namespace, system_name):
        ClientSystem.__init__(self, namespace, system_name)

        print("[CRT6] 客户端系统已初始化")

    def Update(self):
        pass