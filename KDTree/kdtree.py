class Point:
    def __init__(self, x, y, payload=None):
        self.x = x
        self.y = y
        self.payload = payload

    def __getitem__(self, index):
        if index: return self.y
        else: return self.x
  
        
    def __repr__(self):
        return f'{self.x, self.y}: {repr(self.payload)}'


    def __str__(self):
        return f'({self.x}, {self.y})'
        

class Node:
    def __init__(self, left=None, right=None, value=None):
        self.left = left
        self.right = right
        self.value = value


class KDTree:
    def __init__(self, points, k):
        self.points = points
        self.k = k
        self.tree = self._build_tree(points)

    def _build_tree(self, points, depth=0):

        _axis = depth % self.k
        
        if not len(points): return None

        points.sort(key=lambda point: point[_axis])

        median = len(points) // 2

        left = self._build_tree(points[:median], depth+1)
        right = self._build_tree(points[median+1:], depth+1)

        return Node(left=left, right=right, value=points[median])


    def _range_search(self, node, query, depth):
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



