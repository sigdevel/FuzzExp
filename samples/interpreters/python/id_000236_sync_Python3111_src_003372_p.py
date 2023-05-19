import sys





def matmul(a, b): 
	c = [[b[j][i] for j in range(len(b))] for i in range(len(b[0]))]
	d = [[0 for j in range(len(b[0]))] for i in range(len(a))] 
	for i in range(len(a)):
		for j in range(len(b[0])):
			s = 0
			ai = a[i]
			cj = c[j]
			for k in range(len(a[0])):
				s += ai[k] * cj[k]
			d[i][j] = s
	return d
	
def main():
	n = 100
	if (len(sys.argv) > 1): n = int(sys.argv[1])
	n = int(float(n)/2) * 2 
	tmp = 1. / n / n
	a = [[tmp * (i - j) * (i + j) for j in range(n)] for i in range(n)]
	b = [[tmp * (i - j) * (i + j) for j in range(n)] for i in range(n)]
	d = matmul(a, b)
	print(d[int(n/2)][int(n/2)])

if __name__ == '__main__': main()
