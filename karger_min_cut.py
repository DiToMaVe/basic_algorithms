from graph import *

class KargerMinCut3(Graph):

    def find_min_cut(self, iter):
	    
        min_cut = self.edge_count
        for ii in range(0,iter):
	        min_cut = min(min_cut,self.__find_min_cut())
        return min_cut

    def __find_min_cut(self):
        V = self.vertex_count
        E = self.edge_count
        uf = UnionFind([ii for ii in range(0,V)])
        edges = self.edges()
        
        rand_seq = [kk for kk in range(0,E)]
        shuffle(rand_seq)
        idx_rs = 0
        while V > 2:
            ii = rand_seq[idx_rs] 
            idx_rs += 1
            edge = list(edges[ii])
	
            if uf.find(edge[0],edge[1]) == False:
                V -= 1
                uf.unite(edge[0],edge[1])
		
        min_cut = 0
        for ii in range(0,E):
            edge = list(edges[ii])
            if not uf.find(edge[0],edge[1]):
                min_cut += 1 
        return min_cut	

class KargerMinCut2(Graph):

    def find_min_cut(self, iter):
        out = self.__find_min_cut()
        min_cut = out[0]
        supervertices = out[1]
		
        for i in range(iter):
            out = self.__find_min_cut()
            if out[0] < min_cut:
                min_cut = out[0]
                supervertices = out[1]
        return min_cut, supervertices

    def __find_min_cut(self):
        adj_lst = AdjacencyList(copy.deepcopy(self.adj_dict), self.edge_count)
        graph = adj_lst.dict
        supervertices = {}
        edge_count_x2 = int(self.edge_count*2)
        for key in graph:
            supervertices[key] = [key]	
        min_cut = 0

        while len(graph)>2:
            # 1.1: Pick a random edge
            v1, v2 = adj_lst.pick_random_edge(); 
            adj_lst.edge_count -= len(graph[v1])/2
            adj_lst.edge_count -= len(graph[v2])/2
			
            # 1.2: Merge the edges
            graph[v1].extend(graph[v2])
            
			# 1.3: Update all references to v2 to point to v1
            for vertex in graph[v2]:
                graph[vertex].remove(v2)
                graph[vertex].append(v1)
            
			# 1.4: Remove self loops
            graph[v1] = [x for x in graph[v1] if x != v1]
            
			# 1.5: Update total edges
            adj_lst.edge_count += len(graph[v1])/2
            graph.pop(v2)
            
			# 1.6: Update cut groupings
            supervertices[v1].extend(supervertices.pop(v2))
        
		# 1.7: Calc min cut (number of parallel edges between remaining supervertices)
        for edges in graph.values():
            min_cut = len(edges)
        
		# 1.8: Return min cut and the two supervertices
        del adj_lst
        return min_cut, supervertices   		

class KargerMinCut(Graph):

    def find_min_cut(self, iter):
        min_cut = self.__find_min_cut()
        
        for i in range(iter):
            out = self.__find_min_cut()
            if out < min_cut:
                min_cut = out
        return min_cut

    def __find_min_cut(self):	
        adj_lst = AdjacencyList(copy.deepcopy(self.adj_dict), self.edge_count)
        graph = adj_lst.dict
        while len(graph) > 2:
            v1, v2 = adj_lst.pick_random_edge()
            adj_lst.edge_count -= len(graph[v1])/2
            adj_lst.edge_count -= len(graph[v2])/2	
            # Adding the edges from the absorbed node:
            for vertex in graph[v2]:
                if vertex != v1: # this stops us from making a self−loop
                    graph[v1].append(vertex)
		    # Deleting the references to the absorbed node and changing them to the source node:
            for vertex in graph[v2]:
                graph[vertex].remove(v2)
                if vertex != v1: # this stops us from re−adding all the edges in start.
                    graph[vertex].append(v1)
            adj_lst.edge_count += len(graph[v1])/2
            del graph[v2]
        # Calculate min cut
        links = list(graph.values())
        min_cut = len(links[0])
        return min_cut
								