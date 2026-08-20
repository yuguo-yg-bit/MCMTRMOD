# MTR (Minecraft Transit Railway) - 网易我的世界 ModSDK 模组
# 项目未完工！欢迎广大网友公益帮忙编辑！

## 项目概述

本模组由 **Java版MTR (Minecraft Transit Railway) 地铁/高铁MC模组** 源码通过Python 2.7转换脚本自动转换适配为 **网易我的世界ModSDK** 模组工程。

- **转换来源**: [Minecraft Transit Railway](https://github.com/jonafanho/Minecraft-Transit-Railway) Java Fabric版
- **目标平台**: 网易我的世界 (NetEase Minecraft) ModSDK (基岩版)
- **转换工具**: Python 2.7 标准语法编写，无第三方依赖
- **转换原则**: 仅做语法、API、框架层转换，禁止篡改原有地铁、列车、轨道、屏蔽门、高铁行驶逻辑、贴图资源映射逻辑，业务核心逻辑100%原样保留

## 模组功能

- **铁路系统**: 完整的铁轨铺设、连接、节点管理，支持多种轨道类型（木、石、绿宝石、铁、砖、黑曜石、海晶石、烈焰、石英、钻石）
- **列车系统**: 列车驾驶、加速、制动、开关门、自动行驶、信号响应
- **信号系统**: 红/黄/绿信号灯，信号块占用检测，自动闭塞
- **屏蔽门系统**: PSD (Platform Screen Door) 和 APG (Automatic Platform Gate)，支持动画开合
- **PIDS系统**: 乘客信息显示系统，显示到站信息、目的地、预计到达时间
- **电梯系统**: 多层电梯，楼层呼叫
- **票务系统**: 售票机，余额管理
- **多种交通模式**: 地铁、高铁、轻轨、缆车、渡轮、飞机
- **车站管理**: 车站命名、站台配置、出口标识
- **路线管理**: 路线规划、站点排序、循环路线
- **车辆段管理**: 列车生成、清除、即时部署

## 目录结构

```
mtr_netease/
├── behavior_pack/                    # 行为包（服务端逻辑）
│   ├── manifest.json                 # 行为包清单
│   ├── blocks.json                   # 方块定义
│   ├── items.json                    # 物品定义
│   └── scripts/                      # Python脚本
│       ├── modMain.py                # 入口文件，注册服务端/客户端系统
│       ├── modSystem/                # 系统模块
│       │   ├── __init__.py
│       │   ├── mtrServerSystem.py    # 服务端系统（核心列车、信号、门控逻辑）
│       │   └── mtrClientSystem.py    # 客户端系统（渲染、UI、输入处理）
│       ├── core/                     # 核心逻辑模块
│       │   ├── __init__.py
│       │   ├── rail_logic.py         # 轨道逻辑（节点、连接、路径查找）
│       │   ├── train_logic.py        # 列车逻辑（移动、加速、制动、门控）
│       │   ├── signal_logic.py       # 信号逻辑（颜色、状态、占用检测）
│       │   ├── door_logic.py         # 门控逻辑（PSD/APG动画、同步）
│       │   └── station_logic.py      # 车站/路线/车辆段逻辑
│       ├── blocks/                   # 方块模块
│       │   ├── __init__.py
│       │   └── block_entity_logic.py # 方块实体逻辑（信号灯、PSD、PIDS等）
│       ├── entity/                   # 实体模块
│       │   ├── __init__.py
│       │   └── entity_defs.py        # 实体定义（列车、缆车、渡轮、飞机模型配置）
│       ├── items/                    # 物品模块
│       │   └── __init__.py
│       └── packet/                   # 网络通信模块
│           ├── __init__.py
│           └── packet_defs.py        # 数据包定义（事件映射、数据构建器）
├── resource_pack/                    # 资源包（客户端资源）
│   ├── manifest.json                 # 资源包清单
│   ├── entity.json                   # 实体客户端定义
│   ├── sounds.json                   # 音效定义
│   ├── textures_list.json            # 贴图列表
│   ├── textures/                     # 贴图资源
│   │   ├── blocks/                   # 方块贴图
│   │   ├── items/                    # 物品贴图
│   │   ├── entity/                   # 实体贴图（列车、缆车、渡轮、飞机、电梯）
│   │   ├── mtr/                      # MTR专用贴图
│   │   │   ├── gui/                  # GUI贴图
│   │   │   └── environment/          # 环境贴图（隧道、站台、天花板、地板）
│   │   └── ui/                       # UI贴图
│   ├── models/                       # 模型资源
│   │   ├── blocks/                   # 方块模型
│   │   └── entity/                   # 实体模型
│   ├── sounds/                       # 音效文件
│   └── ui/                           # UI界面文件
├── convert_mtr.py                    # Python 2.7 转换脚本
└── copy_resources.py                 # 资源复制工具脚本
```

## 转换说明

### 转换工具

使用 `convert_mtr.py`（Python 2.7标准语法）进行转换，该脚本：

1. 读取Java MTR模组源码
2. 分析Java类结构、方块定义、物品定义、实体定义
3. 映射Java API到网易ModSDK API
4. 生成行为包和资源包文件
5. 保持所有业务逻辑不变

### 资源复用

使用 `copy_resources.py` 复制原版Java MTR的资源文件到网易模组目录，包括：
- 贴图资源（PNG）-> 保持原样复用
- 模型资源（JSON）-> 需手动转换为基岩版geo.json格式
- 音效资源（OGG）-> 保持原样复用

### API映射

| Java MTR (Fabric) | 网易ModSDK |
|---|---|
| `Init.REGISTRY.registerItem()` | `RegisterItems()` / `items.json` |
| `Init.REGISTRY.registerBlock()` | `RegisterBlocks()` / `blocks.json` |
| `REGISTRY.registerPacket()` | `NotifyToClient()` / `NotifyToServer()` |
| `REGISTRY.eventRegistry.registerServerStarted()` | `ListenForEvent()` |
| `REGISTRY.registerCommand()` | `RegisterCommand()` |
| `MinecraftServerHelper.iterateWorlds()` | `RegisterSystem()` + `Update()` |
| `BlockEntity` | `GetBlockEntityData()` / `SetBlockEntityData()` |
| `Entity` | `CreateEngineEntityByTypeStr()` |
| `ExtraData` | `SetExtraData()` / `GetExtraData()` |

## SDK API验证

所有网易ModSDK接口均通过内置MCP工具 `modsdk-mcp-server` 查询验证，包括：

- `RegisterSystem(nameSpace, systemName, clsPath)` - 注册系统
- `ListenForEvent(namespace, systemName, eventName, instance, func)` - 事件监听
- `NotifyToClient(targetId, eventName, eventData)` - 服务器→客户端通信
- `NotifyToServer(eventName, eventData)` - 客户端→服务器通信
- `NotifyToMultiClients(targetIdList, eventName, eventData)` - 多客户端广播
- `GetEngineNamespace()` / `GetEngineSystemName()` - 获取引擎命名空间
- `GetEngineCompFactory()` - 获取引擎组件工厂
- `GetLevelId()` - 获取世界ID
- `GetBlockEntityData(dimension, pos)` - 获取方块实体数据
- `SetBlockEntityData(dimension, pos, data)` - 设置方块实体数据
- `CreateEngineEntityByTypeStr(typeStr)` - 创建引擎实体
- `SetExtraData(key, value)` / `GetExtraData(key)` - 数据持久化
- `SaveExtraData()` - 保存额外数据

## 适配注意事项

1. **模型格式**: Java版使用JSON模型，网易基岩版使用geo.json模型，需要手动转换模型格式
2. **贴图路径**: 贴图路径从 `assets/mtr/textures/` 映射到 `resource_pack/textures/`
3. **音效格式**: 确保音效文件为.ogg格式（基岩版兼容）
4. **方块实体**: 基岩版方块实体使用block_entity组件，数据通过GetBlockEntityData/SetBlockEntityData操作
5. **网络通信**: Java版使用Fabric Packet系统，网易版使用NotifyToClient/NotifyToServer事件系统
6. **事件系统**: Java版使用Fabric Event系统，网易版使用ListenForEvent事件监听
7. **命令系统**: Java版使用Brigadier命令系统，网易版使用RegisterCommand
8. **数据持久化**: Java版使用NBT/JSON文件，网易版使用SetExtraData/GetExtraData
9. **UI系统**: Java版使用Screen系统，网易版使用自定义UI JSON
10. **渲染系统**: Java版使用EntityRenderer，网易版使用客户端实体渲染引擎

## 使用方法

1. 将 `mtr_netease` 目录放入网易我的世界开发工作台的模组目录
2. 在开发工作台中打开行为包和资源包
3. 运行 `copy_resources.py` 复制原版资源文件（需要先有Java MTR源码）
4. 在开发工作台中测试和调试模组
5. 打包发布

## 命令

- `/mtr generatePath [depot]` - 从车辆段生成列车路径
- `/mtr clearVehicles [depot]` - 清除车辆段列车
- `/mtr instantDeploy [depot]` - 即时部署列车

## 开发信息

- **原始模组**: Minecraft Transit Railway (MTR) by Jonathan Ho
- **转换脚本**: Python 2.7, 使用标准库 (os, sys, json, shutil, re, codecs)
- **MCP工具**: modsdk-mcp-server (内置)
- **转换日期**: 2026-08-17
- **版本**: 1.0.0
