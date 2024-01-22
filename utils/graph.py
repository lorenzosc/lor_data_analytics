from matching import Matching

class Graph:
    adj_matrix: list[list[int]] = [[]]
    number_vertex: int

    def __init__ (self, number_vertex: int, adj_matrix: list[tuple[int, int, float]] = []):
        self.number_vertex = number_vertex
        self.adj_matrix = [
            [
                0 if i==j else 1 for j in range(number_vertex)
            ]
            for i in range(number_vertex)
        ]
        for i, j, weight in adj_matrix:
            self.update(i, j, weight)

    def __getitem__ (self, i, j):
        return self.adj_matrix[i][j]

    def update (self, v1: int, v2: int, weight: float):
        if v1 == v2:
            raise ValueError("A vertex cannot have an edge (and therefore, a weight) to itself")
        
        self.adj_matrix[v1][v2] = weight
        self.adj_matrix[v2][v1] = weight

    def add_vertex (self, weight_list: list[tuple[int, float]]):
        weight_list = sorted(weight_list, key=lambda x: x[0])
        new_vertex = []

        for index in range(self.number_vertex):

            if weight_list[0][0] == index:
                self.adj_matrix[index].append(weight_list.pop(0)[1])
                new_vertex.append(weight_list.pop(0)[1])

            else:
                self.adj_matrix[index].append(1)
                new_vertex.append(1)

        self.adj_matrix.append(new_vertex)

        if weight_list is not []:
            indexes = ""
            for index, weight in weight_list:
                indexes += "\n" + str(index) + " " + str(weight)
            raise IndexError(
                "The following indexes and weights were passed as parameters but couldn't be included in adjacency matrix"
                + "\n" + indexes
            )
        
    def remove_vertex (self, index):
        self.number_vertex -= 1
        self.adj_matrix.pop(index)
        for vertex in self.adj_matrix:
            vertex.pop(index)

    # This function has no use alone but it is a template for other functions using BFS algorithm which generate
    # More relevant results, such as calculating shortest path and the blossom algorithm
    def bfs (self, vertex):
        visited = [False for i in range(self.number_vertex)]
        
        queue = []

        queue.append(vertex)
        visited[vertex] = True

        while queue:

            current_vertex = queue.pop(0)

            for index, weight in enumerate(self.adj_matrix[current_vertex]):

                if weight and not visited[index]:
                    queue.append(index)
                    visited[index] = True

    # only suitable for graphs were all the weights are the same
    def shortest_path (self, v1, v2):
        visited = [False for i in range(self.number_vertex)]
        distances = [0 for i in range(self.number_vertex)]
        
        queue = []

        queue.append(v1)
        visited[v1] = True
        distances[v1] = 0

        while queue:

            current_vertex = queue.pop(0)

            for index, weight in enumerate(self.adj_matrix[current_vertex]):

                if weight and not visited[index]:
                    queue.append(index)
                    visited[index] = True
                    distances[index] = distances[current_vertex] + 1

                    if index == v2:
                        return distances[index]
                    
    # General algorithm for shortest path on weighted graphs
    def dijkstra_algorithm (self, v1, v2):
        visited = [False for i in range(self.number_vertex)]
        distances = [0 for i in range(self.number_vertex)]
        
        queue = []

        queue.append((v1, 0))
        distances[v1] = 0

        while queue:

            current_vertex, _ = queue.pop(0)

            if visited[current_vertex] == True:
                continue

            visited[current_vertex] = True

            for index, weight in enumerate(self.adj_matrix[current_vertex]):

                vertex_distance = weight + distances[current_vertex]
                if vertex_distance < distances[index]:

                    distances[index] = vertex_distance
                    #change queue to tuple queue
                    queue.insert(binary_search(queue, vertex_distance, 0, len(queue)-1), (index, vertex_distance))
                    distances[index] = distances[current_vertex] + 1

                    if index == v2:
                        return distances[index]
                    
    def find_augmenting_path (
        self, vertex: int
    ):
        pass
    
    def maximum_matching (
        self
    ) -> tuple[list[tuple[int,int]], list[int]]:
    
        matching = Matching(self.number_vertex)

        while (matching.non_matched):

            for vertex in matching.non_matched:

                path = self.find_augmenting_path(vertex)

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
    
def find_cycles (ancestors_v1: list[int], ancestors_v2: list[int]) -> list[int]:
    
    minimum_lenght = min ([len(ancestors_v1),len(ancestors_v2)])

    for i in range(minimum_lenght):
        if ancestors_v1[i] == ancestors_v2[i]:
            aux = i
            break
    else:
        aux = minimum_lenght

    return ancestors_v1[:aux] + ancestors_v2[aux::-1]
    
def find_ancestors (parents: dict[int,int], vertex: int) -> list[int]:
    ancestors = [vertex]
    current_vertex = vertex

    while (parents[current_vertex]):
        current_vertex = parents[current_vertex]
        ancestors.append(current_vertex)

    return ancestors

def binary_search (ordered_list, value, start, end) -> None:

    if start == end:
        if ordered_list[start][1] > value:
            return start
        else:
            return start+1
        
    if start > end:
        return start
    
    mid = (start + end) // 2
    print(mid)
    if ordered_list[mid][1] < value:
        return binary_search(ordered_list, value, mid+1, end)

    elif ordered_list[mid][1] > value:
        return binary_search(ordered_list, value, start, mid)
    else:
        return mid