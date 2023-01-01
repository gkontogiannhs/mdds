from RangeTree2D import RangeTree2D


if __name__ == '__main__':
    points = [('george', 2, [0, 1, 1, 0]), ('smith', 4, [0, 1, 1, 0]), ('sofi', 5, [0, 1, 1, 0]), ('jannete', 3, [0, 1, 1, 0])]

    # create a 2D range tree with x as the main axis
    tree = RangeTree2D(points, axis=0)

    # query the tree for all points with x in the range [4, 12] and y in the range [5, 8]
    result = tree.query(('a', 'z'), (0, 3))

    print(result)