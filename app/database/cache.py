import redis

class RedisCache:
    def __init__(self):
        self.client = redis.StrictRedis(host='localhost', port=6379, db=0)

    def set(self, key, value, ex=None):
        self.client.set(key, value, ex)

    def get(self, key):
        return self.client.get(key)

    def delete(self, key):
        self.client.delete(key)

    def expire(self, key, ex):
        self.client.expire(key, ex)
