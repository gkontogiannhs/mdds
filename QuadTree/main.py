from quadtree import QuadTree, Rectangle, Point
from random import randint


if __name__ == '__main__':
    ps = [Point(randint(0,100), randint(0,100), '') for _ in range(100)]
    
    qt = QuadTree(points=ps, n=4)

    point1 = Point(10, 30)
    point2 = Point(60, 50)

    temp = []
    for point in ps:
        if point1.x <= point.x <= point2.x and point1.y <= point.y <= point2.y:
            temp.append(point)

    for point in temp:
        print(f"{point.x, point.y}")

    print()
    print()
    found_points = qt.range_search(point1, point2)
    for point in found_points:
        print(f"{point.x, point.y}")