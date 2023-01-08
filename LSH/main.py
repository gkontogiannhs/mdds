from lsh import LSH
from lsh import kshingle, one_hot_encoding, jaccard, cosine_similarity

from numpy import array
from pandas import read_csv
from nltk.corpus import stopwords


if __name__ == "__main__":
    
    # stop words vocab
    stop_words = set(stopwords.words('english'))

    # data
    dataset = read_csv('../List_of_computer_scientists.csv')
    data = dataset['Education'].apply(lambda doc: ' '.join([w for w in doc.split() if w not in stop_words])).to_list()
 
    k = 5 # shingle size step

    # create vocabulary with shingles        
    vocabulary = set().union(*[kshingle(sent, k) for sent in data])

    # one hot representation of each document
    one_hot_matrix = array([one_hot_encoding(vocabulary, sent) for sent in data]).T

    # create LSH model providing the bands magnitute 
    # in fit hashes each column for each band of the sign matrix M to a hash table with k buckets
    lsh = LSH(nfuncs=100, bands=20).fit(data=one_hot_matrix, buckets=10000)
    
    # get candidates with similarity bigger than 60%
    actual_candidates = lsh.candidates(jaccard, similarity=.6)
    
    for cand_pair, sim in actual_candidates.items():
        print(f"Candidate pair {cand_pair}, similarity: {sim}")
        print(data[cand_pair[0]])
        print()
        print(data[cand_pair[1]])
        print()

    print(len(actual_candidates))