# Copyright 2013 Philip N. Klein
""" A module for working with images in matrix format.
    An image is represented by two matrices, representing points and colors.
    The points matrix has row labels {'x', 'y', 'u'} and column labels (0,0) through (w, h), inclusive,
    where (w, h) are the width and height of the original image
    The colors matrix has row labels {'r', 'g', 'b'} and column labels (0,0) through (w-h, h-1).

    The column labels for these matrices represent "lattice points" on the original image.
    For pixel (i,j) in the original image, the (i,j) column in the colors matrix represents
    the pixel color and the (i,j), (i+1, j), (i+1, j+1), and (i, j+1) columns in the points
    matrix represent the boundary of the pixel region
    """

import mat
import png
import numbers
import collections
import webbrowser
import tempfile
import os
import atexit
import math


from IPython.core.display import display, HTML

# Round color coordinate to nearest int and clamp to [0, 255]
def _color_int(col):
    return max(min(round(col), 255), 0)

# utility conversions, between boxed pixel and flat pixel formats
# the png library uses flat, we use boxed.
def _boxed2flat(row):
    return [_color_int(x) for box in row for x in box]

def _flat2boxed(row):
    # Note we skip every 4th element, thus eliminating the alpha channel
    return [tuple(row[i:i+3]) for i in range(0, len(row), 4)]

## Image conversions
def isgray(image):
    "tests whether the image is grayscale"
    col = image[0][0]
    if isinstance(col, numbers.Number):
        return True
    elif isinstance(col, collections.Iterable) and len(col) == 3:
        return False
    else:
        raise TypeError('Unrecognized image type')

def color2gray(image):
    """ Converts a color image to grayscale """
    # we use HDTV grayscale conversion as per https://en.wikipedia.org/wiki/Grayscale
    return [[int(0.2126*p[0] + 0.7152*p[1] + 0.0722*p[2]) for p in row]
                                                          for row in image]

def gray2color(image):
    """ Converts a grayscale image to color """
    return [[(p,p,p) for p in row] for row in image]

#extracting and combining color channels
def rgbsplit(image):
    """ Converts an RGB image to a 3-element list of grayscale images, one for each color channel"""
    return [[[pixel[i] for pixel in row] for row in image] for i in (0,1,2)]

def rgpsplice(R,G,B):
    return [[(R[row][col],G[row][col],B[row][col]) for col in range(len(R[0]))] for row in range(len(R))]

## To and from files
def file2image(path):
    """ Reads an image into a list of lists of pixel values (tuples with
        three values). This is a color image. """
    (w, h, p, m) = png.Reader(filename = path).asRGBA() # force RGB and alpha
    return [_flat2boxed(r) for r in p]


def image2file(image, path):
    """ Writes an image in list of lists format to a file. Will work with
        either color or grayscale. """
    if isgray(image):
        img = gray2color(image)
    else:
        img = image
    with open(path, 'wb') as f:
        png.Writer(width=len(image[0]), height=len(image)).write(f,
            [_boxed2flat(r) for r in img])

## Display functions
def image2display(image, browser=None):
    """ Stores an image in a temporary location and displays it on screen
        using a web browser. """
    path = _create_temp('.png')
    image2file(image, path)
    hpath = _create_temp('.html')
    with open(hpath, 'w') as h:
        h.writelines(["<html><body><img src='file://%s'/></body></html>" % path])
    openinbrowser('file://%s' % hpath, browser)
    print("Hit Enter once the image is displayed.... ", end="")
    input()

_browser = None

def setbrowser(browser=None):
    """ Registers the given browser and saves it as the module default.
        This is used to control which browser is used to display the plot.
        The argument should be a value that can be passed to webbrowser.get()
        to obtain a browser.  If no argument is given, the default is reset
        to the system default.

        webbrowser provides some predefined browser names, including:
        'firefox'
        'opera'

        If the browser string contains '%s', it is interpreted as a literal
        browser command line.  The URL will be substituted for '%s' in the command.
        For example:
        'google-chrome %s'
        'cmd "start iexplore.exe %s"'

        See the webbrowser documentation for more detailed information.

        Note: Safari does not reliably work with the webbrowser module,
        so we recommend using a different browser.
    """
    global _browser
    if browser is None:
        _browser = None  # Use system default
    else:
        webbrowser.register(browser, None, webbrowser.get(browser))
        _browser = browser

def getbrowser():
    """ Returns the module's default browser """
    return _browser

def openinbrowser(url, browser=None):
    if browser is None:
        browser = _browser
    webbrowser.get(browser).open(url)

# Create a temporary file that will be removed at exit
# Returns a path to the file
def _create_temp(suffix='', prefix='tmp', dir=None):
    _f, path = tempfile.mkstemp(suffix, prefix, dir)
    os.close(_f)
    _remove_at_exit(path)
    return path

# Register a file to be removed at exit
def _remove_at_exit(path):
    atexit.register(os.remove, path)

def file2mat(path, row_labels = ('x', 'y', 'u')):
    """input: a filepath to an image in .png format
    output: the pair (points, matrix) of matrices representing the image."""
    return image2mat(file2image(path), row_labels)

