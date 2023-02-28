from numpy import array, zeros, empty
from random import shuffle 
from itertools import combinations
from copy import deepcopy
from mdds.helpers import cosine_similarity

"""
The above code consists of two classes: MinHash and LSH. The MinHash class is used to generate a signature matrix
of an input one-hot encoded matrix, and the LSH class is used to perform approximate nearest neighbor search on the
signature matrix using Locality Sensitive Hashing (LSH).


The MinHash class has the following methods and attributes:

    __init__(self, one_hot_matrix, nfuncs): 
       
    _hash(self): 
        
    _signature_matrix(self):



The LSH class has the following methods and attributes:

    __init__(self, nfuncs, bands): 
        This method is the constructor of the class. It initializes the object with the number of hash functions (nfuncs), the number of
        bands (bands) used to partition the signature matrix
        The attribute hash_tables is initially set to None.

    partition_into_bands(self, sm):
        This method partitions the signature matrix (sm) into bands number of bands.

    fit(self, data, buckets):
        This method is used to fit the LSH model to the input data. It creates an object of the MinHash class with
        the input data and nfuncs number of hash functions. It then creates the signature matrix using the _signature_matrix()
        method from the MinHash class. It then partitions the signature matrix into bands and uses the hash values of the columns
        of each band to create a list of hash tables with buckets number of buckets.

    _get_candidates(self):
        This method finds candidate column pairs for the input matrix by looking for columns that have the same hash value
        in the same band of the signature matrix (items in same buckets). It returns a set of candidate column pairs.

    neigbors(self, similarity, dist_function):
        This method takes two arguments, the similar threshold and the function to measure distance between points.
        It returns all the points that have similarity >= similar. This method finds similar columns in the input matrix based on the
        similarity function passed as an argument. By default, it uses the cosine similarity function. It uses the _find_candidates()
        method to find the candidate column pairs, then it filters false positives by their similarity and return the columns that
        have a similarity greater than the specified threshold

    get_nearest_neighbors(self, query, radius):
        This method, tries to return the points that are similar to a query. This is done by hashing the query and returning the 
        hashed bucket plus the buckets within the specified raddius.
"""

class MinHash:
    def __init__(self, one_hot_matrix, nfuncs):
        """
        This method is the constructor of the class. It initializes the object with the input one-hot encoded matrix, the number
        of hash functions (nfuncs), and the signature matrix (sign_matrix) which is initially set to None.
        """

        # one hot encoded matrix
        self.one_hot_matrix = one_hot_matrix

        # store dimensionality
        self.shape = one_hot_matrix.shape
        
        # vertical dimmensionality of signature M
        self.nfuncs = nfuncs

        # create hash functions
        self.functions = self.build_functions(nfuncs)

        # signatures
        self.sign_matrix = None


    def _hash(self):
        """
        This method creates a list of indices of the rows of the one-hot encoded matrix in a random order.
        build_functions(self, nfuncs): This method builds nfuncs number of hash functions by calling the _hash() method.
        """

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
    def _signature_matrix(self):
        """
        This method creates the signature matrix of the input one-hot encoded matrix using the hash functions created by
        the build_functions() method. It assigns the signature matrix to the sign_matrix attribute of the class.
        The method returns the signature matrix.
        """
        # sign_matrix = []
        sign_matrix = empty(shape=(self.nfuncs, self.shape[1]), dtype=int)

        for i, func in enumerate(self.functions):

            perm_sign = zeros(self.shape[1])

            j = 1
            
            while (perm_sign == 0).any():
                
                idx = func.index(j)
                row = self.one_hot_matrix[idx]

                mask = (perm_sign == 0) & (row == 1)
                perm_sign[mask] = j

                j += 1
                
            sign_matrix[i] = perm_sign
        
        self.sign_matrix = deepcopy(sign_matrix)

        return sign_matrix


