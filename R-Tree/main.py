from rtree import *
from random import randint


if __name__ == '__main__':

    rtree = RTree()

    N = 50
    points = list(set([(randint(0, 24), randint(0, 20)) for _ in range(N)]))
    
    x1, x2 = 0, 14
    y1, y2 = 0, 10

    r_results = []
    for point in points:
        if x1 <= point[0] <= x2 and y1 <= point[1] <= y2:
            r_results += [point]

    r_results.sort(key=lambda p: p[0])
    print("Naive check:")
    print(r_results)


    # insert points
    for point in points: rtree.insert(point)
    
    idx = randint(0, N-5)
    print("Searching for:", points[idx])

    print("Exists:")
    print(rtree.exists(points[idx]))

    print("Ranges")
    matched = rtree.range_search(Rectangle(x1, y1, x2, y2))

    matched.sort(key=lambda p: p[0])
    print(matched)
