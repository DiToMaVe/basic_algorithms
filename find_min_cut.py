from karger_min_cut import *
	
if __name__=="__main__":
    
    graph = Graph(graph_file = 'input\kargerMinCut.txt')
    karger_mc = KargerMinCut(graph.adj_dict)
	
    count = 0
    mincut = karger_mc.edge_count
    for mc in range(0,1):
        out = karger_mc.find_min_cut(100)
        if out < mincut:
            mincut = out
        if out != 17:
            count +=1
        print('iteration', mc)
    print('Number of failed trials:',count)
    print('Minimum cut:',out)