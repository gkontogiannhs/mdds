'''
    A range tree is a data structure that can be used for efficient range searching in multidimensional space.

    The class has three main methods:
        def __init__(self, points, axis=0). 
            The init method is the constructor for the class and takes two inputs:
                points: A list of points in 2D space represented as tuple of x, y coordinates
                axis: decides on which dimension to sort each time
        
        def _build_tree(self, points):
            The _build_tree method is a recursive method that takes two inputs:
                points: A list of points that needs to be added to the tree

        def range_search(self, x_range, y_range):
            The range_search method is used to query the tree and find all points that lie within a specified range. It takes two inputs:
                x_range: Represents the range of x-coord. Could be any iterable containing 2 numbers
                y_range: Represents the range of y-coord. Could be any iterable containing 2 numbers

'''


class Node:
    '''
        Represents a node in the range tree.
        Each node has the following attributes:
            - left: the left child node of the current node
            - right: the right child node of the current node
            - value: the point represented by the node
            - y_tree: the 1D range tree built on the y-coordinates of the points represented by the current node
    '''

    def __init__(self, left=None, right=None, value=None, y_tree=None):
        self.left = left
        self.right = right
        self.value = value
        self.y_tree = y_tree


class RangeTree1D:
    """
        RangeTree1D is a class that represents a 1-dimensional range tree.
        It's a data structure that allows you to efficiently query ranges of points along a single axis.
        The class is implemented as a binary search tree where the nodes represent points and each node has
        a left and a right child representing the points that are less than or greater than the point at the node, respectively. 
    """
    def __init__(self, points, axis=0):
        self.axis = axis
        self.root = self._build_tree(points)
    

    def insert(self, point):
        if not self.root:
            self.root = Node(value=point)
            return
        
        if point[self.axis] < self.root.value[self.axis]:
            if self.root.left:
                self.root.left.insert(point)
            else:
                self.root.left = RangeTree1D([point], axis=self.axis)
        else:
            if self.root.right:
                self.root.right.insert(point)
            else:
                self.root.right = RangeTree1D([point], axis=self.axis)


    def _build_tree(self, points):

        if not points: return None

        if len(points) == 1:
            return Node(value=points[0])

        points.sort(key=lambda point: point[self.axis])

        median = len(points) // 2

        left = RangeTree1D(points[:median], axis=self.axis)
        right = RangeTree1D(points[median+1:], axis=self.axis)
        
        return Node(left=left, right=right, value=points[median])
    
    # NOT USED
    def _get_values(self, range):
        if not self.root:
            return []
        
        values = []
        if range[0] <= self.root.value[self.axis] <= range[1]:
            values.append(self.root.value)
        
        if self.root.left:
            values += self.root.left._get_values(range)
        if self.root.right:
            values += self.root.right._get_values(range)
        
        return values


    def query(self, range):
        if not self.root: return []

        values = []
        if range[0] <= self.root.value[self.axis] <= range[1]:
            values.append(self.root.value)

        if self.root.left:
            values += self.root.left.query(range)
        if self.root.right:
            values += self.root.right.query(range)
        
        return values


    def update(self, point, new_point):
        if not self.root:
            return

        if self.root.value == point:
            self.root.value = new_point
        elif point[self.axis] < self.root.value[self.axis]:
            if self.root.left:
                self.root.left.update(point, new_point)
        elif point[self.axis] > self.root.value[self.axis]:
            if self.root.right:
                self.root.right.update(point, new_point)


    def print_tree(self):
        self._print_tree(self.root, 0)
        

    def _print_tree(self, root, depth):
        if not root:
            return
        self._print_tree(root.right, depth + 1)
        print("  " * depth + "-> " + str(root.value))
        self._print_tree(root.left, depth + 1)


    def delete(self, point):
        if self.root:
            if self.root.value == point:
                if self.root.left is None and self.root.right is None:
                    self.root = None  # The root is a leaf node
                elif self.root.left is None:
                    self.root = self.root.right  # The root has only a right child
                elif self.root.right is None:
                    self.root = self.root.left  # The root has only a left child
                else:
                    # The root has two children, find the minimum value in the right subtree
                    # and replace the root value with it
                    min_node = self.root.right

                    while min_node.left:
                        min_node = min_node.left
                    self.root.value = min_node.value
                    self.root.right.delete(point)  # delete the point instead of the minimum value

            elif point[self.axis] < self.root.value[self.axis]:
                # The point we want to delete is in the left subtree
                if self.root.left:
                    self.root.left.delete(point)
                        
            elif point[self.axis] > self.root.value[self.axis]:
                # The point we want to delete is in the right subtree
                if self.root.right:
                    self.root.right.delete(point)



