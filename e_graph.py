from __future__ import annotations
from typing import Union, List, Set, Dict

from union_find import UnionFind


class E_NODE:
    """Represents an e-node (operator or value with children e-class IDs)."""

    def __init__(self, value: Union[str, int, float], children_ids: List[int]):
        self.value = value  # The function symbol ('*', '/', 'a', '1', etc)
        self.children: List[int] = children_ids  # Child e-class IDs

    def __repr__(self) -> str:
        # Represent using child IDs
        return f"{self.value}({', '.join(map(str, self.children))})"

    # Need eq and hash for storing in sets within E_CLASS
    def __eq__(self, other):
        if not isinstance(other, E_NODE):
            return NotImplemented
        # E-nodes are equal if value and children IDs are the same
        return self.value == other.value and self.children == other.children

    def __hash__(self):
        # Hash based on value and tuple of children IDs
        return hash((self.value, tuple(self.children)))


class E_CLASS:
    """Represents an e-class (an equivalence class of e-nodes)."""

    def __init__(self, id: int, nodes: Set[E_NODE] = None):
        self.id = id  # Unique identifier for this e-class
        self.nodes: Set[E_NODE] = set() if nodes == None else nodes # Set of e-nodes belonging to this class

    def add_node(self, node: E_NODE):
        self.nodes.add(node)

    def __repr__(self) -> str:
        # Show the nodes within the class for detailed view
        node_reprs = sorted([repr(n) for n in self.nodes])
        return f"EClass(id={self.id}, nodes={{{', '.join(node_reprs)}}})"

    # Allow comparison by ID
    def __eq__(self, other):
        if not isinstance(other, E_CLASS):
            return NotImplemented
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


# --- E-Graph acts as the central store mapping IDs to E_Classes ---
class E_GRAPH:
    """Represents the E-Graph, mapping IDs to E_Classes."""

    def __init__(self):
        self.classes: Dict[int, E_CLASS] = {}
        # In a full implementation, would also have union-find, hashcons, etc.
        self.union_find = UnionFind()  # {id: parent_id} for Union-Find
        self.hashcons = {}  # {(op, *child_ids): eclass_id}
        self.next_id = 0  # Counter to generate fresh IDs
        self.parents: Dict[int, Set[E_NODE]] = {}  # {eclass_id: set of parent e-nodes}
        self.worklist: Set[int] = set()

    def get_new_id(self) -> int:
        self.next_id += 1
        return self.next_id

    def get_eclass(self, id: int) -> E_CLASS | None:
        # In a real implementation, this would handle canonicalization via find()
        return self.classes.get(id)

    def add_eclass(self, eclass: E_CLASS):
        # Simple addition for this example
        self.classes[eclass.id] = eclass

    def add_node(self, enode: E_NODE):
        # Step 1: Canonicalize children using Union-Find
        canonical_children = self.canonicalize(enode)
        key = (enode.value, *canonical_children) # create a tuple of value and the children ids

        # Step 2: Hashconsing (check for existing congruent e-node)
        if key in self.hashcons:
            return self.hashcons[
                key
            ]  # Return existing e-class ID, so this means the enode can already be added to an existisng e_class

        # Step 3: Create new e-class
        new_id = self.get_new_id()

        self.union_find.parent[new_id] = new_id  # Ensure new_id is in Union-Find
        new_class = E_CLASS(new_id)
        new_class.add_node(E_NODE(enode.value, canonical_children))
        self.classes[new_id] = new_class
        self.hashcons[key] = new_id

        # Step 4: Update parents of children
        for c in canonical_children:
            if c not in self.parents:
                self.parents[c] = set()
            self.parents[c].add(enode)

        return new_id

    def canonicalize(self, enode: E_NODE) -> List[int]:
        canonical_children = [self.union_find.find(e) for e in enode.children]

        return canonical_children

    def merge(self, a: int, b: int):
        a_root = self.union_find.find(a)
        b_root = self.union_find.find(b)

        if a_root == b_root:
            return

        # Union the classes
        self.union_find.union(a_root, b_root)
        merged_id = self.union_find.find(a_root)
        merged_class = E_CLASS(merged_id, self.classes[a_root].nodes | self.classes[b_root].nodes)

        # Update classes and parents
        self.classes[merged_id] = merged_class
        self.worklist.add(merged_id)  # Schedule for rebuilding

    def __repr__(self):
        lines = ["E-Graph Structure:"]
        for class_id in sorted(self.classes.keys()):
            lines.append(f"  {self.classes[class_id]}")
        return "\n".join(lines)
