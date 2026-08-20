# -*- coding: utf-8 -*-
# Scan actual netease_blocks directory and add netease:block_entity to all blocks
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BLOCKS_DIR = os.path.join(BASE_DIR, "mtr_netease", "behavior_pack", "netease_blocks")

count = 0
skip_count = 0

for filename in os.listdir(BLOCKS_DIR):
    if not filename.endswith(".json"):
        continue

    block_path = os.path.join(BLOCKS_DIR, filename)
    with open(block_path, "r", encoding="utf-8") as f:
        block_data = json.load(f)

    components = block_data.get("minecraft:block", {}).get("components", {})
    if "netease:block_entity" in components:
        skip_count += 1
        continue

    components["netease:block_entity"] = {"tick": True}
    count += 1

    with open(block_path, "w", encoding="utf-8") as f:
        json.dump(block_data, f, indent=2, ensure_ascii=False)

print("Added block_entity to %d blocks (skipped %d already set)" % (count, skip_count))