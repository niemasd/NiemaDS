#! /usr/bin/env python
from collections import deque
from gzip import open as gopen
WORD_IDENT = 'W'

class MWTNode:
    '''Node helper class for ``MultiwayTrie``'''
    def __init__(self):
        '''``MWTNode`` constructor'''
        self.word = None
        self.children = dict()
        self.parent = None

    def traverse_preorder(self):
        '''Traverse the nodes of this ``MultiwayTrie`` via preorder traversal starting at this node'''
        s = deque(); s.append((None, self))
        while len(s) != 0:
            curr = s.pop(); yield curr
            s.extend((k, curr[1].children[k]) for k in sorted(curr[1].children.keys(), reverse=True))

    def traverse_postorder(self):
        '''Traverse the nodes of this ``MultiwayTrie`` via postorder traversal starting at this node'''
        s1 = deque(); s2 = deque(); s1.append((None, self))
        while len(s1) != 0:
            curr = s1.pop(); s2.append(curr); s1.extend((k, curr[1].children[k]) for k in sorted(curr[1].children.keys(), reverse=True))
        while len(s2) != 0:
            yield s2.pop()

    def newick(self):
        '''Newick string conversion starting at this node
        
        Returns:
            ``str``: Newick string conversion starting at this node
        '''
        node_to_str = dict()
        for letter,node in self.traverse_postorder():
            if len(node.children) == 0:
                if node.word is None:
                    raise RuntimeError("Encountered a leaf that is not a word node")
                node_to_str[node] = letter + WORD_IDENT
            else:
                out = ['(']
                for c in node.children.values():
                    out.append(node_to_str[c])
                    out.append(',')
                    del node_to_str[c]
                out.pop() # trailing comma
                out.append(')')
                if node.parent is not None:
                    if node.word is None:
                        out.append(letter)
                    else:
                        out.append(letter + WORD_IDENT)
                node_to_str[node] = ''.join(out)
        return node_to_str[self]

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
        '''Return a Newick string representation of this ``MultiwayTrie``

        Returns:
            ``str``: A Newick string representation of this ``MultiwayTrie``
        '''
        return '%s;' % self.root.newick()

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
        for letter,node in self.root.traverse_preorder():
            if node.word is not None:
                yield node.word

    def iter_descending(self):
        '''Iterate over the elements of this ``MultiwayTrie`` in descending order'''
        for letter,node in self.root.traverse_postorder():
            if node.word is not None:
                yield node.word

    @staticmethod
    def read_tree_newick(newick):
        '''Read a tree from a Newick string or file

        Args:
            ``newick`` (``str``): Either a Newick string or the path to a Newick file (plain-text or gzipped)

        Returns:
            ``MultiwayTrie``: The Multiway Trie represented by ``newick``. If the Newick file has multiple trees (one per line), a ``list`` of ``Tree`` objects will be returned
        '''
        if not isinstance(newick, str):
            try:
                newick = str(newick)
            except:
                raise TypeError("newick must be a str")
        if newick.lower().endswith('.gz'): # gzipped file
            f = gopen(expanduser(newick)); ts = f.read().decode().strip(); f.close()
        elif isfile(expanduser(newick)): # plain-text file
            f = open(expanduser(newick)); ts = f.read().strip(); f.close()
        else:
            ts = newick.strip()
        lines = ts.splitlines()
        if len(lines) != 1:
            return [read_tree_newick(l) for l in lines]
        '''
        try:
            t = MultiwayTrie(); n = t.root; i = 0
            while i < len(ts):
                if ts[i] == '(':
                    c = MWTNode(); n.add_child(c); n = c
                elif ts[i] == ')':
                    n = n.parent
                elif ts[i] == ',':
                    n = n.parent; c = Node(); n.add_child(c); n = c
                elif ts[i] == ':':
                    i += 1; ls = ''
                    while ts[i] != ',' and ts[i] != ')' and ts[i] != ';':
                        ls += ts[i]; i += 1
                    n.edge_length = float(ls); i -= 1
                else:
                    label = ''
                    while ts[i] != ':' and ts[i] != ',' and ts[i] != ';' and ts[i] != ')':
                        label += ts[i]; i += 1
                    i -= 1; n.label = label
                i += 1
        except Exception as e:
            raise RuntimeError("Failed to parse string as Newick: %s"%ts)
        return t
        '''
        return None # not implemented yet
