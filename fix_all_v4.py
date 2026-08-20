#!/usr/bin/env python3
import os
import shutil
import json
import glob as glob_mod

BASE = r'd:\JRByuguo\jrb\MC地铁mod\mtr_netease'
RP = os.path.join(BASE, 'resource_pack')
BP = os.path.join(BASE, 'behavior_pack')

def copy_textures():
    src = os.path.join(RP, 'textures', 'item')
    dst = os.path.join(RP, 'textures', 'blocks')
    os.makedirs(dst, exist_ok=True)
    copied = 0
    for f in os.listdir(src):
        if f.endswith('.png'):
            src_path = os.path.join(src, f)
            dst_path = os.path.join(dst, f)
            if not os.path.exists(dst_path):
                shutil.copy2(src_path, dst_path)
                copied += 1
    print(f"Copied {copied} textures to textures/blocks/")

def fix_entity_json():
    entity_json_path = os.path.join(RP, 'entity.json')
    with open(entity_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for entity_id, entity_def in data.items():
        if 'minecraft:client_entity' not in entity_def:
            continue
        desc = entity_def['minecraft:client_entity']['description']
        if 'textures' not in desc:
            continue
        tex = desc['textures'].get('default', '')

        if tex.startswith('textures/entity/'):
            name = tex.replace('textures/entity/', '')
            vehicle_path = os.path.join(RP, 'textures', 'vehicle', name + '.png')
            if os.path.exists(vehicle_path):
                desc['textures']['default'] = 'textures/vehicle/' + name
                print(f"  Fixed {entity_id}: {tex} -> textures/vehicle/{name}")
            else:
                print(f"  WARN: {entity_id}: no vehicle texture for {name}")

        elif tex.startswith('textures/blocks/'):
            name = tex.replace('textures/blocks/', '')
            blocks_path = os.path.join(RP, 'textures', 'blocks', name + '.png')
            if not os.path.exists(blocks_path):
                item_path = os.path.join(RP, 'textures', 'item', name + '.png')
                if os.path.exists(item_path):
                    print(f"  OK: {entity_id}: {tex} exists in item/")
                else:
                    print(f"  MISSING: {entity_id}: {tex} - texture not found!")
            else:
                print(f"  OK: {entity_id}: {tex}")

    with open(entity_json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Fixed entity.json texture paths")

def create_items_json():
    items = {}

    block_entities = [
        'psd_door', 'psd_glass', 'psd_glass_end', 'psd_glass_end_2',
        'psd_glass_2', 'psd_door_2', 'psd_top',
        'apg_door', 'apg_glass', 'apg_glass_end',
        'signal_light_1', 'signal_light_2', 'signal_light_3', 'signal_light_4',
        'signal_light_3_aspect_1', 'signal_light_3_aspect_2',
        'signal_light_4_aspect_1', 'signal_light_4_aspect_2',
        'signal_semaphore_1', 'signal_semaphore_2',
        'pids_1', 'pids_2', 'pids_3', 'pids_4',
        'pids_single_arrival_1', 'pids_pole',
        'pids_top', 'pids_top_2', 'pids_top_3', 'pids_top_4',
        'station_name_wall', 'station_name_wall_black', 'station_name_wall_gray',
        'station_name_tall_wall', 'station_name_tall_standing',
        'station_name_tall_block', 'station_name_tall_block_double_sided',
        'station_name_entrance',
        'railway_sign_2_even', 'railway_sign_2_odd',
        'railway_sign_3_even', 'railway_sign_3_odd',
        'railway_sign_4_even', 'railway_sign_4_odd',
        'railway_sign_5_even', 'railway_sign_5_odd',
        'railway_sign_6_even', 'railway_sign_6_odd',
        'railway_sign_7_even', 'railway_sign_7_odd',
        'railway_sign_pole', 'railway_sign_middle',
        'route_sign_standing_metal', 'route_sign_standing_light',
        'route_sign_wall_metal', 'route_sign_wall_light',
        'clock', 'clock_pole',
        'ticket_machine', 'ticket_processor',
        'ticket_processor_entrance', 'ticket_processor_exit', 'ticket_processor_enquiry',
        'ticket_barrier_entrance_1', 'ticket_barrier_exit_1', 'ticket_barrier_side_1',
        'lift_door_1', 'lift_door_odd_1',
        'lift_panel_even_1', 'lift_panel_even_2',
        'lift_panel_odd_1', 'lift_panel_odd_2',
        'lift_buttons_1',
        'lift_track_1', 'lift_track_diagonal_1',
        'lift_track_floor_1', 'lift_track_horizontal_1',
        'train_schedule_sensor', 'train_redstone_sensor', 'train_redstone_sensor_2',
        'train_announcer', 'train_cargo_loader', 'train_cargo_unloader',
        'escalator_side', 'escalator_step',
        'eye_candy', 'platform', 'platform_indented', 'platform_slab',
        'platform_na_1', 'platform_na_1_indented', 'platform_na_1_slab',
        'platform_na_2', 'platform_na_2_indented', 'platform_na_2_slab',
        'platform_uk_1', 'platform_uk_1_indented', 'platform_uk_1_slab',
        'glass_fence', 'rubbish_bin', 'logo',
        'tactile_map', 'driver_key_dispenser',
        'rail', 'ceiling', 'ceiling_light', 'ceiling_no_light',
        'station_color', 'arrival_projector',
        'arrival_projector_1_small', 'arrival_projector_1_medium', 'arrival_projector_1_large',
        'marble_blue', 'marble_blue_low', 'marble_blue_middle',
        'marble_blue_tall', 'marble_blue_tile',
        'marble_blue_very_tall', 'marble_blue_very_very_tall',
        'airplane_node', 'boat_node',
        'cable_car_node_lower', 'cable_car_node_station', 'cable_car_node_upper',
        'resource_pack_creator',
    ]

    vehicles = [
        ('train_a320', 'A320'),
        ('train_a_train', 'A Train'),
        ('train_br_423', 'BR 423'),
        ('train_class_345', 'Class 345'),
        ('train_class_377', 'Class 377'),
        ('train_class_802', 'Class 802'),
        ('train_cm_stock', 'CM Stock'),
        ('train_c_train', 'C Train'),
        ('train_drl', 'DRL'),
        ('train_e44', 'E44'),
        ('train_eidan_9000', 'Eidan 9000'),
        ('train_kcr_christmas', 'KCR Christmas'),
        ('train_k_train', 'K Train'),
        ('train_light_rail', 'Light Rail'),
        ('train_london_underground_1938', 'London Underground 1938'),
        ('train_london_underground_1995', 'London Underground 1995'),
        ('train_london_underground_d78', 'London Underground D78'),
        ('train_london_underground_s7', 'London Underground S7'),
        ('train_mlr', 'MLR'),
        ('train_mpl_16', 'MPL 16'),
        ('train_mpl_85', 'MPL 85'),
        ('train_m_train', 'M Train'),
        ('train_r179', 'R179'),
        ('train_r211', 'R211'),
        ('train_r_train', 'R Train'),
        ('train_s700', 'S700'),
        ('train_sp1900', 'SP1900'),
        ('train_s_train', 'S Train'),
        ('boat_medium', 'Medium Boat'),
        ('boat_small', 'Small Boat'),
        ('cable_car_grip', 'Cable Car Grip'),
        ('cable_car_ngong_ping_360', 'Ngong Ping 360'),
        ('lift_1', 'Lift'),
        ('minecart', 'Minecart'),
    ]

    for block_name in block_entities:
        item_name = 'mtr:' + block_name
        block_tex_path = os.path.join(RP, 'textures', 'blocks', block_name + '.png')
        item_tex_path = os.path.join(RP, 'textures', 'item', block_name + '.png')
        icon_name = block_name
        if os.path.exists(block_tex_path) or os.path.exists(item_tex_path):
            items[item_name] = {
                "category": "Construction",
                "icon": icon_name,
                "max_stack_size": 64
            }
        else:
            print(f"  MISSING block tex: {block_name}")

    for vehicle_id, vehicle_name in vehicles:
        item_name = 'mtr:' + vehicle_id
        items[item_name] = {
            "category": "Items",
            "icon": "train",
            "max_stack_size": 1,
            "custom_item_type": "egg"
        }

    items_path = os.path.join(BP, 'items.json')
    with open(items_path, 'w', encoding='utf-8') as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    print(f"Created items.json with {len(items)} items")

def fix_item_texture_json():
    item_tex_path = os.path.join(RP, 'textures', 'item_texture.json')
    texture_data = {}

    items_dir = os.path.join(RP, 'textures', 'item')
    if os.path.exists(items_dir):
        for f in os.listdir(items_dir):
            if f.endswith('.png'):
                name = f[:-4]
                texture_data[name] = {
                    "textures": "textures/item/" + name
                }

    data = {
        "resource_pack_name": "vanilla",
        "texture_name": "atlas.items",
        "texture_data": texture_data
    }

    with open(item_tex_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Created item_texture.json with {len(texture_data)} textures")

def fix_model_sizes():
    models_dir = os.path.join(RP, 'models', 'entity')
    model_scale_fixes = {
        'psd_door': {'scale': 2.0, 'axis': 'x'},
        'psd_glass': {'scale': 2.0, 'axis': 'x'},
        'psd_glass_end': {'scale': 2.0, 'axis': 'x'},
        'psd_door_2': {'scale': 2.0, 'axis': 'x'},
        'psd_glass_2': {'scale': 2.0, 'axis': 'x'},
        'psd_top': {'scale': 2.0, 'axis': 'x'},
        'apg_door': {'scale': 1.0, 'axis': 'x'},
        'apg_glass': {'scale': 1.0, 'axis': 'x'},
        'apg_glass_end': {'scale': 1.0, 'axis': 'x'},
        'rail': {'scale': 0.0625, 'axis': 'all'},
    }

    for model_name, fix in model_scale_fixes.items():
        model_path = os.path.join(models_dir, model_name + '.geo.json')
        if not os.path.exists(model_path):
            print(f"  SKIP model: {model_name} - not found")
            continue

        with open(model_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        scale = fix['scale']
        axis = fix['axis']

        for geom in data.get('minecraft:geometry', []):
            for bone in geom.get('bones', []):
                for cube in bone.get('cubes', []):
                    if axis == 'all':
                        cube['origin'] = [v * scale for v in cube['origin']]
                        cube['size'] = [v * scale for v in cube['size']]
                    elif axis == 'x':
                        cube['origin'][0] *= scale
                        cube['size'][0] *= scale
                    elif axis == 'y':
                        cube['origin'][1] *= scale
                        cube['size'][1] *= scale
                    elif axis == 'z':
                        cube['origin'][2] *= scale
                        cube['size'][2] *= scale

        with open(model_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"  Fixed model: {model_name} scale={scale} axis={axis}")

def fix_rail_model():
    model_path = os.path.join(RP, 'models', 'entity', 'rail.geo.json')
    if not os.path.exists(model_path):
        return

    with open(model_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for geom in data.get('minecraft:geometry', []):
        for bone in geom.get('bones', []):
            for cube in bone.get('cubes', []):
                cube['origin'] = [v / 16.0 for v in cube['origin']]
                cube['size'] = [v / 16.0 for v in cube['size']]

    with open(model_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Fixed rail model: Java units -> Bedrock units (divide by 16)")

def fix_terrain_texture():
    path = os.path.join(RP, 'textures', 'terrain_texture.json')
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    td = data.get('texture_data', {})
    for name, tex_def in td.items():
        if 'textures' in tex_def:
            tex_path = tex_def['textures']
            if tex_path.startswith('textures/blocks/'):
                block_name = tex_path.replace('textures/blocks/', '')
                blocks_path = os.path.join(RP, 'textures', 'blocks', block_name + '.png')
                item_path = os.path.join(RP, 'textures', 'item', block_name + '.png')
                if not os.path.exists(blocks_path) and os.path.exists(item_path):
                    print(f"  terrain_texture: {name} -> copying from item/")
                    shutil.copy2(item_path, blocks_path)

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Fixed terrain_texture.json")

if __name__ == '__main__':
    print("=== Step 1: Copy textures to blocks/ ===")
    copy_textures()

    print("\n=== Step 2: Fix terrain_texture.json ===")
    fix_terrain_texture()

    print("\n=== Step 3: Fix entity.json texture paths ===")
    fix_entity_json()

    print("\n=== Step 4: Fix model sizes ===")
    fix_model_sizes()

    print("\n=== Step 5: Fix rail model ===")
    fix_rail_model()

    print("\n=== Step 6: Create item_texture.json ===")
    fix_item_texture_json()

    print("\n=== Step 7: Create items.json ===")
    create_items_json()

    print("\n=== DONE ===")