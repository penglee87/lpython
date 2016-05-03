class Node:
    def __init__(self, value):
        self._value = value
        self._children = []

    def __str__(self):  # !r打印时保留引号
        return 'Node({!r})'.format(self._value)
    """    
    def __str__(self):
        return 'Node({!s})'.format(self._value)
    """
    def add_child(self, node):
        self._children.append(node)

    def __iter__(self):
        return iter(self._children)

# Example
if __name__ == '__main__':
    root = Node(0)
    child1 = Node('m')
    child2 = Node('2')
    root.add_child(child1)
    root.add_child(child2)
    # Outputs Node(1), Node(2)
    for ch in root:
        print(ch)

"""
#print()打印__str__
>>> class Pair:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return 'Pair({0.x!r}, {0.y!r})'.format(self)
    def __str__(self):
        return '({0.x!s}, {0.y!s})'.format(self)

>>> p = Pair(3, 4)
>>> p
Pair(3, 4)
>>> print(p)
(3, 4)


>>> "repr() shows quotes: {!r}; str() doesn't: {!s}".format('test1', 'test2')
"repr() shows quotes: 'test1'; str() doesn't: test2"
"""