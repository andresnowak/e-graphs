from e_graph import E_GRAPH, E_NODE, E_CLASS

# ((1 * )^∗ a)→accept

e_graph_obj = E_GRAPH()

# E-Class 0: Represents 'a'
node_a = E_NODE(value='a', children_ids=[])
id_a_star = e_graph_obj.add_node(node_a) # id of the e-class

# E-Class 1: Represents '1'
node_1 = E_NODE(value='1', children_ids=[])
id_1 = e_graph_obj.add_node(node_1)

node_mul = E_NODE(value='*', children_ids=[id_a_star, id_1]) # * (EClass 2, EClass 1)
# e_graph_obj.classes[id_a_star].add_node(node_mul)
id_mul = e_graph_obj.add_node(node_mul)  # Returns 2

e_graph_obj.merge(id_a_star, id_mul) # merge this two to represent a and * as the same class because we can have a or 1 * 1 * ... * a

# Print the e-graph state
print("E-Graph Classes:")
for eclass_id, enodes in e_graph_obj.classes.items():
    print(f"EClass {eclass_id}: {enodes}")

print()

print(e_graph_obj)
