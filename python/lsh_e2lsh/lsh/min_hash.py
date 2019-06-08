import numpy as np
import random
import hashlib


def sigGen(matrix):
    # print("in sigGen")
    """
    * generate the signature vector

    :param matrix: a ndarray var
    :return a signature vector: a list var
    """

    # the row sequence set
    seqSet = [i for i in range(matrix.shape[0])]

    # initialize the sig vector as [-1, -1, ..., -1]
    wp_result = [-1 for i in range(matrix.shape[1])]

    count = 0

    while len(seqSet) > 0:

        # choose a row of matrix randomly
        randomSeq = random.choice(seqSet)

        for i in range(matrix.shape[1]):

            if matrix[randomSeq][i] != 0 and wp_result[i] == -1:
                wp_result[i] = randomSeq
                count += 1
        if count == matrix.shape[1]:
            break

        seqSet.remove(randomSeq)

    # return a list
    return wp_result


def sigMatrixGen(wp_input_matrix, n):
    # print("in sigMatrixGen")
    """
    generate the sig matrix

    :param wp_input_matrix: naarray var
    :param n: the row number of sig matrix which we set
    :return sig matrix: ndarray var
    """

    wp_result = []

    for i in range(n):
        sig = sigGen(wp_input_matrix)
        wp_result.append(sig)

    # return a ndarray
    return np.array(wp_result)


def minHash(wp_input_matrix, b, r):
    # print("in minHsah")
    """

    map the sim vector into same hash bucket
    :param wp_input_matrix:
    :param b: the number of bands
    :param r: the row number of a band
    :return the hash bucket: a dictionary, key is hash value, value is column number
    """

    wp_hashBuckets = {}

    # permute the matrix for n times
    n = b * r

    # generate the sig matrix
    sigMatrix = sigMatrixGen(wp_input_matrix, n)

    # begin and end of band row
    begin, end = 0, r

    # count the number of band level
    count = 0

    while end <= sigMatrix.shape[0]:

        count += 1

        # traverse the column of sig matrix
        for colNum in range(sigMatrix.shape[1]):

            # generate the hash object, we used md5
            hashObj = hashlib.md5()

            # calculate the hash value
            band = str(sigMatrix[begin: begin + r, colNum]) + str(count)
            hashObj.update(band.encode())

            # use hash value as bucket tag
            tag = hashObj.hexdigest()

            # update the dictionary
            if tag not in wp_hashBuckets:
                wp_hashBuckets[tag] = [colNum]
            elif colNum not in wp_hashBuckets[tag]:
                wp_hashBuckets[tag].append(colNum)
        begin += r
        end += r

    # return a dictionary
    return wp_hashBuckets


def nn_search(wp_dataSet, wp_query,b,r):
    """

    :param wp_dataSet: 2-dimension array
    :param wp_query: 1-dimension array
    :return: the data columns in data set that are similarity with wp_query
    """

    wp_result = set()

    wp_dataSet.append(wp_query)
    wp_input_matrix = np.array(wp_dataSet).T
    wp_hashBucket = minHash(wp_input_matrix, b, r)


    wp_queryCol = wp_input_matrix.shape[1] - 1

    for key in wp_hashBucket:
        if wp_queryCol in wp_hashBucket[key]:
            for i in wp_hashBucket[key]:
                wp_result.add(i)

    wp_result.remove(wp_queryCol)
    return wp_result

if __name__=="__main__":
    wp_dataSet = [[1, 1, 0, 0, 0, 1, 1], [0, 0, 1, 1, 1, 0, 0], [1, 0, 0, 0, 0, 1, 1]]
    wp_query = [0, 1, 1, 1, 1, 0, 0]
    wp_dataSet.append(wp_query)
    # 把这个查询的数组加入到我们的整个数据集当中，并且将它转换成矩阵的形式
    matrix = np.array(wp_dataSet).T
    print(matrix)
    wp_result=nn_search(wp_dataSet,wp_query,5,3)
    print(wp_result)