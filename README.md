## This is an implementation of a 1-Dimensional Range Tree and a 2-Dimensional Range Tree.

The 1-Dimensional Range Tree is a self-balancing binary search tree where each node stores a single point in the form of a tuple (x-coordinate, y-coordinate). The tree is constructed by sorting the points by their x-coordinates and then recursively building the left and right subtrees. The tree is queried by specifying a range for the x-coordinate and returning all points that fall within that range.

The 2-Dimensional Range Tree extends the 1-Dimensional Range Tree by adding a y-Tree to each node. The y-Tree is also a 1-Dimensional Range Tree, but it stores the points sorted by their y-coordinates. When querying the 2-Dimensional Range Tree, the x-coordinate range is used to determine which subtree to search and the y-coordinate range is used to filter the points in the y-Tree.
