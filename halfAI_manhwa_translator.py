from PIL import Image, ImageFont, ImageDraw 
import math
from itertools import count
from random import randint
import pytesseract
from datetime import datetime
import os
from os import path
import numpy
import matplotlib
import matplotlib.pyplot as plt
import deepl
import textwrap
from string import ascii_letters
from screeninfo import get_monitors
monitor_w= int(str(get_monitors()[0])[+8:-1].split(", ")[2].replace("width=",""))
monitor_h= int(str(get_monitors()[0])[+8:-1].split(", ")[3].replace("height=",""))
import sys
import os
patxh=__file__
dir=os.path.dirname(patxh)
pytesseract.pytesseract.tesseract_cmd = dir+r"\Tesseract-OCR\tesseract"
from pytesseract import Output
now = datetime.now()
#functions
def transformattion(array,im_width):
    import math
    pt=[]
    for i in range(len(array)):
        if i%im_width==0:
            pt.append(list())
            pt[math.floor(i/im_width)].append(array[i])
        else:
            pt[math.floor(i/im_width)].append(array[i])
    return list(pt)
def firstandsec_axist(fcordinate_arr=[0, 0],scordinate_arr=[0, 0]):
    if fcordinate_arr[0]>scordinate_arr[0] and fcordinate_arr[1]>scordinate_arr[1]:
        return scordinate_arr, fcordinate_arr
    elif fcordinate_arr[0]<scordinate_arr[0] and fcordinate_arr[1]>scordinate_arr[1]:
        return [fcordinate_arr[0], scordinate_arr[1]], [scordinate_arr[0], fcordinate_arr[1]]
    elif fcordinate_arr[0]>scordinate_arr[0] and fcordinate_arr[1]<scordinate_arr[1]:
        return [scordinate_arr[0], fcordinate_arr[1]], [fcordinate_arr[0], scordinate_arr[1]]
    else:
        return fcordinate_arr, scordinate_arr
def get_dblist_from_dbarr(dbarr=[],fcords=[0, 0],scords=[0, 0]):
    h=scords[0]-fcords[0]+1
    ret = []
    for i in range(len(dbarr)):
        for t in range(len(dbarr[i])):
            if t>=fcords[0] and t<=scords[0] and i>=fcords[1] and i<=scords[1]:
                ret.append(dbarr[i][t])
    return transformattion(ret,h)
def re_transformattion(arr=[]):
    randim_image = numpy.array(arr, dtype=numpy.uint8)
    im = Image.fromarray(randim_image)
    return im
def merge_textlines(text_lines=[]):
    all_merge=""
    for g in range(len(text_lines)):
        if text_lines[g]!="":
            if text_lines[g][+len(text_lines[g])-1:]=="-":
                all_merge+=text_lines[g][:-1]
            else:
                all_merge+=text_lines[g]+" "
    return all_merge[:-1]
def text_lines(multiline_text=str):
    if multiline_text.count('\n')==0:
        return 1
    return int(multiline_text.count('\n'))
def line_break(line_num=int,string=str):
    lenght=round(len(string)/line_num+12/line_num+3)
    return textwrap.fill(text=string, width=lenght)
def value_within(num=int, val1=int, val2=0):
    if num>val1:
        return val1
    elif num<val2:
        return val2
    else: return num
def cleaner(image):
    hgf=""
    global lang1
    p_arr = pytesseract.image_to_boxes(image, lang=lang1).split("\n")
    pixels=transformattion(list(image.getdata()), image.size[0])
    h=0
    for i in range(len(p_arr)):
        p_arr[i+h]=p_arr[i+h].split(" ")
        del p_arr[i+h][0]
        if len(p_arr[i+h])==5:
            del p_arr[i+h][4]
            j=int(p_arr[i+h][1])
            p_arr[i+h][0]=int(p_arr[i+h][0])-6
            p_arr[i+h][1]=image.size[1]-int(p_arr[i+h][3])-3
            p_arr[i+h][2]=int(p_arr[i+h][2])+3
            p_arr[i+h][3]=image.size[1]-j+3
        else: 
            del p_arr[i+h]
            h+=1
    for t in range(len(p_arr)):
        for d in range(len(pixels)):
            for q in range(len(pixels[d])):
                col=pixels[d][value_within(q-5, image.size[0]-1)]  
                if q>=p_arr[t][0] and q<=p_arr[t][2] and d>=p_arr[t][1] and d<=p_arr[t][3]:
                    pixels[d][q]=col
                    if hgf == "":
                        hgf=pixels[d][value_within(q-8, image.size[0]-1)]   
    return re_transformattion(pixels), pixels, hgf
def blackwhite_opposite_col(r, g=-1, b=-1):
    if g==-1 and b==-1:
        g=int(r[1])
        b=int(r[2])
        r=int(r[0])
    if (r>=128 and b>=128) or (r>=128 and g>=128) or (g>=128 and b>=128):
        return [(0, 0, 0), (255, 255, 255)]
    else:
        return [(255, 255, 255), (0, 0, 0)]
def zero_adder(word,len_add=7):
    word2=word
    if word.find(".")!=-1:
        word2=word[:-(len(word)-word.find("."))]
    o=""
    for i in range(len_add-len(word2)):
        o=o+str(0)
    return str(o+word)
def negative(img=Image):
    arr = transformattion(list(img.getdata()),img.size[0])
    for i in range(len(arr)):
        for t in range(len(arr[i])):
            arr[i][t]=blackwhite_opposite_col(arr[i][t])[0]
    return re_transformattion(arr)
def img_crop(img=Image,cropped_size=int,overlap=0):
    global ret_cords
    global ret_overlap
    arr = transformattion(list(img.getdata()),img.size[0])
    ret_arr=[]
    ret_cords=[]
    ret_overlap=[]
    b=[]
    for i in range(len(arr)):
        b.append(arr[i])
        if i%cropped_size==0 and i!=0:
            ret_cords.append(i-overlap)
        elif i%cropped_size==0:
            ret_cords.append(i)
        if (i%cropped_size==0 or (i==len(arr)-1 and i%cropped_size!=0)) and i!=0:
            ret_arr.append(re_transformattion(b))
            for t in range(len(b)-overlap):
                del b[0]
    return ret_arr
def move_figure(f, x, y):
    """Move figure's upper left corner to pixel (x, y)"""
    backend = matplotlib.get_backend()
    if backend == 'TkAgg':
        f.canvas.manager.window.wm_geometry("+%d+%d" % (x, y))
    elif backend == 'WXAgg':
        f.canvas.manager.window.SetPosition((x, y))
    else:
        f.canvas.manager.window.move(x, y)
def img_rotateandsqueeze(img=Image, angle=int):
    rot_img=img.rotate(-90+angle, expand=True, fillcolor=(255, 3, 200))
    arr=transformattion(list(rot_img.getdata()),rot_img.size[0])
    for i in range(len(arr)):
        k=0
        while k<rot_img.size[0]/2 and arr[i][k]==(255, 3, 200):
            del arr[i][k]
            arr[i].append((250,250,250))
        else:
            for j in range(len(arr[i])):
                if arr[i][j]==(255, 3, 200):
                    arr[i][j]=(250, 250,250)
    return re_transformattion(arr).rotate(90, expand=True)
#############
#app 
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import *
from matplotlib.figure import Figure
from matplotlib.widgets import Button
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMovie
import pyqtgraph as pg
def loading_animation():
    window1.label_animation2.setGeometry(0,0, 800,900)
    window1.label_animation.setGeometry(225,175, 350,350)
    window1.load_dats.setGeometry(0, 550, 800, 50)
    window1.movie.start()

def stopAnimation():
    window1.label_animation2.setGeometry(0,0, 0,0)
    window1.label_animation.setGeometry(0,0, 0,0)
    window1.load_dats.setGeometry(0, 0, 0, 0)
    window1.movie.stop()
def print_load(txt:str):
    window1.load_dats.setText(txt)
    
        
