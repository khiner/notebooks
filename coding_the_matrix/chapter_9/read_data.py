# Copyright 2013 Philip N. Klein
from vec import Vec
from mat import Mat

def read_vectors(filename):
    """File should have the following format:
    First line should consist of labels, separated by tabs or spaces.
    Remaining lines should consist of numeric data.
    Procedure returns a list of Vecs, one for each line of numeric data.
    The labels for the Vecs are the strings given in the first line.
    """
    with open(filename) as file:
        labels = file.readline().split()
        vlist = [Vec(set(labels), dict(zip(labels, map(float, line.split())))) for line in file]
        return vlist

def read_matrix(filename):
    """File should have the following format:
    First line should consist of column labels, separated by tabs or spaces.
    Each subsequent line should consist of a row label followed by numeric data.
    Procedure returns a matrix with the given row and column labels and numeric data
    """
    with open(filename) as file:
        col_labels = file.readline().split()
        row_labels = set()
        f = {}
        for line in file:
            entries = line.split()
            row_label = entries[0]
            row_labels.add(row_label)
            for col, entry in zip(col_labels, entries[1:]):
                f[row_label, col] = entry
        return Mat((row_labels, set(col_labels)), f)

def read_vector(filename):
    """File should have the following format:
    Each line consists of a label followed by a single numeric value, separated by whitespace
    Procedure returns a vector with one entry per line of the file
    """
    with open(filename) as file:
        func = {k: float(v) for k,v in (line.split() for line in file)}
        domain = set(func.keys())
        return Vec(domain, func)
