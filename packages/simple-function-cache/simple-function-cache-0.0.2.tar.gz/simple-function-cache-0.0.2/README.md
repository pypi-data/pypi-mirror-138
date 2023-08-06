# Redis Cache

Cache model results decorator with redis.

#### example

```python
from simple_cache import build_cache

REDIS_CONFIG = {
    "host": "host of redis clusters",
    "port": 6379,
    "password": "password of redis clusters"
}
algo_model_cache = build_cache(db=99, config_json=REDIS_CONFIG)


if __name__ == '__main__':
    from simplex_sdk import SimplexClient
    from hashlib import md5
    import json


    def content_md5(data):
        """计算data的MD5值，经过Base64编码并返回str类型。

        返回值可以直接作为HTTP Content-Type头部的值
        """
        if isinstance(data, str):
            data = data.encode(encoding='utf-8')

        m = md5(data)
        return m.hexdigest().upper()

    def key_calculate(model, data, namespace='production', **kwargs):
        data = json.dumps(data)
        return model + "_" + namespace + "_" + content_md5(data)

    def condition(model_result, model, data, namespace='production', **kwargs):
        if model_result.get('status', '') == 'SUCCESS':
            return True
        return False

    @algo_model_cache(cache_name="test", cache_mode='cache', expire=60, key_func=key_calculate, cache_condition_func=condition)
    def cache_function(cached_func, data, namespace='production', **kwargs):
        """算法"""
        model_result = cached_func(data, namespace)
        return model_result
    
    def func(data, namespace):
        data["result"] = "model_result"
        data["namespace"] = "namespace"
        return data

    input_data = {
        "task_id": "test_cache",
        "data": {
            "curtain_size": [
                1280,
                720
            ]
        }
    }

    result = cache_function(func, data=input_data, namespace='dev')
    print(result)

```

### 下载安装

`pip install simple-function-cache -i https://pypi.python.org/pypi`

环境需求：python>=3.7

#### 初始化

直接通过引入build_cache函数进行初始化，build_cache参数为(db, config_json=None)。db为所选redis的库名，config_json接受包括键为host,port,password的dict数据，安全起见不再提供默认连接。
例如：

`algo_model_cache = build_cache(db=99, config_json={xxx})`

注意：初始化仅在项目第一次引入时有效。同一个项目中，后续如需修改连接配置需要手动调用RedisSingleton中的清除实例操作，否则会始终调用到之前初始化的单例连接，导致传新的参数不生效。

#### Cache装饰器参数

| param        | type            |  description |
| ------------ | ---------------- | ------------ |
| cache_mode | string | 该参数决定装饰器装饰的函数是使用哪种缓存方式：cache、no_cache、refresh； |
| cache_name | string | 装饰器名字，用在缓存key值计算方式和缓存调用次数统计上 |
| key_func  | function | key值计算函数：输入和被装饰的函数一致，输出是一个字符串 |
| cache_condition_func | function | 决定是否要对结果进行缓存的函数，输入为被装饰函数的结果+被装饰函数的输入拼接的列表，输出为bool值，默认为始终返回true |
| expire | int | 缓存数据过期时间，单位为秒，默认3天 |


#### 被装饰函数中的预留参数

| param        | type            |  description |
| ------------ | ---------------- | ------------ |
| namespace | string | 表示被装饰函数的执行环境，默认值为None |
| cache_mode_ | string | 用于动态修改被装饰函数当前执行的cache_mode，强制覆盖装饰器参数，默认值为None |
