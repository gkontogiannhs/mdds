from KDTree.kdtree import KDTree
from LSH.lsh import LSH, kshingle, one_hot_encoding, jaccard, cosine_similarity
from QuadTree.quadtree import QuadTree
from RangeTree.rangetree import RangeTree2D
from RTree.rtree import RTree, Point

from numpy import stack
from pandas import read_csv


if __name__ == "__main__":

    ####################### PREPROCCESS AND DATA FORMATION ###########################################
    letters = 'abcdefghijklmnopqrstuvwxyz'
    let_to_int = {let: i for i, let in enumerate(letters)}
    
    # load datasets
    dataset = read_csv('List_of_computer_scientists.csv')
    docs = dataset['Education'].to_list()

    k = 2 # shingle size step

    # create vocabulary with shingles        
    vocabulary = set().union(*[kshingle(sent, k) for sent in docs])

    # one hot representation of each document
    # one_hot_matrix = stack([one_hot_encoding(vocabulary, sent) for sent in docs]).T

    points = []
    one_hot_matrix = []
    for fullname, awards, education in dataset.to_numpy():
        # surname = let_to_int[fullname.split()[-1][0].lower()]
        surname = fullname.split()[-1].upper()
        one_hot = one_hot_encoding(vocabulary, education)

        points += [Point(surname, awards, one_hot)]
    

    print(f"Total points: {len(points)}")
    ############################## QUERING #############################################

    range_tree = RangeTree2D(points)
    # x_range = (let_to_int['a'], let_to_int['z'])
    range_tree_retrieved = range_tree.range_search(x_range=('A', 'G'), y_range=(0, 5))
    print(f"Range Tree Retrieved: {len(range_tree_retrieved)}")
    
    kdtree = KDTree(points, k=2)
    kdtree_tree_retrieved = kdtree.range_search(query=(('A', 'G'), (0, 5)))
    print(f"KDTree Retrieved: {len(kdtree_tree_retrieved)}")

    # build quad tree with max 4 points per tile
    qtree = QuadTree(points=points, n=4)

    # define range of query
    point1, point2 = Point('A', 0), Point('G', 5)
    # convert to rectangle tile
    search_region = qtree.bounds_to_rect(point1, point2)

    # make query
    quad_tree_retrieved = qtree.range_search(search_region)
    print(f"KDTree Retrieved: {len(quad_tree_retrieved)}")

    """
    one_hot_matrix = stack([point.payload for point in retrieved]).T
    print(one_hot_matrix.shape)
    
    # create LSH model providing the bands magnitute 
    # in fit hashes each column for each band of the sign matrix M to a hash table with k buckets
    lsh = LSH(nfuncs=50, bands=5).fit(data=one_hot_matrix, buckets=1000)
 
    # get candidates with similarity bigger than 60%
    actual_candidates = lsh.candidates(cosine_similarity, similarity=.6)
    
    for cand_pair, sim in actual_candidates.items():
        print(f"Candidate pair {cand_pair}, similarity: {sim}")
        print(retrieved[cand_pair[0]])
        print()
        print(retrieved[cand_pair[1]])
        print()

    print(len(actual_candidates))
    """