import csv

def read_txt(fn):
    f = open (fn)
    lines_aux = f.readlines()
    f.close()
    lines = list([])
    for line_aux in lines_aux:
        lines.append(line_aux.strip())
    return lines
	
