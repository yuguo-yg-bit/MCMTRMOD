# -*- coding: utf-8 -*-
u"""终极修复脚本 V3 - 修复中文编码、方块模型、贴图映射"""
from __future__ import print_function
import os
import json
import glob
import sys

# Force UTF-8 output
if sys.version_info[0] >= 3:
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = os.path.dirname(os.path.abspath(__file__))
BP = os.path.join(BASE, "mtr_netease", "behavior_pack")
RP = os.path.join(BASE, "mtr_netease", "resource_pack")
NEB = os.path.join(BP, "netease_blocks")
BLOCKS_JSON = os.path.join(RP, "blocks.json")
TT_JSON = os.path.join(RP, "textures", "terrain_texture.json")
ZH_CN_LANG = os.path.join(BP, "texts", "zh_CN.lang")
MODEL_DIR = os.path.join(RP, "models", "netease_block")

print("=" * 60)
print("MTR Block Fix V3 - Ultimate Fix")
print("=" * 60)

# ============================================================
# 1. Fix zh_CN.lang encoding - MUST be UTF-8 without BOM
# ============================================================
print("\n[1/5] Fixing zh_CN.lang encoding to UTF-8...")

# Block name translations matching original MTR
TRANSLATIONS = {
    "rail": u"轨道",
    "boat_node": u"船节点",
    "cable_car_node_lower": u"缆车下层节点",
    "cable_car_node_station": u"缆车站台节点",
    "cable_car_node_upper": u"缆车上层节点",
    "airplane_node": u"飞机节点",
    "psd_door": u"屏蔽门",
    "psd_door_2": u"屏蔽门2",
    "psd_glass": u"屏蔽门玻璃",
    "psd_glass_2": u"屏蔽门玻璃2",
    "psd_glass_end": u"屏蔽门玻璃端",
    "psd_glass_end_2": u"屏蔽门玻璃端2",
    "psd_top": u"屏蔽门顶部",
    "apg_door": u"自动站台门",
    "apg_glass": u"自动站台门玻璃",
    "apg_glass_end": u"自动站台门玻璃端",
    "platform": u"站台",
    "platform_indented": u"站台(缩进)",
    "platform_slab": u"站台半砖",
    "platform_na_1": u"站台(北美1)",
    "platform_na_1_indented": u"站台(北美1缩进)",
    "platform_na_1_slab": u"站台半砖(北美1)",
    "platform_na_2": u"站台(北美2)",
    "platform_na_2_indented": u"站台(北美2缩进)",
    "platform_na_2_slab": u"站台半砖(北美2)",
    "platform_uk_1": u"站台(英国1)",
    "platform_uk_1_indented": u"站台(英国1缩进)",
    "platform_uk_1_slab": u"站台半砖(英国1)",
    "station_name_wall": u"站名牌(白)",
    "station_name_wall_gray": u"站名牌(灰)",
    "station_name_wall_black": u"站名牌(黑)",
    "station_name_entrance": u"站名入口牌",
    "station_name_tall_wall": u"高站名牌(墙)",
    "station_name_tall_block": u"高站名牌",
    "station_name_tall_block_double_sided": u"高站名牌(双面)",
    "station_name_tall_standing": u"高站名牌(立)",
    "route_sign_wall_light": u"线路牌(亮)",
    "route_sign_wall_metal": u"线路牌(金属)",
    "route_sign_standing_light": u"线路牌立式(亮)",
    "route_sign_standing_metal": u"线路牌立式(金属)",
    "ticket_machine": u"售票机",
    "ticket_processor": u"票务处理器",
    "ticket_processor_entrance": u"票务处理器(入口)",
    "ticket_processor_exit": u"票务处理器(出口)",
    "ticket_processor_enquiry": u"票务处理器(查询)",
    "ticket_barrier_entrance_1": u"闸机(入口)",
    "ticket_barrier_exit_1": u"闸机(出口)",
    "ticket_barrier_side_1": u"闸机(侧面)",
    "pids_1": u"乘客信息屏1",
    "pids_2": u"乘客信息屏2",
    "pids_3": u"乘客信息屏3",
    "pids_4": u"乘客信息屏4",
    "pids_top": u"乘客信息屏顶",
    "pids_top_2": u"乘客信息屏顶2",
    "pids_top_3": u"乘客信息屏顶3",
    "pids_top_4": u"乘客信息屏顶4",
    "pids_pole": u"乘客信息屏杆",
    "pids_single_arrival_1": u"单班到达屏",
    "arrival_projector_1_small": u"到站投影(小)",
    "arrival_projector_1_medium": u"到站投影(中)",
    "arrival_projector_1_large": u"到站投影(大)",
    "signal_light_1": u"信号灯(2灯1)",
    "signal_light_2": u"信号灯(2灯2)",
    "signal_light_3": u"信号灯(2灯3)",
    "signal_light_4": u"信号灯(2灯4)",
    "signal_light_3_aspect_1": u"信号灯(3灯1)",
    "signal_light_3_aspect_2": u"信号灯(3灯2)",
    "signal_light_4_aspect_1": u"信号灯(4灯1)",
    "signal_light_4_aspect_2": u"信号灯(4灯2)",
    "signal_semaphore_1": u"臂板信号机1",
    "signal_semaphore_2": u"臂板信号机2",
    "signal_pole": u"信号杆",
    "railway_sign_2_even": u"铁路标志(2偶)",
    "railway_sign_2_odd": u"铁路标志(2奇)",
    "railway_sign_3_even": u"铁路标志(3偶)",
    "railway_sign_3_odd": u"铁路标志(3奇)",
    "railway_sign_4_even": u"铁路标志(4偶)",
    "railway_sign_4_odd": u"铁路标志(4奇)",
    "railway_sign_5_even": u"铁路标志(5偶)",
    "railway_sign_5_odd": u"铁路标志(5奇)",
    "railway_sign_6_even": u"铁路标志(6偶)",
    "railway_sign_6_odd": u"铁路标志(6奇)",
    "railway_sign_7_even": u"铁路标志(7偶)",
    "railway_sign_7_odd": u"铁路标志(7奇)",
    "railway_sign_middle": u"铁路标志(中)",
    "railway_sign_pole": u"铁路标志杆",
    "ceiling": u"天花板",
    "ceiling_light": u"天花板(灯)",
    "ceiling_no_light": u"天花板(无灯)",
    "clock": u"时钟",
    "clock_pole": u"时钟杆",
    "escalator_side": u"扶梯侧板",
    "escalator_step": u"扶梯台阶",
    "lift_buttons_1": u"电梯按钮",
    "lift_door_1": u"电梯门",
    "lift_door_odd_1": u"电梯门(奇)",
    "lift_panel_even_1": u"电梯面板(偶1)",
    "lift_panel_odd_1": u"电梯面板(奇1)",
    "lift_panel_even_2": u"电梯面板(偶2)",
    "lift_panel_odd_2": u"电梯面板(奇2)",
    "lift_track_1": u"电梯轨道",
    "lift_track_diagonal_1": u"电梯轨道(斜)",
    "lift_track_floor_1": u"电梯轨道(地板)",
    "lift_track_horizontal_1": u"电梯轨道(横)",
    "station_color_andesite": u"站台颜色(安山岩)",
    "station_color_bedrock": u"站台颜色(基岩)",
    "station_color_birch_wood": u"站台颜色(桦木)",
    "station_color_bone_block": u"站台颜色(骨块)",
    "station_color_chiseled_quartz_block": u"站台颜色(錾制石英)",
    "station_color_chiseled_stone_bricks": u"站台颜色(錾制石砖)",
    "station_color_clay": u"站台颜色(粘土)",
    "station_color_coal_ore": u"站台颜色(煤矿石)",
    "station_color_cobblestone": u"站台颜色(圆石)",
    "station_color_concrete": u"站台颜色(混凝土)",
    "station_color_concrete_powder": u"站台颜色(混凝土粉末)",
    "station_color_cracked_stone_bricks": u"站台颜色(裂石砖)",
    "station_color_dark_prismarine": u"站台颜色(暗海晶石)",
    "station_color_diorite": u"站台颜色(闪长岩)",
    "station_color_gravel": u"站台颜色(砂砾)",
    "station_color_iron_block": u"站台颜色(铁块)",
    "station_color_metal": u"站台颜色(金属)",
    "station_color_mossy_stone_bricks": u"站台颜色(苔石砖)",
    "station_color_packed_ice": u"站台颜色(浮冰)",
    "station_color_planks": u"站台颜色(木板)",
    "station_color_polished_andesite": u"站台颜色(磨制安山岩)",
    "station_color_polished_diorite": u"站台颜色(磨制闪长岩)",
    "station_color_polished_granite": u"站台颜色(磨制花岗岩)",
    "station_color_prismarine": u"站台颜色(海晶石)",
    "station_color_purpur_block": u"站台颜色(紫珀块)",
    "station_color_purpur_pillar": u"站台颜色(紫珀柱)",
    "station_color_quartz_block": u"站台颜色(石英块)",
    "station_color_quartz_bricks": u"站台颜色(石英砖)",
    "station_color_quartz_pillar": u"站台颜色(石英柱)",
    "station_color_red_sandstone": u"站台颜色(红砂岩)",
    "station_color_sandstone": u"站台颜色(砂岩)",
    "station_color_smooth_quartz": u"站台颜色(平滑石英)",
    "station_color_smooth_stone": u"站台颜色(平滑石)",
    "station_color_snow": u"站台颜色(雪)",
    "station_color_stone": u"站台颜色(石头)",
    "station_color_stone_bricks": u"站台颜色(石砖)",
    "station_color_wool": u"站台颜色(羊毛)",
    "marble_blue": u"大理石(蓝)",
    "marble_blue_low": u"大理石(蓝矮)",
    "marble_blue_middle": u"大理石(蓝中)",
    "marble_blue_tall": u"大理石(蓝高)",
    "marble_blue_tile": u"大理石(蓝瓦)",
    "marble_blue_very_tall": u"大理石(蓝很高)",
    "marble_blue_very_very_tall": u"大理石(蓝极高)",
    "logo": u"Logo",
    "eye_candy": u"装饰",
    "resource_pack_creator": u"资源包制作器",
    "train_announcer": u"列车播报器",
    "train_schedule_sensor": u"列车调度传感器",
    "train_redstone_sensor": u"列车红石传感器",
    "train_redstone_sensor_2": u"列车红石传感器2",
    "train_cargo_loader": u"列车货物装载器",
    "train_cargo_unloader": u"列车货物卸载器",
}

