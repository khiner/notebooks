"""
Utility Code for Pagerank Lab (lab 8).

This module provides the following attributes:
data -- directory to look in for data files'
read_data() -- reads data from file and returns link matrix
titles -- a list mapping article numbers to article titles
find_word(w) -- a function that takes a word and returns a list of numbers of articles that contain that word

Author: Landon Judkins (ljudkins)
Date: Spring 2009
Updated by Nick Gaya (ngaya), fall 2013

Requires: porter_stemming
"""

import os.path
import sys
import struct
import array

from mat import Mat
import porter_stemming

_little_endian = (struct.unpack('<i', struct.pack('=i', 1))[0] == 1)
_pstem = porter_stemming.PorterStemmer()

data = ''
if not os.path.exists(data):
    data = 'data'

def _read_windex(fn):
    """ Return word index as dict of words to int pointers """
    with open(fn) as f:
        return dict((w.strip(), int(n)) for w,n in zip(f, f))

def _get_titles(fn, w):
    """ Retrieve the list of title indices for a given word """
    ptr = _wordindex.get(w)
    if(ptr is None): return []
    with open(fn, 'rb') as f:
        f.seek(ptr)
        nints = struct.unpack('>i', f.read(4))[0]
        arr = array.array("i")
        arr.fromfile(f, nints)
    if _little_endian:
        arr.byteswap()
    return arr.tolist()

def _read_titles(fn):
    """ Read titles from file """
    with open(fn) as f:
        return [line.strip().replace(r'\n', '\n') for line in f]

def _read_linkmat(fn, verbose=True):
    """ Read link matrix """
    global titles
    Mf = {}
    with open(fn, 'rb') as f:
        for i, title in enumerate(titles):
            if verbose and (i%10000 == 9999):
                print (".",end='')
                sys.stdout.flush()
            nints = struct.unpack('<i', f.read(4))[0]
            arr = array.array('I')
            arr.fromfile(f, nints)
            if not _little_endian:
                arr.byteswap()
            Mf.update(((title, titles[x]),1) for x in arr)
            # Link every page to itself, to avoid empty columns
            Mf[title,title] = 1
    if verbose: print()
    ts = set(titles)
    return Mat((ts, ts), Mf)

def find_word(w):
    """ Return list of titles that contain a given word
        Returns None if word was not found in index
    """
    global _wordindex
    global _pstem

    wstem = _pstem.stem(w, 0, len(w)-1)
    indices = _get_titles(os.path.join(data, 'inverseindex'), wstem)
    return [titles[i] for i in indices] if indices else []

def read_data(verbose=True):
    """ Read word meta-index, titles, and links """
    global _wordindex, titles
    if verbose: print("Reading word meta-index")
    _wordindex = _read_windex(os.path.join(data, "indexindex.txt"))
    if verbose: print("Reading titles")
    titles = _read_titles(os.path.join(data, "titles.txt"))
    if verbose: print("Reading link structure")
    links = _read_linkmat(os.path.join(data, "links.bin"), verbose)
    if verbose: print("Done")
    return links

