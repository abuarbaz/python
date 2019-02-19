def is_unique1 (alist : [int]) -> bool:
    for i in range(len(alist)):	
        if alist[i] in alist[i+1:]:	
            return False		
    return True
print(is_unique1([1,2.3]))