#! /usr/bin/env python
class DisjointSet:
    '''`DisjointSet` class, implemented using the Up-Tree data structure for amortized O(1) find and union operations'''
    def __init__(self):
        '''`DisjointSet` constructor'''
        self.parent = dict() # parent[u] = parent of node u
        self.num_below = dict() # num_below[u] = number of nodes below u (including u) (only current for sentinels)

    def __contains__(self,x):
        '''Check if an element `x` exists in this `DisjointSet`'''
        try:
            return x in self.parent
        except:
            return False

    def __len__(self):
        '''Return the number of elements in this `DisjointSet`'''
        return len(self.parent)

    def add(self,x): # add x as a sentinel node
        '''Add a new element `x` to this `DisjointSet` as a sentinel node'''
        if x in self:
            raise ValueError("Node already exists: %s"%x)
        self.parent[x] = None; self.num_below[x] = 1

    def remove(self,x):
        '''Remove the element `x` from this `DisjointSet`'''
        if x not in self:
            raise ValueError("Node not found: %s"%x)
        p = self.parent[x]
        if p is not None:
            p = self.parent[x]; self.num_below[p] -= 1
        for e in self.parent:
            if self.parent[e] == x:
                self.parent[e] = p
        del self.parent[x]; del self.num_below[x]

    def find(self,x):
        '''Return the sentinel node of the element `x`. Implements path compression along the search'''
        if x not in self:
            raise ValueError("Node not found: %s"%x)
        explored = Queue(); curr = x
        while self.parent[curr] is not None:
            explored.put(curr); curr = self.parent[curr]
        while not explored.empty():
            self.parent[explored.get()] = curr
        return curr

    def union(self,x,y): # union the sets containing x and y
        '''Union the sets containing `x` and `y`. Implements Union-By-Size'''
        if x not in self:
            raise ValueError("Node not found: %s"%x)
        if y not in self:
            raise ValueError("Node not found: %s"%y)
        sx = self.find(x); sy = self.find(y)
        if self.num_below[sx] > self.num_below[sy]:
            self.parent[sy] = sx; self.num_below[sx] += (self.num_below[sy] + 1)
        else:
            self.parent[sx] = sy; self.num_below[sy] += (self.num_below[sx] + 1)
