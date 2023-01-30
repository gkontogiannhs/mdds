from mdds.helpers import *
from mdds.lsh import LSH

from numpy import stack
from pandas import read_csv


if __name__ == "__main__":

    # load datasets
    dataset = read_csv('List_of_computer_scientists.csv')

    # data to hash
    data = dataset['Education'].to_list()
    
    # shingle size step
    k = 2

    # create vocabulary with shingles        
    vocabulary = set().union(*[kshingle(sent, k) for sent in data])
    
    # one hot representation of each document
    one_hot_matrix = stack([one_hot_encoding(vocabulary, sent) for sent in data]).T

    # create LSH model providing the bands magnitute 
    # in fit hashes each column for each band of the sign matrix M to a hash table with k buckets
    lsh = LSH(nfuncs=50, bands=5).fit(data=one_hot_matrix, num_buckets=1000)

    # get neigbors with similarity bigger than 60%
    actual_neigbors = lsh.neigbors(similar=0.65, dist_func=cosine_similarity)
    print(actual_neigbors)

    import numpy as np
    q_vec = np.random.choice(2, len(vocabulary))
    
    nearest_neigbors = lsh.get_nearest_neigbors(query=q_vec, radius=.1)
    
    print(nearest_neigbors)

