#! /usr/bin/env python
from random import choice

class RandomSet:
    '''``RandomSet`` class, which is a set with random (rather than arbitrary) pop'''
    def __init__(self, initial=None):
        '''``RandomSet`` constructor
        
        Args:
            ``initial`` (iterable): Elements with which to initialize the ``RandomSet``
        '''
        self.elements = list() # list of elements
        self.index = dict() # index[element] = index at which `element` appears in `self.elements`
        if initial is not None:
            for x in initial:
                self.add(x)

    def __contains__(self, x):
        '''Check if an element ``x`` exists in this ``RandomSet``

        Args:
            ``x``: The element to check

        Returns:
            ``bool``: ``True`` if ``x`` exists in this ``RandomSet``, otherwise ``False``
        '''
        return x in self.index

    def __iter__(self):
        ''' Iterate over the elements of this ``RandomSet``'''
        for x in self.elements:
            yield x

    def __len__(self):
        '''Return the number of elements in this ``RandomSet``

        Returns:
            ``int``: The number of elements contained within this ``RandomSet``
        '''
        return len(self.elements)

    def __str__(self):
        '''Return a string representation of this ``RandomSet``

        Returns:
            ``str``: A string representation of this ``RandomSet``
        '''
        return str(self.elements)

    def add(self, x):
        '''Add a new element ``x`` to this ``RandomSet``

        Args:
            ``x``: The element to insert
        '''
        if x in self:
            raise ValueError("Element already exists: %s"%x)
        self.index[x] = len(self); self.elements.append(x)

    def remove(self, x):
        '''Remove the element ``x`` from this ``RandomSet``

        Args:
            ``x``: The element to remove
        '''
        if x not in self:
            raise ValueError("Element not found: %s"%x)
        x_index = self.index[x]
        self.elements[x_index] = self.elements[-1]; self.index[self.elements[-1]] = x_index
        self.elements.pop(); del self.index[x]

    def top_random(self):
        '''Randomly return an element from this ``RandomSet``

        Returns:
            A random element from this ``RandomSet``
        '''
        return choice(self.elements)

    def pop_random(self):
        '''Randomly remove and return an element from this ``RandomSet``

        Returns:
            A random element from this ``RandomSet``
        '''
        x = self.top_random(); self.remove(x)
        return x
