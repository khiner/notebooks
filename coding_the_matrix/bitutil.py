# Copyright 2013 Philip N. Klein
"""
Implements several convenience operations for use with the ECC lab.

Author: Landon Judkins (ljudkins)
Date: Spring 2009
Updated by Nick Gaya, Spring 2013

Requires: fields matutil
"""

from GF2 import zero, one
import mat
import random

def str2bits(inp):
    """
    Convert a string into a list of bits, with each character's bits in order
    of increasing significance.
    """
    bs = [1<<i for i in range(8)]
    return [one if ord(s)&b else zero for s in inp for b in bs]

def bits2str(inp):
    """
    Convert a list of bits into a string.  If the number of bits is not a
    multiple of 8, the last group of bits will be padded with zeros.
    """
    bs = [1<<i for i in range(8)]
    return ''.join(chr(sum(bv if bit else 0 for bv,bit in zip(bs, inp[i:i+8]))) for i in range(0, len(inp), 8))

def bits2mat(bits,nrows=4,trans=False):
    """
    Convert a list of bits into a matrix with nrows rows.

    The matrix is populated by bits column by column

    Keyword arguments:
    nrows -- number of rows in the matrix (default 4)
    trans -- whether to reverse rows and columns of the matrix (default False)
    """
    ncols = len(bits)//nrows
    f = {(i,j):one for j in range(ncols) for i in range(nrows) if bits[nrows*j+i]}
    A = mat.Mat((set(range(nrows)), set(range(ncols))), f)
    if trans: A = mat.transpose(A)
    return A

def mat2bits(A, trans=False):
    """
    Convert a matrix into a list of bits.

    The bits are taken from the matrix column by column with keys in sorted order

    Keyword arguments:
    trans -- whether to reverse rows and columns of the matrix (default False)
    """
    if trans:
        return [A[i,j] for i in sorted(A.D[0]) for j in sorted(A.D[1])]
    else:
        return [A[i,j] for j in sorted(A.D[1]) for i in sorted(A.D[0])]

def noise(A,freq):
    """
    return a random noise matrix with the same domain as A.
    The probability for 1 in any entry of the matrix is freq.
    """
    f = {(i,j):one for i in A.D[0] for j in A.D[1] if random.random() < freq}
    return mat.Mat(A.D, f)
