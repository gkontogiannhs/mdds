"""
    This is an implementation of a QuadTree data structure, which is a type of space-partitioning data structure that is used
    to organize points in two-dimensional space.

    The QuadTree is a recursive data structure that subdivides a space into four quadrants,
    each of which can contain a set of points. Each quadrant can also be further divided into four sub-quadrants, and so on,
    until a maximum capacity of points is reached.
    
    The Rectangle class is used to represent the boundaries of the quadrants and the QuadTree class is used to manage the structure
    of the quadrants and the points they contain. 
"""


""""
The QuadTree class takes an optional tile argument, which is a Rectangle object representing the boundary of the current node,
and an optional points argument, which is a list of Point objects to insert into the tree. The n argument specifies
the maximum number of points that a tile can contain before it needs to be divided into four sub-tiles.

The QuadTree class has a number of methods for interacting with the tree:

    The __init__ method initializes the tree and optionally subdivides it to insert the given points.
    The bounds_to_rect method takes in two Point objects and returns a rectangle representing the boundary of the points.
    The subdivide method divides the current tile into four sub-tiles, creating new QuadTree instances for each.
    The insert method inserts a point into the tree by first checking if it lies within the boundary of the current tile. If there is space in the current tile and the point lies within the boundary, the point is added to the current tile. If the tile is already full, and has not been subdivided, it subdivides the tile and recursively insert the point into one of the subtiles.
    The init_rectangle method calculate the rectangle that encloses all the points passed to the QuadTree.
    The Rectangle class has a number of methods for interacting with the rectangle

    __init__ takes in the position x,y and the width and height of the rectangle
    contains checks if a point lies within the rectangle boundaries
    intersects checks if the rectangle intersects with another rectangle
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
        """ Return True if point in quadrant """
        return (point.x >= self.rx - self.w and
                point.x <= self.rx + self.w and
                point.y >= self.ry - self.h and
                point.y <= self.ry + self.h)


    def intersects(self, rect):
        """ Return True if this rectangle intersects with the given rectangle. """
        return (self.rx - self.w <= rect.rx + rect.w or
                self.rx + self.w >= rect.rx - rect.w or
                self.ry - self.h <= rect.ry + rect.h or
                self.ry + self.h >= rect.ry - rect.h)


class QuadTree:
    def __init__(self, tile=None, points=[], n=4):
        
        # initialize tile fitting all possible points
        self.tile = tile if tile else self.init_rectangle(points) 

        # each tile's capacity of maximum points
        self.capacity = n

        self.points = []

        self.divided = False

        for point in points:
           self.insert(point)


    @staticmethod
    def bounds_to_rect(point1, point2):
        xmin, ymin = min(point1.x, point2.x), min(point1.y, point2.y)
        xmax, ymax = max(point1.x, point2.x), max(point1.y, point2.y)
        return Rectangle((xmin+xmax)/2, (ymin+ymax)/2, (xmax-xmin)/2, (ymax-ymin)/2)


    def subdivide(self):
        """ Divide the tile into four sub-tiles. """
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

    def init_rectangle(self, points):

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

    