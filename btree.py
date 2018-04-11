'''
http://opendatastructures.org/versions/edition-0.1g/ods-python/14_2_B_Trees.html
https://ysangkok.github.io/js-clrs-btree/btree.html
'''
class BTree:
  VISITED = set([])

  def __init__(self, order=None, root=None):
    self.order = order or 1
    self.root = root or Node()

  def __repr__(self):
    ret = "- [id:" + str(self.root.id) + "] "
    ret += ", ".join(map(str, self.root.keys))
    ret += "\n"
    BTree.VISITED = set([])
    for child in self.root.children:
      ret += self._repr_dfs(child)
    return ret

  def _repr_dfs(self, node, depth=0):
    depth += 1
    ret = ""
    ret += "  " * depth + "- [id:" + str(node.id) + "] "
    ret += ", ".join(map(str, node.keys))
    ret += "\n"
    BTree.VISITED.add(node.id)
    for child in node.children:
      if not child.id in BTree.VISITED:
        ret += self._repr_dfs(child, depth)
    return ret


class Node:
  COUNT = 1

  def __init__(self, children=None, keys=None):
    self.id = Node.COUNT
    self.children = children or []
    self.keys = keys or []
    Node.COUNT += 1


tree = BTree(order=5, \
  root=Node(keys=[10], children=[\
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
    ])]))

print(tree)
