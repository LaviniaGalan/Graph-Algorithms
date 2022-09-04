import heapq


class UndirectedGraph:
    def __init__(self):
        self._dictNeighbours = {}
        self._dictCost = {}

    def add_vertex(self, key):
        self._dictNeighbours[key] = []

    def is_vertex(self, x):
        return x in self._dictNeighbours.keys()

    def is_edge(self, x, y):
        return y in self._dictNeighbours[x] or x in self._dictNeighbours[y]

    def add_edge(self, x, y, c):
        if self.is_edge(x, y) is False:
            self._dictNeighbours[x].append(y)
            self._dictNeighbours[y].append(x)
            self._dictCost[(x, y)] = c

    def parse_adjacent_vertices(self, x):
        return self._dictNeighbours[x]

    def get_all_vertices(self):
        return self._dictNeighbours.keys()

    def get_cost(self, x, y):
        if (x, y) in self._dictCost.keys():
            return self._dictCost[(x, y)]
        elif (y, x) in self._dictCost.keys():
            return self._dictCost[(y, x)]

    def get_all_edges(self):
        return self._dictCost.keys()

    def __str__(self):
        s = '\tVertices: '
        for vertex in self.get_all_vertices():
            s += str(vertex) + ', '
        s = s[:-2]
        s += '\n\tEdges: \n'
        for vertex in self.get_all_vertices():
            for adj_vertex in self.parse_adjacent_vertices(vertex):
                if adj_vertex >= vertex:
                    s += '\t' + str(vertex) + ' - ' + str(adj_vertex) + '\n'

        return s


def read_graph_from_file(filename):
    f = open(filename)
    graph = UndirectedGraph()
    value = f.readline()
    value = value[:-1].split(' ')
    # if the text file contains on the first line 2 values (n and m), that means that the graph has as vertices
    # all of the numbers in range (0, n)
    if len(value) == 2:
        n = int(value[0])
        m = int(value[1])
        for i in range(n):
            graph.add_vertex(i)
        for i in range(m):
            value = f.readline()
            value = value[:-1].split(' ')
            graph.add_edge(int(value[0]), int(value[1]), int(value[2]))
    else:
        # else, the text file contains only the edges and their costs. The isolated vertices were stored with the
        # format: the_isolated_vertex -1 0
        while True:
            try:
                x = int(value[0])
                y = int(value[1])
                cost = int(value[2])
                if graph.is_vertex(x) is False:
                    graph.add_vertex(x)
                if y != -1 and graph.is_vertex(y) is False:
                    graph.add_vertex(y)
                if y != -1:
                    graph.add_edge(x, y, cost)
                value = f.readline()
                value = value[:-1].split(' ')
                if len(value) != 3:
                    break
            except EOFError:
                break
    f.close()
    return graph


def vertex_cover(graph):
    visited = [False for i in range(0, len(graph.get_all_vertices()))]

    for x in graph.get_all_vertices():
        # the edge is chosen only if its both endpoints are not visited
        if visited[x] is False:
            for y in graph.parse_adjacent_vertices(x):
                if visited[y] is False:
                    # adding the vertices x, y to the vertex cover
                    # all the edges which are incident on x and y will be ignored
                    visited[x] = True
                    visited[y] = True
                    break
    cover = '\tThe vertex cover found by the algorithm contains the vertices:'
    for x in range(0, len(visited)):
        if visited[x] is True:
            cover += ' ' + str(x)

    print(cover + '.')


def run():
    while True:
        filename = input("Enter the filename. Press x for exit. \n\tFilename: > ")
        if filename == 'x':
            return
        graph = read_graph_from_file(filename)
        vertex_cover(graph)


run()