# Read existing lang file (may be GBK encoded)
try:
    with open(ZH_CN_LANG, "rb") as f:
        raw_bytes = f.read()
    # Try to decode as UTF-8 first, then GBK
    try:
        old_content = raw_bytes.decode('utf-8')
    except:
        old_content = raw_bytes.decode('gbk', errors='replace')
except:
    old_content = ""

# Build new lang lines with proper keys
new_lines = []
seen = set()
for line in old_content.strip().split("\n"):
    line = line.strip()
    if not line:
        continue
    if "=" in line:
        key = line.split("=")[0]
        if key.startswith("tile.mtr:"):
            block_name = key.replace("tile.mtr:", "").replace(".name", "")
            if block_name in TRANSLATIONS:
                new_lines.append(u"tile.mtr:%s.name=%s" % (block_name, TRANSLATIONS[block_name]))
                seen.add(block_name)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

# Add any missing blocks
for block_name, translation in sorted(TRANSLATIONS.items()):
    if block_name not in seen:
        new_lines.append(u"tile.mtr:%s.name=%s" % (block_name, translation))

# CRITICAL: Write with UTF-8 encoding (NO BOM)
with open(ZH_CN_LANG, "w", encoding="utf-8") as f:
    f.write("\n".join(new_lines) + "\n")

