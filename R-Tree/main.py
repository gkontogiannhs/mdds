from rtree import *
from random import randint

if __name__ == '__main__':

    rtree = RTree()

    N = 14
    points = [(randint(0, 100), randint(0, 100)) for _ in range(N)]
    print(points)

    # insert points
    for point in points:
        print(rtree.root.mbr)
        rtree.insert(point)

    for i, child in enumerate(rtree.root.children):
        print(f"Children of root {i}: {child.points}")

    visualize_rtree(rtree.root)
    # search for point (3, 3)
    result = rtree.search(points[0])

    # print the results
    print("Results")
    for node in result: print(node.points)