lang1 = "eng"
lang2 = "hu"
class window1(QMainWindow) :
    def __init__(self):
        super(window1, self).__init__()
        self.setGeometry(100, 100, 800, 900)
        self.setFixedWidth(800)
        self.setFixedHeight(900)
        self.setStyleSheet("background-color: rgb(38, 38, 38)")
        self.setWindowTitle("Half AI Comic Translator")
        self.setWindowIcon(QIcon(dir+r"\files\comic_icon.png"))
        self.setToolTip("")
        self.initUI()
        window1.label_animation2 = QLabel(self)
        window1.label_animation2.setGeometry(0,0, 0,0)
        window1.load_dats = QLabel(self)
        window1.load_dats.setFont(QFont('Franklin Gothic Demi Cond', 15))
        window1.load_dats.setGeometry(0, 0, 0, 0)
        window1.load_dats.setStyleSheet("color: rgb(27, 171, 255)")
        window1.load_dats.setAlignment(QtCore.Qt.AlignCenter)
        window1.load_dats.setText("")
        window1.label_animation = QLabel(self)
        window1.label_animation.setGeometry(0,0, 0,0)
        window1.label_animation.setAlignment(QtCore.Qt.AlignCenter)
        window1.movie = QMovie(dir+r"\files\loading.gif")
        window1.label_animation.setMovie(window1.movie)
        

    def initUI(self):
        self.lbl_appname = QtWidgets.QLabel(self)
        self.lbl_appname.setFont(QFont('Franklin Gothic Demi Cond', 30))
        self.lbl_appname.setGeometry(0, 5, 800, 55)
        self.lbl_appname.setStyleSheet("color: rgb(27, 171, 255)")
        self.lbl_appname.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_appname.setText('Comic Translator')
        
        self.lbl = QtWidgets.QLabel(self)
        self.lbl.setFont(QFont('Franklin Gothic Demi Cond', 16))
        self.lbl.setGeometry(10, 480, 780, 420)
        self.lbl.setStyleSheet("color: rgb(27, 171, 255);padding:0;margin:0;")
        self.lbl.setAlignment(QtCore.Qt.AlignLeft)
        self.lbl.setText('\n*: Or leave it blank and translate it yourself.\n\n\
In the image, double-left-click the selection \nin one corner, then duplicate it in the other corner.\n\n\
Default placement is center, press j to align left. \
Press i for italic font.\n\
Press 2 for the second font. \
Press 3 for the third font.\n\
Press 4 for the fourth font. \
Press 5 for the fifth font.\n\
Press b for bold font. \
Press z for gray font color.')
        
        self.input1 = QtWidgets.QLineEdit(self,placeholderText='Select chapter path...',)
        self.input1.setStyleSheet("color: rgb(27, 171, 255); background-color: rgb(30, 30, 30); outline:none;padding-right:120px; padding-left:5px;border: 2px solid rgb(27, 171, 255);border-radius:10px;font-weight:600;")
        self.input1.setGeometry(10, 70, 380,71)
        self.input1.setFixedHeight(60)
        
        self.browsebtn1 = QtWidgets.QPushButton(self)
        self.browsebtn1.setStyleSheet("color: rgb(27, 171, 255)")
        self.browsebtn1.setText('Browse')
        self.browsebtn1.clicked.connect(self.getdir1)
        self.browsebtn1.setGeometry(275, 80, 105,81)
        self.browsebtn1.setFixedHeight(40)
        
        open(dir+r"\basicfont.txt", "a")
        f = open(dir+r"\basicfont.txt", "r", encoding='utf-8')
        j=str(f.read())
        if j!="":
            self.input2 = QtWidgets.QLineEdit(j,self,placeholderText='Select basic font...',)
        else:
            self.input2 = QtWidgets.QLineEdit(self,placeholderText='Select basic font...',)
        self.input2.setStyleSheet("color: rgb(27, 171, 255); background-color: rgb(30, 30, 30); outline:none;padding-right:120px; padding-left:5px;border: 2px solid rgb(27, 171, 255);border-radius:10px;font-weight:600;")
        self.input2.setGeometry(410, 70, 380,71)
        self.input2.setFixedHeight(60)
        
        self.browsebtn2 = QtWidgets.QPushButton(self)
        self.browsebtn2.setStyleSheet("color: rgb(27, 171, 255)")
        self.browsebtn2.setText('Browse')
        self.browsebtn2.clicked.connect(self.basicfont)
        self.browsebtn2.setGeometry(675, 80, 105,81)
        self.browsebtn2.setFixedHeight(40)
        
        open(dir+r"\italicfont.txt", "a")
        f = open(dir+r"\italicfont.txt", "r", encoding='utf-8')
        j=str(f.read())
        if j!="":
            self.input3 = QtWidgets.QLineEdit(j,self,placeholderText='Select italic font...',)
        else:
            self.input3 = QtWidgets.QLineEdit(self,placeholderText='Select italic font...',)
        self.input3.setStyleSheet("color: rgb(27, 171, 255); background-color: rgb(30, 30, 30); outline:none;padding-right:120px; padding-left:5px;border: 2px solid rgb(27, 171, 255);border-radius:10px;font-weight:600;")
        self.input3.setGeometry(10, 150, 380,71)
        self.input3.setFixedHeight(60)
        
        self.browsebtn3 = QtWidgets.QPushButton(self)
        self.browsebtn3.setStyleSheet("color: rgb(27, 171, 255)")
        self.browsebtn3.setText('Browse')
        self.browsebtn3.clicked.connect(self.italicfont)
        self.browsebtn3.setGeometry(275, 160, 105,81)
        self.browsebtn3.setFixedHeight(40)
        
        open(dir+r"\secfont.txt", "a")
        f = open(dir+r"\secfont.txt", "r", encoding='utf-8')
        j=str(f.read())
        if j!="":
            self.input4 = QtWidgets.QLineEdit(j,self,placeholderText='Select second font...',)
        else:
            self.input4 = QtWidgets.QLineEdit(self,placeholderText='Select second font...',)
        self.input4.setStyleSheet("color: rgb(27, 171, 255); background-color: rgb(30, 30, 30); outline:none;padding-right:120px; padding-left:5px;border: 2px solid rgb(27, 171, 255);border-radius:10px;font-weight:600;")
        self.input4.setGeometry(410, 150, 380,71)
        self.input4.setFixedHeight(60)
        
        self.browsebtn4 = QtWidgets.QPushButton(self)
        self.browsebtn4.setStyleSheet("color: rgb(27, 171, 255)")
        self.browsebtn4.setText('Browse')
        self.browsebtn4.clicked.connect(self.secondfont)
        self.browsebtn4.setGeometry(675, 160, 105,81)
        self.browsebtn4.setFixedHeight(40)
        
        open(dir+r"\thirdfont.txt", "a")
        f = open(dir+r"\thirdfont.txt", "r", encoding='utf-8')
        j=str(f.read())
        if j!="":
            self.input5 = QtWidgets.QLineEdit(j,self,placeholderText='Select third font...',)
        else:
            self.input5 = QtWidgets.QLineEdit(self,placeholderText='Select third font...',)
        self.input5.setStyleSheet("color: rgb(27, 171, 255); background-color: rgb(30, 30, 30); outline:none;padding-right:120px; padding-left:5px;border: 2px solid rgb(27, 171, 255);border-radius:10px;font-weight:600;")
        self.input5.setGeometry(10, 230, 380,71)
        self.input5.setFixedHeight(60)
        
        self.browsebtn5 = QtWidgets.QPushButton(self)
        self.browsebtn5.setStyleSheet("color: rgb(27, 171, 255)")
        self.browsebtn5.setText('Browse')
        self.browsebtn5.clicked.connect(self.thirdfont)
        self.browsebtn5.setGeometry(275, 240, 105,81)
        self.browsebtn5.setFixedHeight(40)
        
        open(dir+r"\fourthfont.txt", "a")
        f = open(dir+r"\fourthfont.txt", "r", encoding='utf-8')
        j=str(f.read())
        if j!="":
            self.input6 = QtWidgets.QLineEdit(j,self,placeholderText='Select fourth font...',)
        else:
            self.input6 = QtWidgets.QLineEdit(self,placeholderText='Select fourth font...',)
        self.input6.setStyleSheet("color: rgb(27, 171, 255); background-color: rgb(30, 30, 30); outline:none;padding-right:120px; padding-left:5px;border: 2px solid rgb(27, 171, 255);border-radius:10px;font-weight:600;")
        self.input6.setGeometry(410, 230, 380,71)
        self.input6.setFixedHeight(60)
        
        self.browsebtn6 = QtWidgets.QPushButton(self)
        self.browsebtn6.setStyleSheet("color: rgb(27, 171, 255)")
        self.browsebtn6.setText('Browse')
        self.browsebtn6.clicked.connect(self.fourthfont)
        self.browsebtn6.setGeometry(675, 240, 105,81)
        self.browsebtn6.setFixedHeight(40)
        
        open(dir+r"\fifthfont.txt", "a")
        f = open(dir+r"\fifthfont.txt", "r", encoding='utf-8')
        j=str(f.read())
        if j!="":
            self.input7 = QtWidgets.QLineEdit(j,self,placeholderText='Select fifth font...',)
        else:
            self.input7 = QtWidgets.QLineEdit(self,placeholderText='Select fifth font...',)
        self.input7.setStyleSheet("color: rgb(27, 171, 255); background-color: rgb(30, 30, 30); outline:none;padding-right:120px; padding-left:5px;border: 2px solid rgb(27, 171, 255);border-radius:10px;font-weight:600;")
        self.input7.setGeometry(10, 310, 380,71)
        self.input7.setFixedHeight(60)
        
        self.browsebtn7 = QtWidgets.QPushButton(self)
        self.browsebtn7.setStyleSheet("color: rgb(27, 171, 255)")
        self.browsebtn7.setText('Browse')
        self.browsebtn7.clicked.connect(self.fifthfont)
        self.browsebtn7.setGeometry(275, 320, 105,1)
        self.browsebtn7.setFixedHeight(40)
        
        open(dir+r"\deeplkey.txt", "a")
        f = open(dir+r"\deeplkey.txt", "r", encoding='utf-8')
        j=str(f.read())
        if j!="":
            self.input8 = QtWidgets.QLineEdit(j,self,placeholderText='Enter the DeepL auth key... *',)
        else:
            self.input8 = QtWidgets.QLineEdit(self,placeholderText='Enter the DeepL auth key... *',)
        self.input8.setStyleSheet("color: rgb(27, 171, 255); background-color: rgb(30, 30, 30); outline:none;padding-right:5px; padding-left:5px;border: 2px solid rgb(27, 171, 255);border-radius:10px;font-weight:600;")
        self.input8.setGeometry(410, 310, 380,71)
        self.input8.setFixedHeight(60)
        
        self.starter = QtWidgets.QPushButton(self)
        self.starter.setStyleSheet("background-color: rgb(27, 171, 255); border-radius:10px;color: rgb(30, 30, 30);font-size:30px; font-weight:600;")
        self.starter.setText('Start')
        self.starter.clicked.connect(self.start)
        self.starter.setGeometry(10, 400, 780,1)
        self.starter.setFixedHeight(60)
        
        
        
        
    def getdir1(self):
        dir = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.input1.setText(dir) 
    def basicfont(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Single File', QtCore.QDir.rootPath() , '*.ttf;*.otf;*.cff')
        self.input2.setText(file)
    def italicfont(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Single File', QtCore.QDir.rootPath() , '*.ttf;*.otf;*.cff')
        self.input3.setText(file)
    def secondfont(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Single File', QtCore.QDir.rootPath() , '*.ttf;*.otf;*.cff')
        self.input4.setText(file)
    def thirdfont(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Single File', QtCore.QDir.rootPath() , '*.ttf;*.otf;*.cff')
        self.input5.setText(file)
    def fourthfont(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Single File', QtCore.QDir.rootPath() , '*.ttf;*.otf;*.cff')
        self.input6.setText(file)
    def fifthfont(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Single File', QtCore.QDir.rootPath() , '*.ttf;*.otf;*.cff')
        self.input7.setText(file)
    def start(self):
        f=open(dir+r"\basicfont.txt", "w", encoding='utf-8')
        f.write(str(self.input2.text()))
        f=open(dir+r"\italicfont.txt", "w", encoding='utf-8')
        f.write(str(self.input3.text()))
        f=open(dir+r"\secfont.txt", "w", encoding='utf-8')
        f.write(str(self.input4.text()))
        f=open(dir+r"\thirdfont.txt", "w", encoding='utf-8')
        f.write(str(self.input5.text()))
        f=open(dir+r"\fourthfont.txt", "w", encoding='utf-8')
        f.write(str(self.input6.text()))
        f=open(dir+r"\fifthfont.txt", "w", encoding='utf-8')
        f.write(str(self.input7.text()))
        f=open(dir+r"\deeplkey.txt", "w", encoding='utf-8')
        f.write(str(self.input8.text()))
        global auth_key
        auth_key= str(self.input8.text())
        if auth_key=="":
            auth_key="none"
        global pathg
        pathg=str(self.input1.text())
        global fifth_font
        fifth_font=str(self.input7.text())
        global fourth_font
        fourth_font=str(self.input6.text())
        global third_font
        third_font=str(self.input5.text())
        global sec_font
        sec_font=str(self.input4.text())
        global normal_font
        normal_font=str(self.input2.text())
        global italic_font
        italic_font=str(self.input3.text())
        if str(self.input1.text())!="" and str(self.input2.text())!="" and str(self.input8.text())!="": 
            global SW
            window1.SW = LangSelect()
            SW=window1.SW
            window1.SW.show()
        elif str(self.input1.text())!="" and str(self.input2.text())!="":
            window1.input = input_win()
            window1.input.show()
            
    def closeEvent(self, event):
        SW.hide()
        window1.SW.hide()
        

class LangSelect(QMainWindow):

    def __init__(self):
        super(LangSelect,self).__init__()
        self.setStyleSheet("background-color: rgb(38, 38, 38)")
        self.setWindowTitle("Select lang")
        self.setWindowIcon(QIcon(dir+r"\files\comic_icon.png"))
        self.setToolTip("Close the window to save.")
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setFocus()
        self.resize(200,100)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.combobox = QComboBox()
        f = open(dir+r"\files\lang2.txt", "r", encoding='utf-8')
        j=str(f.read())
        if j!="":
            self.combobox.addItems([j,"bg", "cs", "da", "de", "el", "es", "et", "fi", "fr", "hu", "id", "it", "ja", "lt", "lv", "nl", "pl", "pt", "pt-BR", "pt-PT", "ro", "ru", "sk", "sl", "sv", "tr", "uk", "zh"])
        else:   
            self.combobox.addItems(["bg", "cs", "da", "de", "el", "es", "et", "fi", "fr", "hu", "id", "it", "ja", "lt", "lv", "nl", "pl", "pt", "pt-BR", "pt-PT", "ro", "ru", "sk", "sl", "sv", "tr", "uk", "zh"])
        self.combobox.setStyleSheet("color: rgb(27, 171, 255)")
        self.combobox2 = QComboBox()
        f = open(dir+r"\files\lang1.txt", "r", encoding='utf-8')
        j=str(f.read())
        if j!="":
            self.combobox2.addItems([j,"eng", "kor", "chi_sim", "chi_tra", "jpn"])
        else:
            self.combobox2.addItems(["eng", "kor", "chi_sim", "chi_tra", "jpn"])
        self.combobox2.setStyleSheet("color: rgb(27, 171, 255)")

        layout = QVBoxLayout()
        layout.addWidget(self.combobox2)
        layout.addWidget(self.combobox)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
       
    def closeEvent(self, event):
        self.hide()
        global lang1,lang2
        lang1 = str(self.combobox2.currentText())
        lang2 = str(self.combobox.currentText())
        f=open(dir+r"\files\lang1.txt", "w", encoding='utf-8')
        f.write(lang1)
        f=open(dir+r"\files\lang2.txt", "w", encoding='utf-8')
        f.write(lang2)
        global SW
        window1.SW = SecWindow()
        SW=window1.SW
        window1.SW.show()
        window1.SW.showMaximized()         
        
class SecWindow(QMainWindow):
        
    def __init__(self, *args, **kwargs):
        super(SecWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Styling")
        self.setGeometry(int(monitor_w/2), 10, int(monitor_w/2), int(monitor_h/2))
        self.setWindowIcon(QIcon(dir+r"\files\comic_icon.png"))
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setFocus()
        
        global layout
        layout = QtWidgets.QVBoxLayout()
        sc = MplCanvas(width = 300, height = 300)
        
        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        global toolbar
        toolbar = NavigationToolbar2QT(sc, self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)

        # Create a placeholder widget to hold our toolbar and canvas.
        global widget
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
    def keyPressEvent(self, event):
        key=int(event.key())
        if (key==77 or key==74) and cordinates[len(cordinates)-1]!=[]:
            if len(cordinates[len(cordinates)-1])>=2 and len(cordinates[len(cordinates)-1])<=7:
                cordinates[len(cordinates)-1].append(str(key)+",")
                if key==74 and cordinates[len(cordinates)-1]!=[]:
                    x1, y1 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][0][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                    x2, y2 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number]]
                    x3, y3 = [cordinates[len(cordinates)-1][1][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                    x4, y4 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                    canv.axes.plot(x1, y1, x2, y2, color="lightgreen")
                    canv.axes.plot(x3, y3, x4, y4, color="lightgreen")
                    canv.draw()
        if key==66 and cordinates[len(cordinates)-1]!=[]:
            if len(cordinates[len(cordinates)-1])>=2 and len(cordinates[len(cordinates)-1])<=7:
                cordinates[len(cordinates)-1].append(str(key)+",")
                x1, y1 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][0][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                x2, y2 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number]]
                x3, y3 = [cordinates[len(cordinates)-1][1][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                x4, y4 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                canv.axes.plot(x1, y1, x2, y2, color="orange", linestyle='dashed')
                canv.axes.plot(x3, y3, x4, y4, color="orange", linestyle='dashed')
                canv.draw()
        if key==90 and cordinates[len(cordinates)-1]!=[]:
            if len(cordinates[len(cordinates)-1])>=2 and len(cordinates[len(cordinates)-1])<=7:
                cordinates[len(cordinates)-1].append(str(key)+",")
                x1, y1 = [cordinates[len(cordinates)-1][0][0]-1, cordinates[len(cordinates)-1][0][0]-1], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number]+1, cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]+1]
                x2, y2 = [cordinates[len(cordinates)-1][0][0]-1, cordinates[len(cordinates)-1][1][0]-1], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number]+1, cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number]+1]
                x3, y3 = [cordinates[len(cordinates)-1][1][0]-1, cordinates[len(cordinates)-1][1][0]-1], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number]+1, cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]+1]
                x4, y4 = [cordinates[len(cordinates)-1][0][0]-1, cordinates[len(cordinates)-1][1][0]-1], [cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]+1, cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]+1]
                canv.axes.plot(x1, y1, x2, y2, color="gray")
                canv.axes.plot(x3, y3, x4, y4, color="gray")
                canv.draw()
        if key==73 and cordinates[len(cordinates)-1]!=[]:
            if len(cordinates[len(cordinates)-1])>=2 and len(cordinates[len(cordinates)-1])<=7:
                cordinates[len(cordinates)-1].append(str(key)+",")
                x1, y1 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][0][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                x2, y2 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number]]
                x3, y3 = [cordinates[len(cordinates)-1][1][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                x4, y4 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                canv.axes.plot(x1, y1, x2, y2, color="white", dashes=[1, 1, 1, 1])
                canv.axes.plot(x3, y3, x4, y4, color="white", dashes=[1, 1, 1, 1])
                canv.draw()
        if key==50 and cordinates[len(cordinates)-1]!=[]:
            if len(cordinates[len(cordinates)-1])>=2 and len(cordinates[len(cordinates)-1])<=7:
                cordinates[len(cordinates)-1].append(str(key)+",")
                x1, y1 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][0][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                x2, y2 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number]]
                x3, y3 = [cordinates[len(cordinates)-1][1][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                x4, y4 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                canv.axes.plot(x1, y1, x2, y2, color="yellow")
                canv.axes.plot(x3, y3, x4, y4, color="yellow")
                canv.draw()
        if key==51 and cordinates[len(cordinates)-1]!=[]:
            if len(cordinates[len(cordinates)-1])>=2 and len(cordinates[len(cordinates)-1])<=7:
                cordinates[len(cordinates)-1].append(str(key)+",")
                x1, y1 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][0][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                x2, y2 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number]]
                x3, y3 = [cordinates[len(cordinates)-1][1][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                x4, y4 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                canv.axes.plot(x1, y1, x2, y2, color="red")
                canv.axes.plot(x3, y3, x4, y4, color="red")
                canv.draw()
        if key==52 and cordinates[len(cordinates)-1]!=[]:
            if len(cordinates[len(cordinates)-1])>=2 and len(cordinates[len(cordinates)-1])<=7:
                cordinates[len(cordinates)-1].append(str(key)+",")
                x1, y1 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][0][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                x2, y2 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number]]
                x3, y3 = [cordinates[len(cordinates)-1][1][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                x4, y4 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                canv.axes.plot(x1, y1, x2, y2, color="purple")
                canv.axes.plot(x3, y3, x4, y4, color="purple")
                canv.draw()
        if key==53 and cordinates[len(cordinates)-1]!=[]:
            if len(cordinates[len(cordinates)-1])>=2 and len(cordinates[len(cordinates)-1])<=7:
                cordinates[len(cordinates)-1].append(str(key)+",")
                x1, y1 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][0][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                x2, y2 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number]]
                x3, y3 = [cordinates[len(cordinates)-1][1][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                x4, y4 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                canv.axes.plot(x1, y1, x2, y2, color="pink")
                canv.axes.plot(x3, y3, x4, y4, color="pink")
                canv.draw()
        if key==16777223 and cordinates[len(cordinates)-1]!=[]:
            x1, y1 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][0][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
            x2, y2 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number]]
            x3, y3 = [cordinates[len(cordinates)-1][1][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
            x4, y4 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
            canv.axes.plot(x1, y1, x2, y2, color="white", linewidth=6.0)
            canv.axes.plot(x3, y3, x4, y4, color="white", linewidth=6.0)
            canv.draw()
            del cordinates[len(cordinates)-1]
            cordinates.append([])
            
    def closeEvent(self, event):
        stopAnimation()
        print_load("")
        global im_number
        global slice_number
        im_number=0
        slice_number=0
        
    
    
   
im_number = 0
class MplCanvas(FigureCanvasQTAgg):
    
    def __init__(self, parent=None, width= 300, height= 300):
        global fig
        fig = Figure(figsize=(width, height))
        self.axes = fig.add_subplot(111)
        global canv
        canv = self

        FigureCanvasQTAgg.__init__(self, fig)
        self.setParent(parent)

        FigureCanvasQTAgg.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)
        global translator
        translator = deepl.Translator(auth_key)
        ####  get path
        global pather
        pather=pathg+"/"
        global save_path
        save_path=pathg+r"[TRANSLATED]/"
        if path.exists(save_path)==False:
            pathe = os.path.join("",save_path ) 
            os.mkdir(pathe)
        ####
        global mylist
        mylist = os.listdir(pather)
        loading_animation()
        print_load("Styling...")
        global im_number
        global img
        img = Image.open(pather+mylist[im_number])
        #create pix arr by line
        global listed_img
        listed_img = transformattion(list(img.getdata()),img.size[0])
        #crop img
        global cordinates
        cordinates=[[]]
        global img_cropped
        img_cropped=img_crop(img,5000,200)
        
        def onclick(event):
            if event.dblclick and event.xdata != None and event.ydata != None:
                if len(cordinates[len(cordinates)-1])>=2 and cordinates[len(cordinates)-1]!=[]:
                    cordinates.append([])
                if len(cordinates[len(cordinates)-1])==1:
                    x1, y1 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][0][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], event.ydata]
                    x2, y2 = [cordinates[len(cordinates)-1][0][0], event.xdata], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number]]
                    x3, y3 = [event.xdata, event.xdata], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], event.ydata]
                    x4, y4 = [cordinates[len(cordinates)-1][0][0], event.xdata], [event.ydata, event.ydata]
                    canv.axes.plot(x1, y1, x2, y2, color="blue")
                    canv.axes.plot(x3, y3, x4, y4, color="blue")
                    canv.draw()
                cordinates[len(cordinates)-1].append([round(event.xdata),round(event.ydata)+ret_cords[slice_number]])
        canv.axes.imshow(img_cropped[slice_number])
        connection_id = fig.canvas.mpl_connect('button_press_event', onclick)
        self.draw()
        
        fig.subplots_adjust(bottom=0.1, top=0.995)
        self.bnext = QtWidgets.QPushButton(self)
        self.bnext.setStyleSheet("color: rgb(27, 171, 255)")
        self.bnext.setText('Next')
        self.bnext.clicked.connect(Index.next)
        self.bnext.setGeometry(0,0,120,81)
        self.bnext.setFixedHeight(65)
        
        connect_box = QVBoxLayout(self)
        connect_box.setAlignment(QtCore.Qt.AlignBottom) 
        connect_box.addWidget(self.bnext, alignment=QtCore.Qt.AlignRight)
        if len(img_cropped)!=1:
            self.bprev = QtWidgets.QPushButton(self)
            self.bprev.setStyleSheet("color: rgb(27, 171, 255)")
            self.bprev.setText('Previous')
            self.bprev.clicked.connect(Index.prev)
            self.bprev.setGeometry(0,0,120,81)
            self.bprev.setFixedHeight(65)
            connect_box.addWidget(self.bprev, alignment=QtCore.Qt.AlignRight)
        self.show()
        
                