print("  Written %d translations in UTF-8" % len(TRANSLATIONS))
print("  File saved to: %s" % ZH_CN_LANG)

# ============================================================
# 2. Fix blocks.json - ensure UTF-8 encoding
# ============================================================
print("\n[2/5] Fixing blocks.json encoding...")

with open(BLOCKS_JSON, "r", encoding="utf-8") as f:
    blocks_json = json.load(f)

with open(BLOCKS_JSON, "w", encoding="utf-8") as f:
    json.dump(blocks_json, f, indent=2, ensure_ascii=False)
print("  Re-saved with UTF-8 encoding")

# ============================================================
# 3. Fix terrain_texture.json - ensure UTF-8 encoding
# ============================================================
print("\n[3/5] Fixing terrain_texture.json encoding...")

with open(TT_JSON, "r", encoding="utf-8") as f:
    tt_json = json.load(f)

with open(TT_JSON, "w", encoding="utf-8") as f:
    json.dump(tt_json, f, indent=2, ensure_ascii=False)
print("  Re-saved with UTF-8 encoding")

# ============================================================
# 4. Fix model JSONs - add textures_descriptions, fix format
# ============================================================
print("\n[4/5] Fixing block model JSONs...")

model_files = [f for f in os.listdir(MODEL_DIR) if f.endswith('.json')]
fixed_models = 0

