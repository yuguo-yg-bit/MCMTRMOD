# -*- coding: utf-8 -*-
# MTR Core - Entity Definitions Module
# Converted from Java: EntityTypes.java, EntityRendering.java, EntityBase.java
# Entity type definitions and rendering entity configuration
# All entity types preserved from original Java MTR

# ==========================================
# Entity Types (from Java EntityTypes.java)
# ==========================================
ENTITY_TYPES = {
    "RENDERING": {
        "type": "rendering",
        "identifier": "mtr:rendering",
        "clientOnly": True,
        "summonable": False,
        "hasSpawnEgg": False,
    },
    "TRAIN": {
        "type": "train",
        "identifier": "mtr:train",
        "clientOnly": False,
        "summonable": False,
        "hasSpawnEgg": False,
    },
    "BOAT_VEHICLE": {
        "type": "boat",
        "identifier": "mtr:boat_vehicle",
        "clientOnly": False,
        "summonable": False,
        "hasSpawnEgg": False,
    },
    "CABLE_CAR": {
        "type": "cable_car",
        "identifier": "mtr:cable_car",
        "clientOnly": False,
        "summonable": False,
        "hasSpawnEgg": False,
    },
    "AIRPLANE": {
        "type": "airplane",
        "identifier": "mtr:airplane",
        "clientOnly": False,
        "summonable": False,
        "hasSpawnEgg": False,
    },
    "LIFT": {
        "type": "lift",
        "identifier": "mtr:lift",
        "clientOnly": False,
        "summonable": False,
        "hasSpawnEgg": False,
    },
}

