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