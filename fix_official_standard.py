# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import json
import glob
import shutil

base_dir = os.path.dirname(os.path.abspath(__file__))
bp = os.path.join(base_dir, "mtr_netease", "behavior_pack")
rp = os.path.join(base_dir, "mtr_netease", "resource_pack")
rp_textures = os.path.join(rp, "textures")
rp_blocks_textures = os.path.join(rp_textures, "blocks")
bp_blocks = os.path.join(bp, "netease_blocks")
bp_textures_blocks = os.path.join(bp, "textures", "blocks")

print("=" * 60)
print("FIX 1: format_version 1.19.40 -> 1.10.0")
print("       components: destructible_by_mining -> destroy_time")
print("       components: destructible_by_explosion -> explosion_resistance")
print("       remove: material_instances (not in official docs)")
print("       remove: is_experimental (not in official docs)")
print("=" * 60)

json_files = glob.glob(os.path.join(bp_blocks, "*.json"))
fixed_count = 0

for filepath in json_files:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        block = data.get("minecraft:block", {})
        desc = block.get("description", {})
        components = block.get("components", {})
        
        changed = False
        
        if data.get("format_version") == "1.19.40":
            data["format_version"] = "1.10.0"
            changed = True
        
        if "is_experimental" in desc:
            del desc["is_experimental"]
            changed = True
        
        if "minecraft:destructible_by_mining" in components:
            old_val = components["minecraft:destructible_by_mining"]
            components["minecraft:destroy_time"] = {
                "value": old_val.get("seconds_to_destroy", 1.5)
            }
            del components["minecraft:destructible_by_mining"]
            changed = True
        
        if "minecraft:destructible_by_explosion" in components:
            old_val = components["minecraft:destructible_by_explosion"]
            components["minecraft:explosion_resistance"] = {
                "value": old_val.get("explosion_resistance", 6.0)
            }
            del components["minecraft:destructible_by_explosion"]
            changed = True
        
        if "minecraft:material_instances" in components:
            del components["minecraft:material_instances"]
            changed = True
        
        if changed:
            data["minecraft:block"]["description"] = desc
            data["minecraft:block"]["components"] = components
            
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.write("\n")
            fixed_count += 1
            
    except Exception as e:
        print("ERROR: " + os.path.basename(filepath) + ": " + str(e))

print("Fixed " + str(fixed_count) + " block definition files")

print("")
print("=" * 60)
print("FIX 2: Ensure blocks.json in resource_pack (NOT behavior_pack)")
print("=" * 60)

src_bj = os.path.join(bp, "blocks.json")
dst_bj = os.path.join(rp, "blocks.json")

if os.path.exists(src_bj):
    shutil.copy2(src_bj, dst_bj)
    os.remove(src_bj)
    print("Moved blocks.json to resource_pack")
elif os.path.exists(dst_bj):
    print("blocks.json already in resource_pack - OK")
else:
    print("WARNING: blocks.json not found!")

print("")
print("=" * 60)
print("FIX 3: Generate terrain_texture.json in resource_pack/textures/")
print("=" * 60)

texture_data = {}
if os.path.exists(rp_blocks_textures):
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
print("FIX 4: Create texts/zh_CN.lang in behavior_pack")
print("=" * 60)

texts_dir = os.path.join(bp, "texts")
if not os.path.exists(texts_dir):
    os.makedirs(texts_dir)

lang_path = os.path.join(texts_dir, "zh_CN.lang")
if not os.path.exists(lang_path):
    with open(lang_path, "w", encoding="utf-8") as f:
        for filepath in json_files:
            try:
                with open(filepath, "r", encoding="utf-8") as jf:
                    data = json.load(jf)
                identifier = data.get("minecraft:block", {}).get("description", {}).get("identifier", "")
                if identifier:
                    short = identifier.replace("mtr:", "")
                    display = short.replace("_", " ").title()
                    f.write("tile." + identifier + ".name=" + display + "\n")
            except:
                pass
    print("Created: " + lang_path)
else:
    print("texts/zh_CN.lang already exists - OK")

print("")
print("=" * 60)
print("FIX 5: Copy textures to behavior_pack/textures/blocks/")
print("=" * 60)

if not os.path.exists(bp_textures_blocks):
    os.makedirs(bp_textures_blocks)

count = 0
if os.path.exists(rp_blocks_textures):
    for fname in os.listdir(rp_blocks_textures):
        src_file = os.path.join(rp_blocks_textures, fname)
        dst_file = os.path.join(bp_textures_blocks, fname)
        if os.path.isfile(src_file) and fname.endswith(".png"):
            shutil.copy2(src_file, dst_file)
            count += 1

print("Copied " + str(count) + " PNG files")

print("")
print("=" * 60)
print("ALL FIXES APPLIED!")
print("")
print("Changes made:")
print("  1. format_version: 1.19.40 -> 1.10.0 (per official docs)")
print("  2. destructible_by_mining -> destroy_time (per official docs)")
print("  3. destructible_by_explosion -> explosion_resistance (per official docs)")
print("  4. Removed material_instances (not in official docs)")
print("  5. Removed is_experimental (not in official docs)")
print("  6. blocks.json in resource_pack (per official docs)")
print("  7. terrain_texture.json in resource_pack/textures/ (per official docs)")
print("  8. texts/zh_CN.lang in behavior_pack (per official docs)")
print("  9. Textures copied to behavior_pack (dual assurance)")
print("=" * 60)