import math

from .routecommon import *


class NodeA(Node):
    g = float('inf')
    f = float('inf')


def H(node_coord, dest_coords):
    return math.sqrt((node_coord[0] - dest_coords[0])**2 + (node_coord[1] - dest_coords[1])**2)


def minFId(list_id, graph):
    min_f_id = list_id[0]
    for i in list_id:
        if graph[i].f < graph[min_f_id].f:
            min_f_id = i
    return min_f_id


def AStarGrid(input_map, start_coords, dest_coords):
    graph = createGraph(input_map, NodeA)
    start_id = idByCoord(start_coords, graph)
    graph[start_id].g = 0
    graph[start_id].f = H(graph[start_id].coord, dest_coords)
    not_watched = list([start_id])
    while len(not_watched) != 0:
        current_id = minFId(not_watched, graph)
        not_watched.remove(current_id)
        graph[current_id].is_watched = True
        nearId = neighbors(current_id, graph)
        for n_id in nearId:
            if graph[n_id].g > graph[current_id].g + 1:
                graph[n_id].g = graph[current_id].g + 1
                graph[n_id].f = graph[current_id].f + H(graph[n_id].coord, dest_coords)
                graph[n_id].parent_id = current_id
            if not graph[n_id].is_watched:
                not_watched.append(n_id)
    return pathFromTo(graph, start_coords, dest_coords)
