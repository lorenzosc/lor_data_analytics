from utils.graph.blossom import Blossom

graph = Blossom(7, [(0, 1, 0), (0, 2, 0), (1, 2, 0), (1, 3, 0), (1,4,0)])
matching, non_matched = graph.maximum_matching()

print(matching)
print(non_matched)