# Multi-Dimensional Data Structures Package
### Requirements
This implementation requires Python 3.x and numpy version 1.22.4, which can be installed using **`pip install numpy==1.22.4`**.

# Trees
## 2D Range Tree
A 2D range tree is a data structure that can be used for efficient range searching in two-dimensional space.The tree is constructed using a modified form of the k-d tree algorithm, where each node in the tree represents a split in the data along one of the two dimensions. Additionally, each node also contains a 1D range tree of the data points that fall within its region, to allow for efficient searches along the other dimension. The RangeTree1D class is implemented as a binary search tree where the nodes represent points and each node has a left and a right child representing the points that are less than or greater than the point at the node, respectively. 

### Usage
To use the 2D range tree, you can create an instance of the RangeTree2D class and pass in a list of points in 2D space:
```
from mdds.trees import RangeTree2D

points = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10)]
# You can also create your own type of point as long as it's attributes can be indexed: x, y, payload = point[0], point[1], point[2]
tree = RangeTree2D(points)
```
You can then use the range_search method to query the tree and find all points that lie within a specified range:
```
x_range, y_range = (2, 6), (3, 8)
results = tree.range_search(x_range, y_range)
print(result)  # [(3, 4), (5, 6)]
```

## KD-Tree
This is an implementation of a KD-Tree in Python. KD-Trees are a type of space partitioning data structure that can be used to efficiently store and
search for points in K-dimensional space. The KD-Tree is implemented using a recursive divide-and-conquer approach. The data structure consists of a set of nodes, each of which represents a region of K-dimensional space. The space is partitioned recursively by splitting along the median value of the data along one of the K dimensions. The result is a balanced binary search tree, where the nodes are ordered based on the values along one of the dimensions.

A range search is performed by traversing the tree and checking if the current node's value falls within the query range. 
If it does, the node is added to the list of matches. If the query range intersects the region represented by the current node,
the search continues in both the left and right subtrees. If the value at the current node is outside the query range,
the search continues in only one of the subtrees, depending on which side of the range the value falls.


### Usage
To use the KD-Tree, you'll need to create an instance of the KDTree class, passing in a list of points and the number of dimensions. For example:
```
from mdds.trees import KDTree

points = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10)]
# You can also create your own type of point as long as it's attributes can be indexed: x, y, payload = point[0], point[1], point[2]
kdtree = KDTree(points, k=len(points[0]))
```
Once you've created the KD-Tree, you can perform a range search by calling the range_search method, passing in a query range for each dimension.
The method will return a list of all points in the tree that fall within the query range. For example:
```
query = [(0, 3), (0, 4)]
result = kdtree.range_search(query)
print(result) # [[1, 2], [3, 4]]
```

## QuadTree  
QuadTrees are a tree data structure used for efficient 2D spatial partitioning. They divide a 2D space into 4 equal quadrants, and recursively partition each quadrant until all elements fit into a single node. This makes it possible to quickly find all elements in a given region, or determine if an element intersects with another element.


### Usage
To use the QuadTree, simply create a list of points (or Point objects) representing the points you wish to store in the tree. Then, define the ranges on each axis for the tree using the x_range and y_range variables.
```
from mdds.trees import QuadTree

# define ranges on each axis
x_range = (2, 7)
y_range = (0, 5)

# create a list of Point objects
points = [Point(2, 3), Point(5, 4), Point(6, 1), Point(3, 2), Point(4, 5), Point(5, 3)]

# build quad tree with max 4 points per tile
qtree = QuadTree(points=points, n=4)
```

You can then perform range searches and exact searches on the QuadTree. To perform a range search, define the range of the search by passing two Point objects representing the corners of the search region to the bounds_to_rect function, and then pass the resulting Rectangle object to the range_search method.
```
# define range of query by passing two point objects
# and convert to rectangle tile
search_region = QuadTree.bounds_to_rect(Point(x_range[0], y_range[0]), Point(x_range[1], y_range[1]))

# make query
results = qtree.range_search(search_region)
print(f"Range Search:")
print(results)
```

To perform an exact search, pass a Point object representing the point you wish to search for to the search method.
```
# exact seach query: true if found else false
idx = randint(0, len(points)-1)
assert True == qtree.search(points[idx])
```

You can also perform radius searches, which return all points within a given radius of a specified point. To perform a radius search, pass a point representing the center point of the search and a radius value to the search_radius method.
```
# radius search, for a given point return neighbors in radius r
radius_points = qtree.search_radius(points[idx], 3)
print("Radius Search:")
print(radius_points)
```



## R-Tree Implementation
This is an implementation of an R-Tree, a spatial index data structure used to efficiently search and query 2D data sets.
The R-Tree is a tree-based data structure that allows for fast searching and querying of data based on its location.
The R-Tree partitions the space it indexes into rectangles, which can be thought of as regions in the data set.
Points in the data set are stored in leaves of the tree, while non-leaf nodes represent the rectangles that encompass their children.

