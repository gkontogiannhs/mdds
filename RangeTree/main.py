from rangetree import RangeTree1D, RangeTree2D, Point
from random import randint


if __name__ == '__main__':
    # points = [('george', 2, [0, 1, 1, 0]), ('smith', 4, [0, 1, 1, 0]), ('sofi', 5, [0, 1, 1, 0]), ('jannete', 3, [0, 1, 1, 0])]
    points = [Point(randint(0, 100), randint(0, 100)) for _ in range(50)]
    print("points:")
    print(points)
    # x_range = ('a', 'k')
    # y_range = (0, 2)

    tree = RangeTree1D(points, axis=0)
    print("Once created:" + str(tree.query((-1, 101))))

    print("Delete node: " + str(points[0]))
    tree.delete(points[0])

    print("Re-query:")
    print(list(set(points)-set(tree.query((-1, 101)))))
    print()
    print()

    x_range = (20, 60)
    y_range = (30, 50)
    temp = []
    for point in points:
        if (x_range[0] <= point[0] <= x_range[1]):
            if  (y_range[0] <= point[1] <= y_range[1]):
                temp.append(point)

    # temp.sort()
    print("Silly")
    temp.sort(key=lambda p: p[0])
    print(temp)
    print()



    tree = RangeTree2D(points)

    # Query the tree for all points in the range (5, 11)
    result = tree.range_search(x_range=x_range, y_range=y_range)
    print("RangeTree")
    result.sort(key=lambda p: p[0])
    print(result)  # Output: [(6,), (7,), (8,), (9,), (10,)]

    # Insert a new point into the tree
    # tree.insert((5,))

    # Query the tree for all points in the range (4, 9)
    # result = tree.query((4, 9))
    # print(result)  # Output: [(5,), (6,), (7,), (8,), (9,)]
