import copy


class Node:
    parent_id = -1
    coord = [-1, -1]
    is_watched = False


def createGraph(input_map: list, node_class):
    graph = dict()
    count = 0
    for x in range(len(input_map)):
        for y in range(len(input_map[x])):
            if not input_map[x][y]:
                n = node_class()
                n.coord = [x, y]
                graph[count] = n
                count += 1
    return graph


def idByCoord(coord: list, graph: dict):
    for id in graph.keys():
        if graph[id].coord == coord:
            return id
    return -1


def neighbors(id: list, graph: dict):
    coord = graph[id].coord

    nearCoords = [[coord[0] + 1, coord[1]],
            [coord[0] - 1, coord[1]],
            [coord[0], coord[1] + 1],
            [coord[0], coord[1] - 1]]

    result = list()
    for n in nearCoords:
        id_n = idByCoord(n, graph)
        if id_n != -1:
            result.append(id_n)
    return result


def pathFromTo(graph: dict, start_coords: list, dest_coords: list):
    path = list([dest_coords])
    current_coord = dest_coords
    dest_parent = graph[idByCoord(current_coord, graph)].parent_id
    if dest_parent == -1:
        return list()
    while current_coord != start_coords:
        parent_id = graph[idByCoord(current_coord, graph)].parent_id
        current_coord = graph[parent_id].coord
        path.append(current_coord)
    return path[::-1]


def startAndEntToMap(input_map, start_coords, dest_coords):
    map_with_start_end = copy.deepcopy(input_map)
    map_with_start_end[start_coords[0]][start_coords[1]] = 5
    map_with_start_end[dest_coords[0]][dest_coords[1]] = 6
    return map_with_start_end


def routeToMap(input_map, route, color=7):
    map_with_all = copy.deepcopy(input_map)
    for r in range(1, len(route) - 1):
        input_map[route[r][0]][route[r][1]] = color
    return map_with_all