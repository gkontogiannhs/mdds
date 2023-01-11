from rtree import *
from random import randint


if __name__ == '__main__':

    rtree = RTree()

    N = 10000
    points = list(set([(randint(0, 3000), randint(0, 3000)) for _ in range(N)]))
    x1, x2 = 10, 90
    y1, y2 = 20, 100

    r_results = []
    for point in points:
        if x1 <= point[0] <= x2 and y1 <= point[1] <= y2:
            r_results += [point]

    r_results.sort(key=lambda p: p[0])
    print("Naive check:", str(r_results))


    # insert points
    for point in points: rtree.insert(point)
    
    idx = randint(0, N)

    matched = rtree.range_search(Rectangle(x1, y1, x2, y2))
    matched.sort(key=lambda p: p[0])
    print("Range query:", str(matched))


    print("Missed out:" , str(set(r_results) - set(matched)))

    print("Searching for:", points[idx])
    print("Exists:", str(rtree.exists(points[idx])))

    print("Deleting node: ", str(points[idx]))
    rtree.delete(points[idx])
    print("Exists:", str(rtree.exists(points[idx])))