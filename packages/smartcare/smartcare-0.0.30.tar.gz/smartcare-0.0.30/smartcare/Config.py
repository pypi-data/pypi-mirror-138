from pkg_resources import resource_filename, Requirement
class ConfigEnum():
    dict = {
        "IMAGE_HEIGHT": 128,
        "IMAGE_WIDTH": 128,
        "LOGS_FOLDER": "logs",
        "CNN_DEFAULT_MODEL": resource_filename(__name__, 'model/modelCNN-1605022224.h5')
    }
    def get(key):
        return ConfigEnum.dict[key]
    
    def set(key, value):
        if key in ConfigEnum.dict.keys():
            ConfigEnum.dict[key] = value

Config = ConfigEnum
