def solution(a):
    cnt = 0
    result = 0
    found_one = False
 
    i = a    
         
    while i:
        if i & 1 == 1:
            if (found_one == False):
                found_one = True
            else:
                result = max(result,cnt)
            cnt = 0
        else:
            cnt += 1
        i >>= 1
    
    return result
print(solution(1000000))