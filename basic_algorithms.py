from math import floor, ceil
import statistics
import timeit

def karatsuba_multiplication(x,y):
    sx = str(x)
    sy = str(y)
    n = max(len(sx),len(sy))
    if len(sx) == 1 and len(sy) == 1:
        return x*y 
    m = ceil(n/2)
    a = int(x//(10**m))
    b = int(x%(10**m))
    c = int(y//(10**m))
    d = int(y%(10**m))
    ac = karatsuba(int(a), int(c))
    bd = karatsuba(int(b),int(d))
    adbc = karatsuba(int(a)+int(b), int(c)+int(d))-ac-bd
    return int(str(ac)+'0'*2*m) + int(str(adbc)+'0'*m) +bd
	
def merge_left_right(left,right):
    result = list()
    i,j = 0,0
    inv_count = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
            inv_count += (len(left)-i)
    result += left[i:]
    result += right[j:]
    return result,inv_count

def merge_sort(lst):
    if len(lst) <= 1:
        return lst, 0
    middle = len(lst) // 2
    left,inv_left = merge_sort(lst[:middle])
    right,inv_right = merge_sort(lst[middle:])
    merged, count = merge_left_right(left,right)
    count += (inv_left + inv_right)
    return merged, count
	
def partition(array,left,right, nbr_cmp):
	
	# select pivot element
    pivot = __select_pivot(array, left, right, 'median')
		
    nbr_cmp += right-left
    ii = left+1
    for jj in range(ii,right+1):
        if array[jj] < pivot:
            # swap elements
            array[ii], array[jj] = array[jj], array[ii]
            # move boundary
            ii += 1
	# swap elements
    array[left], array[ii-1] = array[ii-1], array[left]
    pivot_idx = ii-1
    return pivot_idx, nbr_cmp
	
def quick_sort(array, left, right, nbr_cmp):
    
    if len(array) == 1:
        return nbr_cmp
    
    if left >= right:
        return nbr_cmp

    pivot_idx, nbr_cmp = partition(array,left,right, nbr_cmp)  

    nbr_cmp = quick_sort(array,left,pivot_idx-1,nbr_cmp)
    nbr_cmp = quick_sort(array,pivot_idx+1,right,nbr_cmp)

    return nbr_cmp

def __select_pivot(array, left, right, select_option):
	
    if select_option == 'last':
        array[left], array[right] = array[right], array[left]	
    if select_option == 'median':	# median of three
        mid = (left+right)//2
        mid_val = statistics.median([array[left],array[right], array[mid]])
        if mid_val == array[right]:
            array[left], array[right] = array[right], array[left]
        if mid_val == array[mid]:
            array[left], array[mid] = array[mid], array[left]
    # if select_option == 'first':
	    # idle
    pivot = array[left]	
	
    return pivot


			

    

	
