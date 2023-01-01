from RangeTree1D import RangeTree1D, Node


class RangeTree2D:
    def __init__(self, points, axis=0):
        self.axis = axis
        self.root = self._build_tree(points)


    def _build_tree(self, points):
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


    def query(self, x_range, y_range):
        if self.root is None: return []
        
        if x_range[0] <= self.root.value[self.axis] <= x_range[1]:
            # Return only the points in the y_tree that fall within the x-range of the query
            return [point for point in self.root.y_tree.query(y_range) if x_range[0] <= point[0] <= x_range[1]]
        
        values = []
        if x_range[0] > self.root.value[self.axis]:
            if self.root.right:
                values += self.root.right.query(x_range, y_range)
        elif x_range[1] < self.root.value[self.axis]:
            if self.root.left:
                values += self.root.left.query(x_range, y_range)
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