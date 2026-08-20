# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import json

base_dir = os.path.dirname(os.path.abspath(__file__))
rp = os.path.join(base_dir, "mtr_netease", "resource_pack")
tt_path = os.path.join(rp, "textures", "terrain_texture.json")

print("Fix: Remove .png extension from terrain_texture.json paths")
print("=" * 60)

with open(tt_path, "r", encoding="utf-8") as f:
    data = json.load(f)

changed = 0
for key, val in data.get("texture_data", {}).items():
    old = val.get("textures", "")
    if old.endswith(".png"):
        new = old[:-4]
        val["textures"] = new
        changed += 1
        print("  " + old + " -> " + new)

data["texture_data"] = data.get("texture_data", {})

with open(tt_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("")
print("Fixed " + str(changed) + " entries")
print("")
print("Official docs format: \"textures\": \"textures/blocks/test0\"")
print("(NO .png extension!)")
print("=" * 60)