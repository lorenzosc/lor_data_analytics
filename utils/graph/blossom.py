from utils.graph.matching import Matching
from utils.graph.graph import Graph
from .. import find_ancestors, find_cycles

class blossom(Graph):
    matching: Matching
    blossoms: list[int] #instead of deleting contracted vertices, they'll be referenced by their referred blossom here
           

    def find_augmenting_path (
        self, vertex: int, matching: Matching
    ):
        queue = [vertex]
        visited = [False for i in range(self.number_vertex)]
        parents = [None for i in range(self.number_vertex)]
        
        visited[vertex] = True

        while queue:
            current_vertex = queue.pop(0)

            
            # 1: check for every vertex in non_matched (if any has an edge, it will find an augmenting path)
            # obs: no non_matched vertex can be visited, because if they're visited, the function is terminated
            for neighbor in matching.non_matched:
                if self.adj_matrix[current_vertex][neighbor]:
                    parents[neighbor] = current_vertex
                    return find_ancestors(parents, neighbor)

            for neighbor in matching.matched:
                
                if self.adj_matrix[current_vertex][neighbor] == 0 or matching.pairings[current_vertex] == neighbor:
                    continue
                
            # 2: Now for matched vertex, check if has edge. If not, ignore. Else, check if visited. 
            # If so, find cycle between current_vertex and vertex, and contract if blossom
            # 2.1: find augmenting path in blossom contracted graph
            # 2.2: lift blossom, adjust matches in cycle, and return the augmenting path (without changing pairing)
                if visited[neighbor] == True:
                    n_ancestors = find_ancestors(parents, neighbor)
                    v_ancestors = find_ancestors(parents, current_vertex)
                    cycle = find_cycles(n_ancestors, v_ancestors)
                    blossom = contract(cycle)
                    contracted_path = self.find_augmenting_path()
                    path = self.lift_blossom(blossom, contracted_path)
                    return path

            # 3: for not visited vertex, mark it as visited, it's parent as current vertex, it's mate's parent as itself,
            # it's mate as visited, and finally add it's mate to the queue (this is the only way any vertex ever enters
            # the queue)
                else:
                    visited[neighbor] = True
                    parents[neighbor] = current_vertex

                    visited[matching.pairings[neighbor]] = True
                    parents[matching.pairings[neighbor]] = neighbor

                    queue.append(matching.pairings[neighbor])

    def maximum_matching (
        self
    ) -> tuple[list[tuple[int,int]], list[int]]:
    
        matching = Matching(self.number_vertex)

        while (matching.non_matched):

            for vertex in matching.non_matched:

                path = self.find_augmenting_path(vertex, matching)

                # updating vertexes in path
                if path:
                    matching.make_matched(path[0])
                    matching.make_matched(path[-1])
                    for v1, v2 in zip(path[::2], path[1::2]):
                        matching.change_match(v1, v2)
                    break

            else:
                print("Tried all free nodes and no path were found")
                break

        return (matching.get_pairings(), matching.non_matched)
    
