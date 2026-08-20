# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import json
import glob

# Fix all netease_blocks JSON files
# Issues:
# 1. format_version "1.10.0" -> "1.19.40" (required by minecraft:material_instances)
# 2. "minecraft:explosion_resistance": 6.0 -> "minecraft:destructible_by_explosion": {"explosion_resistance": 6.0}
# 3. "minecraft:destroy_time": 1.5 -> "minecraft:destructible_by_mining": {"seconds_to_destroy": 1.5}
#    (not strictly required by error, but format_version upgrade expects it)

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
        
        original = content
        
        # Fix 1: format_version
        content = content.replace('"format_version": "1.10.0"', '"format_version": "1.19.40"')
        
        # Fix 2: minecraft:explosion_resistance (number -> object)
        # Pattern: "minecraft:explosion_resistance": 6.0
        content = content.replace(
            '"minecraft:explosion_resistance": 6.0',
            '"minecraft:destructible_by_explosion": {"explosion_resistance": 6.0}'
        )
        
        # Fix 3: minecraft:destroy_time (number -> object)
        # Pattern: "minecraft:destroy_time": 1.5
        content = content.replace(
            '"minecraft:destroy_time": 1.5',
            '"minecraft:destructible_by_mining": {"seconds_to_destroy": 1.5}'
        )
        
        if content != original:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            fixed_count += 1
            print("Fixed: " + filename)
        else:
            print("Skipped (no changes): " + filename)
            
    except Exception as e:
        error_count += 1
        print("ERROR in " + filename + ": " + str(e))

print("=" * 60)
print("Done! Fixed: " + str(fixed_count) + ", Errors: " + str(error_count))