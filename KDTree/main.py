from kdtree import KDTree, Point
from pandas import read_excel
from os.path import expanduser
from random import randint

import string
import random


if __name__ == "__main__":

    N = 500
    points = [Point(randint(0, 100), randint(0, 100), random.choice(string.ascii_letters)) for _ in range(N)]

    query = ((20, 60), (30, 70))
    kdtree = KDTree(points, k=2)
    # kdtree.print_tree()
    temp = []
    for point in points:
        if query[0][0] <= point[0] <= query[0][1] and query[1][0] <= point[1] <= query[1][1]:
            temp.append(point)
    temp.sort(key=lambda p: p[0])
    print(temp)

    results = kdtree.range_search(query=query)
    results.sort(key=lambda p: p[0])
    print(results)
    # query = ((20, 30), (10, 20))