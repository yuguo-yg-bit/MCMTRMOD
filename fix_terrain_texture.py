# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import json
import glob

base_dir = os.path.dirname(os.path.abspath(__file__))
blocks_dir = os.path.join(base_dir, "mtr_netease", "behavior_pack", "netease_blocks")
output_path = os.path.join(base_dir, "mtr_netease", "resource_pack", "terrain_texture.json")

json_files = glob.glob(os.path.join(blocks_dir, "*.json"))
print("Found " + str(len(json_files)) + " block definitions")

texture_data = {}
for filepath in json_files:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        tex = data.get("minecraft:block", {}).get("components", {}).get("minecraft:material_instances", {}).get("*", {}).get("texture", "")
        if tex:
            texture_data[tex] = {
                "textures": "textures/blocks/" + tex
            }
    except:
        pass

terrain_texture = {
    "resource_pack_name": "vanilla",
    "texture_name": "atlas.terrain",
    "padding": 8,
    "num_mip_levels": 4,
    "texture_data": texture_data
}

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(terrain_texture, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("Created terrain_texture.json with " + str(len(texture_data)) + " textures")
print("Output: " + output_path)