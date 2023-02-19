from mdds.trees.kdtree import KDTree
from mdds.helpers import StringToIntTransformer, kshingle, one_hot_encoding, jaccard, cosine_similarity
from mdds.neigbors import LSH
from mdds.trees import QuadTree
from mdds.trees import RangeTree2D
from mdds.trees import RTree, Rectangle
from mdds.geometry import Point


from timeit import timeit
from time import time
from sys import getsizeof
from matplotlib import pyplot
from pandas import DataFrame
from random import randint

pyplot.style.use('seaborn')


if __name__ == "__main__":

    ####################### PREPROCCESS AND DATA FORMATION ###########################################

    sizes = [100, 1000, 10_000, 100_000, 1_000_000]
    r = 10_000
    range_tree_s = []
    kd_tree_s = []
    quad_tree_s = []
    r_tree_s = []
    for size in sizes:
        points = [Point(randint(-r, r), randint(-r,r)) for _ in range(size)]

        # number of exp iterations
        n = 1000
        ################## QUERING #############################################

        # define ranges on each axis
        x_range = (-r, r)
        y_range = (-r/2, r/2)

        ######################## Range Tree ##################################

        # Create and build tree
        range_tree = RangeTree2D(points)

        # time query of range tree
        range_tree_s += [round(timeit(lambda: range_tree.range_search(x_range, y_range), number=n), 3)]


        ######################## KD-Tree ##################################

        # build actuall tree
        kdtree = KDTree(points, k=2)

        # time query of KD tree
        kd_tree_s += [round(timeit(lambda: kdtree.range_search(query=(x_range, y_range)), number=n),3)]


        ######################## Quad Tree + LSH ##################################

        # build quad tree with max 4 points per tile
        qtree = QuadTree(points=points, n=4)


        # define range of query by passing two point objects
        # and convert to rectangle tile
        search_region = qtree.bounds_to_rect(Point(x_range[0], y_range[0]), Point(x_range[1], y_range[1]))

        # time query of Quad tree
        quad_tree_s += [round(timeit(lambda: qtree.range_search(search_region), number=n), 3)]


        ######################## R-Tree + LSH #################################

        # create RTree object
        rtree = RTree()
        # insert points
        rtree.insert(points)

        # time query of R tree
        r_tree_s += [round(timeit(lambda: rtree.range_search(Rectangle(x_range[0], y_range[0], x_range[1], y_range[1])), number=n), 3)]
        
    
    
    print("Range Search time:")
    print(range_tree_s)
    print(kd_tree_s)
    print(quad_tree_s)
    print(r_tree_s)

    fig, ax = pyplot.subplots(nrows=1, ncols=1)

    ax.plot(sizes, range_tree_s, label='Range Tree', marker='.', linewidth=1.5, color='#008FD5')
    ax.plot(sizes, kd_tree_s, label='KD-Tree', marker='.', linewidth=1.5, color='#E5AE38')
    ax.plot(sizes, quad_tree_s, label='Quad Tree', marker='.', linewidth=1.5, color='#5EAE83')
    ax.plot(sizes, r_tree_s, label='R-Tree', marker='.', linewidth=1.5, color='#993333')

    # set logaritmic scale
    ax.set_yscale('log')

    # labels
    ax.set_xlabel('size of n')
    ax.set_ylabel('Time * 100 (sec)')

    # title
    ax.set_title('Range Search Time per DS')
    ax.legend()

    pyplot.tight_layout() # helps with padding
    pyplot.grid(True) # enables the grid plot
    pyplot.show()
        