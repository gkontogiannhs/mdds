'''
class KDTree: Represents the KD-Tree itself. The class has the following methods:

    __init__(self, points, k): 
        Initializes the KD-Tree with a list of points and the number of dimensions (k) of each point.
        The constructor also calls the _build_tree method to build the tree.

    _build_tree(self, points, depth=0):
        A helper method that recursively builds the KD-Tree. It takes the current list of points and the current depth
        of the tree as input. At each level of recursion, it sorts the points by the axis specified by the current depth,
        chooses the median point, and creates a new node with that point as the value. The left and right children of the node
        are the results of recursively building the tree on the points to the left and right of the median, respectively.

    _range_search(self, node, query, depth):
        A helper method that does a range search on the KD-Tree. It takes a node, a query (a list of ranges for each dimension),
        and the current depth of the search as input. The method recursively traverses the tree, checking if the value at the
        current node is within the query range. If it is, it adds it to the list of matches. If the query range
        intersects the range of values along the current axis, it continues the search in both the left and right subtrees.
        If the value at the current node is smaller than the lower bound of the query range along the current axis, it continues
        the search in the right subtree. Otherwise, it continues the search in the left subtree.

    range_search(self, query, depth=0):
        A public method that starts the range search at the root of the tree.
'''

from mdds.trees.nodes import Node
class KDTree:
    
    def __init__(self, points, k):
        """
            Initializes the KD-Tree with a list of points and the number of dimensions (k) of each point.
            The constructor also calls the _build_tree method to build the tree.
        """
        self.points = points
        self.k = k
        self.tree = self._build_tree(points)


    def _build_tree(self, points, depth=0):
        """
            A helper method that recursively builds the KD-Tree. It takes the current list of points and the current depth
            of the tree as input. At each level of recursion, it sorts the points by the axis specified by the current depth,
            chooses the median point, and creates a new node with that point as the value. The left and right children of the node
            are the results of recursively building the tree on the points to the left and right of the median, respectively.
        """

        _axis = depth % self.k
        
        if not len(points): return None

        points.sort(key=lambda point: point[_axis])

        median = len(points) // 2

        left = self._build_tree(points[:median], depth+1)
        right = self._build_tree(points[median+1:], depth+1)

        return Node(left=left, right=right, value=points[median])


    def _range_search(self, node, query, depth):
        """
            A helper method that does a range search on the KD-Tree. It takes a node, a query (a list of ranges for each dimension),
            and the current depth of the search as input. The method recursively traverses the tree, checking if the value at the
            current node is within the query range. If it is, it adds it to the list of matches. If the query range
            intersects the range of values along the current axis, it continues the search in both the left and right subtrees.
            If the value at the current node is smaller than the lower bound of the query range along the current axis, it continues
            the search in the right subtree. Otherwise, it continues the search in the left subtree.
        """
        # If the current node is None, return an empty list
        if node is None:
            return []

        # Determine the current axis based on the depth of the search
        _axis = depth % self.k

        # Check if the value at the current node is within the query range
        in_range = all(low <= node.value[i] <= high for i, (low, high) in enumerate(query))

        # If the value is within the range, add it to the list of matches
        matches = [node.value] if in_range else []

        # If the query range intersects the range of values along the current axis,
        # continue the search in both the left and right subtrees
        if query[_axis][0] <= node.value[_axis] <= query[_axis][1]:
            matches += self._range_search(node.left, query, depth+1)
            matches += self._range_search(node.right, query, depth+1)

        # If the value at the current node is smaller than the lower bound of the
        # query range along the current axis, continue the search in the right subtree
        elif node.value[_axis] < query[_axis][0]:
            matches += self._range_search(node.right, query, depth+1)
            
        # Otherwise, continue the search in the left subtree
        else:
            matches += self._range_search(node.left, query, depth+1)

        return matches


    def range_search(self, query, depth=0):

        # Start the search at the root of the tree
        return self._range_search(self.tree, query, depth)


    def print_tree(self):
        self._print_tree(self.tree, 0)
        

    def _print_tree(self, root, depth):

        if not root: return

        self._print_tree(root.right, depth + 1)
        print("  " * depth + "-> " + str(root.value))
        self._print_tree(root.left, depth + 1)



