import warnings
from sklearn.cluster import AffinityPropagation, KMeans
import numpy as np

def flatten(list_of_lists):
    "Flatten nestet lists"
    if len(list_of_lists) == 0:
        return list_of_lists
    if isinstance(list_of_lists[0], list):
        return flatten(list_of_lists[0]) + flatten(list_of_lists[1:])
    if isinstance(list_of_lists[0], set):
        return flatten(list_of_lists[0]) + flatten(list_of_lists[1:])
    return list_of_lists[:1] + flatten(list_of_lists[1:])

def cak(input):
    "CAK-means clustering method."
    random_state = 0
    repeat = True
    while repeat:
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore', 'Affinity propagation did not converge, this model will not have any cluster centers.')
                cluster = AffinityPropagation(max_iter=1000, random_state=random_state).fit(input)
            cluster = KMeans(len(np.unique(cluster.labels_)), init=cluster.cluster_centers_, n_init=1).fit(input)
            repeat = False
        except:
            random_state += 1
            print('Affinity Propagation did not converge. Add 1 to random state:', random_state)
    return cluster

def intersection(lst1, lst2):
    "Returns the elements, which are in both lst1 and lst2"
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def complement(lst1, lst2):
    "Returns the elements of lst1, which are not in lst2"
    lst3 = [word for word in lst1 if not word in lst2]
    return lst3

def recall(lst1, lst2):
    # lst3 = [value for value in lst1 if value in lst2]
    lst3 = intersection(lst1, lst2)
    return np.round(len(lst3)/len(lst2), 2)

def precision(lst1, lst2):
    # lst3 = [value for value in lst1 if value in lst2]
    lst3 = intersection(lst1, lst2)
    return np.round(len(lst3)/len(lst1), 2)

def f1(lst1, lst2):
    return np.round(2*recall(lst1, lst2)*precision(lst1, lst2)/(recall(lst1, lst2) + precision(lst1, lst2)), 2)