slice_number = 0
class Index:
    
    def next(self):
        global slice_number
        if slice_number<len(img_cropped)-1:
            slice_number+=1
            fig.clear()
            canv.axes = fig.add_subplot(111)
            canv.axes.imshow(img_cropped[slice_number])
            canv.draw()
        else:
            SW.hide()
            window1.SW.hide()
            print_load(str(cordinates))
            ##
            #get the selected pixels and draw images
            if cordinates!=[[]]:
                for i in range(len(cordinates)):
                    if len(cordinates[i])>=2:
                        input=""
                        ultimate_font=normal_font
                        for r in range(len(cordinates[i])-2):
                            input+=str(cordinates[i][r+2])
                        cordinates[i][0], cordinates[i][1] = firstandsec_axist(cordinates[i][0],cordinates[i][1])
                        k = get_dblist_from_dbarr(listed_img, cordinates[i][0], cordinates[i][1])
                        tranformed_img = re_transformattion(k)
                        rot_img=tranformed_img
                        global lang1
                        text_base=merge_textlines(pytesseract.image_to_string(rot_img, lang=lang1).split("\n")).replace("/", "!").replace("7", "T").replace("2", "?").replace("3", "S").replace("5", "S").replace("9O", "SO")
                        print(text_base)
                        if text_base!="":
                            line_num=text_lines(pytesseract.image_to_string(rot_img, lang=lang1))
                            ## Translating
                            print_load("translating "+str(i+1))
                            
                            if text_base!="":
                                global lang2
                                result = translator.translate_text(text_base, target_lang=lang2)
                                text_base = str(result.text)
                            ##
                            wrapped_text=line_break(line_num,text_base)
                            print_load("cleaning "+str(i+1))
                            im = cleaner(tranformed_img)[0]
                            pixs = cleaner(tranformed_img)[1]
                            print_load("rendering "+str(i+1))
                            base_col = cleaner(tranformed_img)[2]
                            col=blackwhite_opposite_col(base_col)[0]
                            outline_col=blackwhite_opposite_col(base_col)[1]
                            if input.find("90,")!=-1:
                                col="gray"
                            if input.find("66,")!=-1:
                                outline_col=col
                            if input.find("73,")!=-1 and italic_font!="":
                                ultimate_font=italic_font
                            if input.find("50,")!=-1 and sec_font!="":
                                ultimate_font=sec_font
                            if input.find("51,")!=-1 and third_font!="":
                                ultimate_font=third_font
                            if input.find("52,")!=-1 and fourth_font!="":
                                ultimate_font=fourth_font
                            if input.find("53,")!=-1 and fifth_font!="":
                                ultimate_font=fifth_font
                                
                            draw = ImageDraw.Draw(im)
                            box = ((0, 0, im.size[0], im.size[1]))

                            text = wrapped_text
                            font_size = 100
                            size = None
                            while (size is None or size[0]+line_num > box[2] - box[0] or size[1]+line_num*2.5 > box[3] - box[1]) and font_size > 0:
                                font = ImageFont.truetype(ultimate_font, font_size)
                                size = font.getsize_multiline(text)
                                font_size -= 1
                            font = ImageFont.truetype(ultimate_font, font_size-4)
                            if input.find("74,")!=-1:
                                draw.multiline_text(xy=(0, im.size[1] / 2), text=text, fill=col, font=font, anchor = "lm", stroke_width=2, spacing=8, stroke_fill=outline_col)
                            else:
                                draw.multiline_text(xy=(im.size[0]/2, im.size[1] / 2), text=text, fill=col, font=font, align="center", anchor = "mm", stroke_width=2, spacing=8, stroke_fill=outline_col)
                            img.paste(im, (cordinates[i][0][0],cordinates[i][0][1]))
            print_load("saving")
            global im_number
            img.save(save_path+zero_adder(mylist[im_number], 4))
            print_load(now.strftime("%m/%d/%Y, %H:%M:%S")+"\n") 
            #next iteration
            if im_number<len(mylist)-1:
                fig.clear()
                im_number+=1
                slice_number=0
                window1.SW=SecWindow()
                window1.SW.show()
                window1.SW.showMaximized()
            else:
                stopAnimation()
                print_load("")
                fig.clear()
                im_number=0
                slice_number=0
                

    def prev(self):
        global slice_number
        if slice_number>0:
            slice_number-=1
            fig.clear()
            canv.axes = fig.add_subplot(111)
            canv.axes.imshow(img_cropped[slice_number])
            canv.draw()

