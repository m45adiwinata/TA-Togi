# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 17:00:06 2019

@author: Yogi Prasetya
"""

from Tkinter import *
import ttk, tkMessageBox as messagebox, os, glob, tkFileDialog
from PIL import Image, ImageTk
import numpy as np
import cv2
import os,sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),'libraries/'))
import grayscale
import binary
'''
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
'''

tmppath = 'Data Wayang/templates/'
templates = [os.path.join(tmppath, fname) for fname in os.listdir(tmppath) if fname.endswith('.jpg')]

root = Tk()

class Main():
    def __init__(self, master, title):
        self.master = master
        self.master.title(title)
        self.master.config(background="#0ad6b4")
        self.createMenu()
        self.komponenMain()
        
    def createMenu(self):
        menubar = Menu(self.master)
        self.master.config(menu=menubar)
        fileMenu = Menu(menubar)
        menubar.add_cascade(label="Input Fitur Data", menu=fileMenu)
        
    def komponenMain(self):
        framePhoto = Frame(self.master, bg="#0ad6b4")
        framePhoto.grid(row=0, padx=10, pady=10)
        self.image_empty = Image.open("empty.png")
        self.image_empty = ImageTk.PhotoImage(self.image_empty)
        self.photoIn = Label(framePhoto, bg="#ffffff", image=self.image_empty, width="400", height="600")
        self.photoIn.grid(row=0)
        self.photoIn.image = self.image_empty
        frame = Frame(self.master, bg="#0ad6b4")
        frame.grid(row=1, sticky=N, padx=10, pady=10)
        btn_browse = Button(frame, bg="#ffffff", width="35", height="2", text="Browse Photo",
                            command=self.browse)
        btn_browse.grid(row=0, sticky=W, columnspan=2, padx=5, pady=5)
        frameKanan = Frame(self.master, bg="#4286f4")
        frameKanan.grid(row=0, column=1, padx=10, pady=10)
        frameTombolPrepro = Frame(frameKanan, bg="#833338")
        frameTombolPrepro.grid(row=0, column=0, padx=10, pady=10)
        labelPrepro = Label(frameKanan, text="Pilih Preprocessing", font="12", bg="#4286f4")
        labelPrepro.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.tombolLaplacian = Button(frameKanan, bg="#338833", width="25", height="2", text="Laplacian", command=lambda:self.laplacian(self.img))
        self.tombolLaplacian.grid(row=1, column=0, padx=5, pady=5)
        self.tombolCanny = Button(frameKanan, bg="#338833", width="25", height="2", text="Canny", command=lambda:self.canny(self.img))
        self.tombolCanny.grid(row=1, column=1, padx=5, pady=5)
        self.tombolSobel = Button(frameKanan, bg="#338833", width="25", height="2", text="Sobel", command=lambda:self.sobel(self.img))
        self.tombolSobel.grid(row=2, column=0, padx=5, pady=5)
        self.tombolPrewitt = Button(frameKanan, bg="#338833", width="25", height="2", text="Prewitt", command=lambda:self.prewitt(self.img))
        self.tombolPrewitt.grid(row=2, column=1, padx=5, pady=5)
        frameKananBawah = Frame(self.master, bg="#4286f4")
        frameKananBawah.grid(row=1, column=1, padx=10, pady=10)
        self.tombolKlasifikasi = Button(frameKananBawah, bg="#833338", width="25", height="2", text="Klasifikasi", command=self.klasifikasi)
        self.tombolKlasifikasi.grid(row=0, column=0, padx=5, pady=5)
        self.labelTerdeteksiSbg = Label(frameKananBawah, bg="#4286f4", font="10", text="")
        self.labelTerdeteksiSbg.grid(row=1, column=0, padx=5, pady=5)
        
    def browse(self):
        self.path = tkFileDialog.askopenfilename()
        self.ambilImg()
        self.imgShow(self.img)
        self.choosenPrepro = ""

    def imgShow(self, image):
        image_show = Image.fromarray(image)
        image_show = ImageTk.PhotoImage(image_show)
        self.photoIn.config(image=image_show, width="400", height="600")
        self.photoIn.image = image_show
        
    def ambilImg(self):
        if (len(self.path) > 0):
            self.img = self.read_img(self.path)
            self.imgPro = cv2.imread(self.path)
            self.imgPro = grayscale.grayscaleImage(self.imgPro)
            w = 400
            h = 600
            self.img = cv2.resize(self.img, (w, h))
            self.imgPro = cv2.resize(self.imgPro, (w, h))
            self.convertRGB()

    def saveImg(self, title, img):
        cv2.imwrite(title, img)
    
    def convertRGB(self):
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        self.r, self.g, self.b = cv2.split(self.img)
        self.r2 = self.r
        self.g2 = self.g
        self.b2 = self.b
      
    def read_img(self, filepath):
        return cv2.imread(filepath)
    
    def threshold(self, img):
        #ret,thresh = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
        thresh = binary.binaryImage(img)
        return thresh

    def klikTombol(self, tombol):
        self.tombolLaplacian.config(bg="#338833")
        self.tombolCanny.config(bg="#338833")
        self.tombolPrewitt.config(bg="#338833")
        self.tombolSobel.config(bg="#338833")
        tombol.config(bg="#FEFEFE")
    
    def laplacian(self, img):
        img = self.threshold(self.imgPro)
        self.imgPrepro = cv2.Laplacian(img, cv2.CV_64F)
        print self.imgPrepro.shape
        self.saveImg('Laplacian.jpg', self.imgPrepro)
        self.imgShow(self.imgPrepro)
        self.klikTombol(self.tombolLaplacian)
        self.choosenPrepro = "Laplacian"
    
    def canny(self, img):
        img = self.threshold(self.imgPro)
        self.imgPrepro = cv2.Canny(img, 17, 71)
        print self.imgPrepro.shape
        self.saveImg('Canny.jpg', self.imgPrepro)
        self.imgShow(self.imgPrepro)
        self.klikTombol(self.tombolCanny)
        self.choosenPrepro = "Canny"
    
    def sobel(self, img):
        img = self.threshold(self.imgPro)
        self.imgPrepro = cv2.Sobel(img, cv2.CV_64F, 0, 1)
        print self.imgPrepro.shape
        self.saveImg('Sobel.jpg', self.imgPrepro)
        self.imgShow(self.imgPrepro)
        self.klikTombol(self.tombolSobel)
        self.choosenPrepro = "Sobel"

    def prewitt(self, img):
        img = self.threshold(self.imgPro)
        kernelx = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])
        self.imgPrepro = cv2.filter2D(img, -1, kernelx)
        print self.imgPrepro.shape
        self.saveImg('Prewitt.jpg', self.imgPrepro)
        self.imgShow(self.imgPrepro)
        self.klikTombol(self.tombolPrewitt)
        self.choosenPrepro = "Prewitt"

    def klasifikasi(self):
        if self.choosenPrepro == "":
            return "Preproccessing dulu brots!"
        cv2.imwrite('imgPreproccessed.jpg', self.imgPrepro)
        imgInput = cv2.imread('imgPreproccessed.jpg')
        scores = []
        for template in templates:
            img = cv2.imread(template, 0)
            self.setTemplatePrepro(self.choosenPrepro, img)
            model = cv2.imread('model.jpg')
            res = cv2.matchTemplate(imgInput, model, cv2.TM_CCOEFF_NORMED)
            scores.append(np.max(res))
        winner = templates[np.argmax(scores)]
        winner = winner.split('/')[-1].split('.')[0].split('_')[0]
        self.labelTerdeteksiSbg.config(text = "Karakter %s" % winner)

    def setTemplatePrepro(self, choosen, img):
        img = self.threshold(img)
        if choosen == "Laplacian":
            img = cv2.Laplacian(img, cv2.CV_64F)
            cv2.imwrite('model.jpg', img)
        elif choosen == "Canny":
            img = cv2.Canny(img, 17, 71)
            cv2.imwrite('model.jpg', img)
        elif choosen == "Sobel":
            img = cv2.Sobel(img, cv2.CV_64F, 0, 1)
            cv2.imwrite('model.jpg', img)
        elif choosen == "Prewitt":
            kernelx = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])
            img = cv2.filter2D(img, -1, kernelx)
            cv2.imwrite('model.jpg', img)
    
Main(root, "== Klasifikasi Wayang ==")
root.mainloop()
