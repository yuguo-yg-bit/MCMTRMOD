# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import json
import glob
import shutil

base_dir = os.path.dirname(os.path.abspath(__file__))
rp_textures = os.path.join(base_dir, "mtr_netease", "resource_pack", "textures")
blocks_dir = os.path.join(base_dir, "mtr_netease", "behavior_pack", "netease_blocks")
bp_textures = os.path.join(base_dir, "mtr_netease", "behavior_pack", "textures", "blocks")
rp_blocks_textures = os.path.join(rp_textures, "blocks")

print("=" * 60)
print("Step 1: Generate terrain_texture.json in resource_pack/textures/")
print("=" * 60)

texture_data = {}

for fname in os.listdir(rp_blocks_textures):
    if fname.endswith(".png"):
        short_name = fname.replace(".png", "")
        texture_data[short_name] = {
            "textures": "textures/blocks/" + fname
        }

terrain_json_path = os.path.join(rp_textures, "terrain_texture.json")
terrain_json = {
    "resource_pack_name": "vanilla",
    "texture_name": "atlas.terrain",
    "padding": 8,
    "num_mip_levels": 4,
    "texture_data": texture_data
}

with open(terrain_json_path, "w", encoding="utf-8") as f:
    json.dump(terrain_json, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("Created: " + terrain_json_path)
print("Total texture entries: " + str(len(texture_data)))

print("")
print("=" * 60)
print("Step 2: Restore material_instances in netease_blocks/*.json")
print("=" * 60)

json_files = glob.glob(os.path.join(blocks_dir, "*.json"))
added = 0

for filepath in json_files:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        identifier = data.get("minecraft:block", {}).get("description", {}).get("identifier", "")
        if not identifier:
            continue
        
        texture_name = identifier.replace("mtr:", "")
        
        components = data.get("minecraft:block", {}).get("components", {})
        
        if "minecraft:material_instances" not in components:
            components["minecraft:material_instances"] = {
                "*": {
                    "texture": texture_name,
                    "render_method": "opaque"
                }
            }
            data["minecraft:block"]["components"] = components
            added += 1
            
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.write("\n")
    except Exception as e:
        print("ERROR: " + os.path.basename(filepath) + ": " + str(e))

print("Restored material_instances in " + str(added) + " files")

print("")
print("=" * 60)
print("Step 3: Copy textures to behavior_pack/textures/blocks/")
print("=" * 60)

if not os.path.exists(bp_textures):
    os.makedirs(bp_textures)
    print("Created: " + bp_textures)

count = 0
for fname in os.listdir(rp_blocks_textures):
    src_file = os.path.join(rp_blocks_textures, fname)
    dst_file = os.path.join(bp_textures, fname)
    if os.path.isfile(src_file) and fname.endswith(".png"):
        shutil.copy2(src_file, dst_file)
        count += 1

print("Copied " + str(count) + " PNG files to behavior_pack/textures/blocks/")

print("")
print("=" * 60)
print("ALL DONE! Deploy in MC Studio and test.")
print("=" * 60)