from random import randint,shuffle
import copy

class Graph(object):

    def __init__(self, adj_dict = None, edge_count = None, vertex_count = None, graph_file = None):
        
        if graph_file != None:
            adj_dict, adj_dict_rev, edge_count, vertex_count = self.__generate_graph_from_file2(graph_file)
        if adj_dict == None:
            adj_dict = {}	
            adj_dict_rev = {}
        self.adj_dict = adj_dict
        self.adj_dict_rev = adj_dict_rev
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
        # undirected graph
		# symmetric adjacency list, i.e. if x->y in dictionary then y->x too
		# separated by tab
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
				
    def __generate_graph_from_file2(self, graph_file):
        # directed graph
	    # list of outgoing edges
        # separated by single whitespace	
        graph = {}
        graph_rev = {}
        edge_count = 0
        vertex_count = 0			
        with open(graph_file, "r") as file:
            for line in file:
                s = [int(x)-1 for x in line.split() if x!='\n']
                tail = int(s[0])
                head = int(s[1])
                if tail in graph.keys():
                    (graph[tail]).append(head)
                else :
                    graph[tail] = [head]
                    vertex_count += 1
                if (head in graph.keys()) == False:
                    graph[head] = []
                    vertex_count += 1
                if head in graph_rev.keys():
                    (graph_rev[head]).append(tail)
                else :
                    graph_rev[head] = [tail]
                if (tail in graph_rev.keys()) == False:
                    graph_rev[tail] = []
				
                edge_count += 1 				
        return graph, graph_rev, edge_count, vertex_count
		
    def scc_kosaraju(self, nbr_scc):
        adj_lst = _adjacency_list(self.adj_dict)
        adj_lst_rev = _adjacency_list(self.adj_dict_rev)		
	    # initialize scc_list with zeros
        scc_list = [0]*nbr_scc
        nodes_in_order_of_finishing_time = _dfs_loop_backward(adj_lst_rev)
        leaders = _dfs_loop_forward(adj_lst, nodes_in_order_of_finishing_time, scc_list)    	
        return scc_list

#-----------------------------------------------------------------------------------------------------------------------
		
# Auxiliary functions Kosaraju's algorithm for finding strongly connected components	
def _compare_and_replace(scc_list, component_size):
    scc_list.append(component_size)
    scc_list.sort(reverse=True)
    scc_list.pop(-1)
			
def _dfs_loop_backward(adj_lst_rev):
	# bookkeeping
    vertex_count = len(adj_lst_rev)
    explored = [False]*vertex_count	
    nodes_in_order_of_finishing_time = []
    for start_vertex in range(vertex_count-1,-1,-1):
        if explored[start_vertex] == False:
            _dfs_ft(adj_lst_rev, start_vertex, explored, nodes_in_order_of_finishing_time)    
    return nodes_in_order_of_finishing_time
	
def _dfs_loop_forward(adj_lst, start_vertices, scc_list):
	# bookkeeping
    vertex_count = len(adj_lst)
    explored = [False]*vertex_count
    leaders = [None]*vertex_count
    for ii in range(vertex_count-1,-1,-1):
        if explored[start_vertices[ii]] == False:
            component_size = _dfs_ldr(adj_lst, start_vertices[ii], explored, leaders)
            _compare_and_replace(scc_list, component_size)
    return leaders

def _dfs_ft(adj_lst, start_vertex, explored, nodes_in_order_of_finishing_time):
	# mark start vertex as explored
    explored[start_vertex] = True
    # add start vertex to stack
    stack = list([start_vertex])
	# initialize component size to 1
    component_size = 1
    while stack != []:
        vertex_v = stack[-1]
        found_unexplored = False
        ii = 0
        while not found_unexplored and adj_lst[vertex_v] != []: 
            vertex_w = adj_lst[vertex_v][-1] 
            if explored[vertex_w] == False:
                # mark vertex as explored
                explored[vertex_w] = True
                # add vertex to stack
                stack.append(vertex_w)
				# flag the occurrrence of an unexplored node
                found_unexplored = True
		    # remove node from adjacency list (heads)
            adj_lst[vertex_v].pop()
            ii += 1       		
        if not found_unexplored:
            stack.pop()
            nodes_in_order_of_finishing_time.append(vertex_v)			
    return component_size

def _dfs_ldr(adj_lst, start_vertex, explored, leaders):
	# mark start vertex as explored
    explored[start_vertex] = True
	# start_vertex is its own leader
    leaders[start_vertex] = start_vertex
    # add start vertex to stack
    stack = list([start_vertex])
	# initialize component size to 1
    component_size = 1
    while stack != []:
        vertex_v = stack[-1]
        found_unexplored = False
        ii = 0
        while not found_unexplored and adj_lst[vertex_v] != []: 
            vertex_w = adj_lst[vertex_v][-1] 
            if explored[vertex_w] == False:
                # mark vertex as explored
                explored[vertex_w] = True
                # assign leader
                leaders[vertex_w] = start_vertex
                component_size += 1
                # add vertex to stack
                stack.append(vertex_w)
				# flag the occurrrence of an unexplored node
                found_unexplored = True
		    # remove visited node from adjacency list (heads)
            adj_lst[vertex_v].pop()
			
            ii += 1 		
        if not found_unexplored:
            stack.pop()
    return component_size

# General auxiliary functions 	
def _adjacency_list(adj_dict):
	n = len(adj_dict)
	adj_lst = list([None]*n)
	for ii in range(0,n):
		adj_lst[ii] = adj_dict[ii]		
	return adj_lst	

#-----------------------------------------------------------------------------------------------------------------------
	
# Class implementation of union-find data structure
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

# To do: remove classes related to KargerMinCut	
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

  
