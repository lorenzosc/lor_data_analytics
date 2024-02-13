from utils.graph.matching import Matching
from utils.graph.graph import Graph
from .. import find_ancestors, find_cycles

class Blossom(Graph):
    matching: Matching
    blossoms: list[list[int]] #list of blossoms and their current vertices
    upper_blossoms: list[int] #instead of deleting contracted vertices, 
                              #they'll be referenced by their referred blossom here
    next_blossom: int
    blossoms_original_edges: list[list[int]] # For each blossom, a list mapping the vertex in the graph and their parent in that blossom
           
    def __init__(self, number_vertex: int, adj_matrix: list[tuple[int, int, float]] = ...):
        super().__init__(number_vertex, adj_matrix)
        self.blossoms = []
        self.blossoms_original_edges = []
        self.upper_blossoms = [i for i in range(number_vertex)]
        self.next_blossom = number_vertex
        self.matching = Matching(self.number_vertex)

    def find_augmenting_path (
        self, vertex: int, matching: Matching
    ):
        queue = [vertex]
        visited = [False for i in range(self.number_vertex)]
        parents = [None for i in range(self.number_vertex)]
        
        visited[vertex] = True

        while queue:

            current_vertex = queue.pop(0)
            if self.blossoms[current_vertex] != current_vertex:
                continue

            # 1: check for every vertex in non_matched (if any has an edge, it will find an augmenting path)
            # obs: no non_matched vertex can be visited, because if they're visited, the function is terminated
            for neighbor in matching.non_matched:
                if self.adj_matrix[current_vertex][neighbor]:
                    parents[neighbor] = current_vertex
                    return find_ancestors(parents, neighbor)

            for neighbor in matching.matched:
                
                # No edge, the pair or a contracted vertex
                if (
                    self.adj_matrix[current_vertex][neighbor] == 0 or
                    matching.pairings[current_vertex] == neighbor or
                    self.blossoms[neighbor] != neighbor
                ):
                    continue

            # It's necessary to adjust point 2 logic. For better performance, it's important to evaluate
            # Whether recursive calls or to add the blossom in the start of the queue is more important.
            # It's also important to consider that the list being itearated is also being manipulated,
            # And that should be avoided, if possible. By making recursive calls and returning the answer,
            # That would be avoided
                
            # 2: Now for matched vertex, check if has edge. If not, ignore. Else, check if visited. 
            # If so, find cycle between current_vertex and vertex, and contract if blossom
            # 2.1: find augmenting path in blossom contracted graph
            # 2.2: lift blossom, adjust matches in cycle, and return the augmenting path (without changing pairing)
                if visited[neighbor] == True:
                    n_ancestors = find_ancestors(parents, neighbor)
                    v_ancestors = find_ancestors(parents, current_vertex)
                    cycle, cycle_root = find_cycles(n_ancestors, v_ancestors)
                    if len(cycle) % 2 == 1:
                        blossom = self.contract(cycle, cycle_root)
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

    # Make each vertex in the cycle map to the blossom in upper blossom and add their edges to the blossom
    # Only the first time an edge is seen is taken into account to see their real parent.
    # Then the blossom is added into the graph and their information is stored for later, when lifting
    def contract (
        self, cycle: list[int], cycle_root: int
    ):
        # Generating variables from blossom
        total_size = self.next_blossom+1
        edges = [0 for i in range(total_size)]
        edge_original = [self.next_blossom for i in range(total_size)]

        # Contract vertexes in cycle and add their edges to blossom
        for vertex in cycle:
            self.upper_blossoms[vertex] = self.next_blossom    
            for neighbor in range(total_size-1):
                if self.adj_matrix[vertex][neighbor] and edges[neighbor] == self.next_blossom:
                    edges[neighbor] = self.adj_matrix[vertex][neighbor]
                    edge_original[neighbor] = vertex
        
        # Adding this blossom information to the Blossom graph structure
        self.blossoms.append(cycle)
        self.blossoms_original_edges.append(edge_original)
        self.matching.add_vertex(self.next_blossom)

        # make blossom matched only if root is matched (for when the BFS root is the blossom root)
        if cycle_root in self.matching.matched:
            self.matching.add_match(self.next_blossom, self.matching.pairings[cycle_root])

        assert self.next_blossom == len(self.adj_matrix)
        # Adding edges from blossom into graph
        for ind in range(len(self.adj_matrix)):
            self.adj_matrix[ind].append(edges[ind])
        self.adj_matrix.append(edges)
        
        self.next_blossom += 1
        return self.next_blossom - 1

    # makes each vertex in a blossom map to itself in the upper_blossoms array and delete all edges from the blossom
    # then delete contents of the blossom (although not really necessary, only clears some memory)
    def lift_blossom (
        self, blossom: int
    ):
        # Make each vertex on the blossom not be ignored in search anymore
        vertexes = self.blossoms[blossom]
        for vertex in vertexes:
            self.upper_blossoms[vertex] = vertex

        # Remove edges from blossom
        for i in range(self.next_blossom):
            self.adj_matrix[blossom][i] = 0
            self.adj_matrix[i][blossom] = 0

        # Free space from blossom information since it's no longer useful
        self.blossoms[blossom].clear()
        self.blossoms_original_edges[blossom].clear()

    # if a vertex is an original vertex, add it to the path. If it is a blossom, check the entry point, the exit point
    # decide which direction to go and add vertexes from cycle in order until exit point. Do this for all vertexes
    def construct_path (
        self, path 
    ):
        exp_path = []
        for ind, vertex in enumerate(path):

            # Real vertex should just be appended
            if vertex < self.number_vertex:
                exp_path.append(vertex)
                continue
            
            # Finding references (entry and exit) in blossom
            after_blossom = path[ind+1]
            bl_number = vertex - self.number_vertex
            cycle: list = self.blossoms[bl_number]
            entrance =  cycle.index(self.blossoms_original_edges[bl_number][exp_path[-1]])
            exit = cycle.index(self.blossoms_original_edges[bl_number][after_blossom])

            # Deciding which way to go in the cycle
            if (entrance + exit) % 2 == 0 ^ exit == 0:
                step = 1
            else:
                step = len(cycle) - 1

            # Adding vertex from cycle until exit
            while entrance != exit:
                exp_path.append(cycle[entrance])
                entrance += step
            exp_path.append(cycle[entrance])
        
        return exp_path
            
    # Overload to inutilize add_vertex once any blossom is created by raising exception
    def add_vertex(self, weight_list: list[tuple[int, float]]):
        if self.number_vertex == self.next_blossom:
            return super().add_vertex(weight_list)
        raise Exception("Since blossom keeps track of what is a blossom and what is a vertex by their index, new vertexes cannot be added")

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
    