def image2mat(img, row_labels = ('x', 'y', 'u')):
    """ input: an image in list-of-lists format
        output: a pair (points, colors) of matrices representing the image.
        Note: The input list-of-lists can consist of either integers n [0, 255] for grayscale
        or 3-tuple of integers representing the rgb color coordinates
    """
    h = len(img)
    w = len(img[0])
    rx, ry, ru = row_labels
    ptsD = (set(row_labels), {(x,y) for x in range(w+1) for y in range(h+1)})
    ptsF = {}
    colorsD = ({'r', 'g', 'b'}, {(x,y) for x in range(w) for y in range(h)})
    colorsF = {}
    for y in range(h+1):
        for x in range(w+1):
            pt = (x,y)
            ptsF[(rx, pt)] = x
            ptsF[(ry, pt)] = y
            ptsF[(ru, pt)] = 1
            if x < w and y < h:
                col = img[y][x]
                if type(col) is int:
                    red, green, blue = col, col, col
                else:
                    red, green, blue = col
                colorsF[('r', pt)] = red
                colorsF[('g', pt)] = green
                colorsF[('b', pt)] = blue
    return mat.Mat(ptsD, ptsF), mat.Mat(colorsD, colorsF)

def mat2display(pts, colors, row_labels = ('x', 'y', 'u'),
                scale=1, xscale=None, yscale = None, xmin=0, ymin=0, xmax=None, ymax=None,
                crosshairs=False, browser=None):
    """ input: matrix pts and matrix colors representing an image
        result: Displays the image in a web browser

        Optional arguments:

        row_labels - A collection specifying the points matrix row labels,
        in order.  The first element of this collection is considered the x
        coordinate, the second is the y coordinate, and the third is the u
        coordinate, which is assumed to be 1 for all points.

        scale - The display scale, in pixels per image coordinate unit
        xscale, yscale - in case you want to scale differently in x and y

        xmin, ymin, xmax, ymax - The region of the image to display.  These can
        be set to None to use the minimum/maximum value of the coordinate
        instead of a fixed value.

        crosshairs - Setting this to true displays a crosshairs at (0, 0) in
        image coordinates

        browser - A browser string to be passed to webbrowser.get().
        Overrides the module default, if any has been set.
    """
    if xscale == None: xscale = scale
    if yscale == None: yscale = scale

    rx, ry, ru = row_labels
    if ymin is None:
        ymin = min(v for (k, v) in pts.f.items() if k[0] == ry)
    if xmin is None:
        xmin = min(v for (k, v) in pts.f.items() if k[0] == rx)
    if ymax is None:
        ymax = max(v for (k, v) in pts.f.items() if k[0] == ry)
    if xmax is None:
        xmax = max(v for (k, v) in pts.f.items() if k[0] == rx)

    # Include (0, 0) in the region
    if crosshairs:
        ymin = min(ymin, 0)
        xmin = min(xmin, 0)
        ymax = max(ymax, 0)
        xmax = max(xmax, 0)


    #hpath = _create_temp('.html')
    html = ''.join(['<!DOCTYPE html>\n',
            '<head> <title>image</title> </head>\n',
            '<body>\n',
            '<svg height="%s" width="%s" xmlns="http://www.w3.org/2000/svg">\n' % ((ymax-ymin) * yscale, (xmax-xmin) * xscale),
            '<g transform="scale(%s) translate(%s, %s) ">\n' % (scale, -xmin, -ymin)])
    #with open(hpath, 'w') as h:
    pixels = sorted(colors.D[1])
    Mx, My = pixels[-1]

    # go through the quads, writing each one to canvas
    for l in pixels:
        lx, ly = l
        r = _color_int(colors[('r', l)])
        g = _color_int(colors[('g', l)])
        b = _color_int(colors[('b', l)])

        mx = min(lx+1, Mx)+1
        my = min(ly+1, My)+1

        # coords of corners
        x0 = pts[(rx, l)]
        y0 = pts[(ry, l)]
        x1 = pts[(rx, (mx, ly))]
        y1 = pts[(ry, (mx, ly))]
        x2 = pts[(rx, (mx, my))]
        y2 = pts[(ry, (mx, my))]
        x3 = pts[(rx, (lx, my))]
        y3 = pts[(ry, (lx, my))]

        html += '<polygon points="%s, %s %s, %s, %s, %s %s, %s" fill="rgb(%s, %s, %s)" stroke="none" />\n' % (x0, y0, x1, y1, x2, y2, x3, y3, r, g, b)

        # Draw crosshairs centered at (0, 0)
        if crosshairs:
            html += ''.join(['<line x1="-50" y1="0" x2="50" y2="0" stroke="black" />\n',
                     '<line x1="0" y1="-50" x2="0" y2="50" stroke="black" />\n',
                     '<circle cx="0" cy="0" r="50" style="stroke: black; fill: none;" />\n'])

    html += ''.join(['</g></svg>\n', '</body>\n', '</html>\n'])


    # Render directly in Jupyter instead of loading a temp file in the browser.
    display(HTML(html))
    # openinbrowser('file://%s' % hpath, browser)
    # print("Hit Enter once the image is displayed.... ", end="")
    # input()