class input_win(QMainWindow):
    def __init__(self):
        super(input_win, self).__init__()
        self.setWindowTitle("Select subtitle")
        self.setStyleSheet("background-color: rgb(38, 38, 38)")
        self.setWindowIcon(QIcon(dir+r"\files\comic_icon.png"))
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setFocus()
        self.resize(400,160)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        
        
        self.input7 = QtWidgets.QLineEdit(self,placeholderText='Select subtitle file... *',)
        self.input7.setStyleSheet("color: rgb(27, 171, 255); background-color: rgb(30, 30, 30); outline:none;padding-right:120px; padding-left:5px;border: 2px solid rgb(27, 171, 255);border-radius:10px;font-weight:600;")
        self.input7.setGeometry(10, 10, 380,1)
        self.input7.setFixedHeight(60)
        
        self.browsebtn7 = QtWidgets.QPushButton(self)
        self.browsebtn7.setStyleSheet("color: rgb(27, 171, 255)")
        self.browsebtn7.setText('Browse')
        self.browsebtn7.clicked.connect(self.subtitle)
        self.browsebtn7.setGeometry(275, 20, 105,1)
        self.browsebtn7.setFixedHeight(40)
        
        self.start_btn = QtWidgets.QPushButton(self)
        self.start_btn.setStyleSheet("background-color: rgb(27, 171, 255); border-radius:10px;color: rgb(30, 30, 30);font-size:20px; font-weight:550;")
        self.start_btn.setText('Confirm Subtitle File')
        self.start_btn.clicked.connect(self.confirm)
        self.start_btn.setGeometry(10, 80, 380,1)
        self.start_btn.setFixedHeight(50)
        
        self.lbl=QtWidgets.QLabel(self)
        self.lbl.setStyleSheet("color: rgb(27, 171, 255);font-size:13px;font-weight:550;")
        self.lbl.setGeometry(2, 135, 398,20)
        self.lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl.setText('*: Or, just click "confirm" and enter the translation manually.')
        
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        
    def subtitle(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Single File', QtCore.QDir.rootPath() , '*.txt')
        self.input7.setText(file)
    def confirm(self):
        if self.input7.text()!="" and path.exists(self.input7.text())==True:
            File = open(self.input7.text(), encoding="utf-8")
            global subtl_texts
            subtl_texts = File.read().splitlines()
            xd=0
            self.close()
            window1.SW = ThirdWindow()
            window1.SW.show()
            window1.SW.showMaximized()
        else:
            xd=1
            self.close()
            window1.SW = FourthWindow()
            window1.SW.show()
            window1.SW.showMaximized()
        global rentel
        rentel = xd
        global SW
        SW=window1.SW
            
        
        
class ThirdWindow(QMainWindow):
        
    def __init__(self, *args, **kwargs):
        super(ThirdWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Styling [Where should the text be?]")
        self.setGeometry(int(monitor_w/2), 10, int(monitor_w/2), int(monitor_h/2))
        self.setWindowIcon(QIcon(dir+r"\files\comic_icon.png"))
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setFocus()
        
        global layout
        layout = QtWidgets.QVBoxLayout()
        sc = MplCanvas2(width = 300, height = 300)
        
        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        global toolbar
        toolbar = NavigationToolbar2QT(sc, self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)

        # Create a placeholder widget to hold our toolbar and canvas.
        global widget
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
        
        
    def keyPressEvent(self, event):
        key=int(event.key())
        if (key==77 or key==74) and cordinates[len(cordinates)-1]!=[]:
            if len(cordinates[len(cordinates)-1])>=2 and len(cordinates[len(cordinates)-1])<=7:
                cordinates[len(cordinates)-1].append(str(key)+",")
                if key==74 and cordinates[len(cordinates)-1]!=[]:
                    x1, y1 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][0][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                    x2, y2 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number]]
                    x3, y3 = [cordinates[len(cordinates)-1][1][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                    x4, y4 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                    canv.axes.plot(x1, y1, x2, y2, color="lightgreen")
                    canv.axes.plot(x3, y3, x4, y4, color="lightgreen")
                    canv.draw()
        if key==66 and cordinates[len(cordinates)-1]!=[]:
            if len(cordinates[len(cordinates)-1])>=2 and len(cordinates[len(cordinates)-1])<=7:
                cordinates[len(cordinates)-1].append(str(key)+",")
                x1, y1 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][0][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                x2, y2 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number]]
                x3, y3 = [cordinates[len(cordinates)-1][1][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                x4, y4 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                canv.axes.plot(x1, y1, x2, y2, color="orange", linestyle='dashed')
                canv.axes.plot(x3, y3, x4, y4, color="orange", linestyle='dashed')
                canv.draw()
        if key==90 and cordinates[len(cordinates)-1]!=[]:
            if len(cordinates[len(cordinates)-1])>=2 and len(cordinates[len(cordinates)-1])<=7:
                cordinates[len(cordinates)-1].append(str(key)+",")
                x1, y1 = [cordinates[len(cordinates)-1][0][0]-1, cordinates[len(cordinates)-1][0][0]-1], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number]+1, cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]+1]
                x2, y2 = [cordinates[len(cordinates)-1][0][0]-1, cordinates[len(cordinates)-1][1][0]-1], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number]+1, cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number]+1]
                x3, y3 = [cordinates[len(cordinates)-1][1][0]-1, cordinates[len(cordinates)-1][1][0]-1], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number]+1, cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]+1]
                x4, y4 = [cordinates[len(cordinates)-1][0][0]-1, cordinates[len(cordinates)-1][1][0]-1], [cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]+1, cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]+1]
                canv.axes.plot(x1, y1, x2, y2, color="gray")
                canv.axes.plot(x3, y3, x4, y4, color="gray")
                canv.draw()
        if key==73 and cordinates[len(cordinates)-1]!=[]:
            if len(cordinates[len(cordinates)-1])>=2 and len(cordinates[len(cordinates)-1])<=7:
                cordinates[len(cordinates)-1].append(str(key)+",")
                x1, y1 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][0][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                x2, y2 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number]]
                x3, y3 = [cordinates[len(cordinates)-1][1][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                x4, y4 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                canv.axes.plot(x1, y1, x2, y2, color="white", dashes=[1, 1, 1, 1])
                canv.axes.plot(x3, y3, x4, y4, color="white", dashes=[1, 1, 1, 1])
                canv.draw()
        if key==50 and cordinates[len(cordinates)-1]!=[]:
            if len(cordinates[len(cordinates)-1])>=2 and len(cordinates[len(cordinates)-1])<=7:
                cordinates[len(cordinates)-1].append(str(key)+",")
                x1, y1 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][0][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                x2, y2 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number]]
                x3, y3 = [cordinates[len(cordinates)-1][1][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                x4, y4 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                canv.axes.plot(x1, y1, x2, y2, color="yellow")
                canv.axes.plot(x3, y3, x4, y4, color="yellow")
                canv.draw()
        if key==51 and cordinates[len(cordinates)-1]!=[]:
            if len(cordinates[len(cordinates)-1])>=2 and len(cordinates[len(cordinates)-1])<=7:
                cordinates[len(cordinates)-1].append(str(key)+",")
                x1, y1 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][0][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                x2, y2 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number]]
                x3, y3 = [cordinates[len(cordinates)-1][1][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                x4, y4 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                canv.axes.plot(x1, y1, x2, y2, color="red")
                canv.axes.plot(x3, y3, x4, y4, color="red")
                canv.draw()
        if key==52 and cordinates[len(cordinates)-1]!=[]:
            if len(cordinates[len(cordinates)-1])>=2 and len(cordinates[len(cordinates)-1])<=7:
                cordinates[len(cordinates)-1].append(str(key)+",")
                x1, y1 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][0][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                x2, y2 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number]]
                x3, y3 = [cordinates[len(cordinates)-1][1][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                x4, y4 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                canv.axes.plot(x1, y1, x2, y2, color="purple")
                canv.axes.plot(x3, y3, x4, y4, color="purple")
                canv.draw()
        if key==53 and cordinates[len(cordinates)-1]!=[]:
            if len(cordinates[len(cordinates)-1])>=2 and len(cordinates[len(cordinates)-1])<=7:
                cordinates[len(cordinates)-1].append(str(key)+",")
                x1, y1 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][0][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                x2, y2 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number]]
                x3, y3 = [cordinates[len(cordinates)-1][1][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                x4, y4 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                canv.axes.plot(x1, y1, x2, y2, color="pink")
                canv.axes.plot(x3, y3, x4, y4, color="pink")
                canv.draw()
        if key==16777223 and cordinates[len(cordinates)-1]!=[]:
            x1, y1 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][0][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
            x2, y2 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number]]
            x3, y3 = [cordinates[len(cordinates)-1][1][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
            x4, y4 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
            canv.axes.plot(x1, y1, x2, y2, color="white", linewidth=6.0)
            canv.axes.plot(x3, y3, x4, y4, color="white", linewidth=6.0)
            canv.draw()
            del cordinates[len(cordinates)-1]
            cordinates.append([])
            global sub_number
            sub_number-=1
            MplCanvas2.subtitle_lbl.setText(subtl_texts[sub_number])
            
    def closeEvent(self, event):
        stopAnimation()
        print_load("")
        global im_number
        global slice_number
        im_number=0
        slice_number=0
        global sub_number
        sub_number=0
        
    
    
sub_number = 0
im_number = 0
class MplCanvas2(FigureCanvasQTAgg):
    
    def __init__(self, parent=None, width= 300, height= 300):
        global fig
        fig = Figure(figsize=(width, height))
        self.axes = fig.add_subplot(111)
        global canv
        canv = self

        FigureCanvasQTAgg.__init__(self, fig)
        self.setParent(parent)

        FigureCanvasQTAgg.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)
        global translator
        translator = deepl.Translator(auth_key)
        ####  get path
        global pather
        pather=pathg+"/"
        global save_path
        save_path=pathg+r"[TRANSLATED]/"
        if path.exists(save_path)==False:
            pathe = os.path.join("",save_path ) 
            os.mkdir(pathe)
        ####
        global mylist
        mylist = os.listdir(pather)
        loading_animation()
        print_load("Styling...")
        global im_number
        global img
        img = Image.open(pather+mylist[im_number])
        #create pix arr by line
        global listed_img
        listed_img = transformattion(list(img.getdata()),img.size[0])
        #crop img
        global cordinates
        cordinates=[[]]
        global img_cropped
        img_cropped=img_crop(img,5000,200)
        
        def onclick(event):
            if event.dblclick and event.xdata != None and event.ydata != None:
                if len(cordinates[len(cordinates)-1])>=2 and cordinates[len(cordinates)-1]!=[]:
                    cordinates.append([])
                if len(cordinates[len(cordinates)-1])==1:
                    x1, y1 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][0][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], event.ydata]
                    x2, y2 = [cordinates[len(cordinates)-1][0][0], event.xdata], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number]]
                    x3, y3 = [event.xdata, event.xdata], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], event.ydata]
                    x4, y4 = [cordinates[len(cordinates)-1][0][0], event.xdata], [event.ydata, event.ydata]
                    canv.axes.plot(x1, y1, x2, y2, color="blue")
                    canv.axes.plot(x3, y3, x4, y4, color="blue")
                    canv.draw()
                    global sub_number
                    if sub_number<len(subtl_texts)-1:
                        sub_number+=1
                        MplCanvas2.subtitle_lbl.setText(subtl_texts[sub_number])
                    else:
                        MplCanvas2.subtitle_lbl.setText("no more subtitles")
                cordinates[len(cordinates)-1].append([round(event.xdata),round(event.ydata)+ret_cords[slice_number]])
        canv.axes.imshow(img_cropped[slice_number])
        connection_id = fig.canvas.mpl_connect('button_press_event', onclick)
        self.draw()
        
        MplCanvas2.subtitle_lbl = QtWidgets.QLabel(self)
        MplCanvas2.subtitle_lbl.setFont(QFont('Franklin Gothic Demi Cond', 18))
        MplCanvas2.subtitle_lbl.setGeometry(0, 20, 800, 35)
        MplCanvas2.subtitle_lbl.resize(monitor_w, 35)
        MplCanvas2.subtitle_lbl.setStyleSheet("color: rgb(27, 171, 255)")
        MplCanvas2.subtitle_lbl.setAlignment(QtCore.Qt.AlignCenter)
        global sub_number
        MplCanvas2.subtitle_lbl.setText(subtl_texts[sub_number])
        
        fig.subplots_adjust(bottom=0.1, top=0.915)
        self.bsubnext = QtWidgets.QPushButton(self)
        self.bsubnext.setStyleSheet("color: rgb(27, 171, 255)")
        self.bsubnext.setText('Next subtitle')
        self.bsubnext.clicked.connect(Index2.next_subt)
        self.bsubnext.setGeometry(0,0,120,81)
        self.bsubnext.setFixedHeight(65)
        
        self.bnext = QtWidgets.QPushButton(self)
        self.bnext.setStyleSheet("color: rgb(27, 171, 255)")
        self.bnext.setText('Next')
        self.bnext.clicked.connect(Index2.next)
        self.bnext.setGeometry(0,0,120,81)
        self.bnext.setFixedHeight(65)
        
        connect_box = QVBoxLayout(self)
        connect_box.setAlignment(QtCore.Qt.AlignBottom) 
        connect_box.addWidget(self.bsubnext, alignment=QtCore.Qt.AlignRight)
        connect_box.addWidget(self.bnext, alignment=QtCore.Qt.AlignRight)
        if len(img_cropped)!=1:
            self.bprev = QtWidgets.QPushButton(self)
            self.bprev.setStyleSheet("color: rgb(27, 171, 255)")
            self.bprev.setText('Previous')
            self.bprev.clicked.connect(Index2.prev)
            self.bprev.setGeometry(0,0,120,81)
            self.bprev.setFixedHeight(65)
            connect_box.addWidget(self.bprev, alignment=QtCore.Qt.AlignRight)
        self.show()
        
                

