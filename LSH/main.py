# import the LSH class and the LSHFunction class
from lsh import LSH, LSHFunction
import numpy as np


if __name__ == "__main__":
    # create a dataset of 10 random vectors
    np.random.seed(42)
    dataset = [np.random.randn(100) for _ in range(10)]

    # create an LSH function that uses 10 hash functions
    lsh_function = LSHFunction(num_hash_functions=10, dimensions=100)

    # create an LSH instance using the LSH function and the dataset
    lsh = LSH(dataset, [lsh_function])

    # generate a random query vector
    query_vector = np.random.randn(100)

    # perform a range query with a range of 0.5
    result = lsh.range_query(query_vector, range=0.5)

    print(result)  # prints a list of vectors that are similar to the query vector
