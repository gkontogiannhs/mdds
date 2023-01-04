import hashlib
import numpy as np

class LSHFunction:
  def __init__(self, num_hash_functions, dimensions):
    self.num_hash_functions = num_hash_functions
    self.dimensions = dimensions  # the number of dimensions in the vectors
    self.hash_functions = [self.create_hash_function() for _ in range(self.num_hash_functions)]
  
  def create_hash_function(self):
    # create a hash function using the hashlib library
    return hashlib.sha256()

class LSH:
  def __init__(self, dataset, lsh_function, random_vectors):
    self.dataset = dataset  # the dataset to be hashed, assumed to be a list of numpy arrays
    self.lsh_function = lsh_function  # the LSH function to use
    self.random_vectors = random_vectors  # the random vectors to use for the LSH function
    self.hash_tables = []  # a list to store the hash tables, one for each LSH function
    self.build_hash_tables()  # build the hash tables for the dataset
  
  def build_hash_tables(self):
    for i in range(self.lsh_function.num_hash_functions):
      # create an empty hash table for the current LSH function
      hash_table = {}
      # hash each item in the dataset and add it to the hash table
      for item in self.dataset:
        # compute the hash value of the item using the current random vector
        hash_value = self.lsh_function.hash_functions[i].update(str(np.dot(item, self.random_vectors[i])).encode("utf-8"))
        hash_value = self.lsh_function.hash_functions[i].hexdigest()
        if hash_value not in hash_table:
          hash_table[hash_value] = []
        hash_table[hash_value].append(item)
      # add the hash table to the list of hash tables
      self.hash_tables.append(hash_table)
  
  def retrieve_candidates(self, hash_value, lsh_function):
    # retrieve the candidates for the given hash value and LSH function
    if hash_value in lsh_function:
      return lsh_function[hash_value]
    return []
  

  def compute_similarities(self, candidates, query_item):
    # compute the cosine similarity between the query item and each candidate
    candidate_similarities = {}
    for candidate in candidates:
        similarity = np.dot(candidate, query_item) / (np.linalg.norm(candidate) * np.linalg.norm(query_item))
        candidate_similarities[candidate] = similarity
    return candidate_similarities


  def range_query(self, query_item, range):
    candidates = {}  # empty set to store candidates
    for i, lsh_function in enumerate(self.hash_tables):
      # compute the hash value of the query item using the current random vector
      query_hash = self.lsh_function.hash_functions[i].update(str(np.dot(query_item, self.random_vectors[i])).encode("utf-8"))
      query_hash = self.lsh_function.hash_functions[i].hexdigest()
      # retrieve the candidates for the current hash function
      candidates_for_hash = self.retrieve_candidates(query_hash, lsh_function)
      # add the candidates to the overall set of candidates
      candidates.update(candidates_for_hash)
    # compute the actual similarity between the query item and each candidate
    candidate_similarities = self.compute_similarities(candidates, query_item)
    # return the candidates that fall within the specified range
    return [candidate for candidate in candidate_similarities if candidate_similarities[candidate] <= range]

