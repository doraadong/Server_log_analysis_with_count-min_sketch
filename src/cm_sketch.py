

import sys
import random
import numpy as np
import heapq

class cm_sketch:

    BIG_PRIME = 9223372036854775783

    # setup data structures to store top K elements
    heap = []
    top_k ={} # map of key and entry [estimate, key] 

    def __init__(self, d, w, k):
        # setup variables specific to the instance
        self.w = w
        self.d = d
        self.k = k

        # setup data structures to store counts
        self.count = np.zeros((d, w), dtype='int32')

        self.hash_functions = [self.__generate_hash_function() for i in range(self.d)]

    def query(self,key):
        estimate = sys.maxsize
        for row, hash_function in enumerate(self.hash_functions):
            column = hash_function(abs(hash(key)))
            estimate = min(self.count[row, column], estimate)

        return estimate

    def __generate_hash_function(self):
        a, b = random.randrange(0, self.BIG_PRIME - 1), random.randrange(0, self.BIG_PRIME - 1)
        return lambda x: (a * x + b) % self.BIG_PRIME % self.w


    def update(self, key, weight):    
        for row, hash_function in enumerate(self.hash_functions):
            column = hash_function(abs(hash(key)))
            self.count[row, column] += weight

        self.update_heap(key)

    def update_heap(self,key):

        estimate = self.query(key)

        if not self.heap or estimate >= self.heap[0][0]:
            if key in self.top_k:
                entry = self.top_k.get(key)
                entry[0] = estimate
                heapq.heapify(self.heap)
            else:
                if len(self.top_k) < self.k:
                    heapq.heappush(self.heap, [estimate, key])
                    self.top_k[key] = [estimate, key]
                else:
                    new_entry = [estimate, key]
                    old_entry = heapq.heappushpop(self.heap, new_entry)
                    if old_entry[1] in self.top_k:
                        del self.top_k[old_entry[1]]
                        self.top_k[key] = new_entry
                    else:
                        pass