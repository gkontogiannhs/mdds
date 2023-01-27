""""
    The above code is an implementation of a QuadTree data structure in Python, along with related classes like Point, Rectangle, and QuadTree.

    The Point class is used to represent a point in two-dimensional space, with x and y coordinates and an optional payload attribute.
    The __repr__ and __str__ methods provide a string representation of the point in the format (x, y) and payload if provided.

    The Rectangle class is used to represent a rectangle with a given center point (rx, ry), width (w) and height (h).
    The contains method is used to check if a given point is within the boundaries of the rectangle and intersects method is used to check
    if a given rectangle intersects with another rectangle.

    The QuadTree class is the main class and is used to represent the QuadTree data structure. It has a capacity of n points,
    points array which will keep track of points, a tile attribute which is a Rectangle object and divided attribute which will keep
    track if the tree is divided or not. The insert method is used to insert a point into the tree. If the point does not lie inside
    the boundary of the tile or if the capacity of the current tile is already full, then it subdivides the tile into four sub-tiles,
    each of which can be further divided as necessary.

    This code represents the basic functionality of QuadTree and how to use it to divide the two-dimensional space into smaller regions
    and quickly find points within a specific region. However, you can add more functionality to it as per your requirements.

    You can also use this tree to perform the spatial queries like range queries, nearest neighbour search and more,
    but that depends on how you want to use the tree structure.
"""
class Rectangle:
    def __init__(self, rx, ry, w, h):
        self.rx = rx
        self.ry = ry
        self.w = w
        self.h = h


    def __repr__(self):
        return str(self.rx, self.ry, self.w, self.h)


    def __str__(self):
        return '({:.2f}, {:.2f}, {:.2f}, {:.2f})'.format(self.rx, self.ry, self.w, self.h)


    # check if point is within tile boundaries
    def contains(self, point):

        return (point.x >= self.rx - self.w and
                point.x <= self.rx + self.w and
                point.y >= self.ry - self.h and
                point.y <= self.ry + self.h)


    def intersects(self, rect):
        """
        Return True if this rectangle intersects with the given rectangle.
        """
        return (self.rx - self.w <= rect.rx + rect.w or
                self.rx + self.w >= rect.rx - rect.w or
                self.ry - self.h <= rect.ry + rect.h or
                self.ry + self.h >= rect.ry - rect.h)


class QuadTree:
    def __init__(self, tile=None, points=[], n=4):

        self.tile = tile if tile else self.calculate_rectangle(points) 

        # each tile's capacity of maximum points
        self.capacity = n

        self.points = []

        self.divided = False

        for point in points:
           self.insert(point)


    def bounds_to_rect(self, point1, point2):
        xmin, ymin = min(point1.x, point2.x), min(point1.y, point2.y)
        xmax, ymax = max(point1.x, point2.x), max(point1.y, point2.y)
        return Rectangle((xmin+xmax)/2, (ymin+ymax)/2, (xmax-xmin)/2, (ymax-ymin)/2)


    def subdivide(self):
        """
            Divide the tile into four sub-tiles.
        """
        rx, ry = self.tile.rx, self.tile.ry
        w, h = self.tile.w, self.tile.h

        self.northeast = QuadTree(tile=Rectangle(rx + w/2, ry - h/2 , w/2, h/2), n=self.capacity)

        self.northwest = QuadTree(tile=Rectangle(rx - w/2, ry - h/2 , w/2, h/2), n=self.capacity)

        self.southeast = QuadTree(tile=Rectangle(rx + w/2, ry + h/2 , w/2, h/2), n=self.capacity)

        self.southwest = QuadTree(tile=Rectangle(rx - w/2, ry + h/2 , w/2, h/2), n=self.capacity)

        self.divided = True


    def insert(self, point):
        
        # The point does not lie inside boundary: bail.
        if not self.tile.contains(point): return False

        # if points less than box capacity
        # safely append it
        if len(self.points) < self.capacity:
            self.points += [point]
            return True

        # No room: divide if necessary, then try the sub-quads.
        if not self.divided:
            self.subdivide()

        return (self.northeast.insert(point) or
                self.northwest.insert(point) or
                self.southeast.insert(point) or
                self.southwest.insert(point))


    # The initial rectangle of the quadtree, often called the root rectangle or bounding box,
    # should be large enough to enclose all the points that will be inserted into the tree. 
    # The simplest approach is to define the root rectangle with the minimum and maximum x and y coordinates of all the points in the dataset.

    def calculate_rectangle(self, points):

        # find min max for x-coord
        min_x = min(points, key=lambda p: p.x).x
        max_x = max(points, key=lambda p: p.x).x

        # find min max for x-coord
        min_y = min(points, key=lambda p: p.y).y
        max_y = max(points, key=lambda p: p.y).y

        rx = (min_x + max_x) / 2
        ry = (min_y + max_y) / 2
        w = (max_x - min_x) / 2
        h = (max_y - min_y) / 2

        return Rectangle(rx, ry, w, h)


    def search(self, point):
        """
        Search the tree for a point and return True if point is found, False otherwise
        """
        if not self.tile.contains(point): return False

        if point in self.points: return True

        if not self.divided:
            return False
        else:
            return (self.northeast.search(point) or
                    self.northwest.search(point) or
                    self.southeast.search(point) or
                    self.southwest.search(point))


    def search_radius(self, point, radius):
        from math import hypot
        """
        Search the tree for points within a given radius of the point
        """
        # base case : point not found in this tile
        if not self.tile.contains(point): return []

        results = []
        # point found
        for p in self.points:
            dist = hypot(point.x - p.x, point.y - p.y)
            if dist <= radius:
                results += [p]

        # if not divided go through each sub quadrant
        # and check
        if not self.divided:
            return results
        else:
            results += self.northeast.search_radius(point, radius)
            results += self.northwest.search_radius(point, radius)
            results += self.southeast.search_radius(point, radius)
            results += self.southwest.search_radius(point, radius)

            return results


    def range_search(self, rect):
        """
        Return a list of all points in the Quadtree that lie within the given rectangle.
        """

        results = []
        # If the query rectangle does not intersect the tile, return an empty list
        if not self.tile.intersects(rect):
            return results

        # Check the points in this node
        for point in self.points:
            if rect.contains(point):
                results.append(point)

        # If the node has been divided, search the sub-regions
        if self.divided:
            results += self.northwest.range_search(rect)
            results += self.northeast.range_search(rect)
            results += self.southeast.range_search(rect)
            results += self.southwest.range_search(rect)

        return results

    