# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 13:15:31 2018

@author: Grenceng
"""

import cv2 as cv
import numpy as np
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),'libraries/'))
import grayscale

test = "images/delem.jpg"
model = "images/model_delem.jpg"

img_rgb = cv.imread(test)
img_gray = grayscale.grayscaleImage(img_rgb)
template_rgb = cv.imread(model)
template = grayscale.grayscaleImage(model)
res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
w, h = template.shape[::-1]
w2 = img_rgb.shape[1]
h2 = img_rgb.shape[0]
W = max(w, w2)
H = h + h2
threshold = 0.8
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
    cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
hasil = np.zeros((H, W, 3), np.uint8)
hasil[:h,:w] = template_rgb
hasil[h:,:w2] = img_rgb
while True:
    cv.imshow('result',hasil)
    key = cv.waitKey(20)
    if key == 27:
        break
cv.destroyAllWindows()