### Getting Started
The implementation consists of three classes:  
  **Point**: represents a point in 2D space with an x and y coordinate.  
  **Rectangle**: represents a rectangle in 2D space defined by its upper-left and lower-right corner coordinates.  
  **RTree**: is the main class for the R-Tree, which implements the core functionality of the R-Tree data structure.  

## Example Usage
Here is an example of how you can use the R-Tree implementation:
To use the R-Tree, simply create a list of points (or Point objects) representing the points you wish to store in the tree. Then, create an RTree object and insert the points into the tree using the insert method.
```
from mdds.trees import RTree, Rectangle
from mdds.geometry import Point

# create RTree object
rtree = RTree(min_entries=2, max_entries=4)

# create a list of Point objects
points = [Point(2, 3), Point(5, 4), Point(6, 1), Point(3, 2), Point(4, 5), Point(5, 3)]

# insert points
for point in points:
    rtree.insert(point)
```
Alternatively, you can build the R-Tree in one step by passing the list of Point objects to the build_tree method.
```
rtree.build_tree(points)
```

You can then perform range searches and exact searches on the R-Tree. To perform a range search, define the range of the search by passing two values for each axis representing the minimum and maximum values for that axis, and then pass a Rectangle object representing the search region to the range_search method.
```
# define ranges on each axis
x_range =(1, 7)
y_range = (0, 5)

# retrieve query data
results = rtree.range_search(Rectangle(x_range[0], y_range[0], x_range[1], y_range[1]))

print("Range query:", str(results))
```

To perform an exact search, pass a Point object representing the point you wish to search for to the exists method.
```
idx = randint(0, len(points)-1)

print("Searching for:", points[idx])
print("Exists:", str(rtree.exists(points[idx])))
```

You can also delete a node from the R-Tree using the delete method.
```
print("Deleting node: ", str(points[idx]))
rtree.delete(points[idx])
print("Exists:", str(rtree.exists(points[idx])))
```

### Customizing the R-Tree
You can customize the R-Tree by changing the min_entries and max_entries parameters when creating the R-Tree.
min_entries represents the minimum number of entries a node should contain, while max_entries represents the maximum number of entries a node can contain
before it must be split. If a node is split, its entries are distributed among two new nodes such that the resulting nodes are as balanced as possible.

## Locality-sensitive hashing - LSH Implementation

### MinHash Class
The MinHash class is used to generate a signature matrix of an input one-hot encoded matrix. It uses a specified number of hash functions to create a matrix where each column represents the signature of one document. The signature is a compressed version of the one-hot encoded vector, where the position of the first non-zero value in each row of the signature matrix corresponds to the position of the first non-zero value in the corresponding row of the one-hot encoded matrix.  


### LSH Class
The LSH class is used to perform approximate nearest neighbor search on the signature matrix. The class takes as input the signature matrix, the number of hash functions used to create the signature matrix, the number of bands to partition the signature matrix into, and a radius for searching. It first partitions the signature matrix into bands, and then hashes each band to a hash table with a specified number of buckets. Candidate column pairs are found by looking for columns that hash to the same bucket in at least one band. Finally, the class has a method for computing the similarity between the candidate pairs using a specified similarity function, and returning pairs that are above a certain similarity threshold.


### Usage
To use the LSH implementation, you need to start by creating a vocabulary of the words that appear in your documents. Then, create a one-hot matrix that represents each document, where each row corresponds to a word in the vocabulary and each column corresponds to a document.
```
from mdds.helpers import one_hot_encoding
# one hot representation of each document
one_hot_matrix = stack([one_hot_encoding(vocabulary, sent) for sent in data]).T
```

Next, create an LSH object, providing the number of hash functions to use (nfuncs) and the number of bands to use (bands). Then, call the fit method to create the hash tables.
```
from mdds.neighbors import LSH

# create LSH model providing the bands magnitude and the number of hash functions/permutations
# in fit hashes each column for each band of the sign matrix M to a hash table with k buckets
lsh = LSH(nfuncs=50, bands=5).fit(data=one_hot_matrix, num_buckets=1000)
```

To retrieve the similar documents, use the neighbors method. Provide a similarity threshold value (similar) and a distance function (dist_func) that computes the similarity between two documents.
```
# get documents that are at least 65% similar or greater
actual_neighbors = lsh.neighbors(similar=0.65, dist_func=cosine_similarity)
# actual_neighbors = lsh.neighbors(similar=0.65, dist_func=jaccard)
print(actual_neighbors, end='\n\n')
```

You can also retrieve the nearest neighbors of a given query vector. Pass the query vector to the get_nearest_neighbors method, providing a radius value (radius) to control the maximum distance from the query vector to the retrieved neighbors.
```
import numpy as np
q_vec = np.random.choice(2, len(vocabulary))

# radius is defined as a percentage. 
# radius=1 means retrieve all the similar documents (all the neigbors) while a smaller radius 
# retrieves the neigbors that are % far from the query vector
nearest_neighbors = lsh.get_nearest_neighbors(query=q_vec, radius=.1)

print(nearest_neighbors)
```
