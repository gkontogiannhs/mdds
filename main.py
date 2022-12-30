class Node:
    def __init__(self, value, points):
        self.value = value
        self.points = points
        self.left = None
        self.right = None


class RangeTree:
    def __init__(self, points):
        self.points = points
        self.root = self.build_tree(self.points)

    def build_tree(self, points):
        # Sort the points by the secdary field
        points.sort(key=lambda x: x[1], reverse=True)

        # Find the median point
        median = len(points) // 2

        # Create a new node with the median point
        node = Node(points[median][0], points)
        # print(f'-> {node.value}: {node.points}')
        # print(f'And left will get: {points[:median]}')
        # print(f'And right will get: {points[median + 1:]}')
        # Recursively build the left and right subtrees
        node.left = self.build_tree(points[:median]) if points[:median] else None
        node.right = self.build_tree(points[median + 1:]) if points[median + 1:] else None

        return node


    def search(self, root, awards, surname_range):
        # If the root is None or has no points, return an empty list
        if root is None or not root.points:
            return []

        # Check the points in the root node
        points = []
        for point in root.points:
            surname, num_awards, _ = point
            # If the point has the correct number of awards, and the surname is within the search range, add it to the results list
            if surname_range[0] <= surname[0] <= surname_range[1] and num_awards >= awards:
                    points.append(point)

        # Recursively search the left and right subtrees
        if surname_range[0] <= root.value:
            points.extend(self.search(root.left, awards, surname_range))
        if surname_range[1] >= root.value:
            points.extend(self.search(root.right, awards, surname_range))

        return points


    def print_tree(self, root, level=0):
        if root is not None:
            self.print_tree(root.left, level + 1)
            print(' ' * 4 * level + '->', root.value, root.points)
            self.print_tree(root.right, level + 1)


# Create a list of documents
documents = [
    ('Brown', 1, [1, 1, 0, 0]),
    ('Johnson', 3, [1, 0, 1, 0]),
    ('Jones', 3, [0, 1, 1, 0]),
    ('Smith', 2, [1, 0, 0, 1]),
    ('Williams', 2, [0, 1, 0, 1])
]

# Create a range tree from the documents
tree = RangeTree(documents)

# Print the tree
tree.print_tree(tree.root)

# Search the tree
results = tree.search(tree.root, 2, ('A', 'J'))
print(results)
