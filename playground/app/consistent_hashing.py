import hashlib
import bisect

class ConsistentHashRing:
    def __init__(self, nodes=None):
        self.ring = {}
        self.sorted_keys = []

        if nodes:
            for node in nodes:
                self.add_node(node)

    def _hash(self, key):
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)

    def add_node(self, node):
        hash_val = self._hash(node)
        self.ring[hash_val] = node
        bisect.insort(self.sorted_keys, hash_val)

    def remove_node(self, node):
        hash_val = self._hash(node)
        if hash_val in self.ring:
            del self.ring[hash_val]
            self.sorted_keys.remove(hash_val)

    def get_node(self, key):
        if not self.ring:
            return None

        hash_val = self._hash(key)
        idx = bisect.bisect(self.sorted_keys, hash_val) % len(self.sorted_keys)
        node_hash = self.sorted_keys[idx]
        return self.ring[node_hash]