class RangeTree2D:
    """
        A 2D range tree implementation that allows for efficient range searches in two dimensions.
        The tree is constructed using a modified form of the k-d tree algorithm, where each
        node in the tree represents a split in the data along one of the two dimensions.
        Additionally, each node also contains a 1D range tree of the data points that fall within its
        region, to allow for efficient searches along the other dimension.
    """

    def __init__(self, points, axis=0):
        """
            Initializes a 2D range tree with the given list of points. The tree is balanced based on the x-coordinates of
            the points by default, but the axis can be changed by setting the axis parameter to 1.
            
            Parameters:
            - points (List[Tuple[int, int]]): A list of (x, y) tuples representing the points in the tree.
            - axis (int): The axis to use for the initial split (default: 0, which corresponds to the x-axis)
        """

        self.axis = axis
        self.root = self._build_tree(points)


    def _build_tree(self, points):
        """
            Builds the 2D range tree recursively by dividing the input points into left and right subsets,
            according to the median of the x-coordinates of the points.

            This method is called during initialization and should not be called directly.
            
            Parameters:
            - points (List[Tuple[int, int]]): A list of (x, y) tuples representing the points in the tree.
            
            Returns:
            - Node: The root node of the tree.
        """

        if not points:
            return None

        if len(points) == 1:
            return Node(value=points[0], y_tree=RangeTree1D(points, axis=1))

        # sort by x coord
        points.sort(key=lambda point: point[self.axis])
        
        median = len(points) // 2

        left_points = points[:median]
        right_points = points[median+1:]

        left = RangeTree2D(left_points) if left_points else None
        right = RangeTree2D(right_points) if right_points else None

        return Node(left=left, right=right, value=points[median], y_tree=RangeTree1D(points, axis=1))


    def range_search(self, x_range, y_range):
        """
            Performs a range search on the 2D range tree, returning all points that fall within the given x-range and y-range.
            The search starts at the root of the tree and recursively traverses the left and right subtrees,
            depending on the location of the query range relative to the current node. 
        
            Parameters:
            - x_range (Tuple[int, int]): A tuple representing the x-range of the query, in the form (x_min, x_max).
            - y_range (Tuple[int, int]): A tuple representing the y-range of the query, in the form (y_min, y_max).
            
            Returns:
            - List[Tuple[int, int]]: A list of (x, y) tuples representing the points in the tree that fall within
            the given x-range and y-range.

        """
        if self.root is None: return []
        
        if x_range[0] <= self.root.value[self.axis] <= x_range[1]:
            # Return only the points in the y_tree that fall within the x-range of the query
            return [point for point in self.root.y_tree.query(y_range) if x_range[0] <= point[0] <= x_range[1]]
            # return self.root.y_tree.query(y_range)
        
        values = []
        if x_range[0] > self.root.value[self.axis]:
            if self.root.right:
                values += self.root.right.range_search(x_range, y_range)
        elif x_range[1] < self.root.value[self.axis]:
            if self.root.left:
                values += self.root.left.range_search(x_range, y_range)
        return values


    def print_tree(self):
        self._print_tree(self.root, 0)


    def _print_tree(self, root, depth):
        if not root:
            return
        self._print_tree(root.right, depth + 1)
        print("  " * 2 * depth + "-> " + str(root.value))
        self._print_tree(root.left, depth + 1)
        print("  " * 2 * depth + "    |")
        print("  " * depth + "    +-- Y Tree:")
        root.y_tree.print_tree()





