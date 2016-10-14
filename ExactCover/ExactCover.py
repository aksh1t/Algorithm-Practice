# Problem: https://www.codingame.com/ide/4997062b74f3d83e561acaa2df118df2b53a3e2

class Node:
    left = None
    right = None
    top = None
    bottom = None

    def __init__(self):
        self.left = self.right = self.top = self.bottom = self

    def __repr__(self):
        return "Node"


class ColumnHeader(Node):
    kind = -1
    name = ""
    size = 0

    def __init__(self, nm, kind):
        super().__init__()
        self.name = nm
        self.kind = kind

    def __repr__(self):
        return self.name + " (Type: " + str(self.kind) + ")"


class RowHeader(Node):
    name = ""
    first = None

    def __init__(self, nm):
        super().__init__()
        self.name = nm

    def __repr__(self):
        return self.name


class CellNode(Node):
    col_header = None
    row_header = None

    def __repr__(self):
        return "Column: " + str(self.col_header) + "\t Row: " + str(self.row_header)

    def insert(self, col, row):
        col.size += 1
        self.col_header = col
        self.row_header = row

        self.top = col.top
        self.bottom = col
        col.top.bottom = self
        col.top = self

        if row.first:
            self.left = row.first.left
            self.right = row.first
            row.first.left.right = self
            row.first.left = self
        else:
            row.first = self


class SentinelNode(Node):
    def insert(self, col_header, col_dict):
        col_dict[col_header.name] = col_header
        col_header.left = self.left
        col_header.right = self
        self.left.right = col_header
        self.left = col_header

data = []
rules = set()
row_dict = {}

# Input
nb_characteristics, nb_people = [int(i) for i in input().split()]
for i in range(nb_characteristics):
    characteristics = sorted(input().split())
    data.append(characteristics)
    for c in characteristics:
        row_dict[c] = i

nb_links = int(input())
for i in range(nb_links):
    a, ao, b = input().split()
    a, b = sorted([a, b])
    if ao == '!':
        rules.add(",".join(sorted([a, b])))
    else:
        for c in data[row_dict[b]]:
            if c != b:
                rules.add(",".join(sorted([a, c])))

# Creating columns
sentinel = SentinelNode()
col_node_dict = {}

for k in range(3):
    for i in range(nb_characteristics):
        for j in range(nb_people):
            name = "R"+str(i)+"C"+str(j) if k == 0 else "R"+str(i)+data[i][j] if k == 1 else "C"+str(j)+"R"+str(i)
            sentinel.insert(ColumnHeader(name, k+1), col_node_dict)

for rule in rules:
    for i in range(nb_people):
        name = "C"+str(i)+rule
        sentinel.insert(ColumnHeader(name, 4), col_node_dict)

# Creating rows and initializing data structure
for i in range(nb_characteristics):
    for j in range(nb_people):
        for k in range(1 if i == 0 else nb_people):

            # Row initialization
            row_header_node = RowHeader("R"+str(i)+"C"+str(j)+","+data[i][j if i == 0 else k])

            # Super column 1
            CellNode().insert(col_node_dict["R"+str(i)+"C"+str(j)], row_header_node)

            # Super column 2
            CellNode().insert(col_node_dict["R"+str(i)+data[i][j if i == 0 else k]], row_header_node)

            # Super column 3
            CellNode().insert(col_node_dict["C"+str(j)+"R"+str(i)], row_header_node)

            # Rule columns
            for rule in rules:
                if data[i][j if i == 0 else k] in rule.split(','):
                    CellNode().insert(col_node_dict["C"+str(j)+rule], row_header_node)

# Dancing Links
O = {}


def print_answer():
    for key in O:
        cell = O[key]
        i = int(cell.row_header.name.split("C")[0][1:])
        j = int(cell.row_header.name.split(",")[0].split("C")[1])
        blah = cell.row_header.name.split(",")[1]
        data[i][j] = blah

    for i in range(len(data)):
        for j in range(len(data[i])):
            print(data[i][j], end="")
            if j != len(data[i]) - 1:
                print(" ", end="")
            else:
                print()


def cover(_c):
    _c.right.left = _c.left
    _c.left.right = _c.right
    _b = _c.bottom
    while _b != _c:
        _r = _b.right
        while _r != _b:
            _r.bottom.top = _r.top
            _r.top.bottom = _r.bottom
            _r.col_header.size -= 1
            _r = _r.right
        _b = _b.bottom


def uncover(_u):
    _t = _u.top
    while _t != _u:
        _l = _t.left
        while _l != _t:
            _l.col_header.size += 1
            _l.bottom.top = _l
            _l.top.bottom = _l
            _l = _l.left
        _t = _t.top
    _u.right.left = _u
    _u.left.right = _u


def search(__k):
    if sentinel.right == sentinel or sentinel.right.kind == 4:
        return True

    __c = sentinel.right
    __d = sentinel.right
    mn = __d.size

    while __d != sentinel:
        if __d.size < mn and __d.kind != 4:
            __c = __d
            mn = __d.size
        __d = __d.right

    cover(__c)
    __b = __c.bottom
    while __b != __c:
        O[__k] = __b
        __r = __b.right

        while __r != __b:
            cover(__r.col_header)
            __r = __r.right

        if search(__k+1):
            return True

        __b = O[__k]
        __c = __b.col_header

        __l = __b.left
        while __l != __b:
            uncover(__l.col_header)
            __l = __l.left
        __b = __b.bottom
    uncover(__c)
    return False

search(0)
print_answer()