slice_number = 0
class Index2:
    
    def next(self):
        global slice_number
        if slice_number<len(img_cropped)-1:
            slice_number+=1
            fig.clear()
            canv.axes = fig.add_subplot(111)
            canv.axes.imshow(img_cropped[slice_number])
            canv.draw()
        else:
            SW.hide()
            window1.SW.hide()
            print_load(str(cordinates))
            ##
            #get the selected pixels and draw images
            if cordinates!=[[]]:
                for i in range(len(cordinates)):
                    if len(cordinates[i])>=2:
                        input=""
                        ultimate_font=normal_font
                        for r in range(len(cordinates[i])-2):
                            input+=str(cordinates[i][r+2])
                        cordinates[i][0], cordinates[i][1] = firstandsec_axist(cordinates[i][0],cordinates[i][1])
                        k = get_dblist_from_dbarr(listed_img, cordinates[i][0], cordinates[i][1])
                        tranformed_img = re_transformattion(k)
                        rot_img=tranformed_img
                        text_base=subtl_texts[i]
                        if text_base!="":
                            global lang1
                            line_num=text_lines(pytesseract.image_to_string(rot_img, lang=lang1))
                            wrapped_text=line_break(line_num,text_base)
                            print_load("cleaning "+str(i+1))
                            im = cleaner(tranformed_img)[0]
                            pixs = cleaner(tranformed_img)[1]
                            print_load("rendering "+str(i+1))
                            base_col = cleaner(tranformed_img)[2]
                            col=blackwhite_opposite_col(base_col)[0]
                            outline_col=blackwhite_opposite_col(base_col)[1]
                            if input.find("90,")!=-1:
                                col="gray"
                            if input.find("66,")!=-1:
                                outline_col=col
                            if input.find("73,")!=-1 and italic_font!="":
                                ultimate_font=italic_font
                            if input.find("50,")!=-1 and sec_font!="":
                                ultimate_font=sec_font
                            if input.find("51,")!=-1 and third_font!="":
                                ultimate_font=third_font
                            if input.find("52,")!=-1 and fourth_font!="":
                                ultimate_font=fourth_font
                            if input.find("53,")!=-1 and fifth_font!="":
                                ultimate_font=fifth_font
                                
                            draw = ImageDraw.Draw(im)
                            box = ((0, 0, im.size[0], im.size[1]))

                            text = wrapped_text
                            font_size = 100
                            size = None
                            while (size is None or size[0]+line_num > box[2] - box[0] or size[1]+line_num*2.5 > box[3] - box[1]) and font_size > 0:
                                font = ImageFont.truetype(ultimate_font, font_size)
                                size = font.getsize_multiline(text)
                                font_size -= 1
                            font = ImageFont.truetype(ultimate_font, font_size-4)
                            if input.find("74,")!=-1:
                                draw.multiline_text(xy=(0, im.size[1] / 2), text=text, fill=col, font=font, anchor = "lm", stroke_width=2, spacing=8, stroke_fill=outline_col)
                            else:
                                draw.multiline_text(xy=(im.size[0]/2, im.size[1] / 2), text=text, fill=col, font=font, align="center", anchor = "mm", stroke_width=2, spacing=8, stroke_fill=outline_col)
                            img.paste(im, (cordinates[i][0][0],cordinates[i][0][1]))
            print_load("saving")
            global im_number
            img.save(save_path+zero_adder(mylist[im_number], 4))
            print_load(now.strftime("%m/%d/%Y, %H:%M:%S")+"\n") 
            #next iteration
            if im_number<len(mylist)-1:
                fig.clear()
                im_number+=1
                slice_number=0
                if rentel==0:
                    window1.SW=ThirdWindow()
                else:
                    window1.SW=FourthWindow()
                window1.SW.show()
                window1.SW.showMaximized()
            else:
                stopAnimation()
                print_load("")
                fig.clear()
                im_number=0
                slice_number=0
                global sub_number
                sub_number=0
                
    
    def prev(self):
        global slice_number
        if slice_number>0:
            slice_number-=1
            fig.clear()
            canv.axes = fig.add_subplot(111)
            canv.axes.imshow(img_cropped[slice_number])
            canv.draw()
                        
    def next_subt(self):
        global sub_number
        if sub_number<len(subtl_texts)-1:
            del subtl_texts[sub_number]
            MplCanvas2.subtitle_lbl.setText(subtl_texts[sub_number])
        else:
            MplCanvas2.subtitle_lbl.setText("no more subtitles")



