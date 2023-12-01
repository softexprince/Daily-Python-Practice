# Task 2:- 
# Python Program to Swap Two Elements in a List
# I have one list u want to swap 2 elements in list

# Input : List = [23, 65, 19, 90], pos1 = 1, pos2 = 3
# Output : [19, 65, 23, 90]


def SwapFunc(listname, first, second):
    get = listname[first], listname[second]
    
    listname[second], listname[first] = get
    
    return listname


name = ["prince", "pritha", "prem", "Raja", "tripurarai"]

res = SwapFunc(name, 1,3)
print(res)

# Method Swap Two Elements in a List using comma assignment

def swaplist(listname, pos1, pos2):
    listname[pos1], listname[pos2] = listname[2], listname[1]
    
    return listname

res2 = swaplist(res, 2,4)
print(res2)
