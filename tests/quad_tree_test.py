from mdds.trees import QuadTree
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
    for i, (surname, award, edu_vector) in enumerate(zip(int_surnames, awards, ohm_edu)):
        # create points list
        points += [Point(surname, award, edu_vector, i)]
    
    print(f"Total points: {len(points)}")


    # define ranges on each axis
    x_range = stit.scale(['A', 'G'])
    y_range = (0, 5)

    # build quad tree with max 4 points per tile
    qtree = QuadTree(points=points, n=4)

    # define range of query by passing two point objects
    # and convert to rectangle tile
    search_region = qtree.bounds_to_rect(Point(x_range[0], y_range[0]), Point(x_range[1], y_range[1]))

    # make query
    results = qtree.range_search(search_region)
    print(f"Range Search:")
    print(results)

    # exact seach query: true if found else false
    idx = randint(0, len(points)-1)
    assert True == qtree.search(points[idx])

    # radius search, for a given point return neigbors in radius r
    radius_points = qtree.search_radius(points[idx], 3)
    print("Radius Search:")
    print(radius_points)