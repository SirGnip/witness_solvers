from typing import Any
from dataclasses import dataclass, field


@dataclass
class Node:
    name: str
    links: list['Link'] = field(default_factory=list)

    def neighbors(self) -> set:
        return {link.other(self).name for link in self.links}

    def __or__(self, other: 'Node'):
        Link.make(self, other)
        return other


@dataclass
class Link:
    end1: Node
    end2: Node
    state: bool = False

    @staticmethod
    def make(a: Node, b: Node):
        lnk = Link(a, b)
        a.links.append(lnk)
        b.links.append(lnk)
        return lnk

    def __repr__(self):
        return f'{self.end1.name}({id(self.end1)}) <-> {self.end2.name}({id(self.end2)})'

    def other(self, src):
        return self.end2 if src is self.end1 else self.end1


class Grid:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.nodes: dict[Any, Node] = {}  # (x,y): Node
        for y in range(height):
            for x in range(width):
                pt = (x, y)
                n = Node(pt)
                self.nodes[pt] = n

    def __str__(self) -> str:
        DOT, HORIZ, VERT = '+-|'
        g = TextGrid((self.width-1) * 2 + 1, (self.height-1) * 2 + 1)

        # intersections
        for (x, y), node in self.nodes.items():
            g.write(x*2, y*2, DOT)

        # horiz lines
        for y in range(self.height):
            for x in range(self.width):
                start = (x, y)
                end = (x+1, y)
                if start in self.nodes.keys() and end in self.nodes.keys():
                    g.write(x * 2 + 1, y * 2, HORIZ)

        # vert lines
        for x in range(self.width):
            for y in range(self.height):
                start = (x, y)
                end = (x, y+1)
                if start in self.nodes.keys() and end in self.nodes.keys():
                    g.write(x * 2, y * 2 + 1, VERT)


        return str(g)


class TextGrid:
    def __init__(self, width, height, default='.'):
        self.grid = [[default for x in range(width)] for y in range(height)]

    def __str__(self):
        rows = [''.join(row) for row in self.grid]
        rows.reverse()
        return '\n'.join(rows)

    def write(self, x, y, char):
        self.grid[y][x] = char


def test_make_grid():
    def pairem(name1, name2):
        n1, n2 = Node(name1), Node(name2)
        Link.make(n1, n2)
        return n1, n2

    a, b = pairem('a', 'b')
    c, d = pairem('c', 'd')
    Link.make(a, c)
    Link.make(b, d)

    assert set(a.neighbors()) == {'b', 'c'}
    assert set(b.neighbors()) == {'a', 'd'}
    assert set(c.neighbors()) == {'a', 'd'}
    assert set(d.neighbors()) == {'b', 'c'}


def test_make_grid_op():
    a, b, c, d, e, f = [Node(n) for n in 'abcdef']
    a | b | c | d
    e | c
    f | c
    assert set(a.neighbors()) == {'b'}
    assert set(b.neighbors()) == {'a', 'c'}
    assert set(c.neighbors()) == {'b', 'd', 'e', 'f'}
    assert set(d.neighbors()) == {'c'}
    assert set(e.neighbors()) == {'c'}
    assert set(f.neighbors()) == {'c'}


def test_text_grid():
    g = TextGrid(4, 3)
    g.write(0, 0, '0')
    g.write(3, 2, 'X')
    g.write(3, 0, '/')
    print()
    print(g)


def test_print_grid4():
    g = Grid(3, 3)
    print()
    print(g)
