# -*- coding: utf-8 -*-
from __future__ import print_function
# MTR (Minecraft Transit Railway) Mod for NetEase Minecraft
# modMain.py - Entry point, registers server and client systems
# Converted from Java MTR mod: Init.java, MTR.java

import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi

# Module namespace
MOD_NAME = "mtr"
MOD_NAMESPACE = "mtr"
MOD_VERSION = "1.0.0"

# Server system
SERVER_SYSTEM_NAME = "mtrServerSystem"
SERVER_SYSTEM_CLS = "modSystem.mtrServerSystem.MTRServerSystem"

# Client system
CLIENT_SYSTEM_NAME = "mtrClientSystem"
CLIENT_SYSTEM_CLS = "modSystem.mtrClientSystem.MTRClientSystem"

# Register server system
serverApi.RegisterSystem(MOD_NAMESPACE, SERVER_SYSTEM_NAME, SERVER_SYSTEM_CLS)

# Register client system
clientApi.RegisterSystem(MOD_NAMESPACE, CLIENT_SYSTEM_NAME, CLIENT_SYSTEM_CLS)

# Print initialization message
print("[MTR] Minecraft Transit Railway Mod initialized")
print("[MTR] Namespace: " + MOD_NAMESPACE)
print("[MTR] Version: " + MOD_VERSION)

def __init__():
    pass