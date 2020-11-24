import random
from io_utils import read_txt
from basic_algorithms import quick_sort
		
if __name__=="__main__":
    given_data = read_txt('input\integer_array_1_3_16.txt')
    lst = [int(given_data[i]) for i in range(0,len(given_data))] #len(given_data)
    print(quick_sort(lst,0,len(lst)-1,0))