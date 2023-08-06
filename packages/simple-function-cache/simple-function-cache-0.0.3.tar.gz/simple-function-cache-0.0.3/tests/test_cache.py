import unittest


class MyTestCase(unittest.TestCase):

    def test_model_cache(self):
        from simple_cache import build_cache
        from hashlib import md5
        import json

        REDIS_CONFIG = {
            "host": 'hostname',
            "password": "password",
            "port": 6379
        }
        algo_model_cache = build_cache(db=99, config_json=REDIS_CONFIG)

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

        @algo_model_cache(cache_name="test", cache_mode='cache', expire=300, key_func=key_calculate, cache_condition_func=condition)
        def retry_simplex(model, data, namespace='production', **kwargs):
            """算法"""
            model_result = {
                "status": "SUCCESS",
                "model": model,
                "namespace": namespace,
                "data": data
            }
            return model_result

        input_data = {
            "task_id": "test1111",
            "data": {
                "curtain_size": [
                    1280,
                    720
                ],
                "function": "overlay"
            }
        }
        try:
            result = retry_simplex('ffmpeg-render-slow-process', data=input_data, namespace='dev')
            print(result)
        except Exception as e:
            pass

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
