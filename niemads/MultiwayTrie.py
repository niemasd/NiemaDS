#! /usr/bin/env python
from collections import deque

class MWTNode:
    '''Node helper class for ``MultiwayTrie``'''
    def __init__(self):
        '''``MWTNode`` constructor'''
        self.word = None
        self.children = dict()
        self.parent = None

class MultiwayTrie:
    '''``MultiwayTrie`` class, implemented using ``TreeSwift``'''
    def __init__(self, initial=None):
        '''``MultiwayTrie`` constructor
        
        Args:
            ``initial`` (iterable): Strings with which to initialize the ``MultiwayTrie``
        '''
        self.root = MWTNode(); self.num_elements = 0
        if initial is not None:
            self.extend(initial)

    def __contains__(self, x):
        '''Check if an element ``x`` exists in this ``MultiwayTrie``

        Args:
            ``x``: The element to check

        Returns:
            ``bool``: ``True`` if ``x`` exists in this ``MultiwayTrie``, otherwise ``False``
        '''
        if not isinstance(x, str):
            raise TypeError("Elements must be strings")
        curr = self.root
        for i in range(len(x)):
            if x[i] not in curr.children:
                return False
            curr = curr.children[x[i]]
        return (curr.word is not None)

    def __iter__(self):
        ''' Iterate over the elements of this ``MultiwayTrie`` in ascending order'''
        for x in self.iter_ascending():
            yield x

    def __len__(self):
        '''Return the number of elements in this ``MultiwayTrie``

        Returns:
            ``int``: The number of elements contained within this ``MultiwayTrie``
        '''
        return self.num_elements

    def __str__(self):
        '''Return a string representation of this ``MultiwayTrie``

        Returns:
            ``str``: A string representation of this ``MultiwayTrie``
        '''
        return str(list(self.iter_ascending()))

    def add(self, x):
        '''Add a new element ``x`` to this ``MultiwayTrie``

        Args:
            ``x``: The element to insert
        '''
        if not isinstance(x, str):
            raise TypeError("Elements must be strings")
        curr = self.root
        for i in range(len(x)):
            if x[i] not in curr.children:
                newnode = MWTNode(); curr.children[x[i]] = newnode; newnode.parent = curr
            curr = curr.children[x[i]]
        if curr.word is None:
            curr.word = x; self.num_elements += 1

    def extend(self, xs):
        '''Add each element of ``xs`` to this ``MultiwayTrie``

        Args:
            ``xs``: The elements to insert
        '''
        for x in xs:
            self.add(x)

    def remove(self, x):
        '''Remove the element ``x`` from this ``MultiwayTrie``

        Args:
            ``x``: The element to remove
        '''
        if not isinstance(x, str):
            raise TypeError("Elements must be strings")
        curr = self.root
        for i in range(len(x)):
            if x[i] not in curr.children:
                return
            curr = curr.children[x[i]]
        if curr.word is not None:
            curr.word = None; self.num_elements -= 1
            for i in range(len(x)-1, -1, -1):
                if len(curr.children) == 0:
                    curr = curr.parent; del curr.children[x[i]]
                else:
                    return

    def iter_ascending(self):
        '''Iterate over the elements of this ``MultiwayTrie`` in ascending order'''
        s = deque(); s.append(self.root)
        while len(s) != 0:
            curr = s.pop()
            if curr.word is not None:
                yield curr.word
            s.extend(curr.children[k] for k in sorted(curr.children.keys(), reverse=True))

    def iter_descending(self):
        '''Iterate over the elements of this ``MultiwayTrie`` in descending order'''
        s1 = deque(); s2 = deque(); s1.append(self.root)
        while len(s1) != 0:
            curr = s1.pop(); s2.append(curr); s1.extend(curr.children[k] for k in sorted(curr.children.keys(), reverse=True))
        while len(s2) != 0:
            curr = s2.pop()
            if curr.word is not None:
                yield curr.word
