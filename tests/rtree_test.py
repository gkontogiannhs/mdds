from os.path import dirname, abspath
from sys import path

# Get the path to the project root directory
root_dir = dirname(dirname(abspath(__file__)))
# Add the root directory to the system path
path.append(root_dir)

from mdds.trees import RTree, Rectangle
from mdds.geometry import Point
from mdds.helpers import *

from pandas import read_csv
from numpy import stack
from random import randint


if __name__ == '__main__':

    ####################### PREPROCCESS AND DATA FORMATION ###########################################
    
    # load datasets
    dataset = read_csv('..\List_of_computer_scientists.csv')

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


    ######################## R-Tree ##################################

    # create RTree object
    rtree = RTree(min_entries=2, max_entries=4)

    # insert points
    for point in points:
        rtree.insert(point)

    # alternative way to build R-Tree
    # rtree.build_tree(points)

    # define ranges on each axis
    x_range = stit.transform(['A', 'G'])
    y_range = (0, 5)

    # retrieve query data
    results = rtree.range_search(Rectangle(x_range[0], y_range[0], x_range[1], y_range[1]))

    print("Range query:", str(results))

    idx = randint(0, len(points)-1)

    print("Searching for:", points[idx])
    print("Exists:", str(rtree.exists(points[idx])))

    print("Deleting node: ", str(points[idx]))
    rtree.delete(points[idx])

    print("Exists:", str(rtree.exists(points[idx])))