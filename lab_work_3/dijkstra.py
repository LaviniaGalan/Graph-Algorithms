import random
import copy
import heapq


class DirectedGraph:
    '''
    The graph is represented using three dictionaries:
        > self._dictOUT = a dictionary in which every key (corresponding to every vertex in the graph) has as value
a list of OUTbound neighbours (the list will be empty if the vertex is isolated);
        > self._dictIN = a dictionary in which every key (corresponding to every vertex in the graph) has as value a
list of INbound neighbours (the list will be empty if the vertex is isolated);
        > self._dictCOST = a dictionary in which every key, which is a tuple (x, y) corresponding to each edge of
the graph, has as value the cost of that edge.
    '''

    def __init__(self):
        self._dictIN = {}
        self._dictOUT = {}
        self._dictCOST = {}

    def get_dictOUT(self):
        # a getter for the dictionary of outbound neighbours
        return self._dictOUT

    def get_dictIN(self):
        # a getter for the dictionary of inbound neighbours
        return self._dictIN

    def get_dictCOST(self):
        # a getter for the dictionary of inbound neighbours
        return self._dictCOST

    def initialize_dict_key(self, key):
        self._dictIN[key] = []
        self._dictOUT[key] = []

    def is_vertex(self, x):
        # if x is a key in the dictionary of vertices and their successors, it is a vertex of the graph:
        if x in self._dictOUT.keys():
            return True
        return False

    def is_edge(self, x, y):
        if x in self._dictOUT.keys() and y in self._dictOUT[x]:
            return True
        return False

    def add_edge(self, x, y, c):
        if self.is_vertex(x) is False or self.is_vertex(y) is False:
            raise ValueError("Invalid vertexes!")
        if self.is_edge(x, y) is True:
            raise ValueError("The edge already exists!")

        self._dictOUT[x].append(y)
        self._dictIN[y].append(x)
        self._dictCOST[(x, y)] = c

    def nr_of_vertices(self):
        return len(self._dictOUT.keys())

    def parse_vertices(self):
        list_of_vertices = []
        for key in self._dictOUT.keys():
            list_of_vertices.append(key)
        return list_of_vertices

    def get_outbound_neighbours(self, x):
        if self.is_vertex(x) is False:
            raise ValueError("This is not a vertex!")
        list_of_target_vertices = []
        for vertex in self._dictOUT[x]:
            list_of_target_vertices.append(vertex)
        return list_of_target_vertices

    def get_inbound_neighbours(self, x):
        if self.is_vertex(x) is False:
            raise ValueError("This is not a vertex!")
        list_of_vertices = []
        for vertex in self._dictIN[x]:
            list_of_vertices.append(vertex)
        return list_of_vertices

    def add_vertex(self, x):
        if self.is_vertex(x) is True:
            raise ValueError("The vertex already exists!")
        self.initialize_dict_key(x)

    def __str__(self):
        return str(self._dictOUT)


def read_graph_from_file(filename):
    '''
    The function can read from two formats of files:
    1) if the text file contains on the first line two values (n and m), that means that the graph has as vertices
all of the integer numbers in range (0, n).
    2) if the text file contains on the first line three values, that means that the file contains only the edges
of the graph and their cost (the isolated vertices were stored with the format: the_isolated_vertex -1 0). In this
case, the graph will have as vertices the integers which define the endpoints of the edges, plus the isolated
vertices.
    '''
    f = open(filename)
    graph = DirectedGraph()
    # read the first line of the text file:
    value = f.readline()
    value = value[:-1].split(' ')
    # if the text file contains on the first line 2 values (n and m), that means that the graph has as vertices
    # all of the numbers in range (0, n)
    if len(value) == 2:
        n = int(value[0])
        m = int(value[1])
        for i in range(n):
            graph.initialize_dict_key(i)
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
                    graph.initialize_dict_key(x)
                if y != -1 and graph.is_vertex(y) is False:
                    graph.initialize_dict_key(y)
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


def dijkstra(graph, start, end):
    '''
    Input:  - graph = the graph in which we search for the minimum cost walk
            - start = the start vertex
            - end = the end vertex
    Output: - next = a dictionary in which every key is a node. The value is the vertex which comes
after the key vertex in the minimum cost walk.
            - dist = a dictionary in which every key is a node and the value is the distance between
the key vertex and the end vertex. The minimum distance we search for will be equal to dist[start].
    '''
    next = dict()
    dist = dict()
    priority_queue = []
    heapq.heappush(priority_queue, (0, end))
    dist[end] = 0
    next[end] = None
    while len(priority_queue) > 0:
        distance, x = heapq.heappop(priority_queue)
        for y in graph.get_inbound_neighbours(x):
            if y not in dist.keys() or dist[x] + graph.get_dictCOST()[(y, x)] < dist[y]:
                dist[y] = dist[x] + graph.get_dictCOST()[(y, x)]
                heapq.heappush(priority_queue, (dist[y], y))
                next[y] = x

    if start not in dist.keys():         # we could not find any walk between start and end
        return None
    return (next, dist)


def get_minimum_cost_walk(graph, start, end):
    result = dijkstra(graph, start, end)
    if result is None:
        print("Couldn't find a walk between the given vertices!")
    else:
        next = result[0]
        dist = result[1]
        path = []
        s = "The walk is: "
        node = start
        while node is not None:      # building the minimum cost walk, using the next dictionary
            path.append(node)
            node = next[node]
        s += str(path) + " having the cost: " + str(dist[start])   # the cost is equal to dist[start]
        print(s)


def run():
    while True:
        filename = input("Enter the filename. Press x for exit. \n Filename: > ")
        if filename == 'x':
            return
        graph = read_graph_from_file(filename)

        while True:
            print("Find a lowest cost walk between the given vertices. Press x for exit.")
            start = input("Enter the start vertex: > ")
            if start == 'x':
                break
            end = input("Enter the end vertex: > ")
            get_minimum_cost_walk(graph, int(start), int(end))


run()
