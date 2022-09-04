import random
import copy

class DirectedGraph:
    '''
    The graph is represented using three dictionary:
        > self._dictOUT = a dictionary in which every key (corresponding to every vertex in the graph) has as value
a list of OUTbound neighbours (the list will be empty if the vertex is isolated);
        > self._dictIN = a dictionary in which every key (corresponding to every vertex in the graph) has as value a 
list of INbound neighbours (the list will be empty if the vertex is isolated);
        > self._dictCOST = a dictionary in which every key, which is a tuple (x, y) corresponding to each edge of
the graph, has as value the cost of that edge.
    '''
    def __init__(self):
        '''
        Initialize those three dictionaries with the empty dictionaries. The keys for self._dictOUT and self._dictIN
will be initialized in the function initialize_dict_key.
    '''
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
        '''
        Initialize the list of outbound/inbound neighbours of a given vertex. That given vertex is the key associated
to that list.
        '''
        self._dictIN[key] = []
        self._dictOUT[key] = []

    def is_vertex(self, x):
        # if x is a key in the dictionary of vertices and their successors, it is a vertex of the graph:
        if x in self._dictOUT.keys():
            return True
        return False

    def is_edge(self, x, y):
        '''
        Check if (x, y) is an edge (meaning to check if x has in its list of succesors the vertex y).
        Returns True if (x, y) is an edge, False otherwise.
        '''
        if x in self._dictOUT.keys() and y in self._dictOUT[x]:
            return True
        return False

    def add_edge(self, x, y, c):
        '''
        Adds a valid edge to the graph. An edge (x, y) is valid (can be added to the graph) if:
            - x and y are both vertices
            - the graph does not contain already the edge (x, y) 
        '''
        if self.is_vertex(x) is False or self.is_vertex(y) is False:
            raise ValueError("Invalid vertexes!")
        if self.is_edge(x, y) == True:
            raise ValueError("The edge already exists!")
        '''
        Adding the edge (x, y) means to:
            - add y in the list of the succesors of x
            - add x in the list of the predecesors of y
            - add (x, y) in the dictionary of costs, together with the cost of the edge (as its corresponding value)
        '''
        self._dictOUT[x].append(y)
        self._dictIN[y].append(x)
        self._dictCOST[(x, y)] = c

    def nr_of_vertices(self):
        '''
        Returns the number of vertices of the graph, that is, the number of keys in the dictionary of vertices
and their successors.
        '''
        return len(self._dictOUT.keys())

    def parse_vertices(self):
        '''
        Creates a list (an iterator) of the vertices of the graph and returns it.
        '''
        list_of_vertices = []
        for key in self._dictOUT.keys():
            list_of_vertices.append(key)
        return list_of_vertices

    def get_the_outdegree(self, x):
        '''
        The out degree of a vertex x is the number of edges outgoing from x, that is, the number of elements from
the list of successors of x.
        '''
        if self.is_vertex(x) is False:
            raise ValueError("This is not a vertex!")
        return len(self._dictOUT[x])

    def get_the_indegree(self, x):
        '''
        The in degree of a vertex x is the number of edges incoming to x, that is, the number of elements from
the list of predecessors of x.
        '''
        if self.is_vertex(x) is False:
            raise ValueError("This is not a vertex!")
        return len(self._dictIN[x])

    def get_outbound_edges(self, x):
        '''
        Creates a list (an iterator) of the vertices outgoing from x (forming an outbound edge) and returns it.
        '''
        if self.is_vertex(x) is False:
            raise ValueError("This is not a vertex!")
        list_of_target_vertices = []
        for vertex in self._dictOUT[x]:
            list_of_target_vertices.append(vertex)
        return list_of_target_vertices

    def get_inbound_edges(self, x):
        '''
        Creates a list (an iterator) of the vertices incoming to x (forming an inbound edge) and returns it.
        '''
        if self.is_vertex(x) is False:
            raise ValueError("This is not a vertex!")
        list_of_vertices = []
        for vertex in self._dictIN[x]:
            list_of_vertices.append(vertex)
        return list_of_vertices

    def remove_edge(self, x, y):
        '''
        Removes a valid edge from the graph. An edge (x, y) that can be removed meets the following conditions:
            - x and y are vertices of the graph
            - (x, y) is an edge which belongs to the graph
        '''
        if self.is_vertex(x) is False or self.is_vertex(y) is False:
            raise ValueError("Invalid vertices!")
        if self.is_edge(x, y)  is False:
            raise ValueError("Non-existent edge!")
        '''
        Removing the edge (x, y) means to:
            - remove y from the list of successors of x
            - remove x from the list of predecessors of y
            - remove the pair (x, y) and its cost from the dictionary of costs
        '''
        self._dictOUT[x].remove(y)
        self._dictIN[y].remove(x)
        del self._dictCOST[(x,y)]

    def add_vertex(self, x):
        '''
        A vertex x can be added to the graph if it does not exist already in that graph.
        Adding a vertex x means to add x as a key in self._dictOUT and self._dictIN.
        '''
        if self.is_vertex(x) is True:
            raise ValueError("The vertex already exists!")
        '''
        Adding a vertex x means to add x as a key in self._dictOUT and self._dictIN.
        '''
        self.initialize_dict_key(x)

    def remove_vertex(self, x):
        '''
        A vertex can be removed if it exists in the graph.
        '''
        if self.is_vertex(x) is False:
            raise ValueError("Non-existent vertex!")
        '''
        Deleting the edges which have as start point the vertex x is made as follows:
            - parse the list of successors of x
            - for every successor of x, the pair (x, successor_of_x) is an edge, so we delete it from the dictionary
    of costs
        Also, every successor of x (denoted by y) has in its list of predecessors the vertex x. So we remove the
    vertex x from the list of predecessors of y.
        '''
        for y in self._dictOUT[x]:
            del self._dictCOST[(x,y)]
            self._dictIN[y].remove(x)
            '''
        As above, we delete the edges which have as end point the vertex x by parsing the list of predecessors of x
    and by deleting, for every predecessor of x, the edge (predecessor_of_x, x) from the dictionary of costs.
        Also, every predecessor of x (denoted bt y) has in its list of successors the vertex x, So we delete x from
    the list of successors of y.
            '''
        for y in self._dictIN[x]:
            del self._dictCOST[(y,x)]
            self._dictOUT[y].remove(x)
        '''
        Finally, we remove the key x from the dictionaries of vertices and their successors/ predecessors.
        '''
        del self._dictIN[x]
        del self._dictOUT[x]

    def modify_vertex(self, x, y):
        if self.is_vertex(x) is False or self.is_vertex(y) is True:
            raise ValueError("Invalid vertices!")
        for z in self._dictOUT[x]:
            self._dictCOST[(y, z)] = self._dictCOST.pop((x, z))
            self._dictIN[z].remove(x)
            self._dictIN[z].append(y)
        for z in self._dictIN[x]:
            self._dictCOST[(z, y)] = self._dictCOST.pop((z, x))
            self._dictOUT[z].remove(x)
            self._dictOUT[z].append(y)
        self._dictIN[y] = self._dictIN.pop(x)
        self._dictOUT[y] = self._dictOUT.pop(x)

    def modify_cost(x, y, newC):
        if self.is_edge(x, y) is True:
            self._dictCOST[(x, y)] = newC
            return
        else:
            raise ValueError("NonExistent Edge!")
    
    def copy_graph(self, graph):
        self._dictOUT = copy.deepcopy(graph.get_dictOUT())
        self._dictIN = copy.deepcopy(graph.get_dictIN())
        self._dictOUT = copy.deepcopy(graph.get_dictCOST())

    def __str__(self):
        return str(self._dictOUT)






