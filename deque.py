from collections import deque

class DynDeque:
    def __init__(self, maxlen, iterable=None):
        """The deque can become smaller than the given max length,
        but not bigger."""
        self._deque = deque(maxlen=maxlen)
        self._maxlen = maxlen
        
        if iterable:
            for item in iterable:
                self.append(item)
    
    def resize(self, maxlen):
        """Resizes the deque to the given size and pops as many
        items as necessary to reach the new length"""
        self._maxlen = maxlen
        while len(self._deque) > maxlen:
            self._deque.pop()
    
    def append(self, item):
        if len(self._deque) == self._maxlen:
            self.popleft()
        self._deque.append(item)
    
    def appendleft(self, item):
        if len(self._deque) == self._maxlen:
            self.pop()
        self._deque.appendleft(item)
        
    def pop(self):
        return self._deque.pop()
        
    def popleft(self):
        return self._deque.popleft()
    
    def __iter__(self):
        return self._deque.__iter__()
    

class Deque:
    MIN_SIZE = 16
    def __init__(self, iterator=None, maxlen=0):
        self.r_start = 0
        self.r_insert = self.r_start
        self.l_start = 0
        self.l_insert = self.l_start
        self.size = 0
        self.maxlen = 0
        self.arr = []
        if maxlen:
            self._reserve(maxlen)
            self.l_start = maxlen - 1
            self.l_insert = self.l_start
        
        if iterator is not None:
            for item in iterator:
                self.append(item)
    
    def _reserve(self, count):
        while len(self.arr) < count:
            self.arr.append(None)
    
    def _resize(self, size):
        arr = [None for i in size]
        si = self.r_start
        i = 0
        while si != self.r_insert:
            arr[i] = self.arr[si]
            si = (si + 1) % len(self.arr)
            i += 1
        self.r_start = 0
        self.r_insert = i
        
        si = self.l_start
        i = size - 1
        while si != self.l_insert:
            arr[i] = self.arr[si]
            si = (si - 1) % len(self.arr)
            i -= 1
        self.l_start = size - 1
        self.l_insert = i
        self.arr = arr
    
    def _check_resize_up(self):
        if self.size == 0:
            self._reserve(self.MIN_SIZE)
            self.l_start = self.MIN_SIZE - 1
            self.l_insert = self.l_start
        elif not self.maxlen:
            if self.size == len(self.arr):
                self._resize(self.size * 2)
    
    def append(self, item):
        self._check_resize_up()
        
        if self.maxlen:
            if self.size == self.maxlen:
                self.popleft()
        
        self.arr[self.r_insert] = item
        self.r_insert = (self.r_insert + 1) % len(self.arr)
        self.size += 1
    
    def appendleft(self, item):
        self._check_resize_up()
        
        if self.maxlen:
            if self.size == self.maxlen:
                self.pop()
        
        self.arr[self.l_insert] = item
        self.l_insert = (self.l_insert - 1) % len(self.arr)
        self.size += 1
    
    def pop(self):
        if self.size == 0:
            raise IndexError("pop from empty queue")
    
    def popleft(self):
        if self.size == 0:
            raise IndexError("pop from empty queue")
    
    def __iter__(self):
        i = self.start
        while i != self.end:
            yield self.arr[i]
            i = (i + 1) % len(self.arr)