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


def prims_algorithm(graph, start):
    '''
    Input: > graph = the graph for which we build the minimum spanning tree
           > start = the start vertex
    Output: > edges = the set of edges forming the minimum spanning tree
    '''
    prev = dict()
    dist = dict()
    priority_queue = []
    edges = []
    vertices = [start]
    for adj_vertex in graph.parse_adjacent_vertices(start):
        dist[adj_vertex] = graph.get_cost(start, adj_vertex)
        prev[adj_vertex] = start
        heapq.heappush(priority_queue, (dist[adj_vertex], adj_vertex))

    while len(priority_queue) > 0:
        distance, x = heapq.heappop(priority_queue)
        if x not in vertices:
            edges.append((prev[x], x))
            vertices.append(x)
            for y in graph.parse_adjacent_vertices(x):
                if y not in dist.keys() or graph.get_cost(x, y) < dist[y]:
                    dist[y] = graph.get_cost(x, y)
                    heapq.heappush(priority_queue, (dist[y], y))
                    prev[y] = x
    return edges


def get_minimum_spanning_tree(graph, start):
    result_edges = prims_algorithm(graph, start)
    total_cost = 0
    print("The minimum spanning tree is formed by the following edges: ")
    for edge in result_edges:
        print(edge)
        total_cost += graph.get_cost(edge[0], edge[1])
    print("Total cost is: " + str(total_cost))


def run():
    while True:
        filename = input("Enter the filename. Press x for exit. \n Filename: > ")
        if filename == 'x':
            return
        graph = read_graph_from_file(filename)

        while True:
            print("Find the minimum spanning tree. Press x for exit.")
            start = input("Enter the start vertex: > ")
            if start == 'x':
                break
            get_minimum_spanning_tree(graph, int(start))


run()
