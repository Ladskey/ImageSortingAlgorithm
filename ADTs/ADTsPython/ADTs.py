import math, sys

# |----------------------------- Binary Min-Heap Priority Queue -----------------------------|

class Priority_Queue_Entry:   
    def __init__(self, item, priority):
        self.item = item
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority

class Priority_Queue:
    def __init__(self, array=None):
        if array is None:
            self._entries = []
        else:
            self._entries = array
            self._heapify()

    def _parent(self, i):
        return (i - 1) // 2

    def _children(self, i):
        left = 2 * i + 1
        right = 2 * i + 2
        return range(left, min(len(self._entries), right + 1))

    def _smallest_child(self, i):
        heap = self._entries
        children = self._children(i)
        if children:
            return min(children, key=lambda x: heap[x])
        return None

    def _heapify_up(self, i):
        heap = self._entries
        parent = self._parent(i)
        if i > 0 and heap[i] < heap[parent]:
            heap[i], heap[parent] = heap[parent], heap[i]
            self._heapify_up(parent)

    def _heapify_down(self, i):
        heap = self._entries
        child = self._smallest_child(i)
        if child and heap[child] < heap[i]:
            heap[i], heap[child] = heap[child], heap[i]
            self._heapify_down(child)

    def insert(self, item, priority):
        self._entries.append(Priority_Queue_Entry(item, priority))
        self._heapify_up(len(self._entries) - 1)

    def find_min(self):
        return self._entries[0].item

    def remove_min(self):
        heap = self._entries
        item = heap[0].item
        heap[0] = heap[-1]
        heap.pop()
        self._heapify_down(0)
        return item

    def _heapify(self):
        n = len(self._entries)
        last_inner = n // 2 - 1
        for i in range(last_inner, -1, -1):
            self._heapify_down(i)

    def __len__(self):
        return len(self._entries)

# |----------------------------- Hash Mapping -----------------------------|

class Entry:
    def __init__(self, key, value):
        self.key = key
        self.value = value

class Hash_Mapping:
    def __init__(self):
        self.n_buckets = 100
        self._L = [[] for i in range(self.n_buckets)]
        self._len = 0

    def __setitem__(self, key, value):
        bucket = self.hash(key)

        # Case 1: item in mapping
        for entry in self._L[bucket]:
            if entry.key == key:
                entry.value = value
                return
    
        # Case 2: item not in mapping
        self._L[bucket].append(Entry(key, value))
        self._len += 1
        if len(self) > self.n_buckets: self.rehash()

    def hash(self, key):
        return key % self.n_buckets

    def __getitem__(self, key):
        bucket = self.hash(key)
        for entry in self._L[bucket]:
            if entry.key == key: return entry.value
        raise KeyError("key {} not in Mapping".format(key))
        
    def rehash(self):
        self.n_buckets *= 2
        new_L = [[] for i in range(self.n_buckets)]
        
        # move all items to new list
        for bucket in self._L:
            for entry in bucket:
                new_bucket = self.hash(entry.key)
                new_L[new_bucket].append(entry)

        self._L = new_L[:]
    
    def __len__(self):
        return(self._len)
