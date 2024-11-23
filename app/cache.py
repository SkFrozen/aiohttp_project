class MemoryCache:
    def __init__(self):
        self.cache = {}

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache[key] = value

    def delete(self, key):
        self.cache.pop(key, None)

    def clear(self):
        self.cache = {}


cache = MemoryCache()
