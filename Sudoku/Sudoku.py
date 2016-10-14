# Problem: https://projecteuler.net/problem=96


def print_answer(O):
    data = [[0 for _ in range(9)] for _ in range(9)]
    for key in O:
        z = O[key].row_header.name
        data[int(z[1])-1][int(z[4])-1] = int(z[6])

    for line in data:
        print(line)

    print("\n")


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
    if sentinel.right == sentinel:
        return True

    __c = sentinel.right
    __d = sentinel.right
    mn = __d.size

    while __d != sentinel:
        if __d.size < mn:
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

        if search(__k + 1):
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
    name = ""
    size = 0

    def __init__(self, nm):
        super().__init__()
        self.name = nm

    def __repr__(self):
        return self.name


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

sudokus = open("sudoku").readlines()

for i in range(50):
    sudoku = []
    for j in range(9):
        row = []
        for k in range(9):
            row.append(int(sudokus[(i*10)+1+j][k]))
        sudoku.append(row)

    # Columns
    sentinel = SentinelNode()
    col_node_dict = {}

    for a in range(1, 10):
        for b in range(1, 10):
            name = "R"+str(a)+"-C"+str(b)
            sentinel.insert(ColumnHeader(name), col_node_dict)

    for a in range(1, 10):
        for b in range(1, 10):
            name = "R" + str(a) + "#" + str(b)
            sentinel.insert(ColumnHeader(name), col_node_dict)

    for a in range(1, 10):
        for b in range(1, 10):
            name = "C" + str(a) + "#" + str(b)
            sentinel.insert(ColumnHeader(name), col_node_dict)

    for a in range(1, 10):
        for b in range(1, 10):
            name = "S" + str(a) + "#" + str(b)
            sentinel.insert(ColumnHeader(name), col_node_dict)

    # Rows
    for a in range(9):
        for b in range(9):
            if sudoku[a][b] == 0:
                for c in range(1, 10):
                    row_header_node = RowHeader("R" + str(a + 1) + "-C" + str(b + 1) + "#" + str(c))
                    CellNode().insert(col_node_dict["R" + str(a + 1) + "-C" + str(b + 1)], row_header_node)
                    CellNode().insert(col_node_dict["R" + str(a + 1) + "#" + str(c)], row_header_node)
                    CellNode().insert(col_node_dict["C" + str(b + 1) + "#" + str(c)], row_header_node)
                    box = -1
                    if 1 <= a+1 <= 3:
                        if 1 <= b+1 <= 3:
                            box = 1
                        if 4 <= b+1 <= 6:
                            box = 2
                        if 7 <= b+1 <= 9:
                            box = 3
                    if 4 <= a+1 <= 6:
                        if 1 <= b+1 <= 3:
                            box = 4
                        if 4 <= b+1 <= 6:
                            box = 5
                        if 7 <= b+1 <= 9:
                            box = 6
                    if 7 <= a+1 <= 9:
                        if 1 <= b+1 <= 3:
                            box = 7
                        if 4 <= b+1 <= 6:
                            box = 8
                        if 7 <= b+1 <= 9:
                            box = 9
                    CellNode().insert(col_node_dict["S" + str(box) + "#" + str(c)], row_header_node)
            else:
                row_header_node = RowHeader("R" + str(a + 1) + "-C" + str(b + 1) + "#" + str(sudoku[a][b]))
                CellNode().insert(col_node_dict["R" + str(a + 1) + "-C" + str(b + 1)], row_header_node)
                CellNode().insert(col_node_dict["R" + str(a + 1) + "#" + str(sudoku[a][b])], row_header_node)
                CellNode().insert(col_node_dict["C" + str(b + 1) + "#" + str(sudoku[a][b])], row_header_node)
                box = -1
                if 1 <= a + 1 <= 3:
                    if 1 <= b + 1 <= 3:
                        box = 1
                    if 4 <= b + 1 <= 6:
                        box = 2
                    if 7 <= b + 1 <= 9:
                        box = 3
                if 4 <= a + 1 <= 6:
                    if 1 <= b + 1 <= 3:
                        box = 4
                    if 4 <= b + 1 <= 6:
                        box = 5
                    if 7 <= b + 1 <= 9:
                        box = 6
                if 7 <= a + 1 <= 9:
                    if 1 <= b + 1 <= 3:
                        box = 7
                    if 4 <= b + 1 <= 6:
                        box = 8
                    if 7 <= b + 1 <= 9:
                        box = 9
                CellNode().insert(col_node_dict["S" + str(box) + "#" + str(sudoku[a][b])], row_header_node)


    # Dancing Links
    O = {}
    search(0)
    print_answer(O)