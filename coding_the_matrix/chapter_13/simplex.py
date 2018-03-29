# Copyright 2013 Philip N. Klein
from solver import solve
from mat import Mat
from vec import Vec
from matutil import rowdict2mat, mat2rowdict
import sys # for printing progress

def simplex_step(A, b, c, R_square, show_bases=False):
    if show_bases: print("basis: ", R_square)
    R = A.D[0]
    # Extract the subsystem
    A_square = Mat((R_square, A.D[1]), {(r,c):A[r,c] for r,c in A.f if r in R_square})
    b_square = Vec(R_square, {k:b[k] for k in R_square})
    # Compute the current vertex
    x = solve(A_square, b_square)
    print("(value: ",c*x,") ",end="")
    # Compute a possibly feasible dual solution
    y_square = solve(A_square.transpose(), c) #compute entries with labels in R_square
    y = Vec(R, y_square.f) #Put in zero for the other entries
    if min(y.values()) >= -1e-10: return ('OPTIMUM', x) #found optimum!
    R_leave = {i for i in R if y[i]< -1e-10} #labels at which y is negative
    r_leave = min(R_leave, key=hash) #choose first label at which y is negative
    # Compute the direction to move
    d = Vec(R_square, {r_leave:1})
    w = solve(A_square, d)
    # Compute how far to move
    Aw = A*w # compute once because we use it many times
    R_enter = {r for r in R if Aw[r] < -1e-10}
    if len(R_enter)==0: return ('UNBOUNDED', None)
    Ax = A*x # compute once because we use it many times
    delta_dict = {r:(b[r] - Ax[r])/(Aw[r]) for r in R_enter}
    delta = min(delta_dict.values())
    # Compute the new tight constraint
    r_enter = min({r for r in R_enter if delta_dict[r] == delta}, key=hash)[0]
    # Update the set representing the basis
    R_square.discard(r_leave)
    R_square.add(r_enter)
    return ('STEP', None)

def optimize(A, b, c, R_square, show_bases=False):
    """ solve min { c*x : A*x >= b}
        starting vertex is specified by R_square, i.e.
        R_square is set of row-labels of subsystem specifying initial vertex
        At the end, if the optimization is successful,
        R_square is the set of row-labels specifying final (i.e., optimal) vertex.
        After each pivot step but the last, a - is printed.
    """
    i = 0
    while True:
        i = i+1
        outcome, answer = simplex_step(A, b, c, R_square, show_bases)
        if outcome == 'STEP':
            print(i," ", end='')
            sys.stdout.flush()
            continue
        if outcome == 'UNBOUNDED':
            return None
        assert outcome == 'OPTIMUM'
        return answer

def dict_union(*args):
    dict = {}
    for d in args:
        dict.update(d)
    return dict

def find_vertex(A, b, R_square):
    assert len(A.D[1]) == len(R_square)
    def new_name(r): return (r, -1)
    A_square = Mat((R_square, A.D[1]), {(r,c):A[r,c] for r,c in A.f if r in R_square})
    b_square = Vec(R_square, {k:b[k] for k in R_square})
    x = solve(A_square, b_square)
    A_x = A*x
    missing = A.D[0].difference(R_square) # set of row-labels not in R_square
    extra = {new_name(r) for r in missing}
    f = dict_union(A.f, {(r,new_name(r)):1 for r in missing}, {(e, e):1 for e in extra})
    A_with_extra = Mat((A.D[0].union(extra), A.D[1].union(extra)), f)
    b_with_extra = Vec(b.D.union(extra), b.f)
    new_R_square = R_square | {r if A_x[r]-b[r]<-1e-10 else new_name(r) for r in missing}
    c = Vec(A.D[1].union(extra), {e:1 for e in extra})
    answer= optimize(A_with_extra, b_with_extra, c, new_R_square)
    if answer is None: return False
    basis_candidates=list(new_R_square | D[0])
    R_square.clear()
    R_square.update(set(basis_candidates[:n]))
    return True
