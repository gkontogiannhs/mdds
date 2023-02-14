## 2D Range Tree
This repository contains a Python implementation of a 2D range tree, along with a simple example usage.  
A 2D range tree is a data structure that can be used for efficient range searching in two-dimensional space. It's implemented using two 1D range trees, one built on the x-coordinates and one built on the y-coordinates.

### Usage
To use the 2D range tree, you can create an instance of the RangeTree2D class and pass in a list of points in 2D space:
```
points = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10)]
tree = RangeTree2D(points)
```
You can then use the range_search method to query the tree and find all points that lie within a specified range:
```
result = tree.range_search((2, 6, 3, 8))
print(result)  # [(3, 4), (5, 6)]
```

### Implementation details
The RangeTree2D class has three main methods:

__init__(self, points): The constructor for the class. Takes a list of points in 2D space represented as tuples of x, y coordinates.

_build_tree(self, points, depth): A recursive method that builds the 2D range tree. Takes a list of points and the current depth of the tree.

range_search(self, query, depth): A method that queries the tree and finds all points that lie within a specified range. Takes a tuple representing the range in (xmin, xmax, ymin, ymax) format and the current depth of the tree.

The RangeTree2D class uses two 1D range trees, represented by the RangeTree1D class. The RangeTree1D class is implemented as a binary search tree where the nodes represent points and each node has a left and a right child representing the points that are less than or greater than the point at the node, respectively.


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



### QuadTree  
A Python implementation of a QuadTree data structure for efficient 2D spatial partitioning.

### Introduction
QuadTrees are a tree data structure used for efficient 2D spatial partitioning. They divide a 2D space into 4 equal quadrants, and recursively partition each quadrant until all elements fit into a single node. This makes it possible to quickly find all elements in a given region, or determine if an element intersects with another element.

### Features
Insertion of points into the QuadTree
Removal of points from the QuadTree
Retrieval of points within a bounding box
Retrieval of points within a radius
Fast and efficient search for elements in a given region
Installation
To install the QuadTree library, simply clone the repository and run pip install . from the root directory.

### Usage
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



## LSH Implementation
This repository contains an implementation of Locality Sensitive Hashing (LSH) in Python, using Numpy and other libraries. The implementation includes two main classes: MinHash and LSH.

### MinHash Class
The MinHash class is used to generate a signature matrix of an input one-hot encoded matrix. The following methods are available in the MinHash class:

__init__: This method is the constructor of the class and initializes the object with the input one-hot encoded matrix, the number of hash functions (nfuncs), and the signature matrix (sign_matrix) which is initially set to None.

_hash: This method creates a list of indices of the rows of the one-hot encoded matrix in a random order.

build_functions: This method builds nfuncs number of hash functions by calling the _hash() method.

_signature_matrix: This method creates the signature matrix of the input one-hot encoded matrix using the hash functions created by the build_functions() method. It assigns the signature matrix to the sign_matrix attribute of the class and returns the signature matrix.

### LSH Class
The LSH class is used to perform approximate nearest neighbor search on the signature matrix using Locality Sensitive Hashing (LSH). The following methods are available in the LSH class:

__init__: This method is the constructor of the class and initializes the object with the number of hash functions (nfuncs), the number of bands (bands) used to partition the signature matrix. The attribute hash_tables is initially set to None.

partition_into_bands: This method partitions the signature matrix (sm) into bands number of bands.

fit: This method is used to fit the LSH model to the input data. It creates an object of the MinHash class with the input data and nfuncs number of hash functions. It then creates the signature matrix using the _signature_matrix() method from the MinHash class. It then partitions the signature matrix into bands and uses the hash values of the columns of each band to create a list of hash tables with buckets number of buckets.

_get_candidates: This method finds candidate column pairs for the input matrix by looking for columns that have the same hash value in the same band of the signature matrix (items in same buckets). It returns a set of candidate column pairs.

neighbors: This method takes two arguments, the similarity threshold and the function to measure distance between points. It returns all the points that have similarity >= similar. This method finds similar columns in the input matrix based on the similarity function passed as an argument. By default, it uses the cosine similarity function. It uses the _find_candidates() method to find the candidate column pairs, then it filters false positives by their similarity and return the columns that have a similarity greater than the specified threshold.

get_nearest_neighbors: This method tries to return the points that are similar to a query. This is done by hashing the query and returning the hashed bucket plus the buckets within the specified radius.

### Usage
To use the implementation, you need to create an object of the LSH class and call its fit method to fit the model to the input data. You can then call the `get_nearest


