# -*- coding: utf-8 -*-
"""
Convert MTR Java block models (models/block/*.json) to NetEase geo.json format.
Java format: elements[from/to] in 1/16 block units
NetEase format: cubes[origin/size] in block units, bone pivot at [0,0,0] (center-base)

Key mapping:
  Java "from": [x1, y1, z1]  ->  NetEase "origin": [x1/16 - 0.5, y1/16, z1/16 - 0.5]
  Java "to":   [x2, y2, z2]  ->  NetEase "size":   [(x2-x1)/16, (y2-y1)/16, (z2-z1)/16]

Groups related block parts (like ticket_machine_bottom + ticket_machine_top) into one model.
"""

import os
import json
import re
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BLOCK_MODELS_DIR = os.path.join(
    BASE_DIR, "Minecraft-Transit-Railway-master",
    "fabric", "src", "main", "resources", "assets", "mtr", "models", "block"
)
OUTPUT_DIR = os.path.join(BASE_DIR, "mtr_netease", "resource_pack", "models", "entity")

NETEASE_BLOCK_TYPES = {
    "apg_door": {
        "netease_type": "apg_door",
        "size_hint": [16, 24, 2],
        "category": "door",
        "name_cn": "APG门",
    },
    "apg_glass": {
        "netease_type": "apg_glass",
        "size_hint": [16, 24, 1],
        "category": "door",
        "name_cn": "APG玻璃",
    },
    "apg_glass_end": {
        "netease_type": "apg_glass_end",
        "size_hint": [2, 24, 16],
        "category": "door",
        "name_cn": "APG玻璃端",
    },
    "psd_door": {
        "netease_type": "psd_door",
        "size_hint": [16, 32, 2],
        "category": "door",
        "name_cn": "屏蔽门",
    },
    "psd_glass": {
        "netease_type": "psd_glass",
        "size_hint": [16, 32, 1],
        "category": "door",
        "name_cn": "屏蔽门玻璃",
    },
    "psd_glass_end": {
        "netease_type": "psd_glass_end",
        "size_hint": [2, 32, 16],
        "category": "door",
        "name_cn": "屏蔽门玻璃端",
    },
    "psd_top": {
        "netease_type": "psd_top",
        "size_hint": [16, 4, 16],
        "category": "door",
        "name_cn": "屏蔽门顶部",
    },
    "signal_light": {
        "netease_type": "signal_light",
        "size_hint": [6, 12, 6],
        "category": "signal",
        "name_cn": "信号灯",
    },
    "signal_semaphore": {
        "netease_type": "signal_light",
        "size_hint": [6, 24, 6],
        "category": "signal",
        "name_cn": "臂板信号机",
    },
    "signal_pole": {
        "netease_type": "signal_light",
        "size_hint": [2, 16, 2],
        "category": "signal",
        "name_cn": "信号灯杆",
    },
    "pids": {
        "netease_type": "pids",
        "size_hint": [16, 12, 2],
        "category": "display",
        "name_cn": "PIDS显示屏",
    },
    "pids_top": {
        "netease_type": "pids",
        "size_hint": [16, 4, 16],
        "category": "display",
        "name_cn": "PIDS顶部",
    },
    "pids_pole": {
        "netease_type": "pids",
        "size_hint": [2, 16, 2],
        "category": "display",
        "name_cn": "PIDS杆",
    },
    "station_name": {
        "netease_type": "station_name",
        "size_hint": [16, 4, 1],
        "category": "sign",
        "name_cn": "站名牌",
    },
    "station_name_tall": {
        "netease_type": "station_name",
        "size_hint": [2, 32, 16],
        "category": "sign",
        "name_cn": "高站名牌",
    },
    "station_name_entrance": {
        "netease_type": "station_name",
        "size_hint": [16, 12, 2],
        "category": "sign",
        "name_cn": "入口站名牌",
    },
    "station_pole": {
        "netease_type": "station_name",
        "size_hint": [2, 16, 2],
        "category": "sign",
        "name_cn": "站名牌杆",
    },
    "railway_sign": {
        "netease_type": "railway_sign",
        "size_hint": [2, 12, 12],
        "category": "sign",
        "name_cn": "铁路标志",
    },
    "route_sign": {
        "netease_type": "route_sign",
        "size_hint": [12, 6, 2],
        "category": "sign",
        "name_cn": "线路标志",
    },
    "clock": {
        "netease_type": "clock",
        "size_hint": [8, 8, 2],
        "category": "display",
        "name_cn": "时钟",
    },
    "clock_pole": {
        "netease_type": "clock",
        "size_hint": [2, 16, 2],
        "category": "display",
        "name_cn": "时钟杆",
    },
    "ticket_machine": {
        "netease_type": "ticket_machine",
        "size_hint": [16, 16, 10],
        "category": "machine",
        "name_cn": "售票机",
    },
    "ticket_processor": {
        "netease_type": "ticket_machine",
        "size_hint": [10, 16, 10],
        "category": "machine",
        "name_cn": "检票机",
    },
    "ticket_barrier": {
        "netease_type": "ticket_barrier",
        "size_hint": [6, 16, 12],
        "category": "machine",
        "name_cn": "闸机",
    },
    "lift_door": {
        "netease_type": "lift_door",
        "size_hint": [16, 32, 2],
        "category": "lift",
        "name_cn": "电梯门",
    },
    "lift_panel": {
        "netease_type": "lift_panel",
        "size_hint": [4, 8, 2],
        "category": "lift",
        "name_cn": "电梯面板",
    },
    "lift_buttons": {
        "netease_type": "lift_panel",
        "size_hint": [4, 8, 2],
        "category": "lift",
        "name_cn": "电梯按钮",
    },
    "lift_track": {
        "netease_type": "lift_track",
        "size_hint": [2, 2, 16],
        "category": "lift",
        "name_cn": "电梯轨道",
    },
    "train_sensor": {
        "netease_type": "train_sensor",
        "size_hint": [4, 4, 4],
        "category": "sensor",
        "name_cn": "列车传感器",
    },
    "train_announcer": {
        "netease_type": "train_announcer",
        "size_hint": [4, 6, 4],
        "category": "sensor",
        "name_cn": "列车广播器",
    },
    "rubbish_bin": {
        "netease_type": "eye_candy",
        "size_hint": [6, 10, 6],
        "category": "decor",
        "name_cn": "垃圾桶",
    },
    "glass_fence": {
        "netease_type": "glass_fence",
        "size_hint": [1, 16, 16],
        "category": "decor",
        "name_cn": "玻璃护栏",
    },
    "escalator": {
        "netease_type": "escalator_side",
        "size_hint": [16, 16, 2],
        "category": "escalator",
        "name_cn": "扶梯",
    },
    "tactile_map": {
        "netease_type": "eye_candy",
        "size_hint": [16, 1, 16],
        "category": "decor",
        "name_cn": "触觉地图",
    },
    "station_color": {
        "netease_type": "station_color",
        "size_hint": [16, 16, 16],
        "category": "building",
        "name_cn": "车站颜色方块",
    },
    "platform": {
        "netease_type": "platform",
        "size_hint": [16, 8, 16],
        "category": "building",
        "name_cn": "站台",
    },
    "logo": {
        "netease_type": "logo",
        "size_hint": [8, 4, 1],
        "category": "sign",
        "name_cn": "Logo",
    },
    "ceiling": {
        "netease_type": "ceiling",
        "size_hint": [16, 1, 16],
        "category": "building",
        "name_cn": "天花板",
    },
    "rail": {
        "netease_type": "rail",
        "size_hint": [16, 1, 2],
        "category": "rail",
        "name_cn": "轨道",
    },
    "eye_candy": {
        "netease_type": "eye_candy",
        "size_hint": [8, 8, 8],
        "category": "decor",
        "name_cn": "装饰品",
    },
}

