# -*- coding: utf-8 -*-
from __future__ import print_function
# CRT6 Chongqing Metro Line 6 Mod
# modMain.py - 入口文件，注册服务端和客户端系统
# 参照官方文档：System.md RegisterSystem

import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi

MOD_NAMESPACE = "crt6"
MOD_NAME = "CRT6"
MOD_VERSION = "1.0.0"

SERVER_SYSTEM_NAME = "crt6ServerSystem"
SERVER_SYSTEM_CLS = "modSystem.crt6ServerSystem.CRT6ServerSystem"

CLIENT_SYSTEM_NAME = "crt6ClientSystem"
CLIENT_SYSTEM_CLS = "modSystem.crt6ClientSystem.CRT6ClientSystem"

serverApi.RegisterSystem(MOD_NAMESPACE, SERVER_SYSTEM_NAME, SERVER_SYSTEM_CLS)
clientApi.RegisterSystem(MOD_NAMESPACE, CLIENT_SYSTEM_NAME, CLIENT_SYSTEM_CLS)

print("[CRT6] 重庆地铁6号线模组已加载")
print("[CRT6] Namespace: " + MOD_NAMESPACE)
print("[CRT6] Version: " + MOD_VERSION)