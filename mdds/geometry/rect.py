class Rectangle:
    """
        The Rectangle class is used by the RTree class to create and manage rectangles that bound the different nodes in the tree.
    """

    def __init__(self, x1, y1, x2, y2):
        """
            Initializes a new rectangle with the given coordinates. The coordinates are stored in the variables
            self.x1, self.y1, self.x2, and self.y2, with the constraint that x1 <= x2 and y1 <= y2
        """
        self.x1 = min(x1, x2)
        self.y1 = min(y1, y2)
        self.x2 = max(x1, x2)
        self.y2 = max(y1, y2)
        

    def get_area(self):
        """  Returns the area of the rectangle. """
        return (self.x2 - self.x1) * (self.y2 - self.y1)
    

    def intersects(self, other):
        """  Returns True if the rectangle self intersects with another rectangle other, and False otherwise. """
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)


    def combine(self, other):
        """  Returns a new rectangle that is the smallest rectangle that contains both self and other. """
        x1 = min(self.x1, other.x1)
        y1 = min(self.y1, other.y1)
        x2 = max(self.x2, other.x2)
        y2 = max(self.y2, other.y2)

        return Rectangle(x1, y1, x2, y2)


    def get_enlargement(self, other):
        """ Returns the area by which the rectangle would have to be enlarged in order to contain the rectangle other. """

        if self.intersects(other): return 0

        else:
            combined = self.combine(other)

            return combined.get_area() - self.get_area()
    

    def contains_point(self, point):
        """ Returns True if the rectangle contains the point point, which is an object with x and y attributes, and False otherwise. """
        return self.x1 <= point.x <= self.x2 and self.y1 <= point.y <= self.y2