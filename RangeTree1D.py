class Node:
    def __init__(self, left=None, right=None, value=None, y_tree=None):
        self.left = left
        self.right = right
        self.value = value
        self.y_tree = y_tree


class RangeTree1D:
    def __init__(self, points, axis=0):
        self.axis = axis
        self.root = self._build_tree(points)
    

    def _build_tree(self, points):
        if not points:
            return None
        
        if len(points) == 1:
            return Node(value=points[0])
        
        points.sort(key=lambda point: point[self.axis])
        median = len(points) // 2

        left = self._build_tree(points[:median])
        right = self._build_tree(points[median+1:])
        
        return Node(left=left, right=right, value=points[median])
    

    def query(self, range):
        if not self.root:
            return []

        if range[0] <= self.root.value[self.axis] <= range[1]:
            return self._get_values(self.root, range)

        values = []
        if range[0] > self.root.value[self.axis]:
            if self.root.right:
                values += self._get_values(self.root.right, range)
        elif range[1] < self.root.value[self.axis]:
            if self.root.left:
                values += self._get_values(self.root.left, range)
        return values

        
    def _get_values(self, node, range):
        if not node:
            return []
        
        values = []
        if range[0] <= node.value[self.axis] <= range[1]:
            values.append(node.value)
        
        if node.left:
            values += self._get_values(node.left, range)
        if node.right:
            values += self._get_values(node.right, range)
        
        return values
    

    def print_tree(self):
        self._print_tree(self.root, 0)
        

    def _print_tree(self, root, depth):
        if not root:
            return
        self._print_tree(root.right, depth + 1)
        print("  " * depth + "-> " + str(root.value))
        self._print_tree(root.left, depth + 1)




