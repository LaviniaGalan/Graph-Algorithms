class UndirectedGraph:
    def __init__(self):
        self._dictNeighbours = {}

    def init_key(self, key):
        self._dictNeighbours[key] = []

    def is_vertex(self, x):
        return x in self._dictNeighbours.keys()

    def is_edge(self, x, y):
        return y in self._dictNeighbours[x] or x in self._dictNeighbours[y]

    def add_edge(self, x, y):
        if self.is_edge(x, y) is False:
            self._dictNeighbours[x].append(y)
            self._dictNeighbours[y].append(x)

    def parse_adjacent_vertices(self, x):
        return self._dictNeighbours[x]

    def get_all_vertices(self):
        return self._dictNeighbours.keys()

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
            graph.init_key(i)
        for i in range(m):
            value = f.readline()
            value = value[:-1].split(' ')
            graph.add_edge(int(value[0]), int(value[1]))
    else:
        # else, the text file contains only the edges and their costs. The isolated vertices were stored with the
        # format: the_isolated_vertex -1 0
        while True:
            try:
                x = int(value[0])
                y = int(value[1])
                cost = int(value[2])
                if graph.is_vertex(x) is False:
                    graph.init_key(x)
                if y != -1 and graph.is_vertex(y) is False:
                    graph.init_key(y)
                if y != -1:
                    graph.add_edge(x, y)
                value = f.readline()
                value = value[:-1].split(' ')
                if len(value) != 3:
                    break
            except EOFError:
                break
    f.close()
    return graph


def DFS(graph, start_vertex, visited):
    visited.add(start_vertex)
    accessible = []
    stack = [start_vertex]
    component_as_graph = UndirectedGraph()
    component_as_graph.init_key(start_vertex)
    while stack:
        node = stack.pop()
        if node not in accessible:
            accessible.append(node)
            for adj_node in graph.parse_adjacent_vertices(node):
                if adj_node not in visited:
                    component_as_graph.init_key(adj_node)
                    visited.add(adj_node)
                    stack.append(adj_node)
                component_as_graph.add_edge(node, adj_node)
    return component_as_graph


def connected_components(graph):
    visited = set()
    counter = 1
    for vertex in graph.get_all_vertices():
        if vertex not in visited:
            print("Component nr. " + str(counter))
            component_as_graph = DFS(graph, vertex, visited)
            print(component_as_graph)
            counter += 1


def run_lab_2():
    while True:
        filename = input("Enter the filename: ")
        if filename == 'x':
            return
        graph = read_graph_from_file(filename)
        connected_components(graph)


run_lab_2()

