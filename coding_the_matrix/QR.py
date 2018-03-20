# Copyright 2013 Philip N. Klein
from orthonormalization import aug_orthonormalize
from dictutil import dict2list, list2dict
from matutil import mat2coldict, coldict2mat

def factor(A):
    col_labels = sorted(A.D[1], key=repr)
    Acols = dict2list(mat2coldict(A),col_labels)
    Qlist, Rlist = aug_orthonormalize(Acols)
    #Now make Mats
    Q = coldict2mat(Qlist)
    R = coldict2mat(list2dict(Rlist, col_labels))
    return Q,R
