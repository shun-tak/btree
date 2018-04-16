'''
http://opendatastructures.org/versions/edition-0.1g/ods-python/14_2_B_Trees.html
https://ysangkok.github.io/js-clrs-btree/btree.html
'''
class BTree:
    VISITED = set([])

    def __init__(self, order=None, root=None):
        self.order = order or 1
        self.root = root or Node()
        Node.ORDER = order

    def __repr__(self):
        BTree.VISITED = set([])
        return self._repr_dfs(self.root)

    def _repr_dfs(self, node, depth=0):
        ret = ""
        ret += "    " * depth + "- "
        ret += ", ".join(map(str, node.keys))
#         ret += ", ".join(map(lambda e: str(e)+':'+node.data[e], node.keys))
        ret += "\n"
        BTree.VISITED.add(node.id)
        depth += 1
        for child in node.children:
            if not child.id in BTree.VISITED:
                ret += self._repr_dfs(child, depth)
        return ret

    """
    B木のキーからxを検索する。
    見つかれば (True, data[x]) を返す。
    見つからなければ、(False, None) を返す。
    """
    def find(self, x):
        z = None
        u = self.root
        while u is not None:
            exists, i = binary_search(u.keys, x)
            if exists:
                return (True, u.data[u.keys[i]])
            if i < len(u.keys):
                z = u.keys[i]
            u = u.children[i] if len(u.children) > i else None
        return (False, None)

    def add(self, x, value):
        w = None
        try:
            w = self.root.add_recursive(x, value)
        except DuplicateValueError:
            return False
        # 根まで分割されたか？
        if w is not None:
            m_key = self.root.keys.pop()
            m_value = self.root.data.pop(m_key)
            self.root = Node(data={m_key: m_value}, children=[self.root, w])
        return True


class Node:
    COUNT = 1
    ORDER = None

    def __init__(self, children=None, data=None):
        self.id = Node.COUNT
        self.children = children or []
        self.data = data or {}
        self.keys = list(data.keys())
        self.keys.sort()
        Node.COUNT += 1

    def add_recursive(self, x, value):
        exists, i = binary_search(self.keys, x)
        if exists:
            raise DuplicateValueError()
        # 以下、まだ登録されてないキーを検索した場合
        # 現在のノードが葉ノードか？
        if len(self.children) == 0:
            self.data[x] = value
            self.keys.append(x)
            self.keys.sort()
        else:
            # 葉ノードでなければ子ノードに追加
            w = self.children[i].add_recursive(x, value)
            # 分割されたか？
            if w is not None:
                m_key = self.children[i].keys.pop()
                m_value = self.children[i].data.pop(m_key)
                self.children.insert(i+1, w)
                self.data[m_key] = m_value
                self.keys.insert(i, m_key)
        if self._is_full():
            return self._split()
        return None

    # キーが最大数を超えたかどうか判定
    def _is_full(self):
        return len(self.keys) > Node.ORDER - 1

    def _split(self):
        B = Node.ORDER // 2
        # このノードの右半分から新たな分割ノードを作成
        w_children = self.children[B:]
        w_data = {}
        w_keys = self.keys[B:]
        for key, value in list(map(lambda e: (e, self.data[e]), w_keys)):
            w_data[key] = value
        w = Node(data=w_data, children=w_children)

        # 元のノードは左半分だけにする
        self.children = self.children[:B]
        for del_key in w_keys:
            del self.data[del_key]
        self.keys = self.keys[:B]

        return w


"""
sorted_listからxを検索する。
sorted_list[i] == xとなるxが見つかれば (True, i) を返す。
見つからなければ、
sorted_list[i] > xとなる最小のiがあれば (False, i) を返し、
なければ (False, len(sorted_list)) を返す。
"""
def binary_search(sorted_list, x):
    l = 0
    r = len(sorted_list)
    while l != r:
        m = (l + r) // 2
        if sorted_list[m] == x:
            return (True, m)
        if sorted_list[m] < x:
            l = m + 1
        else:
            r = m
    return (False, l)


class DuplicateValueError(Exception):
    def __init__(self, message=None):
        self.message = message or ''


tree = BTree(order=4, \
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
print("Find 9:", tree.find(9))
print("Add 13.5:", tree.add(13.5, '13.5'))
print(tree)
