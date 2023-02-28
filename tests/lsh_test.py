from os.path import dirname, abspath
from sys import path

# Get the path to the project root directory
root_dir = dirname(dirname(abspath(__file__)))
# Add the root directory to the system path
path.append(root_dir)

from mdds.helpers import *
from mdds.neighbors import LSH

from numpy import stack
from numpy.random import choice
from pandas import read_csv


if __name__ == "__main__":

    # load datasets
    dataset = read_csv('..\List_of_computer_scientists.csv')

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

    # get neigbors with similarity bigger than 65%
    print("All point pairs in space with similarity >= 65%")
    actual_neigbors = lsh.neighbors(similar=0.65, dist_func=cosine_similarity)
    print(actual_neigbors, end='\n\n')

    q_vec = choice(2, len(vocabulary))
    
    r=0.1 # radius to search
    nearest_neigbors = lsh.get_nearest_neighbors(query=q_vec, radius=r)
    print(f"All point pairs withing radius {r} of query")
    
    print(nearest_neigbors)

