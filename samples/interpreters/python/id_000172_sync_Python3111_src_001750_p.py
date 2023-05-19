def sum35a(n):
    'Direct count'
    
    return sum(x for x in range(n) if x%3==0 or x%5==0)

def sum35b(n):
    "Count all the 3's; all the 5's; minus double-counted 3*5's"
    
    return sum(range(3, n, 3)) + sum(range(5, n, 5)) - sum(range(15, n, 15))

def sum35c(n):
    'Sum the arithmetic progressions: sum3 + sum5 - sum15'
    consts = (3, 5, 15)
    
    divs = [(n-1) // c for c in consts]
    sums = [d*c*(1+d)/2 for d,c in zip(divs, consts)]
    return sums[0] + sums[1] - sums[2]


for n in range(1001):
    sa, sb, sc = sum35a(n), sum35b(n), sum35c(n)
    assert sa == sb == sc  

print('For n = %7i -> %i\n' % (n, sc))


for p in range(7):
    print('For n = %7i -> %i' % (10**p, sum35c(10**p)))


p = 20
print('\nFor n = %20i -> %i' % (10**p, sum35c(10**p)))
