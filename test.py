# -*- coding: utf-8 -*-
"""
Created on Sat Feb 09 16:12:33 2019

@author: Yogi Prasetya
"""

import cv2
import numpy as np
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),'libraries/'))
import grayscale
import binary

img = cv2.imread('images/bima.jpg')
img = grayscale.grayscaleImage(img)
cv2.imwrite('grayscale.jpg', img)
thresh1 = binary.binaryImage(img)
cv2.imwrite('binary.jpg', thresh1)
#image = np.zeros((img.shape), np.uint8)
image = thresh1
image = cv2.Laplacian(image, cv2.CV_64F)
mod = cv2.imread('images/model_delem.jpg', 0)
ret,thresh2 = cv2.threshold(mod,127,255,cv2.THRESH_BINARY)
model = thresh2
model = cv2.Laplacian(model, cv2.CV_64F)
#image = cv2.Canny(image, 17, 71)
#image = cv2.Sobel(image, cv2.CV_64F, 0, 1)
#kernelx = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])
#image = cv2.filter2D(image, -1, kernelx)
#kernely = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
#image = cv2.filter2D(image, -1, kernely)
while True:
    cv2.imshow('wayang', image)
    key = cv2.waitKey(20)
    if key == 27:
        break
cv2.destroyAllWindows()
cv2.imwrite('model.jpg', model)
cv2.imwrite('image.jpg', image)
image = cv2.imread('image.jpg')
model = cv2.imread('model.jpg')
res = cv2.matchTemplate(image, model, cv2.TM_CCOEFF_NORMED)
w, h = model.shape[::-1]
w2 = image.shape[1]
h2 = image.shape[0]
W = max(w, w2)
H = h + h2
threshold = 0.8
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
    cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
hasil = np.zeros((H, W, 3), np.uint8)
hasil[:h,:w] = model
hasil[h:,:w2] = image
while True:
    cv2.imshow('result',hasil)
    key = cv2.waitKey(20)
    if key == 27:
        break
cv2.destroyAllWindows()
