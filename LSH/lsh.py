import numpy as np
from random import shuffle # in place


def jaccard(v, u):
    return round(len(set(v) & set(u)) / len(set(v) | set(u)), 3)


def shingle(text, k):

    shingle_set = []

    for i in range(len(text) - k + 1):
        shingle_set += [text[i:i+k]]
    
    return set(shingle_set)


def one_hot_encoding(vocab, sent):

    one_hot = np.zeros(len(vocab), dtype=int)

    for i, sh in enumerate(vocab):
        if sh in sent: one_hot[i] = 1

    return one_hot

    
class MinHash:
    def __init__(self, one_hot_matrix, nfuncs):
        self.one_hot_matrix = one_hot_matrix
        self.shape = self.one_hot_matrix.shape
        self.nfuncs = nfuncs

        self.functions = self.build_functions(self.nfuncs)

        # signatures
        self.sign_matrix = self.create_signs()


    def _hash(self):

        # one_hot indices vector
        hash_indices = list(range(1, self.shape[0]+1))

        # shuffle 
        shuffle(hash_indices)

        return hash_indices


    def build_functions(self, nfuncs):

        self.functions = [self._hash() for _ in range(nfuncs)]

        return self.functions


    # create hash method takes as input a one hot encoded vector 
    # and produces a compressed vector signature for it
    def create_signs(self):

        signature_matrix = []

        # for each permutation
        for func in self.functions:

            # signature vector
            perm_sign = np.zeros(self.shape[1])

            # for each permutation index in orer
            for i in range(1, self.shape[0]+1):
                
                if not np.count_nonzero(perm_sign==0):
                    break

                # find suffled index
                idx = func.index(i)

                # get permutation row 
                row = self.one_hot_matrix[idx]

                # for each elemnt in row
                for i, value in enumerate(row):
                    if not np.count_nonzero(perm_sign==0):
                        break
                    
                    # if specific elemnt is 1 and index is not taken
                    if value == 1 and not perm_sign[i]:
                        perm_sign[i] = idx

            signature_matrix += [perm_sign]

        return np.array(signature_matrix)


class LSH:
    def __init__(self, matrix, b):
        # assign signature matrix
        self.sign_matrix = matrix

        # define size of bands partition
        self.b = b

        # crete bands
        self.bands = self.partition_bands()


    def partition_bands(self):

        # make sure signature can be split into b bands
        assert self.sign_matrix.shape[0] % self.b == 0
        
        # rows within each band
        r = self.sign_matrix.shape[0] // self.b
        
        bands = []
        # split into bands
        for i in range(0, self.sign_matrix.shape[0], r):
            bands += [self.sign_matrix[i : i+r]]

        return np.array(bands)

    # Hash each band of the matrix M to a hash table with k buckets
    def hash_bands(bands, k):

      # Initialize a list to store the hash tables
      hash_tables = []
      for band in bands:

        # Create an empty hash table with k buckets
        hash_table = [set() for _ in range(k)]

        # Hash each column of the band to a bucket in the hash table
        for j in range(band.shape[1]):

          # Compute the hash value of the column
          hash_value = hash(tuple(band[:, j])) % k

          # Add the column to the corresponding bucket in the hash table
          hash_table[hash_value].add(j)

        # Add the hash table to the list
        hash_tables.append(hash_table)

      return hash_tables

    # Find the candidate column pairs for the matrix M
    def find_candidates(M, b, r, k):

      # Divide the matrix M into b bands of r rows
      bands = divide_matrix(M, b, r)

      # Hash each band of the matrix M to a hash table with k buckets
      hash_tables = hash_bands(bands, k)

      # Initialize a set to store the candidate column pairs
      candidates = set()
      # For each band, find the candidate column pairs
      for i, hash_table in enumerate(hash_tables):

        # For each bucket in the hash table
        for bucket in hash_table:

          # If there is more than one column in the bucket
          if len(bucket) > 1:

            # Add all pairs of columns in the bucket to the candidates set
            candidates.update(combinations(bucket, 2))

      # Return the candidate column pairs
      return candidates


    def retrieve_candidates(self, band_a, band_b):
        for a_rows, b_rows in zip(band_a, band_b):
            if a_rows == b_rows:
                print(f"Candidate pair: {b_rows} == {a_rows}")
                break