subtl_texts=[]
class input2_win(QMainWindow):
    def __init__(self):
        super(input2_win, self).__init__()
        self.setWindowTitle("Enter subtitle")
        self.setStyleSheet("background-color: rgb(38, 38, 38)")
        self.setWindowIcon(QIcon(dir+r"\files\comic_icon.png"))
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setFocus()
        self.resize(400,145)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        
        
        self.input7 = QtWidgets.QLineEdit(self,placeholderText='Enter translated text...',)
        self.input7.setStyleSheet("color: rgb(27, 171, 255); background-color: rgb(30, 30, 30); outline:none;padding-right:5px; padding-left:5px;border: 2px solid rgb(27, 171, 255);border-radius:10px;font-weight:600;")
        self.input7.setGeometry(10, 10, 380,1)
        self.input7.setFixedHeight(60)
        
        self.start_btn = QtWidgets.QPushButton(self)
        self.start_btn.setStyleSheet("background-color: rgb(27, 171, 255); border-radius:10px;color: rgb(30, 30, 30);font-size:20px; font-weight:550;")
        self.start_btn.setText('Confirm')
        self.start_btn.clicked.connect(self.confirm)
        self.start_btn.setGeometry(10, 80, 380,1)
        self.start_btn.setFixedHeight(50)
        
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
    
    def confirm(self):
        self.hide()
        global subtl_texts
        subtl_texts.append(self.input7.text())
    
    def closeEvent(self, event):
        global subtl_texts
        subtl_texts.append(self.input7.text())
        

