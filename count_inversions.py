from basic_algorithms import merge_sort
from io_utils import read_txt
	
if __name__=="__main__":
    given_data = read_txt('integer_array.txt')
    lst = [int(given_data[i]) for i in range(0,len(given_data))]
    sorted_list,inversions = merge_sort(lst)
    print(inversions)
	
	

	
	
	
	
	
	
	
	
	
	
	
	
	