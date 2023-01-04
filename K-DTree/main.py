from kdtree import KDTree
from pandas import read_excel
from os.path import expanduser
from random import randint

import string

import random

if __name__ == "__main__":
    
    path = f"{expanduser('~')}/Desktop/Multi-Dimensional-DS/List_of_computer_scientists.xlsx"

    # points = read_excel(path)
    # points = [tuple(x) for x in points.to_numpy()][:50]
    # points = [(randint(0, 100), randint(0, 100), [randint(0, 1) for _ in range(4)]) for _ in range(7)]
    points = [(randint(0, 100), randint(0, 100), random.choice(string.ascii_letters)) for _ in range(200)]
    print(points)

    query = ((20, 60), (30, 70))
    kdtree = KDTree(points, k=2)
    # kdtree.print_tree()
    temp = []
    for point in points:
        if query[0][0] <= point[0] <= query[0][1] and query[1][0] <= point[1] <= query[1][1]:
            temp.append(point)
    temp.sort()
    print(temp)

    results = kdtree.range_search(query=query)
    results.sort()
    print(results)
    # query = ((20, 30), (10, 20))