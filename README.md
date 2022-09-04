# Graph-Algorithms
My projects for GA course at university
- - - -
#### Lab 1 #### 
Design and implement an abstract data type directed graph and a function (either a member function or an external one, as your choice) for reading a directed graph from a text file.

The vertices will be specified as integers from 0 to n-1, where n is the number of vertices.

Edges may be specified either by the two endpoints (that is, by the source and target), or by some abstract data type Edge_id (that data type may be a pointer or reference to the edge representation, but without exposing the implementation details of the graph).

Additionally, create a map that associates to an edge an integer value (for instance, a cost).
- - - -
#### Lab 2 ####
Write a program that finds the connected components of an undirected graph using a depth-first traversal of the graph.
- - - -
#### Lab 3 ####
Write a program that, given a graph with positive costs and two vertices, finds a lowest cost walk between the given vertices, using a "backwards" Dijkstra algorithm (Dijkstra algorithm that searches backwards, from the ending vertex).
- - - -
#### Lab 4 ####
Write a program that, given an undirected connected graph, constructs a minumal spanning tree using the Prim's algorithm.
- - - -
#### Lab 5 ####
Given an undirected graph, find a vertex cover with no more than twice the optimal number of vertices in O(n+m) time.
