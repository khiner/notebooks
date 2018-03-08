# Solutions to procedure-writing exercises from Chapter 5 reproduced here
# so as to not clutter the Chapter 6 Jupyter notebook.

from mat import Mat
from vec import Vec
from vecutil import list2vec
from matutil import coldict2mat
from solver import solve

def rep2vec(u, veclist):
    A = coldict2mat(veclist)
    return A * u

def vec2rep(veclist, v):
    A = coldict2mat(veclist)
    return solve(A, v)

def is_superfluous(L, i):
    if len(L) <= 1:
        return False
    L_copy = L.copy()
    b = L_copy.pop(i)
    A = coldict2mat(L_copy)
    u = solve(A, b)
    residual = b - A * u
    return residual * residual < 10e-14

def is_independent(L):
    return not any([is_superfluous(L, i) for i in range(len(L))])

def subset_basis(T):
    B = []
    for t in T:
        if len(B) == 0 or not is_superfluous(B + [t], len(B)):
            B.append(t)
    return B

def superset_basis(T, L):
    S = T.copy()
    for l in L:
        if len(S) == 0 or not is_superfluous(S + [l], len(S)):
            S.append(l)
    return S

def exchange(S, A, z):
    S_copy = S.copy()
    S_copy.append(z)

    for i in range(len(S_copy)):
        if is_superfluous(S_copy, i) and S_copy[i] not in A and S_copy[i] != z:
            return S_copy[i]
