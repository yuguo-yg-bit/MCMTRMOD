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
print("Found " + str(len(json_files)) + " block definition files")

blocks_json = {}
texture_map = {}

for filepath in json_files:
    filename = os.path.basename(filepath)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        identifier = data.get("minecraft:block", {}).get("description", {}).get("identifier", "")
        if identifier:
            # Get texture name from material_instances
            components = data.get("minecraft:block", {}).get("components", {})
            mat_instances = components.get("minecraft:material_instances", {})
            texture = mat_instances.get("*", {}).get("texture", "")
            
            blocks_json[identifier] = {
                "sound": "stone"
            }
            if texture:
                blocks_json[identifier]["textures"] = texture
                texture_map[texture] = True
            
            print("  " + identifier + (" -> " + texture if texture else ""))
    except Exception as e:
        print("ERROR reading " + filename + ": " + str(e))

# Write blocks.json
blocks_path = os.path.join(base_dir, "mtr_netease", "behavior_pack", "blocks.json")
with open(blocks_path, "w", encoding="utf-8") as f:
    json.dump(blocks_json, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("=" * 60)
print("Generated blocks.json with " + str(len(blocks_json)) + " blocks")
print("Texture names used: " + str(len(texture_map)))