class Matching:
    matched: set[int]
    non_matched: set[int]
    pairings: dict[int, int]

    def __init__ (self, number_vertex: int):
        self.matched = set()
        self.non_matched = set()
        self.pairings = {}
        for i in range(number_vertex):
            self.non_matched.add(i)

    # In blossom, once a vertex is matched, it only changes it's opponent, and never goes unmatched again
    # for better performance, this method was broken into make_matched and change_match
    def add_match (self, v1, v2):
        self.pairings[v1] = v2
        self.pairings[v2] = v1

        for vertex in [v1, v2]:
            self.matched.add(vertex)
            self.non_matched.discard(vertex)

    # By breaking add_match into 2 distinct functions, it is possible to only call make matched once per vertex, when it's
    # found on the edge of a augmenting path. For the rest of the path, it's only necessary to call the change match
    def change_match (self, v1, v2):
        self.pairings[v1] = v2
        self.pairings[v2] = v1

    def make_matched (self, vertex):
        self.matched.add(vertex)
        self.non_matched.remove(vertex)

    # In blossom, once a vertex is matched, it only changes it's opponent, and never goes unmatched again
    # So this method is only for class completude, and probably won't be used
    def remove_match (self, v1, v2):
        self.pairings[v1] = None
        self.pairings[v2] = None
        
        for vertex in [v1, v2]:
            self.matched.discard(vertex)
            self.non_matched.add(vertex)

    def add_vertex (self, vertex):
        self.non_matched.add(vertex)
        
    def remove_vertex (self, vertex):
        self.non_matched.discard(vertex)
        self.matched.discard(vertex)
        
        if vertex in self.pairings:
            self.pairings.pop(vertex)

    def get_pairings (self) -> list[tuple[int,int]]:
        pairings = []
        
        #set to not add duplicates
        used = set()

        for v1, v2 in self.pairings:
            if v2 not in used:
                used.add(v2)
                pairings.append((v1, v2))

        return pairings
    
