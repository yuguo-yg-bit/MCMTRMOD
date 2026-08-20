# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import json
import glob

base_dir = os.path.dirname(os.path.abspath(__file__))
blocks_dir = os.path.join(base_dir, "mtr_netease", "behavior_pack", "netease_blocks")

json_files = glob.glob(os.path.join(blocks_dir, "*.json"))
print("Found " + str(len(json_files)) + " block definition files")

removed = 0
for filepath in json_files:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        components = data.get("minecraft:block", {}).get("components", {})
        if "minecraft:material_instances" in components:
            del components["minecraft:material_instances"]
            data["minecraft:block"]["components"] = components
            removed += 1
            
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.write("\n")
            print("REMOVED material_instances from: " + os.path.basename(filepath))
    except Exception as e:
        print("ERROR: " + os.path.basename(filepath) + ": " + str(e))

print("\nDone! Removed material_instances from " + str(removed) + " files")
print("Now engine will use blocks.json textures field for texture lookup")