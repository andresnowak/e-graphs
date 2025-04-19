from enum import Enum
from typing import Union, Any, Set

class TYPE(Enum):
    operator = 1
    number = 2

class E_NODE:
    def __init__(self, value: TYPE, children: list[Any]):
        self.value = value # op/value
        self.children: list[Any] = children if children is not None else list([])
        self.parents = set() # to maintain congruence

    def __repr__(self):
        return f"{self.value}({', '.join(str(c) for c in self.children)})"

class E_CLASS:
    def __init__(self, id: int, *values: E_NODE):
        self.id = id
        self.nodes: Set[E_NODE] = set(values)
        self.parents: Set[E_CLASS] = set()
        self.children: Set[E_CLASS] = set()

    def add_node(self, node: E_NODE):
        self.nodes.add(node)
        self.children.update(node.children)

    def __repr__(self):
        return f"EClass({self.id}, nodes={self.nodes})"
