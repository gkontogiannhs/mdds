## Multi-Dimensional-DS

## KD-Tree
This is an implementation of a KD-Tree in Python. KD-Trees are a type of space partitioning data structure that can be used to efficiently store and
search for points in K-dimensional space.

### Requirements
This implementation requires Python 3.x.

### Usage
To use the KD-Tree, you'll need to create an instance of the KDTree class, passing in a list of points and the number of dimensions. For example:
```
points = [[1, 2], [3, 4], [5, 6], [7, 8]]
kdtree = KDTree(points, 2)
```
Once you've created the KD-Tree, you can perform a range search by calling the range_search method, passing in a query range for each dimension.
The method will return a list of all points in the tree that fall within the query range. For example:
```
query = [[0, 3], [0, 3]]
result = kdtree.range_search(query)
print(result) # [[1, 2], [3, 4]]
```

### Technical Summary
The KD-Tree is implemented using a recursive divide-and-conquer approach. The data structure consists of a set of nodes, each of which represents a region
of K-dimensional space. The space is partitioned recursively by splitting along the median value of the data along one of the K dimensions. 
The result is a balanced binary search tree, where the nodes are ordered based on the values along one of the dimensions.

A range search is performed by traversing the tree and checking if the current node's value falls within the query range. 
If it does, the node is added to the list of matches. If the query range intersects the region represented by the current node,
the search continues in both the left and right subtrees. If the value at the current node is outside the query range,
the search continues in only one of the subtrees, depending on which side of the range the value falls.


## R-Tree Implementation
This is an implementation of an R-Tree, a spatial index data structure used to efficiently search and query 2D data sets.
The R-Tree is a tree-based data structure that allows for fast searching and querying of data based on its location.
The R-Tree partitions the space it indexes into rectangles, which can be thought of as regions in the data set.
Points in the data set are stored in leaves of the tree, while non-leaf nodes represent the rectangles that encompass their children.

### Getting Started
The implementation consists of three classes: Point, Rectangle, and RTree.

#### Point represents a point in 2D space with an x and y coordinate.
#### Rectangle represents a rectangle in 2D space defined by its upper-left and lower-right corner coordinates.
#### RTree is the main class for the R-Tree, which implements the core functionality of the R-Tree data structure.

## Example Usage
Here is an example of how you can use the R-Tree implementation:
```
from rtree import Point, Rectangle, RTree

# Create a point
point = Point(1, 2)

# Create a rectangle
rectangle = Rectangle(0, 0, 4, 4)

# Create an R-Tree
rtree = RTree()

# Insert a point into the R-Tree
rtree.insert(point)

# Perform a range search on the R-Tree using a rectangle
results = rtree.range_search(rectangle)

# Check if a point exists in the R-Tree
exists = rtree.exists(point)
```

### Customizing the R-Tree
You can customize the R-Tree by changing the min_entries and max_entries parameters when creating the R-Tree.
min_entries represents the minimum number of entries a node should contain, while max_entries represents the maximum number of entries a node can contain
before it must be split. If a node is split, its entries are distributed among two new nodes such that the resulting nodes are as balanced as possible.

### Contributions
This implementation is intended as a simple starting point for those who want to learn about R-Trees. Contributions to improve the implementation or add new features are welcome.



QuadTree
A Python implementation of a QuadTree data structure for efficient 2D spatial partitioning.

Introduction
QuadTrees are a tree data structure used for efficient 2D spatial partitioning. They divide a 2D space into 4 equal quadrants, and recursively partition each quadrant until all elements fit into a single node. This makes it possible to quickly find all elements in a given region, or determine if an element intersects with another element.

Features
Insertion of points into the QuadTree
Removal of points from the QuadTree
Retrieval of points within a bounding box
Retrieval of points within a radius
Fast and efficient search for elements in a given region
Installation
To install the QuadTree library, simply clone the repository and run pip install . from the root directory.

Usage
Here is an example of how to use the QuadTree to insert points, retrieve points within a bounding box, and visualize the structure of the tree:

```
from quadtree import QuadTree
import matplotlib.pyplot as plt

# Initialize the QuadTree with a bounding box
bounds = (0, 0, 100, 100)
qt = QuadTree(bounds, max_depth=5, max_elements=3)

# Insert some points into the tree
points = [(20, 20), (50, 50), (80, 80), (30, 30), (60, 60), (90, 90)]
for point in points:
    qt.insert(point)

# Retrieve all points within a bounding box
search_bounds = (40, 40, 70, 70)
result = qt.query(search_bounds)
print(result)

# Visualize the structure of the tree
fig, ax = plt.subplots()
qt.plot(ax)
plt.show()
```

Contributing
If you would like to contribute to the QuadTree library, please feel free to submit a pull request.

