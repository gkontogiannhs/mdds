class Point:
    def __init__(self, x, y, payload=None):
        self.x = x
        self.y = y
        self.payload = payload


class Rectangle:
    def __init__(self, rx, ry, w, h):
        self.rx = rx
        self.ry = ry
        self.w = w
        self.h = h


    # check if point is within tile boundaries
    def contains(self, point):

        return (point.x >= self.rx - self.w and
                point.x < self.rx + self.w and
                point.y >= self.ry - self.h and
                point.y < self.ry + self.h)


    def intersects(self, rect):
        """
        Return True if this rectangle intersects with the given rectangle.
        """
        return (self.rx - self.w < rect.rx + rect.w and
                self.rx + self.w > rect.rx - rect.w and
                self.ry - self.h < rect.ry + rect.h and
                self.ry + self.h > rect.ry - rect.h)


class QuadTree:
    def __init__(self, tile=None, points=[], n=4):

        self.tile = tile if tile else self.calc_root_rect(points) 

        # each tile's capacity of maximum points
        self.capacity = n

        self.points = []

        self.divided = False

        for point in points:
            self.insert(point)


    def subdivide(self):
        """
            Divide the tile into four sub-tiles.
        """
        rx, ry = self.tile.rx, self.tile.ry
        w, h = self.tile.w, self.tile.h

        self.northeast = QuadTree(tile=Rectangle(rx + w/2, ry - h/2 , w/2, h/2), n=self.capacity)

        self.northwest = QuadTree(tile=Rectangle(rx + w/2, ry - h/2 , w/2, h/2), n=self.capacity)

        self.southeast = QuadTree(tile=Rectangle(rx - w/2, ry + h/2 , w/2, h/2), n=self.capacity)

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



    # One way to determine the boundary of the root node is to find
    # the minimum and maximum x and y values among all the points in your input list,
    # and use these values to define the Rectangle object.

    def calc_root_rect(self, points):

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

    
    def exact_search(self, point):
        
        # Search the QuadTree for the given point.
        # Return True if the point is found, False otherwise.

        # If the point does not lie inside the boundaries of the current tile,
        # it can't be in this quadrant.
        if not self.tile.contains(point):
            return False

        # Check if the point is one of the points in this quadrant.
        if point in self.points:
            return True

        # If the quadrant has been divided, search the sub-quadrants.
        if self.divided:
            return (self.northeast.exact_search(point) or
                    self.northwest.exact_search(point) or
                    self.southeast.exact_search(point) or
                    self.southwest.exact_search(point))

        # If we get here, the point is not in this quadrant.
        return False


    def search_radius(self, p, r):
        """
        Search the QuadTree for points within `r` units of the given point `p`.
        Return a list of the points found.
        """
        # Create a rectangle that represents the search range.
        rect = Rectangle(p.x, p.y, r, r)

        # Use the existing search method to find points within the search range.
        return self.exact_search(rect)


    def _search(self, rect):
        """
        Search the QuadTree for points within the boundaries of the given rectangle.
        Return a list of the points found.
        """
        found_points = []

        # If the search rectangle does not intersect with the current tile,
        # there's no point in searching this quadrant further.
        if not self.tile.intersects(rect):
            return found_points

        # Check if any points in this quadrant are within the search rectangle.
        for point in self.points:
            if rect.contains(point):
                found_points.append(point)

        # If the quadrant has been divided, search the sub-quadrants.
        if self.divided:
            found_points += self.northeast._search(rect)
            found_points += self.northwest._search(rect)
            found_points += self.southeast._search(rect)
            found_points += self.southwest._search(rect)

        return found_points


    def range_search(self, point1, point2):
        """
        Search the QuadTree for points within the range [point1.x, point2.x] and
        [point1.y, point2.y]. Return a list of the points found.
        """
        # Create a rectangle that represents the search range.
        rect = Rectangle(0, 0, abs(point1.x - point2.x), abs(point1.y - point2.y))
        rect.rx = min(point1.x, point2.x) + rect.w / 2
        rect.ry = min(point1.y, point2.y) + rect.h / 2

        # Use the existing search method to find points within the search range.
        return self._search(rect)


    