# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import json
import glob

# Remove minecraft:material_instances from all netease_blocks files
# because texture files are missing

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
            content = f.read()
        
        data = json.loads(content)
        
        # Check if material_instances exists
        if "minecraft:block" in data:
            components = data["minecraft:block"].get("components", {})
            if "minecraft:material_instances" in components:
                del components["minecraft:material_instances"]
                data["minecraft:block"]["components"] = components
                
                # Write back with pretty formatting
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                    f.write("\n")
                fixed_count += 1
                print("Fixed: " + filename)
            else:
                print("Skipped (no material_instances): " + filename)
        else:
            print("Skipped (no minecraft:block): " + filename)
            
    except Exception as e:
        error_count += 1
        print("ERROR in " + filename + ": " + str(e))

print("=" * 60)
print("Done! Fixed: " + str(fixed_count) + ", Errors: " + str(error_count))