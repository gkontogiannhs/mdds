from numpy import array, zeros, dot, count_nonzero
from numpy.linalg import norm

from random import shuffle # in place
from itertools import combinations


def kshingle(text, k):

    shingle_set = []

    for i in range(len(text) - k + 1):
        shingle_set += [text[i:i+k]]
    
    return set(shingle_set)


def one_hot_encoding(vocab, sent):

    one_hot = zeros(len(vocab), dtype=int)

    for i, sh in enumerate(vocab):
        if sh in sent: one_hot[i] = 1

    return one_hot


def jaccard(v, u):
    return round(len(set(v) & set(u)) / len(set(v) | set(u)), 3)
    

def cosine_similarity(u, v):
    if (u == 0).all() | (v == 0).all():
        return 0.
    else:
        return round(dot(u,v) / (norm(u)*norm(v)), 3)


class MinHash:
    def __init__(self, one_hot_matrix, nfuncs):

        # one hot encoded matrix
        self.one_hot_matrix = one_hot_matrix

        # store dimensionality
        self.shape = one_hot_matrix.shape

        # create hash functions
        self.functions = self.build_functions(nfuncs)

        # signatures
        self.sign_matrix = None


    def _hash(self):

        # one_hot indices vector
        hash_indices = list(range(1, self.shape[0]+1))

        # shuffle 
        shuffle(hash_indices)

        return hash_indices


    # basically, it returns a 2D list of indices permutations
    def build_functions(self, nfuncs):

        return [self._hash() for _ in range(nfuncs)]


    # create hash method takes as input a one hot encoded vector 
    # and produces a compressed vector signature for it
    def signature_matrix(self):

        sign_matrix = []

        # for each permutation
        for func in self.functions:

            # signature vector
            perm_sign = zeros(self.shape[1])

            # for each permutation index in orer
            for i in range(1, self.shape[0]+1):
                
                if not count_nonzero(perm_sign==0):
                    break

                # find suffled index
                idx = func.index(i)

                # get permutation row 
                row = self.one_hot_matrix[idx-1]

                # for each elemnt in row
                for j, value in enumerate(row):
                    
                    # if specific elemnt is 1 and index is not taken
                    if value == 1 and not perm_sign[j]:
                        perm_sign[j] = idx

            sign_matrix += [perm_sign]

        self.sign_matrix = array(sign_matrix)
        
        return self.sign_matrix


class LSH:
    def __init__(self, nfuncs, bands, radius=1):

        # shingle size
        self.nfuncs = nfuncs
        
        # define size of bands partition
        self.bands = bands

        # radius to search for 
        self.radius = radius
        
        # Initialize a list to store the hash tables
        self.hash_tables = None
        

    # class method to partition signature matrix into b bands
    def partition_into_bands(self, sm):

        # make sure signature can be split into b bands
        assert sm.shape[0] % self.bands == 0
        
        # rows within each band
        r = sm.shape[0] // self.bands
        
        # split into bands
        # pick r rows and append
        bands = [sm[i:i+r] for i in range(0, sm.shape[0], r)]
        
        return array(bands)


    # Hash each band of the matrix M to a hash table with k buckets
    def fit(self, data, buckets):
        
        # create and define as class attribute minhash object
        self.hash_mehod = MinHash(data, nfuncs=self.nfuncs)
        
        # each column represent the signature of each document
        sign_matrix = self.hash_mehod.signature_matrix()

        # Initialize a list to store the hash tables
        hash_tables = []

        # split into bands
        bands = self.partition_into_bands(sign_matrix)

        # for each band
        for band in bands:

            # Create an empty hash table with k buckets
            hash_table = [set() for _ in range(buckets)]

            # Hash each column of the band to a bucket in the hash table
            for j, column in enumerate(band.T):

                # Compute the hash value of the column
                hash_value = hash(tuple(column)) % buckets

                # Add the column to the corresponding bucket in the hash table
                hash_table[hash_value].add(j)

            # Add the hash table to the list
            hash_tables.append(hash_table)

        # assign to class attribute
        self.hash_tables = hash_tables

        return self


    # Find the candidate column pairs for the matrix M
    def _find_candidates(self):

      # Initialize a set to store the candidate column pairs
      candidates = set()

      # For each band, find the candidate column pairs
      for i, hash_table in enumerate(self.hash_tables):

        # For each bucket in the hash table
        for bucket in hash_table:

          # If there is more than one column in the bucket
          if len(bucket) > 1:

            # Add all pairs of columns in the bucket to the candidates set
            candidates.update(combinations(bucket, 2))

      # Return the candidate column pairs
      return candidates


    def candidates(self, sim_function=cosine_similarity, similarity=0.5):

        # get reduced candidates 
        cands = self._find_candidates()

        # each document is represented by a column
        one_hot_matrix = self.hash_mehod.one_hot_matrix

        actual_cands = {}
        
        # filter by similarity 
        for c1, c2 in cands:
            cos_sim = sim_function(one_hot_matrix[:, c1], one_hot_matrix[:, c2])
            if cos_sim >= similarity: 
                actual_cands[c1, c2] = cos_sim 

        return actual_cands      
        # return [(c1, c2) for (c1, c2) in cands if cosine_similarity(one_hot_matrix[:, c1], one_hot_matrix[:, c2]) >= sim]