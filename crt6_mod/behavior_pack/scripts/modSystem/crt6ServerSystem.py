# -*- coding: utf-8 -*-
from __future__ import print_function
# CRT6 服务端系统
# 参照官方文档：System.md, 实体.md, 世界/实体管理.md

import mod.server.extraServerApi as serverApi

ServerSystem = serverApi.GetServerSystemCls()
engine_namespace = serverApi.GetEngineNamespace()
engine_system = serverApi.GetEngineSystemName()


class CRT6ServerSystem(ServerSystem):
    def __init__(self, namespace, system_name):
        ServerSystem.__init__(self, namespace, system_name)

        self.ListenForEvent(engine_namespace, engine_system,
                            "ServerItemUseOnEvent", self, self._on_item_use_on)

        self.ListenForEvent(engine_namespace, engine_system,
                            "AddServerPlayerEvent", self, self._on_player_join)

        print("[CRT6] 服务端系统已初始化")

    def _on_player_join(self, event):
        player_id = event.get("id", "")
        player_name = event.get("name", "")
        print("[CRT6] 玩家 {0} 加入游戏".format(player_name))

    def _on_item_use_on(self, event):
        item_name = event.get("itemName", "")
        player_id = event.get("entityId", "")

        if item_name == "crt6:spawn_egg_crt6":
            self._spawn_crt6_train(player_id, event)

    def _spawn_crt6_train(self, player_id, event):
        x = event.get("x", 0)
        y = event.get("y", 0)
        z = event.get("z", 0)
        dimension_id = event.get("dimensionId", 0)

        spawn_pos = (x, y + 1, z)

        entity_id = serverApi.GetEngineCompFactory().CreateGame(
            player_id).SpawnEntity(
            dimension_id, "crt6:train_crt6", spawn_pos, (0, 0)
        )

        if entity_id:
            print("[CRT6] 重庆地铁6号线已生成! EntityID: {0}".format(entity_id))
            serverApi.GetEngineCompFactory().CreateGame(
                player_id).SetEntityPos(
                entity_id, spawn_pos
            )
        else:
            print("[CRT6] 生成失败!")