class LSH:
    def __init__(self, nfuncs, bands):
        """
        This method is the constructor of the class. It initializes the object with the number of hash functions (nfuncs), the number of
        bands (bands) used to partition the signature matrix. The attribute hash_tables is initially an empty list.
        """
        # shingle size
        self.nfuncs = nfuncs
        
        # define size of bands partition
        self.bands = bands
        
        # Initialize a list to store the hash tables
        self.hash_tables = []
        

    # class method to partition signature matrix into b bands
    def partition_into_bands(self, sm):
        """
        This method partitions the signature matrix (sm) into bands number of bands.
        """

        # make sure signature can be split into b bands
        assert sm.shape[0] % self.bands == 0
        
        # rows within each band
        r = sm.shape[0] // self.bands
        
        # split into bands
        # pick r rows and append
        bands = [sm[i:i+r] for i in range(0, sm.shape[0], r)]
        
        return array(bands)
    

    # Hash each band of the matrix M to a hash table with k buckets
    def fit(self, data, num_buckets):
        """
        This method is used to fit the LSH model to the input data. It creates an object of the MinHash class with
        the input data and nfuncs number of hash functions. It then creates the signature matrix using the _signature_matrix()
        method from the MinHash class. It then partitions the signature matrix into bands and uses the hash values of the columns
        of each band to create a list of hash tables with buckets number of buckets.
        """

        self.num_buckets = num_buckets
        
        # create and define as class attribute minhash object
        self.hash_mehod = MinHash(data, nfuncs=self.nfuncs)
       
        # each column represent the signature of each document
        sign_matrix = self.hash_mehod._signature_matrix()

        # split into bands
        bands = self.partition_into_bands(sign_matrix)

        # for each band
        for band in bands:

            # Create an empty hash table with k buckets
            hash_table = [set() for _ in range(self.num_buckets)]

            # Hash each column of the band to a bucket in the hash table
            for j, column in enumerate(band.T):

                # Compute the hash value of the column
                hash_value = hash(tuple(column)) % self.num_buckets

                # Add the column to the corresponding bucket in the hash table
                hash_table[hash_value].add(j)

            # Add the hash table to the list
            self.hash_tables.append(hash_table)

        return self


    # Find the candidate column pairs for the matrix M
    def cands(self):

      # Initialize a set to store the candidate column pairs
      candidates = set()

      # For each band, find the candidate column pairs
      for hash_table in self.hash_tables:

        # For each bucket in the hash table
        for bucket in hash_table:

          # If there is more than one column in the bucket
          if len(bucket) > 1:
            # Add all pairs of columns in the bucket to the candidates set
            candidates.update(combinations(bucket, 2))
            
      # Return the candidate column pairs
      return candidates


    def _get_candidates(self):
        """
        This method finds candidate column pairs for the input matrix by looking for columns that have the same hash value
        in the same band of the signature matrix (items in same buckets). It returns a set of candidate column pairs.
        """

        # Initialize a set to store the candidate column pairs
        candidates = [set() for _ in range(self.num_buckets)]

        # For each band's hash_table, find the candidate column pairs
        for hash_table in self.hash_tables:

            # For each bucket in the hash table
            for i, bucket in enumerate(hash_table):

                # If there is more than one column in the bucket
                if len(bucket) > 1:

                    # Add all pairs of columns in the bucket to the candidates set
                    candidates[i].update(combinations(bucket, 2))

        # Return the candidate column pairs
        return candidates  
      

    def neighbors(self, similar=.6, dist_func=cosine_similarity):
        """
        This method takes two arguments, the similar threshold and the function to measure distance between points.
        It returns all the points that have similarity >= similar. This method finds similar columns in the input matrix based on the
        similarity function passed as an argument. By default, it uses the cosine similarity function. It uses the _find_candidates()
        method to find the candidate column pairs, then it filters false positives by their similarity and return the columns that
        have a similarity greater than the specified threshold
        """
        
        # fetch unfiltered candidates
        cands = set().union(*self._get_candidates())
        
        actual_neigbors = {}

        # for each pair in each bucket of each band
        for c1, c2 in cands:

            # get similarity
            sim = dist_func(self.hash_mehod.one_hot_matrix[:, c1], self.hash_mehod.one_hot_matrix[:, c2])
            
            # if above given threshold
            if sim >= similar: actual_neigbors[c1, c2] = sim 

        return actual_neigbors


    def get_nearest_neighbors(self, query, radius=.1):
        """
        This method, tries to return the points that are similar to a query. This is done by hashing the query and returning the 
        hashed bucket plus the buckets within the specified raddius.
        """
        
        # get concatenated form of hashed band buckets
        buckets = self._get_candidates()
        
        # create hash value for the query item
        query_hash = hash(tuple(query)) % self.num_buckets
        
        # neibgor buckets index
        index = int((len(buckets) * radius)//2)

        # include left and right neigbor buckets within the radius
        cands = set.union(*buckets[index:query_hash-1], buckets[query_hash], *buckets[query_hash+1:index])

        return cands

