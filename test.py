from KDTree.kdtree import KDTree
from LSH.lsh import LSH, kshingle, one_hot_encoding, jaccard, cosine_similarity
from QuadTree.quadtree import QuadTree
from RangeTree.rangetree import RangeTree2D
from RTree.rtree import RTree

from numpy import stack
from pandas import read_csv

if __name__ == "__main__":

    # load datasets
    dataset = read_csv('../List_of_computer_scientists.csv')

    data = dataset['Education'].to_list()

    k = 10 # shingle size step

    # create vocabulary with shingles        
    vocabulary = set().union(*[kshingle(sent, k) for sent in data])

    # one hot representation of each document
    one_hot_matrix = stack([one_hot_encoding(vocabulary, sent) for sent in data]).T
    
    # create LSH model providing the bands magnitute 
    # in fit hashes each column for each band of the sign matrix M to a hash table with k buckets
    lsh = LSH(nfuncs=100, bands=5).fit(data=one_hot_matrix, buckets=1000)
    
    # get candidates with similarity bigger than 60%
    actual_candidates = lsh.candidates(jaccard, similarity=.6)
    
    
    for cand_pair, sim in actual_candidates.items():
        print(f"Candidate pair {cand_pair}, similarity: {sim}")
        print(data[cand_pair[0]])
        print()
        print(data[cand_pair[1]])
        print()

    print(len(actual_candidates))
