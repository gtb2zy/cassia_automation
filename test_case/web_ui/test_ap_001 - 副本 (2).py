a = [2,4,5,6,7,8,9,30,19,10,54]
for x in reversed(range(len(a))):
	i=0
	while i < x:
		if a[i] > a[i+1]:
			a[i],a[i+1] = a[i+1],a[i]
		i += 1
print(a)