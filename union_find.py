from __future__ import annotations
from typing import Dict, Any

class UnionFind:
    def __init__(self):
        self.parent: Dict[int, int] = {}  # {id: parent_id}

    def find(self, x: int) -> int:
        if x not in self.parent:
            self.parent[x] = x  # New element is its own parent
        if self.parent[x] != x: # it means we haven't finished, we havent found the root (the root doesn't have a parent, so the parent its him)
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x: int, y: int):
        x_root = self.find(x)
        y_root = self.find(y)
        if x_root != y_root:
            self.parent[y_root] = x_root # we make x_root the root of the set of x and y
