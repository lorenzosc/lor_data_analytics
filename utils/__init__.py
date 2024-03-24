def find_cycles (ancestors_v1: list[int], ancestors_v2: list[int]) -> tuple[list[int], int]:
    
    minimum_lenght = min ([len(ancestors_v1),len(ancestors_v2)])

    for i in range(minimum_lenght):
        if ancestors_v1[i] == ancestors_v2[i]:
            aux = i
            break
    else:
        aux = minimum_lenght

    return (ancestors_v2[aux::-1] + ancestors_v1[:aux], aux)
    
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
