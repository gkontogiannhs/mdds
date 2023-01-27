from KDTree.kdtree import KDTree
from LSH.lsh import LSH
from LSH.helpers import kshingle, one_hot_encoding, jaccard, cosine_similarity
from QuadTree.quadtree import QuadTree
from RangeTree.rangetree import RangeTree2D
from RTree.rtree import RTree, Rectangle
from Point.point import Point
from pandas import read_csv


def string_to_int(string):
    numbers = {letter: n for n, letter in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ', start=1)}
    dist = 0
    for char in string:
        try:
            dist += numbers[char]
        except KeyError:
            dist += 1
    return dist


class StringToIntTransformer:
    def __init__(self):
        self.char_to_int_mapping = {}
        self.string_max_length = 0
    
    def fit(self, X, y=None):
        for string in X:
            self.string_max_length = max(self.string_max_length, len(string))
            for char in string:
                if char.isalpha():
                    ascii_val = ord(char.upper()) - ord('A') + 1
                    self.char_to_int_mapping[char] = ascii_val
    
        return self
    
    def transform(self, X):
        # slope = (output_end - output_start) / (input_end - input_start)
        # output = output_start + slope * (input - input_start)
        X_transformed = []
        for string in X:
            string_sum = 0
            for char in string:
                if char.isalpha():
                    string_sum += self.char_to_int_mapping.get(char.upper(), 0)
            X_transformed.append(string_sum)
        return X_transformed
        

if __name__ == "__main__":

    ####################### PREPROCCESS AND DATA FORMATION ###########################################
    
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

        # get surname from the name information
        surname = fullname.split()[-1].upper()

        # vectorize education text to one hot encoding
        one_hot = one_hot_encoding(vocabulary, education)
        
        # create points list
        points += [Point(0, awards, one_hot, surname)]
    
    h = [fullname.split()[-1] for fullname in dataset['Name'].to_list()]
    
    stit = StringToIntTransformer().fit(h)
    print(stit.transform(h))

    print(stit.transform(['A', 'Z']))
    print(f"Total points: {len(points)}")
    ############################## QUERING #############################################

    range_tree = RangeTree2D(points)
    x_range = (string_to_int('A'), string_to_int('L'))
    
    range_tree_retrieved = range_tree.range_search(x_range=x_range, y_range=(0, 5))
    print(f"Range Tree Retrieved: {len(range_tree_retrieved)}")
    
    kdtree = KDTree(points, k=2)
    kdtree_tree_retrieved = kdtree.range_search(query=(x_range, (0, 5)))
    print(f"KDTree Retrieved: {len(kdtree_tree_retrieved)}")


    # build quad tree with max 4 points per tile
    qtree = QuadTree(points=points, n=4)

    # define range of query
    point1, point2 = Point(x_range[0], 0), Point(x_range[1], 5)

    # convert to rectangle tile
    search_region = qtree.bounds_to_rect(point1, point2)

    # make query
    quad_tree_retrieved = qtree.range_search(search_region)
    print(f"QuadTree Retrieved: {len(quad_tree_retrieved)}")

    # create RTree object
    rtree = RTree()

    # insert points
    for point in points: rtree.insert(point)
    rtree_retrieved = rtree.range_search(Rectangle(x_range[0], 0, x_range[1], 5))
    print(f"RTree Retrieved: {len(rtree_retrieved)}")
    
    # rtree_retrieved.sort(key=lambda point: point.x)
    print(rtree_retrieved)
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