class UI:

    def __init__(self):
        self.graph = DirectedGraph()

    def init_graph_to_work_with(self, graph):
        self.graph = graph

    def print_main_menu(self):
        print("Chose the graph you want to work with:")
        print("1. Randomly generated graph;")
        print("2. A graph read from a text file.")

    def print_menu(self):
        print("1. Get the number of vertices.")
        print("2. Parse the set of vertices.")
        print("3. Check if there is an edge between two vertices.")
        print("4. Get the degree in and the degree out of a vertex.")
        print("5. Parse the set of outbound edges of a vertex.")
        print("6. Parse the set of inbound edges of a vertex.")
        print("7. Modify the information attached to a vertex.")
        print("8. Add a new edge.")
        print("9. Remove an edge.")
        print("10. Add a new vertex.")
        print("11. Remove a vertex.")
        print("12. Modify the cost.")
        print("13. Make a copy of the graph.")
        print("x. Exit.")

    def run(self):
        self.print_main_menu()
        command = input("Enter your choice: ")
        if command == '1':
            graph = initialize_random_graph()
        elif command == '2':
            filename = input("Enter the name of the file: ")
            graph = read_graph_from_file(filename)
        self.init_graph_to_work_with(graph)
        print(self.graph)
        commands = {
                    '1': self.nr_of_vertices,
                    '2': self.parse_vertices,
                    '3': self.check_edge,
                    '4': self.get_degree,
                    '5': self.get_outbound_edges,
                    '6': self.get_inbound_edges,
                    '7': self.modify_vertex,
                    '8': self.add_edge,
                    '9': self.remove_edge,
                    '10': self.add_vertex,
                    '11': self.remove_vertex,
                    '12': self.modify_cost,
                    '13': self.copy_graph
        }

        while True:
            self.print_menu()
            cmd = input("Enter your command: ")
            if cmd == 'x':
                write_to_file("output.txt", self.graph)
                return
            elif cmd in commands:
                try:
                    commands[cmd]()
                except Exception as exc:
                    print(exc)
            else:
                print("Bad command.")


    def nr_of_vertices(self):
        result = self.graph.nr_of_vertices()
        print(result)

    def parse_vertices(self):
        result = self.graph.parse_vertices()
        print(result)

    def check_edge(self):
        x = input("Enter the first vertex: ")
        y = input("Enter the second vertex: ")
        result = self.graph.is_edge(int(x), int(y))
        print(result)

    def get_degree(self):
        x = input("Enter the vertex:")
        indegree = self.graph.get_the_indegree(int(x))
        outdegree = self.graph.get_the_outdegree(int(x))
        s = 'The degree in is: ' + str(indegree) + '. The degree out is: ' + str(outdegree) + '.'
        print(s)

    def get_outbound_edges(self):
        x = input("Enter the vertex:")
        result = self.graph.get_outbound_edges (int(x))
        print(result)

    def get_inbound_edges(self):
        x = input("Enter the vertex:")
        result = self.graph.get_inbound_edges(int(x))
        print(result)

    def modify_vertex(self):
        x = input("Enter the vertex to be modified:")
        y = input("Enter the new integer of the vertex:")

        self.graph.modify_vertex(int(x), int(y))

    def add_edge(self):
        x = input("Enter the start point of the edge to be added: ")
        y = input("Enter the end point of the edge to be added: ")
        c = input("Enter the cost: ")

        self.graph.add_edge(int(x), int(y), int(c))

    def remove_edge(self):
        x = input("Enter the start point of the edge to be removed: ")
        y = input("Enter the end point of the edge to be removed: ")

        self.graph.remove_edge(int(x), int(y))

    def add_vertex(self):
        x = input("Enter the integer of the new vertex:")
        self.graph.add_vertex(int(x))

    def remove_vertex(self):
        x = input("Enter the vertex to be removed:")
        self.graph.remove_vertex(int(x))
    def modify_cost(self):
        x = input("Enter the start point of the edge: ")
        y = input("Enter the end point of the edge: ")
        newC = input("Enter the new cost: ")
        self.graph.modify_cost(int(x), int(y), int(newC))
    def copy_graph(self):
        '''
        Makes an exact copy of a graph, so that the original can be then modified independently of its copy. The
    function creates a new object of type 'Directed graph', which has the same vertices and edges as the 
    original one.
        '''
        copy_of_graph = DirectedGraph()
        copy_of_graph.copy_graph(self.graph)




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

