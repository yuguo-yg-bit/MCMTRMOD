# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import json
import glob

base_dir = os.path.dirname(os.path.abspath(__file__))
blocks_dir = os.path.join(base_dir, "mtr_netease", "behavior_pack", "netease_blocks")

json_files = glob.glob(os.path.join(blocks_dir, "*.json"))
print("Found " + str(len(json_files)) + " block definition files")

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
            print("ADDED material_instances to: " + os.path.basename(filepath))
    except Exception as e:
        print("ERROR: " + os.path.basename(filepath) + ": " + str(e))

print("\nDone! Added material_instances to " + str(added) + " files")