class FourthWindow(QMainWindow):
        
    def __init__(self, *args, **kwargs):
        super(FourthWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Styling")
        self.setGeometry(int(monitor_w/2), 10, int(monitor_w/2), int(monitor_h/2))
        self.setWindowIcon(QIcon(dir+r"\files\comic_icon.png"))
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setFocus()
        
        global layout
        layout = QtWidgets.QVBoxLayout()
        sc = MplCanvas3(width = 300, height = 300)
        
        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        global toolbar
        toolbar = NavigationToolbar2QT(sc, self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)

        # Create a placeholder widget to hold our toolbar and canvas.
        global widget
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
        
        
    def keyPressEvent(self, event):
        key=int(event.key())
        if (key==77 or key==74) and cordinates[len(cordinates)-1]!=[]:
            if len(cordinates[len(cordinates)-1])>=2 and len(cordinates[len(cordinates)-1])<=7:
                cordinates[len(cordinates)-1].append(str(key)+",")
                if key==74 and cordinates[len(cordinates)-1]!=[]:
                    x1, y1 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][0][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                    x2, y2 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number]]
                    x3, y3 = [cordinates[len(cordinates)-1][1][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                    x4, y4 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                    canv.axes.plot(x1, y1, x2, y2, color="lightgreen")
                    canv.axes.plot(x3, y3, x4, y4, color="lightgreen")
                    canv.draw()
        if key==66 and cordinates[len(cordinates)-1]!=[]:
            if len(cordinates[len(cordinates)-1])>=2 and len(cordinates[len(cordinates)-1])<=7:
                cordinates[len(cordinates)-1].append(str(key)+",")
                x1, y1 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][0][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                x2, y2 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number]]
                x3, y3 = [cordinates[len(cordinates)-1][1][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                x4, y4 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                canv.axes.plot(x1, y1, x2, y2, color="orange", linestyle='dashed')
                canv.axes.plot(x3, y3, x4, y4, color="orange", linestyle='dashed')
                canv.draw()
        if key==90 and cordinates[len(cordinates)-1]!=[]:
            if len(cordinates[len(cordinates)-1])>=2 and len(cordinates[len(cordinates)-1])<=7:
                cordinates[len(cordinates)-1].append(str(key)+",")
                x1, y1 = [cordinates[len(cordinates)-1][0][0]-1, cordinates[len(cordinates)-1][0][0]-1], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number]+1, cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]+1]
                x2, y2 = [cordinates[len(cordinates)-1][0][0]-1, cordinates[len(cordinates)-1][1][0]-1], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number]+1, cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number]+1]
                x3, y3 = [cordinates[len(cordinates)-1][1][0]-1, cordinates[len(cordinates)-1][1][0]-1], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number]+1, cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]+1]
                x4, y4 = [cordinates[len(cordinates)-1][0][0]-1, cordinates[len(cordinates)-1][1][0]-1], [cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]+1, cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]+1]
                canv.axes.plot(x1, y1, x2, y2, color="gray")
                canv.axes.plot(x3, y3, x4, y4, color="gray")
                canv.draw()
        if key==73 and cordinates[len(cordinates)-1]!=[]:
            if len(cordinates[len(cordinates)-1])>=2 and len(cordinates[len(cordinates)-1])<=7:
                cordinates[len(cordinates)-1].append(str(key)+",")
                x1, y1 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][0][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                x2, y2 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number]]
                x3, y3 = [cordinates[len(cordinates)-1][1][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                x4, y4 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                canv.axes.plot(x1, y1, x2, y2, color="white", dashes=[1, 1, 1, 1])
                canv.axes.plot(x3, y3, x4, y4, color="white", dashes=[1, 1, 1, 1])
                canv.draw()
        if key==50 and cordinates[len(cordinates)-1]!=[]:
            if len(cordinates[len(cordinates)-1])>=2 and len(cordinates[len(cordinates)-1])<=7:
                cordinates[len(cordinates)-1].append(str(key)+",")
                x1, y1 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][0][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                x2, y2 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number]]
                x3, y3 = [cordinates[len(cordinates)-1][1][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                x4, y4 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                canv.axes.plot(x1, y1, x2, y2, color="yellow")
                canv.axes.plot(x3, y3, x4, y4, color="yellow")
                canv.draw()
        if key==51 and cordinates[len(cordinates)-1]!=[]:
            if len(cordinates[len(cordinates)-1])>=2 and len(cordinates[len(cordinates)-1])<=7:
                cordinates[len(cordinates)-1].append(str(key)+",")
                x1, y1 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][0][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                x2, y2 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number]]
                x3, y3 = [cordinates[len(cordinates)-1][1][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                x4, y4 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                canv.axes.plot(x1, y1, x2, y2, color="red")
                canv.axes.plot(x3, y3, x4, y4, color="red")
                canv.draw()
        if key==52 and cordinates[len(cordinates)-1]!=[]:
            if len(cordinates[len(cordinates)-1])>=2 and len(cordinates[len(cordinates)-1])<=7:
                cordinates[len(cordinates)-1].append(str(key)+",")
                x1, y1 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][0][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                x2, y2 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number]]
                x3, y3 = [cordinates[len(cordinates)-1][1][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                x4, y4 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                canv.axes.plot(x1, y1, x2, y2, color="purple")
                canv.axes.plot(x3, y3, x4, y4, color="purple")
                canv.draw()
        if key==53 and cordinates[len(cordinates)-1]!=[]:
            if len(cordinates[len(cordinates)-1])>=2 and len(cordinates[len(cordinates)-1])<=7:
                cordinates[len(cordinates)-1].append(str(key)+",")
                x1, y1 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][0][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                x2, y2 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number]]
                x3, y3 = [cordinates[len(cordinates)-1][1][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                x4, y4 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
                canv.axes.plot(x1, y1, x2, y2, color="pink")
                canv.axes.plot(x3, y3, x4, y4, color="pink")
                canv.draw()
        if key==16777223 and cordinates[len(cordinates)-1]!=[]:
            x1, y1 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][0][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
            x2, y2 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number]]
            x3, y3 = [cordinates[len(cordinates)-1][1][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
            x4, y4 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][1][0]], [cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][1][1]-ret_cords[slice_number]]
            canv.axes.plot(x1, y1, x2, y2, color="white", linewidth=6.0)
            canv.axes.plot(x3, y3, x4, y4, color="white", linewidth=6.0)
            canv.draw()
            del cordinates[len(cordinates)-1]
            cordinates.append([])
            global subtl_texts
            del subtl_texts[len(subtl_texts)-1]
            
    def closeEvent(self, event):
        stopAnimation()
        print_load("")
        global im_number
        global slice_number
        im_number=0
        slice_number=0
        
    
    
