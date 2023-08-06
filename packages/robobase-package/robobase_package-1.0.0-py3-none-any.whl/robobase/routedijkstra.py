from .routecommon import *


class NodeDij(Node):
    distance = float('inf')


def minDistId(list_id: list, graph: dict):
    min_dist_id = list_id[0]
    for i in list_id:
        if graph[i].distance < graph[min_dist_id].distance:
            min_dist_id = i
    return min_dist_id


def dijkstraGrid(input_map, start_coords, dest_coords):
    graph = createGraph(input_map, NodeDij)
    start_id = idByCoord(start_coords, graph)
    graph[start_id].distance = 0
    not_watched = list([start_id])
    while len(not_watched) != 0:
        current_id = minDistId(not_watched, graph)
        not_watched.remove(current_id)
        graph[current_id].is_watched = True
        nearId = neighbors(current_id, graph)
        for n_id in nearId:
            if graph[n_id].distance > graph[current_id].distance + 1:
                graph[n_id].distance = graph[current_id].distance + 1
                graph[n_id].parent_id = current_id
            if not graph[n_id].is_watched:
                not_watched.append(n_id)
    return pathFromTo(graph, start_coords, dest_coords)
