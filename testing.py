import cv2
import numpy as np
import os, sys
import pandas as pd
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),'libraries/'))
import grayscale
import binary

imgpath = 'Data Wayang/images/'
tmppath = 'Data Wayang/templates/'

images = [os.path.join(imgpath, fname) for fname in os.listdir(imgpath) if fname.endswith('.jpg')]
templates = [os.path.join(tmppath, fname) for fname in os.listdir(tmppath) if fname.endswith('.jpg')]
#print len(images)
#print len(templates)
deteksi_tepis = ['Laplacian', 'Canny', 'Prewitt', 'Sobel']

total_data = len(images)
for i in range(4):
    for j in range(4):
        results = []
        beneh = 0
        for src in images:
            print src
            filename = src.split('/')[-1].split('.')[0].split('_')[0]
            img = cv2.imread(src)
            img = grayscale.grayscaleImage(img)
            image = binary.binaryImage(img)
            if i == 0:
                image = cv2.Laplacian(image, cv2.CV_64F)
            elif i == 1:
                image = cv2.Canny(image, 17, 71)
            elif i == 2:
                kernelx = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])
                image = cv2.filter2D(image, -1, kernelx)
            elif i == 3:
                image = cv2.Sobel(image, cv2.CV_64F, 0, 1)
            cv2.imwrite('image.jpg', image)
            image = cv2.imread('image.jpg')
            results.append(filename)
            scores = []
            for tmpsrc in templates:
                mod = cv2.imread(tmpsrc, 0)
                ret,model = cv2.threshold(mod,127,255,cv2.THRESH_BINARY)
                if j == 0:
                    print "Lapla"
                    model = cv2.Laplacian(model, cv2.CV_64F)
                elif j == 1:
                    print "Canny"
                    model = cv2.Canny(model, 17, 71)
                elif j == 2:
                    print "Prewitt"
                    kernelx = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])
                    model = cv2.filter2D(model, -1, kernelx)
                elif j == 3:
                    print "Sobel"
                    model = cv2.Sobel(model, cv2.CV_64F, 0, 1)
                cv2.imwrite('model.jpg', model)
                model = cv2.imread('model.jpg')
                res = cv2.matchTemplate(image, model, cv2.TM_CCOEFF_NORMED)
                scores.append(np.max(res))
        #    print np.max(scores)
            winner = templates[np.argmax(scores)]
            winner = winner.split('/')[-1].split('.')[0].split('_')[0]
            results.append(winner)
            if filename == winner:
                results.append('Benar')
                beneh += 1
            else:
                results.append('Salah')
            print winner
            
        results.append('')
        results.append('Akurasi')
        results.append(beneh/float(total_data))
        results = np.array(results)
        results = np.reshape(results, (len(images)+1,-1))
        df = pd.DataFrame(results)
        h = ['Input', 'Output', 'Result']
        excel_name = 'hasil testing', deteksi_tepis[i],'_', deteksi_tepis[j],'.xlsx'
        df.to_excel(''.join(excel_name), index=False, header=h)
