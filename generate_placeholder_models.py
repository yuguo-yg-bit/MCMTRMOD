# -*- coding: utf-8 -*-
# Generate placeholder geo.json models for block entity rendering
# These are simple placeholder cubes that will be replaced with real models later
# Each model represents the approximate shape of the block

import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "mtr_netease", "resource_pack", "models", "entity")

MODEL_DEFS = {
    "psd_door": {
        "size": [16, 32, 2],
        "offset": [0, 0, 7],
        "texture": [64, 64],
    },
    "psd_glass": {
        "size": [16, 32, 1],
        "offset": [0, 0, 7],
        "texture": [64, 64],
    },
    "psd_glass_end": {
        "size": [2, 32, 16],
        "offset": [7, 0, 0],
        "texture": [64, 64],
    },
    "psd_top": {
        "size": [16, 4, 16],
        "offset": [0, 28, 0],
        "texture": [64, 64],
    },
    "apg_door": {
        "size": [16, 24, 2],
        "offset": [0, 0, 7],
        "texture": [64, 64],
    },
    "apg_glass": {
        "size": [16, 24, 1],
        "offset": [0, 0, 7],
        "texture": [64, 64],
    },
    "apg_glass_end": {
        "size": [2, 24, 16],
        "offset": [7, 0, 0],
        "texture": [64, 64],
    },
    "signal_light": {
        "size": [4, 8, 4],
        "offset": [6, 4, 6],
        "texture": [32, 32],
    },
    "pids": {
        "size": [16, 12, 2],
        "offset": [0, 2, 7],
        "texture": [64, 32],
    },
    "station_name": {
        "size": [16, 4, 1],
        "offset": [0, 6, 7],
        "texture": [64, 16],
    },
    "railway_sign": {
        "size": [2, 12, 12],
        "offset": [7, 2, 0],
        "texture": [32, 32],
    },
    "route_sign": {
        "size": [12, 6, 2],
        "offset": [2, 4, 7],
        "texture": [32, 16],
    },
    "clock": {
        "size": [8, 8, 2],
        "offset": [4, 4, 7],
        "texture": [32, 32],
    },
    "ticket_machine": {
        "size": [8, 16, 6],
        "offset": [4, 0, 5],
        "texture": [32, 32],
    },
    "ticket_barrier": {
        "size": [6, 16, 12],
        "offset": [5, 0, 0],
        "texture": [32, 32],
    },
    "lift_door": {
        "size": [16, 32, 2],
        "offset": [0, 0, 7],
        "texture": [64, 64],
    },
    "lift_panel": {
        "size": [4, 8, 2],
        "offset": [6, 4, 7],
        "texture": [16, 32],
    },
    "lift_track": {
        "size": [2, 2, 16],
        "offset": [7, 7, 0],
        "texture": [16, 16],
    },
    "train_sensor": {
        "size": [4, 4, 4],
        "offset": [6, 6, 6],
        "texture": [16, 16],
    },
    "escalator_side": {
        "size": [16, 16, 2],
        "offset": [0, 0, 7],
        "texture": [64, 32],
    },
    "escalator_step": {
        "size": [16, 2, 16],
        "offset": [0, 0, 0],
        "texture": [64, 64],
    },
    "eye_candy": {
        "size": [8, 8, 8],
        "offset": [4, 4, 4],
        "texture": [32, 32],
    },
    "platform": {
        "size": [16, 8, 16],
        "offset": [0, 0, 0],
        "texture": [64, 64],
    },
    "glass_fence": {
        "size": [1, 16, 16],
        "offset": [7, 0, 0],
        "texture": [32, 32],
    },
    "rubbish_bin": {
        "size": [6, 10, 6],
        "offset": [5, 0, 5],
        "texture": [16, 16],
    },
    "logo": {
        "size": [8, 4, 1],
        "offset": [4, 6, 7],
        "texture": [32, 16],
    },
    "train_announcer": {
        "size": [4, 6, 4],
        "offset": [6, 4, 6],
        "texture": [16, 16],
    },
    "tactile_map": {
        "size": [16, 1, 16],
        "offset": [0, 0, 0],
        "texture": [64, 64],
    },
    "rail": {
        "size": [16, 1, 2],
        "offset": [0, 0, 7],
        "texture": [64, 16],
    },
    "ceiling": {
        "size": [16, 1, 16],
        "offset": [0, 15, 0],
        "texture": [64, 64],
    },
    "station_color": {
        "size": [16, 16, 16],
        "offset": [0, 0, 0],
        "texture": [64, 64],
    },
}

os.makedirs(MODELS_DIR, exist_ok=True)

for entity_type, defs in MODEL_DEFS.items():
    model_file = os.path.join(MODELS_DIR, entity_type + ".geo.json")
    if os.path.exists(model_file):
        with open(model_file, "r", encoding="utf-8") as f:
            model = json.load(f)
    else:
        model = {
            "format_version": "1.12.0",
            "minecraft:geometry": [
                {
                    "description": {
                        "identifier": "geometry.mtr." + entity_type,
                        "texture_width": 64,
                        "texture_height": 64,
                    },
                    "bones": []
                }
            ]
        }

    geo = model["minecraft:geometry"][0]
    geo["description"]["texture_width"] = defs["texture"][0]
    geo["description"]["texture_height"] = defs["texture"][1]

    size = defs["size"]
    offset = defs["offset"]

    cube = {
        "origin": [offset[0] / 16.0 * -1, offset[1] / 16.0 * -1, offset[2] / 16.0 * -1],
        "size": [size[0] / 16.0, size[1] / 16.0, size[2] / 16.0],
        "uv": [0, 0],
        "mirror": False,
        "inflate": 0.0,
    }

    if not geo["bones"]:
        geo["bones"].append({
            "name": "root",
            "pivot": [0.0, 0.0, 0.0],
            "cubes": []
        })
    else:
        geo["bones"][0]["cubes"] = []

    geo["bones"][0]["cubes"].append(cube)

    with open(model_file, "w", encoding="utf-8") as f:
        json.dump(model, f, indent=2, ensure_ascii=False)

    print("  Generated: " + entity_type + ".geo.json")

print("\nDone! Generated %d placeholder models" % len(MODEL_DEFS))
print("Models directory: " + MODELS_DIR)