def write_to_file(filename, graph):
    '''
    The function writes the graph in the file so that the file can be used further as an input file. In other words,
the graph will be written in the format 2) of the reading: every line will contain the endpoints of an edge and its
cost and the isolated vertices will be stored with the format: the_isolated_vertex -1 0.
    '''
    f = open(filename, 'w')
    dict_out = graph.get_dictOUT()
    dict_cost = graph.get_dictCOST()
    for x in dict_out.keys():
        if len(dict_out[x]) == 0:
            value = str(x) + ' -1 0' + '\n'
            f.write(value)
        else:
            for y in dict_out[x]:
                value = str(x) + ' ' + str(y) + ' ' + str(dict_cost[(x, y)]) + '\n'
                f.write(value)

def initialize_random_graph():
    '''
    Reads the number of vertices (n) and the number of edges (m) of the randomly created graph.
    The function chose random endpoints for the edges from the interval [0, n-1] and random costs from the interval
[-50, 50], then checks if the chosen edge already exists in the graph. If it not exists already, the edge created in
this way will be added to the graph. The process stops when the number of edges of the graph become equal to m.
    '''
    done = False
    while done is False:
        n = int(input("Enter the number of vertices:"))
        m = int(input("Enter the number of edges: "))
        filename = input("Enter the file name in which the graph will be saved:")
        if m > n*n:
            print("Invalid number of edges.")
            f = open(filename, 'w')
            f.write("A graph with n = " + str(n) + " and m = " + str(m) + " does not exist.")
            f.close()
        else:
            done = True
    graph = DirectedGraph()
    for i in range(n):
        graph.initialize_dict_key(i)
    added_edges = 0
    while added_edges < m:
        x = random.randrange(0, n)
        y = random.randrange(0, n)
        c = random.randrange(-50, 50)
        if not graph.is_edge(x, y):
            graph.add_edge(x, y, c)
            added_edges += 1
    write_to_file(filename, graph)
    return graph


ui = UI()
ui.run()
