def passOne(ll):
	i = 0
	for l in ll:
		if i == 2:
			break
		yield {'val' : l}
		i += 1

def pasTwo():
	ll = [1, 2, 3]
	i = 0
	for l in ll:
		# if i == 2: break
		yield {'val' : l}
		i += 1
	ll = [[4, 5, 6], [7, 8, 9], [10, 11, 12]]
	for l in ll:
		for m in l:
			yield {'val' : l}

def test():
	for l in pasTwo():
		print(l)

if __name__ == '__main__':
	test()