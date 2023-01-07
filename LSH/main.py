from lsh import * 


if __name__ == "__main__":

    data = [
            "Patricia loves the sound of nails strongly pressed against the chalkboard",
            "She was sad to hear that fireflies are facing extinction due to artificial light, habitat loss, and pesticides",
            "Im confused: when people ask me whats up, and I point, they groan"
            ]
    k = 2

    # create vocabulary with shingles        
    vocabulary = set().union(*[shingle(sent, k) for sent in data])

    # one hot representation of each document
    one_hot_matrix = np.array([one_hot_encoding(vocabulary, sent) for sent in data]).T
    # print(one_hot_matrix)

    # create minhash function
    minhash = MinHash(one_hot_matrix, nfuncs=20)

    # each column represent the signature of each document
    sign_matrix = minhash.sign_matrix #; print(sign_matrix)

    # create LSH model providing the data vectors, hash techuiqe and numbers of bands to split
    lsh = LSH(sign_matrix, b=5)

    print(lsh.bands)
