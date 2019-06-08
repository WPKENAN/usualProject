import random
import numpy as np


class TableNode(object):
    def __init__(self, index):
        self.val = index
        self.buckets = {}


def genPara(n, r):
    """

    :param n: length of data vector
    :param r:
    :return: a, b
    """

    a = []
    for i in range(n):
        a.append(random.gauss(0, 1))
    b = random.uniform(0, r)

    return a, b


def gen_wp_e2LSH_family(n, k, r):
    """

    :param n: length of data vector
    :param k:
    :param r:
    :return: a list of parameters (a, b)
    """
    wp_result = []
    for i in range(k):
        wp_result.append(genPara(n, r))

    return wp_result


def gen_HashVals(wp_e2LSH_family, v, r):
    """

    :param wp_e2LSH_family: include k hash funcs(parameters)
    :param v: data vector
    :param r:
    :return hash values: a list
    """

    # wp_hashVals include k values
    wp_hashVals = []

    for hab in wp_e2LSH_family:
        hashVal = (np.inner(hab[0], v) + hab[1]) // r
        wp_hashVals.append(hashVal)

    return wp_hashVals


def H2(wp_hashVals, wp_fpRand, k, C):
    """

    :param wp_hashVals: k hash vals
    :param wp_fpRand: ri', the random vals that used to generate fingerprint
    :param k, C: parameter
    :return: the fingerprint of (x1, x2, ..., xk), a int value
    """
    return int(sum([(wp_hashVals[i] * wp_fpRand[i]) for i in range(k)]) % C)


def e2LSH(wp_dataSet, k, L, r, tableSize):
    """
    generate hash table

    * hash table: a list, [node1, node2, ... node_{tableSize - 1}]
    ** node: node.val = index; node.buckets = {}
    *** node.buckets: a dictionary, {fp:[v1, ..], ...}

    :param wp_dataSet: a set of vector(list)
    :param k:
    :param L:
    :param r:
    :param tableSize:
    :return: 3 elements, hash table, hash functions, wp_fpRand
    """

    wp_hashTable = [TableNode(i) for i in range(tableSize)]

    n = len(wp_dataSet[0])
    m = len(wp_dataSet)

    C = pow(2, 32) - 5
    wp_hashFuncs = []
    wp_fpRand = [random.randint(-10, 10) for i in range(k)]

    for times in range(L):

        wp_e2LSH_family = gen_wp_e2LSH_family(n, k, r)

        # wp_hashFuncs: [[h1, ...hk], [h1, ..hk], ..., [h1, ...hk]]
        # wp_hashFuncs include L hash functions group, and each group contain k hash functions
        wp_hashFuncs.append(wp_e2LSH_family)

        for dataIndex in range(m):

            # generate k hash values
            wp_hashVals = gen_HashVals(wp_e2LSH_family, wp_dataSet[dataIndex], r)

            # generate fingerprint
            fp = H2(wp_hashVals, wp_fpRand, k, C)

            # generate index
            index = fp % tableSize

            # find the node of hash table
            node = wp_hashTable[index]

            # node.buckets is a dictionary: {fp: vector_list}
            if fp in node.buckets:

                # bucket is vector list
                bucket = node.buckets[fp]

                # add the data index into bucket
                bucket.append(dataIndex)

            else:
                node.buckets[fp] = [dataIndex]

    return wp_hashTable, wp_hashFuncs, wp_fpRand


def nn_search(wp_dataSet, wp_query, k, L, r, tableSize):
    """

    :param wp_dataSet:
    :param wp_query:
    :param k:
    :param L:
    :param r:
    :param tableSize:
    :return: the data index that similar with wp_query
    """

    wp_result = set()

    temp = e2LSH(wp_dataSet, k, L, r, tableSize)
    C = pow(2, 32) - 5

    wp_hashTable = temp[0]
    wp_wp_hashFuncGroups = temp[1]
    wp_fpRand = temp[2]

    for wp_hashFuncGroup in wp_wp_hashFuncGroups:

        # get the fingerprint of wp_query
        wp_wp_queryFp = H2(gen_HashVals(wp_hashFuncGroup, wp_query, r), wp_fpRand, k, C)

        # get the index of wp_query in hash table
        wp_wp_queryIndex = wp_wp_queryFp % tableSize

        # get the bucket in the dictionary
        if wp_wp_queryFp in wp_hashTable[wp_wp_queryIndex].buckets:
            wp_result.update(wp_hashTable[wp_wp_queryIndex].buckets[wp_wp_queryFp])

    return wp_result
