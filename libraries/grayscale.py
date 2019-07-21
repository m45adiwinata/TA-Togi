# -*- coding: utf-8 -*-
"""
Created on Sun May 12 21:36:29 2019

@author: Grenceng
"""

import numpy as np

def grayscaleImage(image):
    grayImg = np.zeros((image.shape[0], image.shape[1]))
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            grayImg[i,j] = int(np.mean(image[i,j,:]))
    return grayImg
            