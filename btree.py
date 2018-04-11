'''
http://opendatastructures.org/versions/edition-0.1g/ods-python/14_2_B_Trees.html
https://ysangkok.github.io/js-clrs-btree/btree.html
'''
class BTree:
  VISITED = set([])

  def __init__(self, order=None, children=None, keys=None):
    self.order = order or 1
    self.children = children or []
    self.keys = keys or []

  def __repr__(self):
    ret = ""
    ret += ", ".join(map(str, self.keys))
    ret += "\n"
    BTree.VISITED = set([])
    for child in self.children:
      ret += self._dfs_repr(child)
    return ret

  def _dfs_repr(self, node, depth=0):
    depth += 1
    ret = ""
    ret += "  " * depth
    ret += "- "
    ret += ", ".join(map(str, node.keys))
    ret += "\n"
    BTree.VISITED.add(node.id)
    for child in node.children:
      if not child.id in BTree.VISITED:
        ret += self._dfs_repr(child, depth)
    return ret

#   def validate(self):


class Node:
  COUNT = 1

  def __init__(self, children=None, keys=None):
    self.id = Node.COUNT
    self.children = children or []
    self.keys = keys or []
    Node.COUNT += 1


tree = BTree(order=5, \
  keys=[10], children=[\
    Node(keys=[3,6], children=[\
      Node(keys=[0,1,2]), \
      Node(keys=[4,5]), \
      Node(keys=[7,8,9])\
    ]), \
    Node(keys=[14,17,21], children=[\
      Node(keys=[11,12,13]), \
      Node(keys=[15,16]), \
      Node(keys=[18,19,20]), \
      Node(keys=[22,23])\
    ])])

print(tree)
