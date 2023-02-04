from functools import reduce

a = [1,2,3]
value = reduce(lambda x,y:x+y,a)
print(type(value),value)