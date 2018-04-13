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
    BTree.VISITED = set([])
    return self._repr_dfs(self.root)

  def _repr_dfs(self, node, depth=0):
    ret = ""
    ret += "  " * depth + "- "
    ret += ", ".join(map(str, node.keys))
#     ret += ", ".join(map(lambda e: str(e)+':'+node.data[e], node.keys))
    ret += "\n"
    BTree.VISITED.add(node.id)
    depth += 1
    for child in node.children:
      if not child.id in BTree.VISITED:
        ret += self._repr_dfs(child, depth)
    return ret


class Node:
  COUNT = 1

  def __init__(self, children=None, data=None):
    self.id = Node.COUNT
    self.children = children or []
    self.data = data or {}
    self.keys = list(data.keys())
    self.keys.sort()
    Node.COUNT += 1

  """
  keysからxを探索する。
  keys[i] == x となるiがあればそのiを返す。
  そうでなければ
  """
  def _(self, x):
    keysSet = set(self.keys)
    if x in keysSet:
      return self.keys.index(x)

    l = 0
    r = len(self.keys)
    while l + 1 < r:
      i = (l + r) // 2
      if self.keys[i] <= v:
        l = i
      else:
        r = i
    return self.keys[l] == v


tree = BTree(order=5, \
  root=Node(data={10: '10'}, children=[\
    Node(data={3: '3', 6: '6'}, children=[\
      Node(data={0: '0', 1: '1', 2: '2'}), \
      Node(data={4: '4', 5: '5'}), \
      Node(data={7: '7', 8: '8', 9: '9'})\
    ]), \
    Node(data={14: '14', 17: '17', 21: '21'}, children=[\
      Node(data={11: '11', 12: '12', 13: '13'}), \
      Node(data={15: '15', 16: '16'}), \
      Node(data={18: '18', 19: '19', 20: '20'}), \
      Node(data={22: '22', 23: '23'})\
    ])]))

print(tree)
