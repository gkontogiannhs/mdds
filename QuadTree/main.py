from quadtree import QuadTree, Point
from random import randint


if __name__ == '__main__':

    # create random poitns
    points = [Point(randint(0,100), randint(0,100)) for _ in range(100)]
    
    # build quad tree with max 4 points per tile
    qtree = QuadTree(points=points, n=4)
    
    # define range of query
    point1 = Point(10, 20)
    point2 = Point(40, 50)

    # convert to rectangle tile
    search_region = qtree.bounds_to_rect(point1, point2)

    # make query
    found_points = qtree.range_search(search_region)
    print(found_points)

    # exact seach query: true if found else false
    assert True == qtree.search(points[randint(0, 99)])

    # radius search, for a given point return neigbors in radius r
    radius_points = qtree.search_radius(points[20], 5)
    print(radius_points)
