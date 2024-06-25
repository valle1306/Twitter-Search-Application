#!/usr/bin/env python
# coding: utf-8
# %%

# # Strategy
# 
# __Data to Cache__: based on the previous implementation for nonrelational and relational db, it seems like we should focus on caching popular hashtags and user data, which are frequently queried
# 
# __Cache Storage__: use python dict to store cached data, with keys and hashatgs or userIDs and values as the data objects
# 
# __Eviction policy__: implement an eviction policy such as '__Least recently used (LRU)__' to remove the least accessed items when the cache reaches its size limit
# 
# __Persistent__: Periodically serialize and save the state of the cache to disk. On startup, deserialize the data to restore the cache state
# 
# __Stale data handling__: entries in the cache can become stale if the dara in the db is updated. We need to implment a strategy to check for stale data and update/ rm as necessary
# 
# __Expiry mechanism__: Assign a time-to-live (TTL) to each cache entry. When an entry TTL expires, it should be considered for eviction.

# %%


import json
import time
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity, ttl, persistence_path):
        """ 
        The initializer method where the cache is instantiated.
        self.cache is an 'oderdict' that will store the cached items
        self.capcity is the maximum num of items that the cache can hold
        self.ttl is time-to-live in seconds, or how long an item should stay in the cache
        before it is considered expired. 
        self.persistence is a file path where the cache's state is saved for persistence
        """
        self.cache = OrderedDict()
        self.capacity = capacity
        self.ttl = ttl
        self.persistence_path = persistence_path

    def get(self, key):
        """
        Uses to retrieve an item from the cache. It checks if the key exists in the cache
        and if the corresponding item is not expired
        """
        if key in self.cache and not self.is_expired(key):
            self.cache.move_to_end(key)
            return self.cache[key]['data']
        # Handle miss: Retrieve from DB and update cache
        return None

    def put(self, key, value):
        """
        Add a new item to the cache or update an existing item
        If the key already exists in cache, it updates the item and moves it to the end
        of OrderDict
        If key doesn't exists, it adds item to the cache with current timestamp
        After adding new item, if cache exceeds its capacity, then evicts the LRU,
        which is the first item in OrderedDict
        """
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = {'data': value, 'timestamp': time.time()}
        if len(self.cache) > self.capacity:
            oldest = next(iter(self.cache))
            del self.cache[oldest]

    def is_expired(self, key):
        """
        Method would determine if a cached item is expired based on the timestamp
        on TTL
        Could be use to calculate the difference between current time and timestamp
        of the cache item, comparing it to TTL
        """
        return (time.time() - self.cache[key]['timestamp']) > self.ttl

    def evict(self):
        """
        Removes the LRU item from cache, which is first item in OrderDict
        """
        oldest = next(iter(self.cache))
        del self.cache[oldest]

    def persist(self):
        """
        Serializes the current state of the cache(key, value, timestamp) and 
        writes it to the 'persistence_path'
        Helps ensure that cahce can be restored to its last state if program restarts
        """
        with open(self.persistence_path, 'w') as f:
            json.dump({k: {'data': str(v['data']), 'timestamp': v['timestamp']} for k, v in self.cache.items()}, f)

    def restore(self):
        """
        Reads the state of the cache from persistence path and deserializes it to restore cache
        Can be called when program starts up to reload the cache with its most recent state
        """
        try:
            with open(self.persistence_path, 'r') as f:
                loaded_cache = json.load(f)
                self.cache = OrderedDict((k, {'data': v['data'], 'timestamp': v['timestamp']}) for k, v in loaded_cache.items())
        except FileNotFoundError:
            print("Cache file not found, starting with an empty cache.")
    def print_cache(self):
        # This method prints the current state of the cache
        print("Cache contents:")
        for key, value in self.cache.items():
            data = value['data']
            timestamp = value['timestamp']
            current_time = time.time()
            age = current_time - timestamp
            print(f"Key: {key}, Data: {data}, Timestamp: {timestamp}, Age: {age:.2f} seconds")
            
    def get_with_mongo_fallback(self, key):
        start_time = time.perf_counter()  # Change to use perf_counter
        data = super().get(key)  # Assuming super() refers to the parent class with the original get method
        if data is not None:
            # Cache hit, Log the performance
            end_time = time.perf_counter()  # Change to use perf_counter
            log_performance(start_time, end_time, "Cache hit", key, "hit")
        else:
            # Cache miss, fetch from MongoDB and then put it in the cache
            data = fetch_tweet_from_mongodb(key)  # This function should be defined elsewhere
            if data is not None:
                self.put(key, data)
            end_time = time.perf_counter()  # Change to use perf_counter
            log_performance(start_time, end_time, "MongoDB fetch", key, "miss")
        return data


cache = LRUCache(capacity=100, ttl=3600, persistence_path='cache.json')
cache.restore()

