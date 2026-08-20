# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import shutil

base_dir = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(base_dir, "mtr_netease", "resource_pack", "textures", "blocks")
dst = os.path.join(base_dir, "mtr_netease", "behavior_pack", "textures", "blocks")

if not os.path.exists(dst):
    os.makedirs(dst)
    print("Created: " + dst)

count = 0
for fname in os.listdir(src):
    src_file = os.path.join(src, fname)
    dst_file = os.path.join(dst, fname)
    if os.path.isfile(src_file) and fname.endswith(".png"):
        shutil.copy2(src_file, dst_file)
        count += 1

print("Copied " + str(count) + " PNG files to behavior_pack/textures/blocks/")