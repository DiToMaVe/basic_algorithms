from random import randint,shuffle
import copy

class Graph(object):

    def __init__(self, adj_dict = None, edge_count = None, vertex_count = None, graph_file = None):
        
        if graph_file != None:
            adj_dict, edge_count, vertex_count = self.__generate_graph_from_file(graph_file)
        if adj_dict == None:
            adj_dict = {}	
        self.adj_dict = adj_dict	  
        if edge_count == None:
            edge_count = self.__count_edges()
        if vertex_count == None:
            vertex_count = len(adj_dict.keys())
        self.vertex_count = vertex_count
        self.edge_count = edge_count
        
    def vertices(self):
        return list(self.adj_dict.keys())
       
    def edges(self):
        return self.__generate_edges()[0]
 
    def __count_edges(self):
        out  = self.__generate_edges()
        return out[1]
	
    def __generate_edges(self):
        edges = []
        edge_count = 0
        for vertex in self.adj_dict:
            for neighbour in self.adj_dict[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
                    edge_count += 1
        return edges, edge_count

    def __generate_graph_from_file(self,graph_file):		     
        graph = {}
        edge_count = 0
        vertex_count = 0
        with open(graph_file, "r") as file:
            for line in file:
                numbers = [int(x)-1 for x in line.split('\t') if x!='\n']
                vertex = numbers[0]
                vertex_edges = numbers[1:]
                graph[vertex] = vertex_edges
                edge_count+=len(vertex_edges)
                vertex_count+=1 
        edge_count = edge_count//2 # counted each edge twice				
        return graph, edge_count, vertex_count
		
class AdjacencyList(object):
    def __init__(self, adj_dict, edge_count = None):
        self.dict = adj_dict
        self.edge_count = edge_count
	
    def pick_random_edge(self):
        rand_edge = randint(0, int(self.edge_count*2)-1)
        for vertex, vertex_edges in self.dict.items():
            if len(vertex_edges) < rand_edge:
                rand_edge -= len(vertex_edges)
            else:
                from_vertex = vertex
                to_vertex = vertex_edges[rand_edge-1]
                return from_vertex, to_vertex
		
class UnionFind(object):

    def __init__(self, id):
        self.id = id
        self.__sz = [1 for ii in range(0,len(id))]	# number of connected nodes (not the depth of the node)
    
    def root(self,ii):
        while ii != self.id[ii]:
            self.id[ii] = self.root(self.id[ii]) # or self.id[self.id[ii]]: one-passs path compression, make every node in path point to its grandparent
            ii = self.id[ii]
        return ii
    
    def find(self, pp, qq):
        return self.root(pp) == self.root(qq)
	
    def unite(self, pp, qq):
        ii = self.root(pp)
        jj = self.root(qq)
        if self.__sz[ii] >= self.__sz[jj]:
            self.id[jj] = ii
            self.__sz[ii] += self.__sz[jj]
        else:
            self.id[ii] = jj
            self.__sz[jj] += self.__sz[ii]	
				

  
