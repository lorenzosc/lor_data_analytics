from utils.graph.blossom import Blossom


vertex = 7
edges = [(0, 1, 0), (0, 2, 0), (1, 2, 0), (1, 3, 0), (1,4,0)]
graph = Blossom(vertex, edges)
matching, non_matched = graph.maximum_matching()

print(matching)
print(non_matched)

vertex = 6
graph = Blossom(vertex, edges)
matching, non_matched = graph.maximum_matching()

print(matching)
print(non_matched)

vertex = 3
edges = [(0, 1, 0), (0, 2, 0), (1, 2, 0)]
graph = Blossom(vertex, edges)
matching, non_matched = graph.maximum_matching()

print(matching)
print(non_matched)

vertex = 6
edges = [(0, 2, 0), (1, 5, 0), (2, 5, 0), (3, 5, 0), (4, 5, 0)]
graph = Blossom(vertex, edges)
matching, non_matched = graph.maximum_matching()

print(matching)
print(non_matched)

vertex = 6
edges = [(0, 5, 0), (0,4,0), (1,3,0), (2,4,0), (3,4,0), (1, 5, 0), (2, 3, 0), (3, 5, 0), (4, 5, 0)]
graph = Blossom(vertex, edges)
matching, non_matched = graph.maximum_matching()

print(matching)
print(non_matched)