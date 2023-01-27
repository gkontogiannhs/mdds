from kdtree import KDTree
# from Point.point import Point
from random import randint
from pandas import read_csv
from numpy import stack
from LSH.helpers import kshingle, one_hot_encoding, jaccard, cosine_similarity


if __name__ == "__main__":

    # load datasets
    dataset = read_csv('..\List_of_computer_scientists.csv')

    # Education column
    edu = dataset['Education'].to_list()
    print(edu)
    # scientist name column
    fullnames = dataset['Names'].to_list()
    surnames = [sname.split()[-1] for sname in fullnames]
    print(surnames)
    # scientists awards
    awards = dataset['Awards'].to_list()
    print(awards)
    # create vocabulary with shingles        
    vocabulary = set().union(*[kshingle(sent, 2) for sent in edu])
    
    # one hot representation of each document
    one_hot_matrix = stack([one_hot_encoding(vocabulary, sent) for sent in edu]).T

    # create points
    points = []
    query_range = ((20, 60), (30, 70))

    # Create and build KD-Tree
    kdtree = KDTree(points, k=2)

    results = kdtree.range_search(query_range)
    results.sort(key=lambda p: p[0])

    print(results)