from json import dumps, loads


class ExecMappingData:
    def __init__(self, proj_name, redis_app, redis_name_postfix='MappingData', logger_func=print):
        self.__proj_name = proj_name
        self.__name_postfix = redis_name_postfix
        self.__redis_app = redis_app
        self.__logger = logger_func
        self.__default_mapping_data = {}

    def hget(self, name: str, default_value):
        self.__default_mapping_data.update({name: default_value})
        return loads(self.__redis_app.hget(
            f"{self.__proj_name}." + self.__name_postfix, key=name.lower()) or b'null') or default_value

    def redis_setup_mapping_data(self, MappingData: type, mapping_data_default):
        default_value = mapping_data_default
        mapping_data = MappingData.__dict__
        name = list(mapping_data.keys())[list(mapping_data.values()).index(default_value)]
        default_value = self.__default_mapping_data[name]
        self.__setup_mapping_data(mapping_data, name, default_value)

    def redis_setup_all_mapping_data(self, MappingData: type, support_types=(list, int, dict, str)):
        flag = input(f'Will set all {self.__name_postfix} with default value on Redis. Y/N:')
        mapping_data = MappingData.__dict__
        if flag == 'Y':
            for k, v in self.__default_mapping_data.items():
                if "__" not in k and isinstance(v, support_types):
                    self.__setup_mapping_data(mapping_data, k, v)

    def __setup_mapping_data(self, mapping_data, name: str, value):
        hset_res = self.__hset_mapping_data(name.lower(), dumps(value))
        hset_num = 0 if dumps(value) == dumps(mapping_data[name]) else 1
        log = f"Setup {self.__proj_name}.{self.__name_postfix}.{name}: {hset_res or hset_num}"
        self.__logger(log)

    def __hset_mapping_data(self, key=None, value=None):
        return self.__redis_app.hset(f"{self.__proj_name}." + self.__name_postfix, key=key, value=value)
