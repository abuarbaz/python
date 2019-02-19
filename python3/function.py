import math

def squareroot(n):
	root = n/2
	for k in range(20):
		root = (1/2)*(root + (n / root))
	
	return root

	
print(squareroot(9
))