from image import color2gray, file2image
import os
   
def load_images(path, n = 20):
    '''
    Input:
        - path: path to directory containing img*.png
        - n: number of images to load
    Output:
        - dict mapping numbers 0 to (n-1) to a list of rows,
          each of which is a list of pixel brightnesses
    '''
    return {i:color2gray(file2image(os.path.join(path,"img%02d.png" % i))) for i in range(n)}

from mat import *
from math import sqrt
M_f = {(0,0):1/sqrt(2) , (1,0):1/sqrt(2) , (0,1):1/sqrt(3), (1,1):-1/sqrt(3), (2,1):1/sqrt(3)}
test_M = Mat(({0,1,2},{0,1}), M_f)
test_x = Vec({0,1,2}, {0:10,1:20,2:30})
