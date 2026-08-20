# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import json
import glob

base_dir = os.path.dirname(os.path.abspath(__file__))
blocks_dir = os.path.join(base_dir, "mtr_netease", "behavior_pack", "netease_blocks")

if not os.path.isdir(blocks_dir):
    print("ERROR: blocks directory not found: " + blocks_dir)
    exit(1)

json_files = glob.glob(os.path.join(blocks_dir, "*.json"))
print("Found " + str(len(json_files)) + " block definition files to fix")
print("=" * 60)

fixed_count = 0
error_count = 0

for filepath in json_files:
    filename = os.path.basename(filepath)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        identifier = data.get("minecraft:block", {}).get("description", {}).get("identifier", "")
        components = data.get("minecraft:block", {}).get("components", {})
        
        if not identifier:
            print("SKIP: " + filename + " (no identifier)")
            continue
        
        if "minecraft:material_instances" in components:
            print("SKIP: " + filename + " (already has textures)")
            continue
        
        texture_name = identifier.replace("mtr:", "")
        
        components["minecraft:material_instances"] = {
            "*": {
                "texture": texture_name,
                "render_method": "opaque"
            }
        }
        data["minecraft:block"]["components"] = components
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        
        fixed_count += 1
        print("Fixed: " + filename + " -> " + texture_name)
        
    except Exception as e:
        error_count += 1
        print("ERROR in " + filename + ": " + str(e))

print("=" * 60)
print("Done! Fixed: " + str(fixed_count) + ", Errors: " + str(error_count))