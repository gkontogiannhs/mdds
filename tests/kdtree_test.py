from mdds.trees import KDTree
from mdds.geometry import Point
from mdds.helpers import *
from pandas import read_csv
from numpy import stack
from random import randint


if __name__ == '__main__':

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


    # define ranges on each axis
    x_range = stit.scale(['A', 'G'])
    y_range = (0, 5)

    # Create and build KD-Tree
    kdtree = KDTree(points, k=2)

    results = kdtree.range_search(query=(x_range, y_range))
    print(f"Range Search:")
    print(results)