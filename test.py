from mdds.trees.kdtree import KDTree
from mdds.helpers import StringToIntTransformer, kshingle, one_hot_encoding, jaccard, cosine_similarity
from mdds.lsh import LSH
from mdds.trees.quadtree import QuadTree
from mdds.trees.rangetree import RangeTree2D
from mdds.trees.rtree import RTree, Rectangle
from mdds.point import Point
from pandas import read_csv
from numpy import stack
from time import time


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
    for i, (surname, awards, edu_vector) in enumerate(zip(int_surnames, awards, ohm_edu)):
        # create points list
        points += [Point(surname, awards, edu_vector, i)]
    
    print(f"Total points: {len(points)}")

    
    ds_build_time = []
    ds_query_time = []
    ds_space = []
    total_time = []
    # number of exp iterations
    n = 10
    from timeit import timeit
    from time import time
    from sys import getsizeof
    from matplotlib import pyplot
    ################################################# QUERING #############################################

    # define ranges on each axis
    x_range = stit.scale(['A', 'Z'])
    y_range = (0, 100)

    ######################## Range Tree ##################################

    # average time to build Range Trees
    ds_build_time += [timeit(lambda: RangeTree2D(points), number=n)]

    # Create and build tree
    range_tree = RangeTree2D(points)

    # space requirments
    ds_space += [getsizeof(range_tree)]

    # time query of range tree
    ds_query_time += [timeit(lambda: range_tree.range_search(x_range, y_range), number=n)]

    # make query
    range_tree_retrieved = range_tree.range_search(x_range, y_range)
    print(f"Range Tree Retrieved: {len(range_tree_retrieved)}")
    
    start = time()
    # applying LSH
    indices = [point.id for point in range_tree_retrieved]
    query_one_hot = ohm_edu[indices].T
    
    # create LSH model providing the bands magnitute 
    # in fit hashes each column for each band of the sign matrix M to a hash table with k buckets
    lsh = LSH(nfuncs=50, bands=5, radius=0.6).fit(data=query_one_hot, buckets=100)
 
    # get candidates with similarity/radius bigger than 60%
    actual_candidates = lsh.candidates(sim_function=cosine_similarity)

    total_time += [(time()-start)*n]

    # print(actual_candidates)
    print(len(actual_candidates))


    ######################## KD-Tree ##################################

    # average time to build KD Tree
    ds_build_time += [timeit(lambda: KDTree(points, k=2), number=n)]

    # build actuall tree
    kdtree = KDTree(points, k=2)

    # space requirments
    ds_space += [getsizeof(kdtree)]

    # time query of KD tree
    ds_query_time += [timeit(lambda: kdtree.range_search(query=(x_range, y_range)), number=n)]

    kdtree_tree_retrieved = kdtree.range_search(query=(x_range, y_range))
    print(f"KDTree Retrieved: {len(kdtree_tree_retrieved)}")

    start = time()
    # applying LSH
    indices = [point.id for point in kdtree_tree_retrieved]
    query_one_hot = ohm_edu[indices].T
    
    # create LSH model providing the bands magnitute 
    # in fit hashes each column for each band of the sign matrix M to a hash table with k buckets
    lsh = LSH(nfuncs=50, bands=5, radius=0.6).fit(data=query_one_hot, buckets=100)
 
    # get candidates with similarity/radius bigger than 60%
    actual_candidates = lsh.candidates(sim_function=cosine_similarity)
    
    total_time += [(time()-start)*n]

    # print(actual_candidates)
    print(len(actual_candidates))


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
    ds_query_time += [timeit(lambda: qtree.range_search(search_region), number=n)]

    # make query
    quad_tree_retrieved = qtree.range_search(search_region)
    print(f"QuadTree Retrieved: {len(quad_tree_retrieved)}")

    start = time()
    # applying LSH
    indices = [point.id for point in quad_tree_retrieved]
    query_one_hot = ohm_edu[indices].T
    
    # create LSH model providing the bands magnitute 
    # in fit hashes each column for each band of the sign matrix M to a hash table with k buckets
    lsh = LSH(nfuncs=50, bands=5, radius=0.6).fit(data=query_one_hot, buckets=100)
 
    # get candidates with similarity/radius bigger than 60%
    actual_candidates = lsh.candidates(sim_function=cosine_similarity)
    
    total_time += [(time()-start)*n]

    # print(actual_candidates)
    print(len(actual_candidates))


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
    ds_query_time += [timeit(lambda: rtree.range_search(Rectangle(x_range[0], y_range[0], x_range[1], y_range[1])), number=n)]

    # retrieve query data
    rtree_retrieved = rtree.range_search(Rectangle(x_range[0], y_range[0], x_range[1], y_range[1]))
    print(f"RTree Retrieved: {len(rtree_retrieved)}")
    
    start = time()
    indices = [point.id for point in rtree_retrieved]
    query_one_hot = ohm_edu[indices].T
    
    # create LSH model providing the bands magnitute 
    # in fit hashes each column for each band of the sign matrix M to a hash table with k buckets
    lsh = LSH(nfuncs=50, bands=5, radius=0.6).fit(data=query_one_hot, buckets=100)
 
    # get candidates with similarity/radius bigger than 60%
    actual_candidates = lsh.candidates(sim_function=cosine_similarity)

    total_time += [(time()-start)*n]

    # print(actual_candidates)
    print(len(actual_candidates))

    print("RangeTree - KD-Tree - QuadTree - R-Tree")
    print("Build time:")
    print(ds_build_time)
    print("Query time:")
    print(ds_query_time)
    print("Space:")
    print(ds_space)
    print("Build + Query + LSH time:")
    print(total_time)

    from pandas import DataFrame
    df = DataFrame({'Data Structure':['RangeTree', 'KDTree', 'QuadTree', 'R-Tree'], 
                    'Construction Time': ds_build_time,
                    'Query Time': ds_query_time,
                    'Total Time': total_time})

    print(df)
    print(df.plot(x='Data Structure', marker='.', ylabel='Time * 1000 (sec)', logy=True))
    pyplot.show()
    