for fname in model_files:
    path = os.path.join(MODEL_DIR, fname)
    with open(path, "r", encoding="utf-8") as f:
        try:
            model = json.load(f)
        except:
            print("  SKIP (invalid JSON): %s" % fname)
            continue

    desc = model.get("netease:block_geometry", {}).get("description", {})
    
    # Add textures_descriptions if missing
    if "textures_descriptions" not in desc:
        textures = desc.get("textures", [])
        desc["textures_descriptions"] = []
        for t in textures:
            desc["textures_descriptions"].append({"width": 16, "length": 16})
    
    # Ensure use_ao is set (default true for non-slab blocks)
    if "use_ao" not in desc:
        desc["use_ao"] = True
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(model, f, indent=2, ensure_ascii=False)
    fixed_models += 1

print("  Fixed %d model JSONs" % fixed_models)

# ============================================================
# 5. Verify all behavior pack blocks have proper light_absorption
# ============================================================
print("\n[5/5] Verifying behavior pack block configs...")

# Load blocks.json to know which blocks have models
with open(BLOCKS_JSON, "r", encoding="utf-8") as f:
    blocks_json = json.load(f)
blocks_with_model = set(k for k, v in blocks_json.items() if "netease_model" in v)

bp_files = [f for f in os.listdir(NEB) if f.endswith('.json')]
fixed_blocks = 0

for fname in bp_files:
    path = os.path.join(NEB, fname)
    block_id = "mtr:" + fname.replace(".json", "")
    has_model = block_id in blocks_with_model
    
    with open(path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except:
            continue
    
    comp = data.get("minecraft:block", {}).get("components", {})
    modified = False
    
    # Blocks with custom models MUST have light_absorption = 0
    if has_model:
        if "minecraft:block_light_absorption" not in comp:
            comp["minecraft:block_light_absorption"] = {"value": 0}
            modified = True
        elif comp["minecraft:block_light_absorption"].get("value") != 0:
            comp["minecraft:block_light_absorption"]["value"] = 0
            modified = True
    
    if modified:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        fixed_blocks += 1

print("  Fixed %d behavior pack blocks" % fixed_blocks)
print()
print("=" * 60)
print("V3 Fix Complete!")
print("  - zh_CN.lang: UTF-8 encoding with %d translations" % len(TRANSLATIONS))
print("  - blocks.json: UTF-8 encoding")
print("  - terrain_texture.json: UTF-8 encoding")
print("  - %d model JSONs: added textures_descriptions" % fixed_models)
print("  - %d behavior blocks: ensured light_absorption=0" % fixed_blocks)
print("=" * 60)