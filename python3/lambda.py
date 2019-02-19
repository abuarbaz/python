def make_increment(n):
	return lambda x: x + n
f = make_increment(40)
print(f(0))
print(f(1))
print(f(20))