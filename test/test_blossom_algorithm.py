import pytest
from utils.graph.blossom import Blossom
import random
import sys

@pytest.fixture(params=[100, 500, 1000, 2000])
def random_edges_graph(request):
    number_vertex = request.param
    all_edges = [(i, j, 0) for i in range(number_vertex) for j in range(number_vertex) if i != j]

    vertexes = [i for i in range(number_vertex)]
    first_solution = list()
    while vertexes:
        v1 = vertexes.pop(random.randint(0,len(vertexes)-1))
        v2 = vertexes.pop(random.randint(0,len(vertexes)-1))
        first_solution.append(
            (
                v1,
                v2, 
                1
            )
        )
    all_edges.extend(first_solution)

    number_random_edges = 3*number_vertex
    random_edges = []
    while number_random_edges:
        v1, v2 = random.sample(range(number_vertex), 2)
        random_edges.append(
            (v1, v2, 1)
        )
        number_random_edges -= 1
    all_edges.extend(random_edges)

    return number_vertex, all_edges

@pytest.fixture
def complete_matching_graph(random_edges_graph):
    number_vertex, all_edges = random_edges_graph
    with open(f"complete_matching_graph_{number_vertex}.txt", "w+") as file:
        file.write(f"{number_vertex}\n")
        file.write(repr(all_edges))
    
    graph = Blossom(number_vertex, edge_list=all_edges)
    return graph

@pytest.fixture
def isolated_node_graph(random_edges_graph):
    number_vertex, all_edges = random_edges_graph
    j = random.randint(0,number_vertex-1)
    all_edges.extend([(i, j, 0) for i in range(number_vertex) if i!=j])
    with open(f"isolated_node_graph_{number_vertex}.txt", "w+") as file:
        file.write(f"{number_vertex}\n")
        file.write(repr(all_edges))
    
    graph = Blossom(number_vertex, edge_list=all_edges)
    return graph


def ensure_no_blossoms_in_match (graph: Blossom) -> None:
    for v1,v2 in graph.matching.pairings.items():
        assert v1 < graph.number_vertex
        assert v2 < graph.number_vertex

def ensure_edge_in_graph (graph: Blossom) -> None:
    for v1, v2 in graph.matching.pairings.items():
        assert graph[(v1,v2)] != 0
        assert graph[(v2,v1)] == graph[(v1,v2)]

def ensure_all_nodes_matched (graph: Blossom) -> None:
    assert not graph.matching.non_matched

def check_valid_answer (graph: Blossom) -> None:
    ensure_no_blossoms_in_match(graph)
    ensure_edge_in_graph(graph)

def check_valid_answer_full_match (graph: Blossom) -> None:
    check_valid_answer(graph)
    ensure_all_nodes_matched(graph)

# Complete graph
@pytest.mark.parametrize("number_vertex", [(6),(20),(100),(1000)])
def test_small_graph (number_vertex):
    graph = Blossom(number_vertex)
    graph.maximum_matching()
    check_valid_answer_full_match(graph)

# Empty graph
@pytest.mark.parametrize("number_vertex", [(5),(20),(100)])
def test_empty_graph (number_vertex):
    all_edges = [(i, j, 0) for i in range(number_vertex) for j in range(number_vertex) if i != j]
    graph = Blossom(number_vertex, edge_list=all_edges)
    graph.maximum_matching()
    check_valid_answer(graph)

# 0-3, 1-4, 2-5 matching
def test_specific_matching ():
    vertex = 6
    edges = [(0, 5, 0), (0,4,0), (1,3,0), (2,4,0), (3,4,0), (1, 5, 0), (2, 3, 0), (3, 5, 0), (4, 5, 0)]
    graph = Blossom(vertex, edges)
    matching, non_matched = graph.maximum_matching()
    assert non_matched == set()
    assert (0, 3) in matching
    assert (1, 4) in matching
    assert (2, 5) in matching

# 1 isolated node 30-node graph
@pytest.mark.parametrize("number_vertex,number_isolated", [(30, 1), (30, 3), (100, 3)])
def test_isolated_nodes (number_vertex, number_isolated):
    edges = []
    for ind in range(1,number_isolated+1):
        edges.extend([(j,number_vertex-ind,0) for j in range(number_vertex-ind)])
    graph = Blossom(number_vertex, edge_list=edges)
    matching, non_matched = graph.maximum_matching()
    check_valid_answer(graph)

# Randomly generated edges 500 node graph with a complete matching
def test_random_edges_full_match (complete_matching_graph):
    complete_matching_graph.maximum_matching()
    check_valid_answer_full_match(complete_matching_graph)

# Randomly generated edges 500 node graph with one isolated node
def test_random_edges_isolated_node (isolated_node_graph):
    isolated_node_graph.maximum_matching()
    check_valid_answer(isolated_node_graph)
