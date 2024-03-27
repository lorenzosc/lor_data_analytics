from utils.graph.blossom import Blossom
import time
import random


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

start = time.time()
vertex = 500
graph = Blossom(vertex, edges)
matching, non_matched = graph.maximum_matching()

print(matching[:10])
print(non_matched)
print(time.time() - start)

start = time.time()
no_edge = 30
edges = [(i,no_edge-1,0) for i in range(no_edge-1)]
vertex = no_edge
graph = Blossom(vertex, edges)
matching, non_matched = graph.maximum_matching()

print(matching[:10])
print(non_matched)
print(time.time() - start)

start = time.time()
no_edge = 100
edges = [(i,no_edge-1,0) for i in range(no_edge-1)]
edges.extend([(i,no_edge-2,0) for i in range(no_edge-2)])
edges.extend([(i,no_edge-3,0) for i in range(no_edge-3)])
vertex = no_edge
graph = Blossom(vertex, edges)
matching, non_matched = graph.maximum_matching()

print(matching[:10])
print(non_matched)
print(time.time() - start)

def big_test ():
    vertex = 500
    vertexes = [i for i in range(vertex)]
    first_solution = list()
    while vertexes:
        first_solution.append(
            (
                vertexes.pop(random.randint(0,len(vertexes))),
                vertexes.pop(random.randint(0,len(vertexes))), 
                1
            )
        ) 
    all_edges = [(i, j, 0) for i in range(500) for j in range(500) if i != j]
    all_edges.extend(first_solution)
    number_random_edges = 1000
    random_edges = []
    while number_random_edges:
        v1, v2 = random.sample(range(vertex), 2)
        random_edges.append(
            v1, v2, 1
        )
        number_random_edges -= 1

    all_edges.extend(random_edges)
