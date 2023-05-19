from random import random, choice
from math import sqrt

"chaos game"
def chaos_game(n, shape_points):
    
    point = [random(), random()]

    for _ in range(n):
        
        point = [(p + s) / 2 for p, s in zip(point, choice(shape_points))]
        yield point







shape_points = [[0.0, 0.0],
                [0.5, sqrt(0.75)],
                [1.0, 0.0]]
with open("sierpinski.dat", "w") as f:
    for point in chaos_game(10000, shape_points):
        f.write("{0}\t{1}\n".format(*point))
