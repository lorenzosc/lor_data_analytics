from utils.graph.blossom import Blossom
import time
import random

file_name = "isolated_node_graph_100.txt"

with open(file_name, "r") as file:
    number_vertex = eval(file.readline())
    all_edges = eval(file.readline())

graph = Blossom(number_vertex, edge_list=all_edges)
matching, non_matched = graph.maximum_matching()

print(matching)
print(non_matched)
