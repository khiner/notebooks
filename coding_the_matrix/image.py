# Copyright 2013 Philip N. Klein
"""
Basic types:
file - a png file on disk
image - a list of list of pixels. pixels can be triples of RGB intensities,
        or single grayscale values.
display - not a type per se, but rather causing the type to be shown on screen

Functions convert between these formats, and also can write to temporary files
and display them with a web browser.
"""

# To do: check types of arguments, check that image has no alpha channel
# Note that right now, we ignore the alpha channel, but allow it. - @dbp

import png
import numbers
import collections

# Native imports
import webbrowser
import tempfile
import os
import atexit

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
    image = [[x for x in row] for row in image]
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
