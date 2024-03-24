from .matching import Matching
from .graph import Graph
from .. import find_cycles

class Blossom(Graph):
    matching: Matching
    blossoms: list[list[int]] #list of blossoms and their current vertices
    upper_blossoms: list[int] #instead of deleting contracted vertices, 
                              #they'll be referenced by their referred blossom here
    next_blossom: int
    blossoms_original_edges: list[list[int]] # For each blossom, a list mapping the vertex in the graph and their parent in that blossom
    parents: list[int]
    visited: list[bool]

    def __init__(self, number_vertex: int, edge_list: list[tuple[int, int, float]] = []):
        super().__init__(number_vertex, edge_list)
        self.blossoms = []
        self.blossoms_original_edges = []
        self.upper_blossoms = [i for i in range(number_vertex)]
        self.next_blossom = number_vertex
        self.matching = Matching(self.number_vertex)

    def find_augmenting_path (
        self, vertex: int
    ):
        queue = [vertex]
        self.visited = [False for _ in range(self.next_blossom)]
        self.parents = [None for _ in range(self.next_blossom)]
        
        self.visited[vertex] = True

        while queue:

            current_vertex = queue.pop(0)
            if self.upper_blossoms[current_vertex] != current_vertex:
                continue

            # 1: check for every vertex in non_matched (if any has an edge, it will find an augmenting path)
            # obs: no non_matched vertex can be visited, because if they're visited, the function is terminated
            for neighbor in self.matching.non_matched:
                if self.adj_matrix[current_vertex][neighbor]:
                    self.parents[neighbor] = current_vertex
                    return self.trace(neighbor)

            for neighbor in self.matching.matched:
                
                # No edge, the pair or a contracted vertex
                if (
                    self.adj_matrix[current_vertex][neighbor] == 0 or
                    self.matching.pairings[current_vertex] == neighbor or
                    self.upper_blossoms[neighbor] != neighbor
                ):
                    continue
            
            # 2: Check if visited. If so, find cycle between current_vertex and vertex
                if self.visited[neighbor] == True:
                    n_ancestors = self.trace(neighbor)
                    v_ancestors = self.trace(current_vertex)
                    cycle, cycle_root = find_cycles(n_ancestors, v_ancestors)

                # Contract if blossom and add blossom to queue
                    if len(cycle) % 2 == 1:
                        blossom = self.contract(cycle, cycle_root)
                        queue.insert(0, blossom)
                        self.parents.append(self.parents[cycle_root])
                        self.visited.append(True)
                        break

            # 3: for not visited vertex, mark it as visited, it's parent as current vertex, it's mate's parent as itself,
            # it's mate as visited, and finally add it's mate to the queue (this is the only way a real vertex ever enters
            # the queue)
                else:
                    self.visited[neighbor] = True
                    self.parents[neighbor] = current_vertex

                    self.visited[self.matching.pairings[neighbor]] = True
                    self.parents[self.matching.pairings[neighbor]] = neighbor

                    queue.append(self.matching.pairings[neighbor])

        return []

    # Trace path to root from a vertex
    def trace (self, vertex: int):
        ancestors = []
        current_vertex = vertex

        while self.parents[current_vertex] is not None:
            while (self.upper_blossoms[current_vertex] != current_vertex):
                current_vertex = self.upper_blossoms[current_vertex]
            ancestors.append(current_vertex)
            current_vertex = self.parents[current_vertex]

        ancestors.append(current_vertex)

        return ancestors

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
            for neighbor in range(self.next_blossom):
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
        for ind in range(self.next_blossom):
            self.adj_matrix[ind].append(edges[ind])
        self.adj_matrix.append(edges)
        
        self.next_blossom += 1
        return self.next_blossom - 1

    # makes each vertex in a blossom map to itself in the upper_blossoms array and delete all edges from the blossom
    # then delete contents of the blossom (although not really necessary, only clears some memory)
    def lift_blossom (
        self, blossom: int
    ):
        if blossom in self.matching.matched:
            self.matching.change_match(self.blossoms[blossom-self.number_vertex][0], self.matching.pairings[blossom-self.number_vertex])

        # Make each vertex on the blossom not be ignored in search anymore
        vertexes = self.blossoms[blossom-self.number_vertex]
        for vertex in vertexes:
            self.upper_blossoms[vertex] = vertex

        # Remove edges from blossom
        for i in range(self.next_blossom):
            self.adj_matrix[blossom][i] = 0
            self.adj_matrix[i][blossom] = 0

        # Free space from blossom information since it's no longer useful
        self.blossoms[blossom-self.number_vertex].clear()
        self.blossoms_original_edges[blossom-self.number_vertex].clear()

    # if a vertex is an original vertex, add it to the path. If it is a blossom, check the entry point, the exit point
    # decide which direction to go and add vertexes from cycle in order until exit point. Do this for all vertexes
    def construct_path (
        self, path: list
    ):
        exp_path = []

        while path:
            vertex = path.pop()

            # Real vertex should just be appended
            if vertex < self.number_vertex:
                exp_path.append(vertex)
                continue
            
            # Finding references (entry and exit) in blossom
            bl_number = vertex - self.number_vertex
            cycle: list = self.blossoms[bl_number]
            entrance =  cycle.index(self.blossoms_original_edges[bl_number][exp_path[-1]])

            if vertex in self.matching.matched:
                exit = cycle.index(self.blossoms_original_edges[bl_number][path[-1]])
            else:
                exit = cycle[0]

            # Deciding which way to go in the cycle
            if (entrance + exit) % 2 == 0 ^ exit == 0:
                step = 1
            else:
                step = len(cycle) - 1

            # Adding vertex from cycle until exit
            while entrance != exit:
                path.append(cycle[entrance])
                entrance += step
                entrance %= len(cycle)
            path.append(cycle[entrance])

            self.lift_blossom(vertex)
        
        return exp_path
            
    # Overload to inutilize add_vertex once any blossom is created by raising exception
    def add_vertex(self, weight_list: list[tuple[int, float]]):
        if self.number_vertex == self.next_blossom:
            return super().add_vertex(weight_list)
        raise Exception("Since blossom keeps track of what is a blossom and what is a vertex by their index, new vertexes cannot be added")

    def lift_all_blossom(
        self
    ):
        for ind in range(self.number_vertex, self.next_blossom):
            if self.blossoms[ind-self.number_vertex]:
                self.lift_blossom(ind)

    def maximum_matching (
        self
    ) -> tuple[list[tuple[int,int]], list[int]]:
    
        while len(self.matching.non_matched)>1:

            for vertex in self.matching.non_matched:

                path = self.find_augmenting_path(vertex)

                path = self.construct_path(path)

                # updating vertexes in path
                if path:
                    self.matching.make_matched(path[0])
                    self.matching.make_matched(path[-1])
                    for v1, v2 in zip(path[::2], path[1::2]):
                        self.matching.change_match(v1, v2)
                    break

            else:
                print("Tried all free nodes and no path were found")
                break

        return (self.matching.get_pairings(), self.matching.non_matched)
    
