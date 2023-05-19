import time
import sys
import itertools

from itertools import groupby
count = itertools.count(0)


def next_val():
    return next(count) % 25


start_time = time.time()
letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


l = sorted([''.join([letters[next_val()] for _ in range(40)]) for _ in range(10000)])

g = {k: list(v) for k, v in groupby(l, lambda x: x[:2])}

if False:
    pass  

print('TotalTime>>%s<<' % (time.time() - start_time,))
print('TEST SUCEEDED')
