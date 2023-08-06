from execredis import ExecMappingData
from tests.test_connection import redis_client


m = ExecMappingData(proj_name='test', redis_app=redis_client.redis)


class MappingData:
    PROJ_PREFIX = m.hget("PROJ_PREFIX", f"test.")
    not_setup_to_redis__ = "类变量名称含有双下划线不会存储到redis"


if __name__ == '__main__':
    pass
    # print(inspect.getfile(MappingData))
    # print(MappingData.PROJ_PREFIX)
    # m.redis_setup_all_mapping_data(MappingData)  # 所有变量MappingData上传到redis，双下划线变量除外
    m.redis_setup_mapping_data(MappingData, MappingData.PROJ_PREFIX)  # 单一变量上传到redis，双下划线变量除外
