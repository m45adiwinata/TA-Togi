# -*- coding: utf-8 -*-
"""
Created on Sun May 12 21:52:39 2019

@author: Grenceng
"""

import numpy as np

def binaryImage(image):
    newImage = np.zeros((image.shape[0], image.shape[1]))
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if image[i,j] > 127:
                newImage = 255
    return newImage