# ==========================================
# Train Model Types (from Java vehicle model definitions)
# ==========================================
TRAIN_MODEL_TYPES = {
    "default": {
        "length": 20.0,
        "width": 2.9,
        "height": 3.5,
        "maxSpeed": 80.0,
        "acceleration": 0.5,
        "brakeForce": 1.0,
        "doorCount": 4,
        "doorWidth": 1.5,
        "doorHeight": 2.0,
        "passengerCapacity": 200,
        "modelPaths": {
            "train": "models/train/train.geo.json",
            "bogie": "models/train/bogie.geo.json",
            "door": "models/train/door.geo.json",
            "interior": "models/train/interior.geo.json",
        },
        "texturePaths": {
            "exterior": "textures/entity/train/exterior.png",
            "interior": "textures/entity/train/interior.png",
            "door": "textures/entity/train/door.png",
        },
    },
    "express": {
        "length": 25.0,
        "width": 2.9,
        "height": 3.5,
        "maxSpeed": 160.0,
        "acceleration": 0.8,
        "brakeForce": 1.5,
        "doorCount": 4,
        "doorWidth": 1.5,
        "doorHeight": 2.0,
        "passengerCapacity": 150,
        "modelPaths": {
            "train": "models/train/express.geo.json",
            "bogie": "models/train/bogie_express.geo.json",
            "door": "models/train/door_express.geo.json",
            "interior": "models/train/interior_express.geo.json",
        },
        "texturePaths": {
            "exterior": "textures/entity/train/express_exterior.png",
            "interior": "textures/entity/train/express_interior.png",
            "door": "textures/entity/train/express_door.png",
        },
    },
    "light_rail": {
        "length": 15.0,
        "width": 2.6,
        "height": 3.2,
        "maxSpeed": 60.0,
        "acceleration": 0.6,
        "brakeForce": 1.2,
        "doorCount": 3,
        "doorWidth": 1.4,
        "doorHeight": 1.9,
        "passengerCapacity": 120,
        "modelPaths": {
            "train": "models/train/light_rail.geo.json",
            "bogie": "models/train/bogie_light.geo.json",
            "door": "models/train/door_light.geo.json",
            "interior": "models/train/interior_light.geo.json",
        },
        "texturePaths": {
            "exterior": "textures/entity/train/light_rail_exterior.png",
            "interior": "textures/entity/train/light_rail_interior.png",
            "door": "textures/entity/train/light_rail_door.png",
        },
    },
    "metro": {
        "length": 18.0,
        "width": 2.8,
        "height": 3.3,
        "maxSpeed": 100.0,
        "acceleration": 0.7,
        "brakeForce": 1.3,
        "doorCount": 4,
        "doorWidth": 1.5,
        "doorHeight": 2.0,
        "passengerCapacity": 180,
        "modelPaths": {
            "train": "models/train/metro.geo.json",
            "bogie": "models/train/bogie_metro.geo.json",
            "door": "models/train/door_metro.geo.json",
            "interior": "models/train/interior_metro.geo.json",
        },
        "texturePaths": {
            "exterior": "textures/entity/train/metro_exterior.png",
            "interior": "textures/entity/train/metro_interior.png",
            "door": "textures/entity/train/metro_door.png",
        },
    },
    "high_speed": {
        "length": 25.0,
        "width": 2.9,
        "height": 3.8,
        "maxSpeed": 300.0,
        "acceleration": 1.0,
        "brakeForce": 2.0,
        "doorCount": 2,
        "doorWidth": 1.0,
        "doorHeight": 2.0,
        "passengerCapacity": 100,
        "modelPaths": {
            "train": "models/train/high_speed.geo.json",
            "bogie": "models/train/bogie_hs.geo.json",
            "door": "models/train/door_hs.geo.json",
            "interior": "models/train/interior_hs.geo.json",
        },
        "texturePaths": {
            "exterior": "textures/entity/train/high_speed_exterior.png",
            "interior": "textures/entity/train/high_speed_interior.png",
            "door": "textures/entity/train/high_speed_door.png",
        },
    },
    "cable_car": {
        "length": 8.0,
        "width": 2.0,
        "height": 2.5,
        "maxSpeed": 20.0,
        "acceleration": 0.3,
        "brakeForce": 0.5,
        "doorCount": 1,
        "doorWidth": 1.0,
        "doorHeight": 1.8,
        "passengerCapacity": 8,
        "modelPaths": {
            "train": "models/cable_car/cabin.geo.json",
            "door": "models/cable_car/door.geo.json",
            "interior": "models/cable_car/interior.geo.json",
        },
        "texturePaths": {
            "exterior": "textures/entity/cable_car/exterior.png",
            "interior": "textures/entity/cable_car/interior.png",
            "door": "textures/entity/cable_car/door.png",
        },
    },
    "boat": {
        "length": 15.0,
        "width": 4.0,
        "height": 3.0,
        "maxSpeed": 30.0,
        "acceleration": 0.2,
        "brakeForce": 0.3,
        "doorCount": 2,
        "doorWidth": 1.2,
        "doorHeight": 1.8,
        "passengerCapacity": 50,
        "modelPaths": {
            "train": "models/boat/ferry.geo.json",
            "door": "models/boat/door.geo.json",
            "interior": "models/boat/interior.geo.json",
        },
        "texturePaths": {
            "exterior": "textures/entity/boat/exterior.png",
            "interior": "textures/entity/boat/interior.png",
            "door": "textures/entity/boat/door.png",
        },
    },
    "airplane": {
        "length": 30.0,
        "width": 3.5,
        "height": 4.0,
        "maxSpeed": 200.0,
        "acceleration": 1.5,
        "brakeForce": 2.0,
        "doorCount": 2,
        "doorWidth": 1.0,
        "doorHeight": 1.8,
        "passengerCapacity": 150,
        "modelPaths": {
            "train": "models/airplane/plane.geo.json",
            "door": "models/airplane/door.geo.json",
            "interior": "models/airplane/interior.geo.json",
        },
        "texturePaths": {
            "exterior": "textures/entity/airplane/exterior.png",
            "interior": "textures/entity/airplane/interior.png",
            "door": "textures/entity/airplane/door.png",
        },
    },
}

# ==========================================
# Entity Factory
# ==========================================
class EntityFactory:
    @staticmethod
    def get_entity_type(identifier):
        for entity_type, config in ENTITY_TYPES.items():
            if config["identifier"] == identifier:
                return entity_type
        return None

    @staticmethod
    def get_train_model(train_type):
        return TRAIN_MODEL_TYPES.get(train_type, TRAIN_MODEL_TYPES["default"])

    @staticmethod
    def get_model_paths(train_type):
        model = TRAIN_MODEL_TYPES.get(train_type, TRAIN_MODEL_TYPES["default"])
        return model.get("modelPaths", {})

    @staticmethod
    def get_texture_paths(train_type):
        model = TRAIN_MODEL_TYPES.get(train_type, TRAIN_MODEL_TYPES["default"])
        return model.get("texturePaths", {})