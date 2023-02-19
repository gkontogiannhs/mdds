from mdds.trees import KDTree, RangeTree2D, QuadTree
from mdds.neigbors import LSH
from mdds.helpers import StringToIntTransformer, kshingle, one_hot_encoding, jaccard, cosine_similarity
from mdds.trees import RTree, Rectangle
from mdds.geometry.point import Point
from pandas import read_csv, DataFrame
from numpy import stack

from timeit import timeit
from time import time
from sys import getsizeof
from matplotlib import pyplot

pyplot.style.use('seaborn')


if __name__ == "__main__":

    ####################### PREPROCCESS AND DATA FORMATION ###########################################
    
    # load datasets
    dataset = read_csv('List_of_computer_scientists.csv')

    # surnames
    surnames = [fullname.split()[-1] for fullname in dataset['Name'].to_list()]
    
    # convert sting surnames to int
    stit = StringToIntTransformer().fit(surnames)
    int_surnames = stit.transform(surnames)
    
    # awards per scientist
    awards = dataset['Awards'].to_list()

    # education column
    docs = dataset['Education'].to_list()

    # create vocabulary with shingles        
    vocabulary = set().union(*[kshingle(edu, k=2) for edu in docs])

    # one hot representation of each document
    ohm_edu = stack([one_hot_encoding(vocabulary, edu) for edu in docs]).T
    
    points = []
    for i, (surname, award, edu_vector) in enumerate(zip(int_surnames, awards, ohm_edu)):
        # create points list
        points += [Point(surname, award, edu_vector, i)]
    
    print(f"Total points: {len(points)}")

    ds_build_time = []
    ds_range_time = []
    ds_space = []
    ann_time = []
    total_time = []
    # number of exp iterations
    n = 1
    ################## QUERING #############################################

    # define ranges on each axis
    x_range = stit.transform(['A', 'Z'])
    y_range = (0, 10)

    ######################## Range Tree ##################################

    # average time to build Range Trees
    ds_build_time += [timeit(lambda: RangeTree2D(points), number=n)]

    # Create and build tree
    range_tree = RangeTree2D(points)

    # space requirments
    ds_space += [getsizeof(range_tree)]

    # time query of range tree
    ds_range_time += [timeit(lambda: range_tree.range_search(x_range, y_range), number=n)]

    # make query
    range_tree_retrieved = range_tree.range_search(x_range, y_range)
    print(f"Range Tree Retrieved: {len(range_tree_retrieved)}")

    start = time()
    # applying LSH
    indices = [point.id for point in range_tree_retrieved]
    query_one_hot = ohm_edu[indices].T
    
    # create LSH model providing the bands magnitute 
    # in fit hashes each column for each band of the sign matrix M to a hash table with k buckets
    lsh = LSH(nfuncs=50, bands=5).fit(data=query_one_hot, num_buckets=100)
 
    # get candidates with similarity/radius bigger than 60%
    actual_candidates = lsh.neigbors(similar=0.7, dist_func=cosine_similarity)

    ann_time += [(time()-start)*n]

    # print(actual_candidates)
    print(actual_candidates)


    ######################## KD-Tree ##################################

    # average time to build KD Tree
    ds_build_time += [timeit(lambda: KDTree(points, k=2), number=n)]

    # build actuall tree
    kdtree = KDTree(points, k=2)

    # space requirments
    ds_space += [getsizeof(kdtree)]

    # time query of KD tree
    ds_range_time += [timeit(lambda: kdtree.range_search(query=(x_range, y_range)), number=n)]

    kdtree_tree_retrieved = kdtree.range_search(query=(x_range, y_range))
    print(f"KDTree Retrieved: {len(kdtree_tree_retrieved)}")

    start = time()
    # applying LSH
    indices = [point.id for point in kdtree_tree_retrieved]
    query_one_hot = ohm_edu[indices].T
    
    # create LSH model providing the bands magnitute 
    # in fit hashes each column for each band of the sign matrix M to a hash table with k buckets
    lsh = LSH(nfuncs=50, bands=5).fit(data=query_one_hot, num_buckets=100)
 
    # get candidates with similarity/radius bigger than 60%
    actual_candidates = lsh.neigbors(similar=0.7, dist_func=cosine_similarity)
    
    ann_time += [(time()-start)*n]

    # print(actual_candidates)
    print(actual_candidates)
    

    ######################## Quad Tree + LSH ##################################

    # average time to build Quad Tree
    ds_build_time += [timeit(lambda: QuadTree(points=points, n=4), number=n)]

    # build quad tree with max 4 points per tile
    qtree = QuadTree(points=points, n=4)

    # space requirments
    ds_space += [getsizeof(qtree)]

    # define range of query by passing two point objects
    # and convert to rectangle tile
    search_region = qtree.bounds_to_rect(Point(x_range[0], y_range[0]), Point(x_range[1], y_range[1]))

    # time query of Quad tree
    ds_range_time += [timeit(lambda: qtree.range_search(search_region), number=n)]

    # make query
    quad_tree_retrieved = qtree.range_search(search_region)
    print(f"QuadTree Retrieved: {len(quad_tree_retrieved)}")

    start = time()
    # applying LSH
    indices = [point.id for point in quad_tree_retrieved]
    query_one_hot = ohm_edu[indices].T
    
    # create LSH model providing the bands magnitute 
    # in fit hashes each column for each band of the sign matrix M to a hash table with k buckets
    lsh = LSH(nfuncs=50, bands=5).fit(data=query_one_hot, num_buckets=100)
 
    # get candidates with similarity/radius bigger than 60%
    actual_candidates = lsh.neigbors(similar=0.7, dist_func=cosine_similarity)
    
    ann_time += [(time()-start)*n]

    # print(actual_candidates)
    print(actual_candidates)


    ######################## R-Tree + LSH ##################################

    # average time to build R Tree
    ds_build_time += [timeit(lambda: RTree().insert(points), number=n)]

    # create RTree object
    rtree = RTree()

    # insert points
    rtree.insert(points)

    # space requirments
    ds_space += [getsizeof(rtree)]

    # time query of R tree
    ds_range_time += [timeit(lambda: rtree.range_search(Rectangle(x_range[0], y_range[0], x_range[1], y_range[1])), number=n)]

    # retrieve query data
    rtree_retrieved = rtree.range_search(Rectangle(x_range[0], y_range[0], x_range[1], y_range[1]))
    print(f"RTree Retrieved: {len(rtree_retrieved)}")

    # for scientist in rtree_retrieved:
    #    print(surnames[scientist.id], awards[scientist.id])

    start = time()
    indices = [point.id for point in rtree_retrieved]
    query_one_hot = ohm_edu[indices].T
    
    # create LSH model providing the bands magnitute 
    # in fit hashes each column for each band of the sign matrix M to a hash table with k buckets
    lsh = LSH(nfuncs=50, bands=5).fit(data=query_one_hot, num_buckets=100)
 
    # get candidates with similarity/radius bigger than 60%
    actual_candidates = lsh.neigbors(similar=.7, dist_func=cosine_similarity)
    ann_time += [(time()-start)*n]

    # print(actual_candidates)
    print(actual_candidates)

    # total_time = [ds_range_time[i]+ann_time[i] for i in range(len(ds_range_time))]
    print("RangeTree - KD-Tree - QuadTree - R-Tree")
    print("Build time:")
    print(ds_build_time)
    print("Range Search time:")
    print(ds_range_time)
    print("ANN time:")
    print(ann_time)
    # print("Range Search + ANN time:")
    # print(total_time)
    print("Space:")
    print(ds_space)
    
    df = DataFrame({'Data Structure':['RangeTree', 'KDTree', 'QuadTree', 'R-Tree'], 
                    'Construction Time': ds_build_time,
                    'Range Search Time': ds_range_time,
                    'Aproximate NN Time': ann_time})

    print(df)
    print(df.plot(x='Data Structure', marker='.', ylabel='Time * 1000 (sec)', logy=True))
    pyplot.tight_layout() # helps with padding
    pyplot.grid(True) # enables the grid plot
    pyplot.show()
    