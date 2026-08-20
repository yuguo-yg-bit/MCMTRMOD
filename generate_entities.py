# -*- coding: utf-8 -*-
# Generate entity behavior definitions and update entity.json
# Creates all entity types for block entity rendering (方案A)

import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = BASE_DIR
BEHAVIOR_DIR = os.path.join(PROJECT_DIR, "mtr_netease", "behavior_pack", "entities")
RESOURCE_DIR = os.path.join(PROJECT_DIR, "mtr_netease", "resource_pack")
ENTITY_JSON = os.path.join(RESOURCE_DIR, "entity.json")
MODELS_DIR = os.path.join(RESOURCE_DIR, "models", "entity")
TEXTURES_DIR = os.path.join(RESOURCE_DIR, "textures", "entity")

ENTITY_TYPES = [
    ("psd_door", "屏蔽门", "entity_alphatest"),
    ("psd_glass", "屏蔽门玻璃", "entity_alphatest"),
    ("psd_glass_end", "屏蔽门玻璃端", "entity_alphatest"),
    ("psd_top", "屏蔽门顶部", "entity_alphatest"),
    ("apg_door", "自动站台门", "entity_alphatest"),
    ("apg_glass", "自动站台门玻璃", "entity_alphatest"),
    ("apg_glass_end", "自动站台门玻璃端", "entity_alphatest"),
    ("signal_light", "信号灯", "entity_alphatest"),
    ("pids", "PIDS显示屏", "entity_alphatest"),
    ("station_name", "站名牌", "entity_alphatest"),
    ("railway_sign", "铁路标志", "entity_alphatest"),
    ("route_sign", "线路标志", "entity_alphatest"),
    ("clock", "时钟", "entity_alphatest"),
    ("ticket_machine", "售票机", "entity_alphatest"),
    ("ticket_barrier", "检票闸机", "entity_alphatest"),
    ("lift_door", "电梯门", "entity_alphatest"),
    ("lift_panel", "电梯面板", "entity_alphatest"),
    ("lift_track", "电梯轨道", "entity_alphatest"),
    ("train_sensor", "列车传感器", "entity"),
    ("escalator_side", "扶梯侧板", "entity_alphatest"),
    ("escalator_step", "扶梯台阶", "entity_alphatest"),
    ("eye_candy", "装饰", "entity_alphatest"),
    ("platform", "站台", "entity_alphatest"),
    ("glass_fence", "玻璃护栏", "entity_alpha_test"),
    ("rubbish_bin", "垃圾桶", "entity_alphatest"),
    ("logo", "标志", "entity_alphatest"),
    ("train_announcer", "列车播报器", "entity_alphatest"),
    ("tactile_map", "盲文地图", "entity_alphatest"),
    ("rail", "轨道", "entity_alphatest"),
    ("ceiling", "天花板", "entity"),
    ("station_color", "站台颜色", "entity"),
]

os.makedirs(BEHAVIOR_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(TEXTURES_DIR, exist_ok=True)

# 1. Generate entity behavior definitions
for entity_type, _, _ in ENTITY_TYPES:
    entity_json = {
        "format_version": "1.10.0",
        "minecraft:entity": {
            "description": {
                "identifier": "mtr:" + entity_type,
                "is_spawnable": False,
                "is_summonable": False,
                "is_experimental": False
            },
            "components": {
                "minecraft:type_family": {
                    "family": ["mtr", "block_entity"]
                },
                "minecraft:physics": {
                    "has_gravity": False
                },
                "minecraft:collision_box": {
                    "width": 0.0,
                    "height": 0.0
                },
                "minecraft:pushable": {
                    "is_pushable": False,
                    "is_pushable_by_piston": False
                },
                "minecraft:damage_sensor": {
                    "triggers": {
                        "cause": "all",
                        "deals_damage": False
                    }
                },
                "minecraft:health": {
                    "value": 999999,
                    "max": 999999
                },
                "minecraft:nameable": {
                    "allow_name_tag_renaming": False
                },
                "minecraft:persistent": {},
                "minecraft:fire_immune": True
            }
        }
    }
    filepath = os.path.join(BEHAVIOR_DIR, entity_type + ".json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(entity_json, f, indent=2, ensure_ascii=False)
    print("  Created entity: " + filepath)

# 2. Generate model template files
for entity_type, _, _ in ENTITY_TYPES:
    model_json = {
        "format_version": "1.12.0",
        "minecraft:geometry": [
            {
                "description": {
                    "identifier": "geometry.mtr." + entity_type,
                    "texture_width": 64,
                    "texture_height": 64,
                    "visible_bounds_width": 2,
                    "visible_bounds_height": 3,
                    "visible_bounds_offset": [0, 1.5, 0]
                },
                "bones": [
                    {
                        "name": "root",
                        "pivot": [0, 0, 0],
                        "cubes": []
                    }
                ]
            }
        ]
    }
    filepath = os.path.join(MODELS_DIR, entity_type + ".geo.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(model_json, f, indent=2, ensure_ascii=False)
    print("  Created model: " + filepath)

# 3. Update entity.json
print("\n[3/3] Updating entity.json...")
if os.path.exists(ENTITY_JSON):
    with open(ENTITY_JSON, "r", encoding="utf-8") as f:
        entity_data = json.load(f)
else:
    entity_data = {"format_version": [1, 19, 0]}

for entity_type, _, material in ENTITY_TYPES:
    key = "mtr:" + entity_type
    if key not in entity_data:
        entity_data[key] = {
            "minecraft:client_entity": {
                "description": {
                    "identifier": "mtr:" + entity_type,
                    "materials": {
                        "default": material
                    },
                    "geometry": {
                        "default": "geometry.mtr." + entity_type
                    },
                    "textures": {
                        "default": "textures/entity/" + entity_type
                    },
                    "render_controllers": ["controller.render.default"],
                    "scripts": {
                        "animate": []
                    }
                }
            }
        }
        print("  Added entity: " + key)

with open(ENTITY_JSON, "w", encoding="utf-8") as f:
    json.dump(entity_data, f, indent=2, ensure_ascii=False)

print("\nComplete! Created %d entity types" % len(ENTITY_TYPES))
print("  Entities: " + BEHAVIOR_DIR)
print("  Models: " + MODELS_DIR)
print("  entity.json: " + ENTITY_JSON)