# Copyright 2013 Philip N. Klein
from vec import Vec
from mat import Mat
import GF2

def row_reduce(rowlist):
    """Given a list of vectors, transform the vectors.
       Mutates the argument.
       Returns a list of the nonzero reduced vectors in echelon form.
    """
    col_label_list = sorted(rowlist[0].D, key=repr)
    rows_left = set(range(len(rowlist)))
    new_rowlist = []
    for c in col_label_list:
        #among rows left, list of row-labels whose rows have a nonzero in position c
        rows_with_nonzero = [r for r in rows_left if rowlist[r][c] != 0]
        if rows_with_nonzero != []:
            pivot = rows_with_nonzero[0]
            rows_left.remove(pivot)
            new_rowlist.append(rowlist[pivot])
            for r in rows_with_nonzero[1:]:
                rowlist[r] -= (rowlist[r][c]/rowlist[pivot][c])*rowlist[pivot]
    return new_rowlist

def transformation_rows(rowlist_input, col_label_list = None):
    """Given a matrix A represented by a list of rows
        optionally given the unit field element (1 by default),
        and optionally given a list of the domain elements of the rows,
        return a matrix M represented by a list of rows such that
        M A is in echelon form
    """
    one = GF2.one # replace this with 1 if working over R or C
    rowlist = list(rowlist_input)
    if col_label_list == None: col_label_list = sorted(rowlist[0].D, key=repr)
    m = len(rowlist)
    row_labels = set(range(m))
    M_rowlist = [Vec(row_labels, {i:one}) for i in range(m)]
    new_M_rowlist = []
    rows_left = set(range(m))
    for c in col_label_list:
        rows_with_nonzero = [r for r in rows_left if rowlist[r][c] != 0]
        if rows_with_nonzero != []:
            pivot = rows_with_nonzero[0]
            rows_left.remove(pivot)
            new_M_rowlist.append(M_rowlist[pivot])
            for r in rows_with_nonzero[1:]:
                multiplier = rowlist[r][c]/rowlist[pivot][c]
                rowlist[r] -= multiplier*rowlist[pivot]
                M_rowlist[r] -= multiplier*M_rowlist[pivot]
    for r in rows_left: new_M_rowlist.append(M_rowlist[r])
    return new_M_rowlist

def transformation(A, col_label_list = None):
    """Given a matrix A, and optionally the unit field element (1 by default),
       compute matrix M such that M is invertible and
       U = M*A is in echelon form.
    """
    row_labels, col_labels = A.D
    m = len(row_labels)
    row_label_list = sorted(row_labels, key=repr)
    rowlist = [Vec(col_labels, {c:A[r,c] for c in col_labels}) for r in row_label_list]
    M_rows = transformation_rows(rowlist, col_label_list)
    M = Mat((set(range(m)), row_labels), {})
    for r in range(m):
        for (i,value) in M_rows[r].f.items():
            M[r,row_label_list[i]] = value
    return M
