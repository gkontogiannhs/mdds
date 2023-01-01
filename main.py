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
            # Return only the points in the y_tree that fall within the y-range of the query
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



from random import randint
# points = [(1, 4), (3, 4), (12, 5), (5, 6), (7, 8), (9, 10), (11, 3), (2, 9), (4, 5), (5, 7), (6, 8), (8, 2), (9, 4), (10, 5), (11, 6), (1, 2), (3, 5), (4, 6), (5, 7), (6, 8)]

points = [(randint(0, 100), randint(0, 100)) for _ in range(50)]
print(points)
print()
temp  = []
for point in points:
    if 30 <= point[0] <= 60 and 20 <= point[1] <= 50:
        temp += [point]

temp.sort()
print(temp)
print()

# create a 2D range tree with x as the main axis
tree = RangeTree2D(points, axis=0)

# query the tree for all points with x in the range [4, 12] and y in the range [5, 8]
result = tree.query((30, 60), (20, 50))
result.sort()
print(result)  # should print [(5, 6), (7, 8)]