im_number = 0
class MplCanvas3(FigureCanvasQTAgg):
    
    def __init__(self, parent=None, width= 300, height= 300):
        global fig
        fig = Figure(figsize=(width, height))
        self.axes = fig.add_subplot(111)
        global canv
        canv = self

        FigureCanvasQTAgg.__init__(self, fig)
        self.setParent(parent)

        FigureCanvasQTAgg.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)
        global translator
        translator = deepl.Translator(auth_key)
        ####  get path
        global pather
        pather=pathg+"/"
        global save_path
        save_path=pathg+r"[TRANSLATED]/"
        if path.exists(save_path)==False:
            pathe = os.path.join("",save_path ) 
            os.mkdir(pathe)
        ####
        global mylist
        mylist = os.listdir(pather)
        loading_animation()
        print_load("Styling...")
        global im_number
        global img
        img = Image.open(pather+mylist[im_number])
        #create pix arr by line
        global listed_img
        listed_img = transformattion(list(img.getdata()),img.size[0])
        #crop img
        global cordinates
        cordinates=[[]]
        global img_cropped
        img_cropped=img_crop(img,5000,200)
        
        def onclick(event):
            if event.dblclick and event.xdata != None and event.ydata != None:
                if len(cordinates[len(cordinates)-1])>=2 and cordinates[len(cordinates)-1]!=[]:
                    cordinates.append([])
                if len(cordinates[len(cordinates)-1])==1:
                    x1, y1 = [cordinates[len(cordinates)-1][0][0], cordinates[len(cordinates)-1][0][0]], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], event.ydata]
                    x2, y2 = [cordinates[len(cordinates)-1][0][0], event.xdata], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number]]
                    x3, y3 = [event.xdata, event.xdata], [cordinates[len(cordinates)-1][0][1]-ret_cords[slice_number], event.ydata]
                    x4, y4 = [cordinates[len(cordinates)-1][0][0], event.xdata], [event.ydata, event.ydata]
                    canv.axes.plot(x1, y1, x2, y2, color="blue")
                    canv.axes.plot(x3, y3, x4, y4, color="blue")
                    canv.draw()
                    window1.input2 = input2_win()
                    window1.input2.show()
                cordinates[len(cordinates)-1].append([round(event.xdata),round(event.ydata)+ret_cords[slice_number]])
        canv.axes.imshow(img_cropped[slice_number])
        connection_id = fig.canvas.mpl_connect('button_press_event', onclick)
        self.draw()
        
        fig.subplots_adjust(bottom=0.1, top=0.995)
        self.bnext = QtWidgets.QPushButton(self)
        self.bnext.setStyleSheet("color: rgb(27, 171, 255)")
        self.bnext.setText('Next')
        self.bnext.clicked.connect(Index2.next)
        self.bnext.setGeometry(0,0,120,81)
        self.bnext.setFixedHeight(65)
        
        connect_box = QVBoxLayout(self)
        connect_box.setAlignment(QtCore.Qt.AlignBottom) 
        connect_box.addWidget(self.bnext, alignment=QtCore.Qt.AlignRight)
        if len(img_cropped)!=1:
            self.bprev = QtWidgets.QPushButton(self)
            self.bprev.setStyleSheet("color: rgb(27, 171, 255)")
            self.bprev.setText('Previous')
            self.bprev.clicked.connect(Index2.prev)
            self.bprev.setGeometry(0,0,120,81)
            self.bprev.setFixedHeight(65)
            connect_box.addWidget(self.bprev, alignment=QtCore.Qt.AlignRight)
        self.show()
        
                



def window ():
    app = QApplication(sys.argv)
    win = window1()
    win.show()
    sys.exit(app.exec_())


window()
