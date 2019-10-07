import random
list = [[random.randint(10, 99) for i in range(5)] for j in range(60)]
print(list)
print(len(list))
results = [sum (i) for i in list]
print(results)
print(len(results))