os.makedirs(OUTPUT_DIR, exist_ok=True)

def java_to_netease_cube(element):
    x1, y1, z1 = element["from"]
    x2, y2, z2 = element["to"]

    origin = [
        round(x1 / 16.0 - 0.5, 4),
        round(y1 / 16.0, 4),
        round(z1 / 16.0 - 0.5, 4),
    ]
    size = [
        round((x2 - x1) / 16.0, 4),
        round((y2 - y1) / 16.0, 4),
        round((z2 - z1) / 16.0, 4),
    ]

    return {
        "origin": origin,
        "size": size,
        "uv": [0, 0],
        "mirror": False,
        "inflate": 0.0,
    }

def load_block_model(model_name):
    model_path = os.path.join(BLOCK_MODELS_DIR, model_name + ".json")
    if not os.path.exists(model_path):
        return None
    try:
        with open(model_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print("  WARN: Cannot read %s: %s" % (model_name, str(e)))
        return None

def group_block_models():
    all_files = [f for f in os.listdir(BLOCK_MODELS_DIR) if f.endswith(".json")]
    groups = defaultdict(list)

    for filename in all_files:
        name = filename[:-5]
        groups["__all__"].append(name)

    return groups

def build_geo_json(entity_type, elements, texture_size=(64, 64)):
    return {
        "format_version": "1.12.0",
        "minecraft:geometry": [
            {
                "description": {
                    "identifier": "geometry.mtr." + entity_type,
                    "texture_width": texture_size[0],
                    "texture_height": texture_size[1],
                },
                "bones": [
                    {
                        "name": "root",
                        "pivot": [0.0, 0.0, 0.0],
                        "cubes": [java_to_netease_cube(e) for e in elements],
                    }
                ],
            }
        ],
    }

def main():
    print("=" * 60)
    print("MTR Java Block Model -> NetEase geo.json Converter")
    print("=" * 60)

    all_files = sorted(f for f in os.listdir(BLOCK_MODELS_DIR) if f.endswith(".json"))
    print("\nFound %d block model files" % len(all_files))

    processed = {}
    for filename in all_files:
        model_name = filename[:-5]
        model = load_block_model(model_name)
        if model is None:
            continue
        elements = model.get("elements", [])
        if not elements:
            continue
        processed[model_name] = elements

    print("Loaded %d models with geometry" % len(processed))

    # Group models by entity type
    entity_models = defaultdict(list)

    for model_name, elements in processed.items():
        found = False
        for prefix, info in sorted(NETEASE_BLOCK_TYPES.items(), key=lambda x: -len(x[0])):
            if model_name.startswith(prefix):
                if model_name == prefix or model_name.startswith(prefix + "_"):
                    entity_models[info["netease_type"]].append((model_name, elements))
                    found = True
                    break
        if not found:
            print("  UNMATCHED: %s" % model_name)

    # Generate geo.json for each entity type
    generated = 0
    for entity_type, model_parts in entity_models.items():
        all_elements = []
        for model_name, elements in model_parts:
            all_elements.extend(elements)

        if not all_elements:
            continue

        geo_json = build_geo_json(entity_type, all_elements)

        output_path = os.path.join(OUTPUT_DIR, entity_type + ".geo.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(geo_json, f, indent=2, ensure_ascii=False)

        info = NETEASE_BLOCK_TYPES.get(
            next((k for k, v in NETEASE_BLOCK_TYPES.items() if v["netease_type"] == entity_type), ""),
            {}
        )
        print("  [%s] %s <- %d parts (%d cubes)" % (
            entity_type,
            info.get("name_cn", "?"),
            len(model_parts),
            len(all_elements),
        ))
        generated += 1

    print("\nGenerated %d geo.json models" % generated)
    print("Output: " + OUTPUT_DIR)

    # Also generate a simple model for any entity types that had no block model matches
    all_entity_types = set(info["netease_type"] for info in NETEASE_BLOCK_TYPES.values())
    missing = all_entity_types - set(entity_models.keys())
    if missing:
        print("\nMissing models (no block geometry found, using simple cube):")
        for et in sorted(missing):
            info = next((v for v in NETEASE_BLOCK_TYPES.values() if v["netease_type"] == et), None)
            if info is None:
                continue
            size_hint = info["size_hint"]
            cube = {
                "origin": [
                    round(size_hint[0] / 32.0 - 0.5, 4),
                    round(0.0, 4),
                    round(size_hint[2] / 32.0 - 0.5, 4),
                ],
                "size": [
                    round(size_hint[0] / 16.0, 4),
                    round(size_hint[1] / 16.0, 4),
                    round(size_hint[2] / 16.0, 4),
                ],
                "uv": [0, 0],
                "mirror": False,
                "inflate": 0.0,
            }
            geo_json = build_geo_json(et, [{"from": [0, 0, 0], "to": size_hint}])
            # Actually rebuild properly
            geo_json["minecraft:geometry"][0]["bones"][0]["cubes"] = [cube]

            output_path = os.path.join(OUTPUT_DIR, et + ".geo.json")
            if not os.path.exists(output_path):
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(geo_json, f, indent=2, ensure_ascii=False)
                print("  [%s] %s (placeholder)" % (et, info.get("name_cn", "?")))

    print("\nDone!")

if __name__ == "__main__":
    main()