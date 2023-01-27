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


    def range_search(self, x_range, y_range):
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





