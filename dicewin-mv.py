#-*- coding: utf-8 -*-

import sys
import os
import re
import time

import numpy
import matplotlib
matplotlib.use('Qt4Agg')
import matplotlib.pyplot
from scipy.odr import ODR, Model, Data, RealData

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

from PyQt4 import QtGui, QtCore

from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from direct.task import Task


class Scene(ShowBase):
   
   elements = {
    '1':{'elSym':'H', 'atmRad':0.53, 'ioRad':0.25, 'covRad':0.37, 'vdwRad':1.2, 'crystRad':0.1, 'color':(255/255,255/255,255/255, 1)},
    '2':{'elSym':'He', 'atmRad':0.31, 'ioRad':0.31, 'covRad':0.32, 'vdwRad':1.4, 'crystRad':'VOID', 'color':(217/255,255/255,255/255, 1)},
    '3':{'elSym':'Li', 'atmRad':1.67, 'ioRad':1.45, 'covRad':1.34, 'vdwRad':1.82, 'crystRad':0.9, 'color':(204/255,128/255,255/255, 1)},
    '4':{'elSym':'Be', 'atmRad':1.12, 'ioRad':1.05, 'covRad':0.9, 'vdwRad':'VOID', 'crystRad':0.41, 'color':(194/255,255/255,0/255, 1)},
    '5':{'elSym':'B', 'atmRad':0.87, 'ioRad':0.85, 'covRad':0.82, 'vdwRad':'VOID', 'crystRad':0.25, 'color':(255/255,181/255,181/255, 1)},
    '6':{'elSym':'C', 'atmRad':0.67, 'ioRad':0.7, 'covRad':0.77, 'vdwRad':1.7, 'crystRad':0.29, 'color':(144/255,144/255,144/255, 1)},
    '7':{'elSym':'N', 'atmRad':0.56, 'ioRad':0.65, 'covRad':0.75, 'vdwRad':1.55, 'crystRad':0.3, 'color':(48/255,80/255,248/255, 1)},
    '8':{'elSym':'O', 'atmRad':0.48, 'ioRad':0.6, 'covRad':0.73, 'vdwRad':1.52, 'crystRad':1.21, 'color':(255/255,13/255,13/255, 1)},
    '9':{'elSym':'F', 'atmRad':0.42, 'ioRad':0.5, 'covRad':0.71, 'vdwRad':1.47, 'crystRad':1.19, 'color':(144/255,224/255,80/255, 1)},
    '10':{'elSym':'Ne', 'atmRad':0.38, 'ioRad':0.38, 'covRad':0.69, 'vdwRad':1.54, 'crystRad':'VOID', 'color':(179/255,227/255,245/255, 1)},
    '11':{'elSym':'Na', 'atmRad':1.9, 'ioRad':1.8, 'covRad':1.54, 'vdwRad':2.27, 'crystRad':1.16, 'color':(171/255,92/255,242/255, 1)},
    '12':{'elSym':'Mg', 'atmRad':1.45, 'ioRad':1.5, 'covRad':1.3, 'vdwRad':1.73, 'crystRad':0.86, 'color':(138/255,255/255,0/255, 1)},
    '13':{'elSym':'Al', 'atmRad':1.18, 'ioRad':1.25, 'covRad':1.18, 'vdwRad':'VOID', 'crystRad':0.53, 'color':(191/255,166/255,166/255, 1)},
    '14':{'elSym':'Si', 'atmRad':1.11, 'ioRad':1.1, 'covRad':1.11, 'vdwRad':2.1, 'crystRad':0.4, 'color':(240/255,200/255,160/255, 1)},
    '15':{'elSym':'P', 'atmRad':0.98, 'ioRad':1, 'covRad':1.06, 'vdwRad':1.8, 'crystRad':0.31, 'color':(255/255,128/255,0/255, 1)},
    '16':{'elSym':'S', 'atmRad':0.88, 'ioRad':1, 'covRad':1.02, 'vdwRad':1.8, 'crystRad':0.43, 'color':(255/255,255/255,48/255, 1)},
    '17':{'elSym':'Cl', 'atmRad':0.79, 'ioRad':1, 'covRad':0.99, 'vdwRad':1.75, 'crystRad':1.67, 'color':(31/255,240/255,31/255, 1)},
    '18':{'elSym':'Ar', 'atmRad':0.71, 'ioRad':0.71, 'covRad':0.97, 'vdwRad':1.88, 'crystRad':'VOID', 'color':(128/255,209/255,227/255, 1)},
    '19':{'elSym':'K', 'atmRad':2.43, 'ioRad':2.2, 'covRad':1.96, 'vdwRad':2.75, 'crystRad':1.52, 'color':(143/255,64/255,212/255, 1)},
    '20':{'elSym':'Ca', 'atmRad':1.94, 'ioRad':1.8, 'covRad':1.74, 'vdwRad':'VOID', 'crystRad':1.14, 'color':(61/255,255/255,0/255, 1)},
    '21':{'elSym':'Sc', 'atmRad':1.84, 'ioRad':1.6, 'covRad':1.44, 'vdwRad':'VOID', 'crystRad':0.89, 'color':(230/255,230/255,230/255, 1)},
    '22':{'elSym':'Ti', 'atmRad':1.76, 'ioRad':1.4, 'covRad':1.36, 'vdwRad':'VOID', 'crystRad':0.75, 'color':(191/255,194/255,199/255, 1)},
    '23':{'elSym':'V', 'atmRad':1.71, 'ioRad':1.35, 'covRad':1.25, 'vdwRad':'VOID', 'crystRad':0.68, 'color':(166/255,166/255,171/255, 1)},
    '24':{'elSym':'Cr', 'atmRad':1.66, 'ioRad':1.4, 'covRad':1.27, 'vdwRad':'VOID', 'crystRad':0.76, 'color':(138/255,153/255,199/255, 1)},
    '25':{'elSym':'Mn', 'atmRad':1.61, 'ioRad':1.4, 'covRad':1.39, 'vdwRad':'VOID', 'crystRad':0.81, 'color':(156/255,122/255,199/255, 1)},
    '26':{'elSym':'Fe', 'atmRad':1.56, 'ioRad':1.4, 'covRad':1.25, 'vdwRad':'VOID', 'crystRad':0.69, 'color':(224/255,102/255,51/255, 1)},
    '27':{'elSym':'Co', 'atmRad':1.52, 'ioRad':1.35, 'covRad':1.26, 'vdwRad':'VOID', 'crystRad':0.54, 'color':(240/255,144/255,160/255, 1)},
    '28':{'elSym':'Ni', 'atmRad':1.49, 'ioRad':1.35, 'covRad':1.21, 'vdwRad':1.63, 'crystRad':0.7, 'color':(80/255,208/255,80/255, 1)},
    '29':{'elSym':'Cu', 'atmRad':1.45, 'ioRad':1.35, 'covRad':1.38, 'vdwRad':1.4, 'crystRad':0.71, 'color':(200/255,128/255,51/255, 1)},
    '30':{'elSym':'Zn', 'atmRad':1.42, 'ioRad':1.35, 'covRad':1.31, 'vdwRad':1.39, 'crystRad':0.74, 'color':(125/255,128/255,176/255, 1)},
    '31':{'elSym':'Ga', 'atmRad':1.36, 'ioRad':1.3, 'covRad':1.26, 'vdwRad':1.87, 'crystRad':0.76, 'color':(194/255,143/255,143/255, 1)},
    '32':{'elSym':'Ge', 'atmRad':1.25, 'ioRad':1.25, 'covRad':1.22, 'vdwRad':'VOID', 'crystRad':0.53, 'color':(102/255,143/255,143/255, 1)},
    '33':{'elSym':'As', 'atmRad':1.14, 'ioRad':1.15, 'covRad':1.19, 'vdwRad':1.85, 'crystRad':0.72, 'color':(189/255,128/255,227/255, 1)},
    '34':{'elSym':'Se', 'atmRad':1.03, 'ioRad':1.15, 'covRad':1.16, 'vdwRad':1.9, 'crystRad':0.56, 'color':(255/255,161/255,0/255, 1)},
    '35':{'elSym':'Br', 'atmRad':0.94, 'ioRad':1.15, 'covRad':1.14, 'vdwRad':1.85, 'crystRad':1.82, 'color':(166/255,41/255,41/255, 1)},
    '36':{'elSym':'Kr', 'atmRad':0.88, 'ioRad':0.88, 'covRad':1.1, 'vdwRad':2.02, 'crystRad':'VOID', 'color':(92/255,184/255,209/255, 1)},
    '37':{'elSym':'Rb', 'atmRad':2.65, 'ioRad':2.35, 'covRad':2.11, 'vdwRad':'VOID', 'crystRad':1.66, 'color':(112/255,46/255,176/255, 1)},
    '38':{'elSym':'Sr', 'atmRad':2.19, 'ioRad':2, 'covRad':1.92, 'vdwRad':'VOID', 'crystRad':1.32, 'color':(0/255,255/255,0/255, 1)},
    '39':{'elSym':'Y', 'atmRad':2.12, 'ioRad':1.85, 'covRad':1.62, 'vdwRad':'VOID', 'crystRad':1.04, 'color':(148/255,255/255,255/255, 1)},
    '40':{'elSym':'Zr', 'atmRad':2.06, 'ioRad':1.55, 'covRad':1.48, 'vdwRad':'VOID', 'crystRad':0.86, 'color':(148/255,224/255,224/255, 1)},
    '41':{'elSym':'Nb', 'atmRad':1.98, 'ioRad':1.45, 'covRad':1.37, 'vdwRad':'VOID', 'crystRad':0.78, 'color':(115/255,194/255,201/255, 1)},
    '42':{'elSym':'Mo', 'atmRad':1.9, 'ioRad':1.45, 'covRad':1.45, 'vdwRad':'VOID', 'crystRad':0.79, 'color':(84/255,181/255,181/255, 1)},
    '43':{'elSym':'Tc', 'atmRad':1.83, 'ioRad':1.35, 'covRad':1.56, 'vdwRad':'VOID', 'crystRad':0.79, 'color':(59/255,158/255,158/255, 1)},
    '44':{'elSym':'Ru', 'atmRad':1.78, 'ioRad':1.3, 'covRad':1.26, 'vdwRad':'VOID', 'crystRad':0.82, 'color':(36/255,143/255,143/255, 1)},
    '45':{'elSym':'Rh', 'atmRad':1.73, 'ioRad':1.35, 'covRad':1.35, 'vdwRad':'VOID', 'crystRad':0.81, 'color':(10/255,125/255,140/255, 1)},
    '46':{'elSym':'Pd', 'atmRad':1.69, 'ioRad':1.4, 'covRad':1.31, 'vdwRad':1.63, 'crystRad':0.78, 'color':(0/255,105/255,133/255, 1)},
    '47':{'elSym':'Ag', 'atmRad':1.65, 'ioRad':1.6, 'covRad':1.53, 'vdwRad':1.72, 'crystRad':1.29, 'color':(192/255,192/255,192/255, 1)},
    '48':{'elSym':'Cd', 'atmRad':1.61, 'ioRad':1.55, 'covRad':1.48, 'vdwRad':1.58, 'crystRad':0.92, 'color':(255/255,217/255,143/255, 1)},
    '49':{'elSym':'In', 'atmRad':1.56, 'ioRad':1.55, 'covRad':1.44, 'vdwRad':1.93, 'crystRad':0.94, 'color':(166/255,117/255,115/255, 1)},
    '50':{'elSym':'Sn', 'atmRad':1.45, 'ioRad':1.45, 'covRad':1.41, 'vdwRad':2.17, 'crystRad':0.69, 'color':(102/255,128/255,128/255, 1)},
    '51':{'elSym':'Sb', 'atmRad':1.33, 'ioRad':1.45, 'covRad':1.38, 'vdwRad':'VOID', 'crystRad':0.9, 'color':(158/255,99/255,181/255, 1)},
    '52':{'elSym':'Te', 'atmRad':1.23, 'ioRad':1.4, 'covRad':1.35, 'vdwRad':2.06, 'crystRad':1.11, 'color':(212/255,122/255,0/255, 1)},
    '53':{'elSym':'I', 'atmRad':1.15, 'ioRad':1.4, 'covRad':1.33, 'vdwRad':1.98, 'crystRad':2.06, 'color':(148/255,0/255,148/255, 1)},
    '54':{'elSym':'Xe', 'atmRad':1.08, 'ioRad':1.08, 'covRad':1.3, 'vdwRad':2.16, 'crystRad':0.62, 'color':(66/255,158/255,176/255, 1)},
    '55':{'elSym':'Cs', 'atmRad':2.98, 'ioRad':2.6, 'covRad':2.25, 'vdwRad':'VOID', 'crystRad':1.81, 'color':(87/255,23/255,143/255, 1)},
    '56':{'elSym':'Ba', 'atmRad':2.53, 'ioRad':2.15, 'covRad':1.98, 'vdwRad':'VOID', 'crystRad':1.49, 'color':(0/255,201/255,0/255, 1)},
    '57':{'elSym':'La', 'atmRad':1.95, 'ioRad':1.95, 'covRad':1.69, 'vdwRad':'VOID', 'crystRad':1.36, 'color':(112/255,212/255,255/255, 1)},
    '58':{'elSym':'Ce', 'atmRad':1.85, 'ioRad':1.85, 'covRad':'VOID', 'vdwRad':'VOID', 'crystRad':1.15, 'color':(255/255,255/255,199/255, 1)},
    '59':{'elSym':'Pr', 'atmRad':2.47, 'ioRad':1.85, 'covRad':'VOID', 'vdwRad':'VOID', 'crystRad':1.32, 'color':(217/255,255/255,199/255, 1)},
    '60':{'elSym':'Nd', 'atmRad':2.06, 'ioRad':1.85, 'covRad':'VOID', 'vdwRad':'VOID', 'crystRad':1.3, 'color':(199/255,255/255,199/255, 1)},
    '61':{'elSym':'Pm', 'atmRad':2.05, 'ioRad':1.85, 'covRad':'VOID', 'vdwRad':'VOID', 'crystRad':1.28, 'color':(163/255,255/255,199/255, 1)},
    '62':{'elSym':'Sm', 'atmRad':2.38, 'ioRad':1.85, 'covRad':'VOID', 'vdwRad':'VOID', 'crystRad':1.1, 'color':(143/255,255/255,199/255, 1)},
    '63':{'elSym':'Eu', 'atmRad':2.31, 'ioRad':1.85, 'covRad':'VOID', 'vdwRad':'VOID', 'crystRad':1.31, 'color':(97/255,255/255,199/255, 1)},
    '64':{'elSym':'Gd', 'atmRad':2.33, 'ioRad':1.8, 'covRad':'VOID', 'vdwRad':'VOID', 'crystRad':1.08, 'color':(69/255,255/255,199/255, 1)},
    '65':{'elSym':'Tb', 'atmRad':2.25, 'ioRad':1.75, 'covRad':'VOID', 'vdwRad':'VOID', 'crystRad':1.18, 'color':(48/255,255/255,199/255, 1)},
    '66':{'elSym':'Dy', 'atmRad':2.28, 'ioRad':1.75, 'covRad':'VOID', 'vdwRad':'VOID', 'crystRad':1.05, 'color':(31/255,255/255,199/255, 1)},
    '67':{'elSym':'Ho', 'atmRad':2.26, 'ioRad':1.75, 'covRad':'VOID', 'vdwRad':'VOID', 'crystRad':1.04, 'color':(0/255,255/255,156/255, 1)},
    '68':{'elSym':'Er', 'atmRad':2.26, 'ioRad':1.75, 'covRad':'VOID', 'vdwRad':'VOID', 'crystRad':1.03, 'color':(0/255,230/255,117/255, 1)},
    '69':{'elSym':'Tm', 'atmRad':2.22, 'ioRad':1.75, 'covRad':'VOID', 'vdwRad':'VOID', 'crystRad':1.02, 'color':(0/255,212/255,82/255, 1)},
    '70':{'elSym':'Yb', 'atmRad':2.22, 'ioRad':1.75, 'covRad':'VOID', 'vdwRad':'VOID', 'crystRad':1.13, 'color':(0/255,191/255,56/255, 1)},
    '71':{'elSym':'Lu', 'atmRad':2.17, 'ioRad':1.75, 'covRad':1.6, 'vdwRad':'VOID', 'crystRad':1, 'color':(0/255,171/255,36/255, 1)},
    '72':{'elSym':'Hf', 'atmRad':2.08, 'ioRad':1.55, 'covRad':1.5, 'vdwRad':'VOID', 'crystRad':0.85, 'color':(77/255,194/255,255/255, 1)},
    '73':{'elSym':'Ta', 'atmRad':2, 'ioRad':1.45, 'covRad':1.38, 'vdwRad':'VOID', 'crystRad':0.78, 'color':(77/255,166/255,255/255, 1)},
    '74':{'elSym':'W', 'atmRad':1.93, 'ioRad':1.35, 'covRad':1.46, 'vdwRad':'VOID', 'crystRad':0.74, 'color':(33/255,148/255,214/255, 1)},
    '75':{'elSym':'Re', 'atmRad':1.88, 'ioRad':1.35, 'covRad':1.59, 'vdwRad':'VOID', 'crystRad':0.77, 'color':(38/255,125/255,171/255, 1)},
    '76':{'elSym':'Os', 'atmRad':1.85, 'ioRad':1.3, 'covRad':1.28, 'vdwRad':'VOID', 'crystRad':0.77, 'color':(38/255,102/255,150/255, 1)},
    '77':{'elSym':'Ir', 'atmRad':1.8, 'ioRad':1.35, 'covRad':1.37, 'vdwRad':'VOID', 'crystRad':0.77, 'color':(23/255,84/255,135/255, 1)},
    '78':{'elSym':'Pt', 'atmRad':1.77, 'ioRad':1.35, 'covRad':1.28, 'vdwRad':1.75, 'crystRad':0.74, 'color':(208/255,208/255,224/255, 1)},
    '79':{'elSym':'Au', 'atmRad':1.74, 'ioRad':1.35, 'covRad':1.44, 'vdwRad':1.66, 'crystRad':1.51, 'color':(255/255,209/255,35/255, 1)},
    '80':{'elSym':'Hg', 'atmRad':1.71, 'ioRad':1.5, 'covRad':1.49, 'vdwRad':1.55, 'crystRad':0.83, 'color':(184/255,184/255,208/255, 1)},
    '81':{'elSym':'Tl', 'atmRad':1.56, 'ioRad':1.9, 'covRad':1.48, 'vdwRad':1.96, 'crystRad':1.03, 'color':(166/255,84/255,77/255, 1)},
    '82':{'elSym':'Pb', 'atmRad':1.54, 'ioRad':1.8, 'covRad':1.47, 'vdwRad':2.02, 'crystRad':1.49, 'color':(87/255,89/255,97/255, 1)},
    '83':{'elSym':'Bi', 'atmRad':1.43, 'ioRad':1.6, 'covRad':1.46, 'vdwRad':'VOID', 'crystRad':1.17, 'color':(158/255,79/255,181/255, 1)},
    '84':{'elSym':'Po', 'atmRad':1.35, 'ioRad':1.9, 'covRad':'VOID', 'vdwRad':'VOID', 'crystRad':1.08, 'color':(171/255,92/255,0/255, 1)},
    '85':{'elSym':'At', 'atmRad':1.27, 'ioRad':1.27, 'covRad':'VOID', 'vdwRad':'VOID', 'crystRad':0.76, 'color':(117/255,79/255,69/255, 1)},
    '86':{'elSym':'Rn', 'atmRad':1.2, 'ioRad':1.2, 'covRad':1.45, 'vdwRad':'VOID', 'crystRad':'VOID', 'color':(66/255,130/255,150/255, 1)},
    '87':{'elSym':'Fr', 'atmRad':'VOID', 'ioRad':'VOID', 'covRad':'VOID', 'vdwRad':'VOID', 'crystRad':1.94, 'color':(66/255,0/255,102/255, 1)},
    '88':{'elSym':'Ra', 'atmRad':'VOID', 'ioRad':2.15, 'covRad':'VOID', 'vdwRad':'VOID', 'crystRad':1.62, 'color':(0/255,125/255,0/255, 1)},
    '89':{'elSym':'Ac', 'atmRad':1.95, 'ioRad':1.95, 'covRad':'VOID', 'vdwRad':'VOID', 'crystRad':1.26, 'color':(112/255,171/255,250/255, 1)},
    '90':{'elSym':'Th', 'atmRad':1.8, 'ioRad':1.8, 'covRad':'VOID', 'vdwRad':'VOID', 'crystRad':1.19, 'color':(0/255,186/255,255/255, 1)},
    '91':{'elSym':'Pa', 'atmRad':1.8, 'ioRad':1.8, 'covRad':'VOID', 'vdwRad':'VOID', 'crystRad':1.09, 'color':(0/255,161/255,255/255, 1)},
    '92':{'elSym':'U', 'atmRad':1.75, 'ioRad':1.75, 'covRad':'VOID', 'vdwRad':1.86, 'crystRad':0.87, 'color':(0/255,143/255,255/255, 1)},
    '93':{'elSym':'Np', 'atmRad':1.75, 'ioRad':1.75, 'covRad':'VOID', 'vdwRad':'VOID', 'crystRad':'VOID', 'color':(0/255,128/255,255/255, 1)},
    '94':{'elSym':'Pu', 'atmRad':1.75, 'ioRad':1.75, 'covRad':'VOID', 'vdwRad':'VOID', 'crystRad':1, 'color':(0/255,107/255,255/255, 1)},
    '95':{'elSym':'Am', 'atmRad':1.75, 'ioRad':1.75, 'covRad':'VOID', 'vdwRad':'VOID', 'crystRad':1.12, 'color':(84/255,92/255,242/255, 1)},
    '96':{'elSym':'Cm', 'atmRad':'VOID', 'ioRad':'VOID', 'covRad':'VOID', 'vdwRad':'VOID', 'crystRad':1.11, 'color':(120/255,92/255,227/255, 1)}
   }
   
   
   def __init__(self, coord):
      ShowBase.__init__(self)
      
      self.molCoord = coord
      self.rad = 'covRad'
      
      displayRegion = self.win.makeDisplayRegion(0, 1, 0, 1)
      camNode = Camera('cam')
      camNP = NodePath(camNode)
      displayRegion.setCamera(camNP)
      camNP.reparentTo(self.camera)
      
      ambientLight = AmbientLight("ambientLight")
      ambientLight.setColor((.33, .33, .33, 1))
      directionalLight = DirectionalLight("directionalLight")
      directionalLight.setDirection(LVector3(1, 1, -2))
      directionalLight.setColor((1, 1, 1, 1))
      directionalLight.setSpecularColor((1, 1, 1, 1))
      render.setLight(render.attachNewNode(ambientLight))
      render.setLight(render.attachNewNode(directionalLight))
      render.setAntialias(AntialiasAttrib.MPolygon)
      
      self.drawAtoms()
         
   
   def changeRadius(self, rad):
     """
     (String) -> (None)
     Change the atomic radii and redraw the scene.
     """
     self.rad = rad
     render.getChildren().detach()
     #render.clearLight()
     self.camera.reparentTo(render)
     self.drawAtoms()
   
   def isNum(self, s):
     """
     (String) -> (Bool)
     Check if string is convertible to float.
     """
     try:
       eval(' '.join(s.split()).replace(' ', '+'))
       return True
     except SyntaxError as e:
       return False
     except NameError as e:
       return False
   
   
   def step(self):
     """
     (None) -> (None)
     Run the animation on scene.
     """
     taskMgr.step()
     
   
   def bindToWindow(self, windowHandle):
     """
     (None) -> (None)
     Run the animation on scene.
     """
     wp = WindowProperties().getDefault()
     wp.setOrigin(0, 0)
     wp.setSize(600, 400)
     wp.setParentWindow(windowHandle)
     base.openDefaultWindow(props=wp)
     self.wp = wp
   
   
   def drawAtoms(self):
      """
      (None) -> (None)
      Place spheres at the coordinates from .txt file.
      """
      arq = self.readCoordFile()
      boundx = [0]
      boundy = [0]
      boundz = [0]
      for i in arq:
        tmpBoundx = 0
        tmpBoundy = 0
        tmpBoundz = 0
        for j in arq[i]:
           particle = loader.loadModel("smiley.egg")
           particle.setTextureOff(1)
           particle.setColor(self.elements[j[1]]['color'])
           particle.setScale(self.elements[j[1]][self.rad])
           
           x = float(j[2]) + 1.5*boundx[-1]
           y = float(j[3]) + 1.5*boundy[-1]
           z = float(j[4]) + 1.5*boundz[-1]
           particle.reparentTo(render)
           particle.setPos(x, y, z)
           
           if abs(x) > tmpBoundx:
             tmpBoundx = abs(x)
           if abs(y) > tmpBoundy:
             tmpBoundy = abs(y)
           if abs(z) > tmpBoundz:
             tmpBoundz = abs(z)
           
           mat = Material()
           mat.setSpecular((.33, .33, .33, 1))
           mat.setShininess(50)
           particle.setMaterial(mat, 1)        
        
        boundx.append(tmpBoundx)
        boundy.append(tmpBoundy)
        boundz.append(tmpBoundz)
      self.trackball.node().setPos(0, 5*boundy[-1], 0)
   
   
   def readCoordFile(self):
      """
      (None) -> (Dict)
      Place spheres at the coordinates from .txt file.
      """
      arquivo = '{}.txt'.format(self.molCoord)
      with open(arquivo, 'r') as file:
            data = dict()
            mol = list()
            for line in file:
               linha = line.rstrip()
               if self.isNum(linha) == False:
                 if linha != '*' and '$' not in linha and len(linha.split()) != 0:
                   if len(mol) > 0:
                     data[numMol] = mol
                     mol = list()
                   numMol = linha.split()[0]
               else:
                 if len(linha.split()) > 1:
                   mol.append( linha.split()[:5] )
            data[numMol] = mol
            return data


class DialogWindow(QtGui.QDialog):
  def __init__(self, pandaCallback, pandaWorld, parent=None):
    super(QtGui.QDialog, self).__init__(parent)
    self.setWindowTitle("Molecule viewer")
    #self.setGeometry(0, 0, 600, 650)
    self.setFixedSize(600, 550)
    
    self.PW = pandaWorld
    
    self.quitButton = QtGui.QPushButton('Quit', self)
    self.connect(self.quitButton, QtCore.SIGNAL('clicked()'), self.close)
    
    self.pandaContainer = QtGui.QWidget(self)
    self.pandaContainer.setGeometry(0, 0, 600, 400)
    
    self.instructions = QtGui.QGridLayout()
    self.instructions.addWidget(QtGui.QLabel('<small><b>Mouse controls:</b><br/>Left: move   |   Middle: rotate   |   Right: zoom</small>'), 0, 0, 1, 1)
    
    self.instructionsFrame = QtGui.QFrame()
    self.instructionsFrame.setFrameShape(QtGui.QFrame.StyledPanel)
    self.instructionsFrame.setLayout(self.instructions)

    self.atmRad = QtGui.QRadioButton('Atomic', self)
    self.ioRad = QtGui.QRadioButton('Ionic', self)
    self.covRad = QtGui.QRadioButton('Covalent', self)
    self.crystRad = QtGui.QRadioButton('Crystal', self)
    
    self.covRad.toggle()    
    self.atmRad.clicked.connect(self.signalAtomic)
    self.ioRad.clicked.connect(self.signalIonic)
    self.covRad.clicked.connect(self.signalCovalent)
    self.crystRad.clicked.connect(self.signalCrystal)

    self.radiiOptions = QtGui.QHBoxLayout()
    self.radiiOptions.addWidget(self.atmRad)
    self.radiiOptions.addWidget(self.ioRad)
    self.radiiOptions.addWidget(self.covRad)
    self.radiiOptions.addWidget(self.crystRad)
    
    self.widgetRadiiOptions = QtGui.QGroupBox('Radii options', self)
    self.widgetRadiiOptions.setLayout(self.radiiOptions) 
    
    self.boxOuterFrame = QtGui.QGridLayout()
    self.boxOuterFrame.addWidget(self.widgetRadiiOptions, 0, 0, 1, 2)
    self.boxOuterFrame.addWidget(self.instructionsFrame, 1, 0, 1, 1)
    self.boxOuterFrame.addWidget(self.quitButton, 1, 1, 1, 1)
    
    self.buttonsFrame = QtGui.QWidget(self)
    self.buttonsFrame.setLayout(self.boxOuterFrame)
    self.buttonsFrame.setGeometry(0, 400, 600, 150)
    
    self.masterFrame = QtGui.QVBoxLayout()
    self.masterFrame.addWidget(self.pandaContainer)
    self.masterFrame.addWidget(self.buttonsFrame)
    
    timer =  QtCore.QTimer(self)
    self.connect( timer, QtCore.SIGNAL("timeout()"), pandaCallback )
    timer.start(0)
    
  
  def signalAtomic(self):
    """
    (None) -> (None)
    Emit signal to change atomic radii.
    """
    self.PW.changeRadius('atmRad')
  
  def signalIonic(self):
    """
    (None) -> (None)
    Emit signal to change atomic radii.
    """
    self.PW.changeRadius('ioRad')
  
  def signalCovalent(self):
    """
    (None) -> (None)
    Emit signal to change atomic radii.
    """
    self.PW.changeRadius('covRad')
  
  def signalCrystal(self):
    """
    (None) -> (None)
    Emit signal to change atomic radii.
    """
    self.PW.changeRadius('crystRad')


class mplCustomizedToolbar(NavigationToolbar):
  """
  Modify the default matplotlib toolbar excluding some buttons that implicitly do the same that interface is designed to.
  """
  toolitems = [ t for t in NavigationToolbar.toolitems if t[0] in ('Home', 'Pan', 'Zoom', 'Save', ) ]
  def __init__( self, *args, **kwargs ):
    super( mplCustomizedToolbar, self ).__init__( *args, **kwargs )
    self.layout().takeAt(4)



class graphMainWindow(QtGui.QMainWindow):
  """
  Main window environment.
  """
  
  typeGraphMenu = [
    'line', 
    'scatter',
    'histogram', 
    'autocorrelation'
    ]
  
  [grMenuItems,
  eijMenuItems,
  dataSet,
  labels,
  histogramTitles,
  plotTitles,
  dataTitles,
  xData,
  yData,
  nrData,
  viewAllCoord] = [ [] for i in range(11) ]

  extension = ''
  filename = ''
  integralMarker = False
  integralIndex = 0
  molDimAdjust = False
  horizontalGrLine = False

  # Information and values related to the last graph to be plotted.
  canvasInfo = {
    'type': '',
    'title': '',
    'data': [],
    'user parameters': '',
    'user data': [],
    'user boundaries': []
    }

  molViewStatus = 0

  def __init__(self, parent=None):
    super(graphMainWindow, self).__init__(parent)
    #QtGui.QShortcut(QtGui.QKeySequence('Shift+Return'), self, self.plot)
    #self.setWindowIcon(QtGui.QIcon('icone.png'))
    #icone.png -> https://www.dropbox.com/s/t4kyvv3uhpb3a4a/icone.png
    
    self.setWindowTitle('Interface')
    self.upperMenuBar()
    self.status = QtGui.QStatusBar()
    self.setStatusBar(self.status)
    
    self.form = None
    self.connect(self, QtCore.SIGNAL('pandastarted()'), self.spawnPanda)
    self.connect(self, QtCore.SIGNAL('pandaclosed()'), self.clearPanda)
    
    self.layoutElements()



  def layoutElements(self):
    """
    (None) -> None
    Set up the widgets that will compose the main window.
    """
    ## graph options widgets
    self.eijMenulLabel = QtGui.QLabel('Output list:')
    self.eijMenulLabel.hide()
    self.eijMenu = QtGui.QComboBox()
    self.eijMenu.addItems(self.eijMenuItems)
    self.eijMenu.setStyleSheet('QComboBox {combobox-popup: 0;}')
    self.eijMenu.setMaxVisibleItems(10)
    self.eijMenu.currentIndexChanged.connect(self.changeSimulationOutput)
    self.eijMenu.hide()

    self.dataXMenu = QtGui.QComboBox()
    self.dataXMenu.addItems(self.labels)
    self.dataXMenu.currentIndexChanged.connect(self.changeXData)

    self.dataYMenu = QtGui.QComboBox()
    self.dataYMenu.addItems(self.labels)
    self.dataYMenu.currentIndexChanged.connect(self.changeYData)

    self.intervalXMin = QtGui.QLineEdit()
    self.intervalXMax = QtGui.QLineEdit()
    self.intervalYMin = QtGui.QLineEdit()
    self.intervalYMax = QtGui.QLineEdit()

    self.plotXIntervalMin = QtGui.QLineEdit()
    self.plotXIntervalMax = QtGui.QLineEdit()
    self.plotYIntervalMin = QtGui.QLineEdit()
    self.plotYIntervalMax = QtGui.QLineEdit()


    ## histogram options widgets
    self.histIndexMin = QtGui.QDoubleSpinBox()
    self.histIndexMin.setDecimals(0)
    self.histIndexMin.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)

    self.histIndexMax = QtGui.QDoubleSpinBox()
    self.histIndexMax.setDecimals(0)
    self.histIndexMax.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)

    self.binValue = QtGui.QDoubleSpinBox()
    self.binValue.setDecimals(0)
    self.binValue.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)


    ## autocorrelation options widgets
    self.largestT = QtGui.QLineEdit()
    
    self.expMenu = QtGui.QComboBox()
    self.expMenu.addItems([
      'A1*exp(-t/B1)', 
      'A1*exp(-t/B1)+A2*exp(-t/B2)',
      'A1*exp(-t/B1)+A2*exp(-t/B2)+A3*exp(-t/B3)'
      ])
    self.expMenu.currentIndexChanged.connect(self.changeFitParameters)
    
    self.A1 = QtGui.QLineEdit()
    self.A1.setPlaceholderText('A1')
    self.A1.setEnabled(True)
    
    self.A2 = QtGui.QLineEdit()
    self.A2.setPlaceholderText('A2')
    self.A2.setEnabled(False)
    
    self.A3 = QtGui.QLineEdit()
    self.A3.setPlaceholderText('A3')
    self.A3.setEnabled(False)
    
    self.B1 = QtGui.QLineEdit()
    self.B1.setPlaceholderText('B1')
    self.B1.setEnabled(True)
    
    self.B2 = QtGui.QLineEdit()
    self.B2.setPlaceholderText('B2')
    self.B2.setEnabled(False)
    
    self.B3 = QtGui.QLineEdit()
    self.B3.setPlaceholderText('B3')
    self.B3.setEnabled(False)
    
    self.buttonApply = QtGui.QPushButton('Apply')
    self.buttonApply.clicked.connect(self.applyUserParameters)
    
    self.largestTLabel = QtGui.QLabel('')
    
    ## rdf widgets
    self.grMenu = QtGui.QComboBox()
    self.grMenu.addItems(self.grMenuItems)
    self.grMenu.setStyleSheet('QComboBox {combobox-popup: 0;}')
    self.grMenu.setMaxVisibleItems(10)
    self.grMenu.currentIndexChanged.connect(self.changeXData)
    self.grMenu.currentIndexChanged.connect(self.changeYData)

    self.molDimA = QtGui.QLineEdit()
    self.molDimB = QtGui.QLineEdit()
    self.molDimC = QtGui.QLineEdit()
    
    self.buttonApplyRDF = QtGui.QPushButton('Apply')
    self.buttonApplyRDF.clicked.connect(self.applyMolDim)
    
    
    ## ueff widgets
    self.temperature = QtGui.QLineEdit()
    self.temperature.setText('298.0')
    
    ## canvas widgets
    self.graphxyFrame = QtGui.QWidget()
    self.graphxyFigure = Figure(facecolor='white', dpi=72)
    self.graphxyFigure.set_size_inches(8.0, 5.5)
    self.graphxyCanvas = FigureCanvas(self.graphxyFigure)
    self.graphxyAxes = self.graphxyFigure.add_subplot(111, axisbg='white')
    self.graphxyCanvas.setParent(self.graphxyFrame)
    self.cid = self.graphxyFigure.canvas.mpl_connect('button_press_event', self.clickIntegral)
    self.mpl_toolbar = mplCustomizedToolbar(self.graphxyCanvas, self.graphxyFrame)
    
    self.checkOverplot = QtGui.QCheckBox('Overplot')

    self.buttonRedefinePlotInterval = QtGui.QPushButton('Apply')
    self.buttonRedefinePlotInterval.clicked.connect(self.applyCanvasBoundaries)

    self.buttonViewAll = QtGui.QPushButton('View all')
    self.buttonViewAll.clicked.connect(self.viewAll)
    
    ## output widgets
    self.oa1 = QtGui.QLabel('A1=')
    self.oa2 = QtGui.QLabel('A2=')
    self.oa3 = QtGui.QLabel('A3=')
    self.ob1 = QtGui.QLabel('B1=')
    self.ob2 = QtGui.QLabel('B2=')
    self.ob3 = QtGui.QLabel('B3=')
    
    self.fittingLabel = QtGui.QLabel('fitting<br/>parameters')
    
    self.integralLabel = QtGui.QLabel('')
    
    self.meanLabel = QtGui.QLabel('')
    
    self.stdDeviationLabel = QtGui.QLabel('')

    self.typeGraph = QtGui.QComboBox()
    self.typeGraph.addItems(self.typeGraphMenu)
    self.typeGraph.currentIndexChanged.connect(self.changeDefaultBoundaries)

    self.buttonPlot = QtGui.QPushButton('Show')
    self.buttonPlot.clicked.connect(self.plot)
    
    self.buttonSave = QtGui.QPushButton('Save')
    self.buttonSave.clicked.connect(self.savePlotData)
    
    self.intervalXMin.returnPressed.connect(self.plot)
    self.intervalXMax.returnPressed.connect(self.plot)
    self.intervalYMin.returnPressed.connect(self.plot)
    self.intervalYMax.returnPressed.connect(self.plot)

    self.plotXIntervalMin.returnPressed.connect(self.applyCanvasBoundaries)
    self.plotXIntervalMax.returnPressed.connect(self.applyCanvasBoundaries)
    self.plotYIntervalMin.returnPressed.connect(self.applyCanvasBoundaries)
    self.plotYIntervalMax.returnPressed.connect(self.applyCanvasBoundaries)
    
    self.A1.returnPressed.connect(self.applyUserParameters)
    self.A2.returnPressed.connect(self.applyUserParameters)
    self.A3.returnPressed.connect(self.applyUserParameters)
    self.B1.returnPressed.connect(self.applyUserParameters)
    self.B2.returnPressed.connect(self.applyUserParameters)
    self.B3.returnPressed.connect(self.applyUserParameters)
    self.largestT.returnPressed.connect(self.applyUserParameters)

    self.molDimA.returnPressed.connect(self.applyMolDim)
    self.molDimA.setPlaceholderText('A') 
    self.molDimB.returnPressed.connect(self.applyMolDim)
    self.molDimB.setPlaceholderText('B')
    self.molDimC.returnPressed.connect(self.applyMolDim)
    self.molDimC.setPlaceholderText('C')

    #    
    AllEntries = [
      self.intervalXMin,
      self.intervalXMax, 
      self.intervalYMin, 
      self.intervalYMax, 
      self.plotXIntervalMin, 
      self.plotXIntervalMax, 
      self.plotYIntervalMin, 
      self.plotYIntervalMax,
      self.largestT,
      self.A1,
      self.A2,
      self.A3,
      self.B1,
      self.B2,
      self.B3,
      self.molDimA,
      self.molDimB,
      self.molDimC,
      self.temperature
      ]
    for e in AllEntries:
      e.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
    
    
    self.horizontalLine = QtGui.QFrame()
    self.horizontalLine.setFrameShape(QtGui.QFrame.HLine)
    self.horizontalLine.setFrameShadow(QtGui.QFrame.Sunken)
    self.blankWidget = QtGui.QWidget()

    ## graph options frame
    self.gridGraphEntries = QtGui.QGridLayout()
    self.gridGraphEntries.addWidget(self.eijMenulLabel, 0, 0, 1, 1, QtCore.Qt.AlignHCenter)
    self.gridGraphEntries.addWidget(self.eijMenu, 0, 1, 1, 4)
    self.gridGraphEntries.addWidget(QtGui.QLabel('<small>x-axis</small>'), 1, 1, 1, 1, QtCore.Qt.AlignHCenter)
    self.gridGraphEntries.addWidget(QtGui.QLabel('<small>y-axis</small>'), 1, 4, 1, 1, QtCore.Qt.AlignHCenter)
    self.gridGraphEntries.addWidget(QtGui.QLabel('Data'), 2, 0, 1, 1, QtCore.Qt.AlignHCenter)
    self.gridGraphEntries.addWidget(self.dataXMenu, 2, 1, 1, 1)
    self.gridGraphEntries.addWidget(QtGui.QLabel('Min. value:'), 3, 0, 1, 1, QtCore.Qt.AlignRight)
    self.gridGraphEntries.addWidget(QtGui.QLabel('Max. value:'), 4, 0, 1, 1, QtCore.Qt.AlignRight)
    self.gridGraphEntries.addWidget(self.intervalXMin, 3, 1, 1, 1)
    self.gridGraphEntries.addWidget(self.intervalXMax, 4, 1, 1, 1)
    self.gridGraphEntries.addWidget(QtGui.QLabel('<b>Data<b/>'), 2, 3, 1, 1, QtCore.Qt.AlignHCenter)
    self.gridGraphEntries.addWidget(self.dataYMenu, 2, 4, 1, 1)
    self.gridGraphEntries.addWidget(QtGui.QLabel('Min. value:'), 3, 3, 1, 1, QtCore.Qt.AlignRight)
    self.gridGraphEntries.addWidget(QtGui.QLabel('Max. value:'), 4, 3, 1, 1, QtCore.Qt.AlignRight)
    self.gridGraphEntries.addWidget(self.intervalYMin, 3, 4, 1, 1)
    self.gridGraphEntries.addWidget(self.intervalYMax, 4, 4, 1, 1)
    
    self.widgetButtonsEntries = QtGui.QGroupBox('Line and Scatter options')
    self.widgetButtonsEntries.setLayout(self.gridGraphEntries)
    
    ## histogram options frame
    self.gridHistogramEntries = QtGui.QGridLayout()
    self.gridHistogramEntries.addWidget(QtGui.QLabel('Num. of bins:'), 0, 0, 2, 1, QtCore.Qt.AlignRight)
    self.gridHistogramEntries.addWidget(self.binValue, 0, 1, 2, 1, QtCore.Qt.AlignVCenter)
    self.gridHistogramEntries.addWidget(QtGui.QLabel('Min. index:'), 0, 2, 1, 1, QtCore.Qt.AlignRight)
    self.gridHistogramEntries.addWidget(self.histIndexMin, 0, 3, 1, 1)
    self.gridHistogramEntries.addWidget(QtGui.QLabel('Max. index:'), 1, 2, 1, 1, QtCore.Qt.AlignRight)
    self.gridHistogramEntries.addWidget(self.histIndexMax, 1, 3, 1, 1)
    
    self.widgetHistogramEntries = QtGui.QGroupBox('Histogram options')
    self.widgetHistogramEntries.setLayout(self.gridHistogramEntries)
    
    ## autocorrelation options frame    
    self.gridAutoCorrEntries = QtGui.QGridLayout()
    self.gridAutoCorrEntries.addWidget(QtGui.QLabel('Fit type:'), 1, 0, 1, 1, QtCore.Qt.AlignRight)
    self.gridAutoCorrEntries.addWidget(self.expMenu, 1, 1, 1, 4)
    self.gridAutoCorrEntries.addWidget(QtGui.QLabel('A:'), 2, 0, 1, 1, QtCore.Qt.AlignRight)
    self.gridAutoCorrEntries.addWidget(self.A1, 2, 1, 1, 1)
    self.gridAutoCorrEntries.addWidget(self.A2, 2, 2, 1, 1)
    self.gridAutoCorrEntries.addWidget(self.A3, 2, 3, 1, 1)
    self.gridAutoCorrEntries.addWidget(QtGui.QLabel('B:'), 3, 0, 1, 1, QtCore.Qt.AlignRight)
    self.gridAutoCorrEntries.addWidget(self.B1, 3, 1, 1, 1)
    self.gridAutoCorrEntries.addWidget(self.B2, 3, 2, 1, 1)
    self.gridAutoCorrEntries.addWidget(self.B3, 3, 3, 1, 1)
    self.gridAutoCorrEntries.addWidget(QtGui.QLabel('Largest t:'), 4, 0, 1, 1, QtCore.Qt.AlignRight)
    self.gridAutoCorrEntries.addWidget(self.largestT, 4, 1, 1, 1)
    self.gridAutoCorrEntries.addWidget(self.largestTLabel, 4, 2, 1, 2)
    self.gridAutoCorrEntries.addWidget(self.buttonApply, 4, 3, 1, 1)
    
    self.widgetAutoCorrEntries = QtGui.QGroupBox('Autocorrelation options')
    self.widgetAutoCorrEntries.setLayout(self.gridAutoCorrEntries)
    
    ## rdf options frame
    self.gridGr = QtGui.QGridLayout()
    self.gridGr.addWidget(self.grMenu, 0, 0, 1, 3)
    self.gridGr.addWidget(QtGui.QLabel('<small>MOLECULAR DIMENSIONS</small>'), 1, 0, 1, 3, QtCore.Qt.AlignLeft)
    #self.gridGr.addWidget(QtGui.QLabel('A:'), 2, 0, 1, 1, QtCore.Qt.AlignRight)
    self.gridGr.addWidget(self.molDimA, 2, 0, 1, 1)
    #self.gridGr.addWidget(QtGui.QLabel('B:'), 2, 2, 1, 1, QtCore.Qt.AlignRight)
    self.gridGr.addWidget(self.molDimB, 2, 1, 1, 1)
    #self.gridGr.addWidget(QtGui.QLabel('C:'), 2, 4, 1, 1, QtCore.Qt.AlignRight)
    self.gridGr.addWidget(self.molDimC, 2, 2, 1, 1)
    self.gridGr.addWidget(self.buttonApplyRDF, 3, 2, 1, 1)
    self.gridGr.addWidget(QtGui.QLabel('<b>Ueff options</b>'), 4, 0, 1, 3)
    self.gridGr.addWidget(QtGui.QLabel('Temperature:'), 5, 0, 1, 1, QtCore.Qt.AlignRight)
    self.gridGr.addWidget(self.temperature, 5, 1, 1, 1)
    self.gridGr.addWidget(QtGui.QLabel('K'), 5, 2, 1, 1)
    #self.gridGr.setColumnStretch(0, 2)
    #self.gridGr.setColumnStretch(1, 1)
    #self.gridGr.setColumnStretch(2, 2)
    
    self.widgetGr = QtGui.QGroupBox('RDF options')
    self.widgetGr.setLayout(self.gridGr)
    self.widgetGr.hide()
    
    ## Ueff options frame
    #self.gridUeff = QtGui.QUeffidLayout()
    #self.gridUeff.addWidget(QtGui.QLabel('Temperature'), 0, 0, 1, 1)
    #self.gridUeff.addWidget(self.temperature, 0, 1, 1, 1)
    #self.gridUeff.addWidget(QtGui.QLabel('K'), 0, 3, 1, 1)
    
    #self.widgetUeff = QtGui.QUeffoupBox('Ueff options')
    #self.widgetUeff.setLayout(self.gridUeff)
    #self.widgetUeff.hide()
    
    ## type of graph
    self.gridTypeOfGraph = QtGui.QGridLayout()
    self.gridTypeOfGraph.addWidget(self.typeGraph, 0 , 0, 1, 1)
    self.gridTypeOfGraph.addWidget(self.buttonPlot, 0, 1, 1, 1)
    self.gridTypeOfGraph.addWidget(self.buttonSave, 0, 2, 1, 1)
    self.gridTypeOfGraph.setColumnStretch(0, 2)
    self.gridTypeOfGraph.setColumnStretch(1, 1)
    self.gridTypeOfGraph.setColumnStretch(2, 1)
    
    self.widgetTypeOfGraph = QtGui.QGroupBox('Graph options')
    self.widgetTypeOfGraph.setLayout(self.gridTypeOfGraph)
    
    ## output frame
    self.gridOutput = QtGui.QGridLayout()
    self.gridOutput.addWidget(self.meanLabel, 1, 0, 1, 2)
    self.gridOutput.addWidget(self.stdDeviationLabel, 1, 2, 1, 2)
    self.gridOutput.addWidget(self.integralLabel, 0, 0, 1, 1)
    self.gridOutput.addWidget(self.fittingLabel, 2, 0, 2, 1, QtCore.Qt.AlignHCenter)
    self.gridOutput.addWidget(self.oa1, 2, 1, 1, 1)
    self.gridOutput.addWidget(self.oa2, 2, 2, 1, 1)
    self.gridOutput.addWidget(self.oa3, 2, 3, 1, 1)
    self.gridOutput.addWidget(self.ob1, 3, 1, 1, 1)
    self.gridOutput.addWidget(self.ob2, 3, 2, 1, 1)
    self.gridOutput.addWidget(self.ob3, 3, 3, 1, 1)
    
    self.widgetOutput = QtGui.QFrame()
    self.widgetOutput.setFrameShape(QtGui.QFrame.StyledPanel)
    self.widgetOutput.setLayout(self.gridOutput)
    
    ## graph intervals frame
    self.gridAxesIntervals = QtGui.QGridLayout()
    self.gridAxesIntervals.addWidget(QtGui.QLabel('Min. X:'), 0, 0, 1, 1, QtCore.Qt.AlignRight)
    self.gridAxesIntervals.addWidget(self.plotXIntervalMin, 0, 1, 1, 1)
    self.gridAxesIntervals.addWidget(QtGui.QLabel('Max. X:'), 0, 2, 1, 1, QtCore.Qt.AlignRight)
    self.gridAxesIntervals.addWidget(self.plotXIntervalMax, 0, 3, 1, 1)
    self.gridAxesIntervals.addWidget(QtGui.QLabel('Min. Y:'), 1, 0, 1, 1, QtCore.Qt.AlignRight)
    self.gridAxesIntervals.addWidget(self.plotYIntervalMin, 1, 1, 1, 1)
    self.gridAxesIntervals.addWidget(QtGui.QLabel('Max. Y:'), 1, 2, 1, 1, QtCore.Qt.AlignRight)
    self.gridAxesIntervals.addWidget(self.plotYIntervalMax, 1, 3, 1, 1)
    self.gridAxesIntervals.addWidget(self.buttonRedefinePlotInterval, 0, 4, 2, 1)
    
    self.widgetAxesIntervals = QtGui.QGroupBox('Axes range options')
    self.widgetAxesIntervals.setLayout(self.gridAxesIntervals)
    
    ## canvas frame
    self.boxGraph = QtGui.QGridLayout()
    self.boxGraph.addWidget(self.mpl_toolbar, 0, 0, 1, 3)
    self.boxGraph.addWidget(self.horizontalLine, 1, 0, 1, 3)
    self.boxGraph.addWidget(self.graphxyCanvas, 2, 0, 1, 3)
    self.boxGraph.addWidget(self.checkOverplot, 3, 0, 1, 1)
    self.boxGraph.addWidget(self.buttonViewAll, 3, 2, 1, 1, QtCore.Qt.AlignRight)
    self.boxGraph.addWidget(self.widgetAxesIntervals, 6, 0, 1, 3)
    self.boxGraph.setColumnStretch(0, 2)
    self.boxGraph.setColumnStretch(1, 1)
    self.boxGraph.setColumnStretch(2, 2)
    
    self.frameGraph = QtGui.QFrame()
    self.frameGraph.setFrameShape(QtGui.QFrame.StyledPanel)
    self.frameGraph.setLayout(self.boxGraph)
    self.frameGraph.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
    
    ##
    self.boxOuterFrame = QtGui.QGridLayout()
    self.boxOuterFrame.addWidget(self.widgetButtonsEntries, 0, 0, 1, 1)
    self.boxOuterFrame.addWidget(self.widgetHistogramEntries, 1, 0, 1, 1)
    self.boxOuterFrame.addWidget(self.widgetAutoCorrEntries, 2, 0, 1, 1)
    self.boxOuterFrame.addWidget(self.widgetGr, 2, 0, 1, 1)
    self.boxOuterFrame.addWidget(self.widgetTypeOfGraph, 3, 0, 1, 1)
    self.boxOuterFrame.addWidget(self.widgetOutput, 4 , 0, 1, 1)
    self.boxOuterFrame.addWidget(self.frameGraph, 0, 1, 5, 1)   
    
    self.mainFrame = QtGui.QWidget()
    self.mainFrame.setLayout(self.boxOuterFrame)
    self.mainFrame.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)

    self.setCentralWidget(self.mainFrame)
    self.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
  


  def upperMenuBar(self):
    """
    (None) -> None
    Set up the widgets that will compose the upper menu.
    """
    upperMenuBar = self.menuBar()
    
    menuFile = upperMenuBar.addMenu('&File')

    openAction = QtGui.QAction('Open...', self)
    openAction.setShortcut('Ctrl+O')
    openAction.triggered.connect(self.selectDataFile)
    menuFile.addAction(openAction)
    menuFile.addSeparator()

    saveDataAs = QtGui.QAction('Save data', self)
    saveDataAs.setShortcut('Ctrl+S')
    saveDataAs.triggered.connect(self.savePlotData)
    menuFile.addAction(saveDataAs)
    menuFile.addSeparator()

    closeAction = QtGui.QAction('Close', self)
    closeAction.setShortcut('Ctrl+C')
    menuFile.addAction(closeAction)
    
    menuAbout = upperMenuBar.addMenu('&About')
    infoAction = QtGui.QAction('Info', self)
    infoAction.triggered.connect(self.aboutWindow)
    menuAbout.addAction(infoAction)
  


  def aboutWindow(self):
    """
    (None) -> None
    Create a pop-up window containing information about the interface.
    """
    info = QtGui.QMessageBox()
    info.setWindowTitle('About')
    info.setText('Application written in Python<br/><br/> \
                  Authors: Thiago Duarte and Kaline Coutinho<br/> \
                  Institution: Physics Institute, University of Sao Paulo<br/> \
                  Funding: CNPq-PIBIC<br/> \
                  Year: 2015<br/><br/> \
                  Last modified date: July 22, 2017')
    info.setIcon(1)
    info.exec_()



  def readFile(self):
    """
    (None) -> List, List, List, List, String, String
    Create a window that allows the user to select the file which will be read. Return the data read and file name information.
    """
    openFile = QtGui.QFileDialog()
    openFile.setFileMode(QtGui.QFileDialog.ExistingFile)
    openFile.setViewMode(0)
    selectedFileName = openFile.getOpenFileName()
    
    if selectedFileName:
      [labels, dataRows, finalDataSet, grItems, eijItems, tempLabels, dataSample, finalLabels, dataBlock] = [[] for i in range(0,9)]
      filename = str((selectedFileName.split('.'))[0])
      extension = str((selectedFileName.split('.'))[-1])

      # *.out files
      if (extension == 'out'):
        with open(selectedFileName, 'rt') as f:
          for line in f:
            if '#N' in line:
              lineReadLabels = line.rstrip()
              dataRows.append(lineReadLabels.split()[:-1])
            if 'NMOVE' in line:
              lineReadData = line.rstrip()
              labels = lineReadData.split()
        for i in range(0, len(dataRows[0])):
          finalDataSet.append([float(r[i]) for r in dataRows])

      # *.dst files
      elif (extension == 'dst'):
        with open(selectedFileName, 'rt') as f:
          for i in range(0, 5):
            # 5 is an arbitrary number of lines to read in order to get the columns titles.
            lineRead = ((f.readline()).rstrip()).split()
            if 'Mol' in lineRead:
              tempLabels = lineRead
            else:
              dataSample = lineRead
          indexes = [i for i, v in enumerate(dataSample) if not '.' in v]
          for i, v in enumerate(tempLabels):
            if i in indexes:
              tempLabels[i] = 'REMOVE'
          labels = [i for i in tempLabels if i != 'REMOVE']
          f.seek(0, 0)
          for line in f:
            if not 'Mol' in line:
              dataRows.append([i for i in ((line.rstrip()).split()) if '.' in i])
        for i in range(0, len(dataRows[0])):
          finalDataSet.append([float(r[i]) for r in dataRows])

      # *.hbd files
      elif (extension == 'hbd'):
        with open(selectedFileName, 'rt') as f:
          for i in range(0, 5):
            # 5 is an arbitrary number of lines to read in order to get the columns titles.
            lineRead = ((f.readline()).rstrip())
            if '#' in lineRead:
              if not 'Criteria' in lineRead:
                tempLabels = lineRead.split()[1:]
            else:
              lineRead = re.sub('\\s+(?=[^()]*\\))', '', lineRead.replace('(', ' ('))
              dataSample = lineRead.split()
          indexes = [i for i, v in enumerate(dataSample) if not '.' in v]
          for i, v in enumerate(tempLabels):
            if i in indexes:
              tempLabels[i] = 'REMOVE'
          labels = [i for i in tempLabels if i != 'REMOVE']
          f.seek(0, 0)
          for line in f:
            if not '#' in line:
              dataRows.append([i for i in ((line.rstrip()).split()) if '.' in i])
        for i in range(0, len(dataRows[0])):
          finalDataSet.append([float(r[i]) for r in dataRows])

      # *.avr files
      elif extension == 'avr':
        with open(selectedFileName,'rt') as f:
          for line in f:
            if 'NMOVE' in line:
              lineReadData = line.rstrip()
              labels = lineReadData.split()
            else:
              lineRead = line.rstrip()
              dataRows.append(lineRead.split())
        for i in range(0, len(dataRows[0])):
          finalDataSet.append([float(r[i]) for r in dataRows])

      # *.gr files
      elif extension == 'gr':
        with open(selectedFileName,'rt') as f:
          for line in f:
            if '# RDF ' in line.strip():
              lineReadLabels = line.rstrip()
              labelsList = lineReadLabels.split()
              labels = ''
              for i, v in enumerate(labelsList):
                if (v == 'atom'):
                  labels += '{}{}'.format(labelsList[i+1], labelsList[i+2])
                if (v == 'and'):
                  labels += '-{}{}'.format(labelsList[i+1], labelsList[i+2])
                if v == 'type':
                   labels += '({})'.format(labelsList[i+1])
              grItems.append(labels)
              labels = ['r','G(r)','N(r)']
              if len(dataBlock) != 0:
                finalDataSet.append(dataBlock)
                dataBlock = []
            elif '# RDFs ' not in line.strip():
              dataRow = line.rstrip()
              if dataRow != '':
                dataBlock.append(dataRow.split())
          finalDataSet.append(dataBlock)

      # *.eij files
      elif (((extension)[0]) == 'e') and ((((extension)[-2:]) == 'ij') or (((extension)[-2:]).isdigit() == True)):
        with open(selectedFileName,'rt') as f:
          count = 0
          for line in f:
            if 'NMOVE' in line.strip():
              lineReadData = line.rstrip()
              labels.append(lineReadData.split())
              count += 1
              eijItems.append('Simulation output {}'.format(count))
              if len(dataRows) > 0:
                dataBlock.append(dataRows)
                dataRows = []
            else:
              lineReadData = line.rstrip()
              dataRows.append(lineReadData.split())
          dataBlock.append(dataRows)
          for i, v in enumerate(labels):
            dataColumn = []
            for j, w in enumerate(v):
              tempColumn = []
              for k in dataBlock[i]:
                tempColumn.append(float(k[j]))
              dataColumn.append(tempColumn)
            finalDataSet.append(dataColumn)
    
      # *.txt files
      elif extension == 'txt':
        self.molViewStatus += 1
        pass
    
    try:
      return labels, finalDataSet, grItems, eijItems, extension, filename
    except (UnboundLocalError) as e:
      None

  
  
  def selectDataFile(self):
    """
    (None) -> None
    Fill the main lists with the data read from files and change layout according to the selected file extension.
    """
    try:
      self.xData, self.yData = [], []
      self.labels, self.dataSet, self.grMenuItems, self.eijMenuItems, self.extension, self.filename = self.readFile()

      if (self.extension == 'txt'):
        if self.molViewStatus > 1:
          self.scene.destroy()
        self.spawnPanda()
        
      
      elif (self.extension == 'gr'):
        self.typeGraphMenu = [
          'line', 
          'scatter',
          'histogram',
          'ueff'
          ]
        self.default('gr')
        self.widgetGr.show()
        self.widgetAutoCorrEntries.hide()
        self.eijMenu.hide()
        self.eijMenulLabel.hide()
        self.fittingLabel.hide()
        self.oa1.hide()
        self.oa2.hide()
        self.oa3.hide()
        self.ob1.hide()
        self.ob2.hide()
        self.ob3.hide()

        
      elif (len(self.eijMenuItems) != 0):
        self.typeGraphMenu = [
          'line', 
          'scatter',
          'histogram', 
          'autocorrelation'
          ]
        
        self.eijLabels = self.labels
        self.labels = self.eijLabels[0]
        
        self.eijMenu.setCurrentIndex(0)  
        self.default('normal')
        self.widgetAutoCorrEntries.show()
        self.widgetGr.hide()
        self.eijMenu.show()
        self.eijMenulLabel.show()
        self.fittingLabel.show()
        self.oa1.show()
        self.oa2.show()
        self.oa3.show()
        self.ob1.show()
        self.ob2.show()
        self.ob3.show()

      else:
        self.typeGraphMenu = [
          'line', 
          'scatter',
          'histogram', 
          'autocorrelation'
          ]
        self.default('normal')
        self.widgetAutoCorrEntries.show()
        self.widgetGr.hide()
        self.eijMenu.hide()
        self.eijMenulLabel.hide()
        self.fittingLabel.show()
        self.oa1.show()
        self.oa2.show()
        self.oa3.show()
        self.ob1.show()
        self.ob2.show()
        self.ob3.show()

      gmw = graphMainWindow()
      self.resize(gmw.minimumSizeHint())
    except TypeError as e:
      self.status.showMessage('ERROR: failed to open file.', 3456)
    except ValueError as e:
      self.status.showMessage('ERROR: failed to open file.', 3456)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# MOLECULAR VIEWER                                                                #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  def spawnPanda(self):                                                           #
    """
    (None) -> None
    Invoke the molecular viewer main window.
    """
    self.scene = Scene(self.filename)                                   #
    self.form = DialogWindow(self.scene.step, self.scene)                         #
    self.scene.bindToWindow(int(self.form.winId()))                               #
    self.connect(self.form, QtCore.SIGNAL('pandaclosed()'), self.closePanda)      #
    self.form.show()                                                              #

  
  def closePanda(self):                                                           #
    """
    (None) -> None
    Close the molecular viewer main window.
    """
    self.emit(QtCore.SIGNAL('pandaclosed()'))                                     #
  
  
  def clearPanda(self):                                                           #
    """
    (None) -> None
    Clear the molecular viewer main window content.
    """
    del self.form                                                                 #
    self.form = None                                                              #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  
  
  def default(self, plotType):
    """
    (String) -> None
    Set up the default values and show the first graph according to the selected file extension.
    """
    if (plotType == 'normal'):
      self.layoutElements()
      self.dataXMenu.setEnabled(True)
      self.integralLabel.hide()
      
      self.dataXMenu.setCurrentIndex(0)
      self.dataYMenu.setCurrentIndex(1)
      
      self.updateData()
      self.intervalXMin.setText(str(min(self.xData)))
      self.intervalXMax.setText(str(max(self.xData)))
      self.intervalYMin.setText(str(min(self.yData)))
      self.intervalYMax.setText(str(max(self.yData)))

      self.histIndexMin.setMinimum(0)
      self.histIndexMin.setMaximum(len(self.yData) - 1)
      self.histIndexMin.setValue(0)
      self.histIndexMax.setMinimum(0)
      self.histIndexMax.setMaximum(len(self.yData) - 1)
      self.histIndexMax.setValue(len(self.yData) - 1)
      self.binValue.setMinimum(1)
      self.binValue.setMaximum(999)
      self.binValue.setValue(50)

      self.plotXIntervalMin.setText(str(min(self.xData)))
      self.plotXIntervalMax.setText(str(max(self.xData)))
      self.plotYIntervalMin.setText(str(min(self.yData)))
      self.plotYIntervalMax.setText(str(max(self.yData)))
          
      self.plot()

    elif (plotType == 'gr'):
      self.layoutElements()
      self.dataXMenu.setEnabled(False)
      self.integralLabel.show()

      self.grMenu.setCurrentIndex(1)
      self.dataXMenu.setCurrentIndex(0)
      self.dataYMenu.setCurrentIndex(1)
      
      self.updateData()
      self.intervalXMin.setText(str(min(self.xData)))
      self.intervalXMax.setText(str(max(self.xData)))
      self.intervalYMin.setText(str(min(self.yData)))
      self.intervalYMax.setText(str(max(self.yData)))
      
      self.histIndexMin.setMinimum(0)
      self.histIndexMin.setMaximum(len(self.yData) - 1)
      self.histIndexMin.setValue(0)
      self.histIndexMax.setMinimum(0)
      self.histIndexMax.setMaximum(len(self.yData) - 1)
      self.histIndexMax.setValue(len(self.yData) - 1)
      self.binValue.setMinimum(1)
      self.binValue.setMaximum(999)
      self.binValue.setValue(50)

      self.plotXIntervalMin.setText(str(min(self.xData)))
      self.plotXIntervalMax.setText(str(max(self.xData)))
      self.plotYIntervalMin.setText(str(min(self.yData)))
      self.plotYIntervalMax.setText(str(max(self.yData)))
      
      self.plot()



  def updateData(self):
    """
    (None) -> None
    Fill the menus with the data read from selected file.
    """
    try:
      if (self.extension == 'gr'):
        [self.xData,
         self.yData,
         self.nrData] = [[] for i in range(0, 3)]

        i = int(self.grMenu.currentIndex())
        j = int(self.dataXMenu.currentIndex())
        k = int(self.dataYMenu.currentIndex())
        for v in (self.dataSet[i]):
          self.xData.append(float(v[j]))
          self.yData.append(float(v[k]))
          self.nrData.append(float(v[2]))
      
      elif (self.extension[0] == 'e'):
        [self.xData, self.yData] = [[] for i in range(0, 2)]
        
        i = int(self.eijMenu.currentIndex())
        j = int(self.dataXMenu.currentIndex())
        k = int(self.dataYMenu.currentIndex())
        self.labels = self.eijLabels[i]
        self.xData = self.dataSet[i][j]
        self.yData = self.dataSet[i][k]
      
      else:
        j = int(self.dataXMenu.currentIndex())
        k = int(self.dataYMenu.currentIndex())
        self.xData = self.dataSet[j]
        self.yData = self.dataSet[k]
    except (IndexError) as e:
      self.status.showMessage('ERROR: unable to load or update data. Please try to check if any file was already loaded.', 3456)



  def dataProcessing(self):
    """
    (None) -> List
    Filter data from datasets according to values from 'Line and Scatter options'.
    """
    try:
      xMIN = float(self.intervalXMin.text())
      xMAX = float(self.intervalXMax.text())
      yMIN = float(self.intervalYMin.text())
      yMAX = float(self.intervalYMax.text())
      IDhMIN = int(self.histIndexMin.value())
      IDhMAX = int(self.histIndexMax.value())

      if (xMIN <= xMAX) and (yMIN <= yMAX):
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        dataSet = [[],[],[]]

        if (self.canvasInfo['type'] == 'histogram'):
          for index, value in enumerate(self.yData):
            if ((index >= IDhMIN) and (index <= IDhMAX)):
              if (float(value) >= float(yMIN)) and (float(value) <= float(yMAX)):
                dataSet[1].append(float(value))
              
        elif (self.canvasInfo['type'] == 'autocorrelation'):
          dataSet[0] = self.xData
          dataSet[1] = self.yData
        
        elif (self.canvasInfo['type'] == 'ueff'):
          for index, value in enumerate(self.xData):
            if (float(value) >= float(xMIN)) and (float(value) <= float(xMAX)):
              if (self.yData[index] >= float(yMIN)) and (self.yData[index] <= float(yMAX)):
                dataSet[0].append( value )
                if float(self.yData[index]) < 1e-20:
                  dataSet[1].append(0.0)
                  print(float(self.yData[index]), 0.0)
                else:
                  dataSet[1].append( -(1.985e-3) * float(self.temperature.text()) * numpy.log(float(self.yData[index])) )
                  print(float(self.yData[index]), (1.985e-3) * float(self.temperature.text()) * numpy.log(float(self.yData[index])))
                dataSet[2].append( self.nrData[index] )
        
        elif (self.canvasInfo['type'] == 'line') or (self.canvasInfo['type'] == 'scatter'):
          if (self.extension == 'gr'):
            for index, value in enumerate(self.xData):
              if (float(value) >= float(xMIN)) and (float(value) <= float(xMAX)):
                if (self.yData[index] >= float(yMIN)) and (self.yData[index] <= float(yMAX)):
                  dataSet[0].append( value )
                  dataSet[1].append( self.yData[index] )
                  dataSet[2].append( self.nrData[index] )
          else:
            for index, value in enumerate(self.xData):
              if (float(value) >= float(xMIN)) and (float(value) <= float(xMAX)):
                if (self.yData[index] >= float(yMIN)) and (self.yData[index] <= float(yMAX)):
                  dataSet[0].append( value )
                  dataSet[1].append( self.yData[index] )
        
        QtGui.QApplication.restoreOverrideCursor()
        return dataSet
      else:
        self.status.showMessage('ERROR: invalid data interval range, Min. value > Max. value. \
                                 Please try to adjust the intervals or just click on RESET DATA FIELDS', 3456)
        return 1
    except (IndexError, ValueError) as e:
      self.status.showMessage('ERROR: invalid data interval values. \
                               Please try to adjust the intervals or just click on RESET DATA FIELDS', 3456)
      return 1



  def plot(self):
    """
    (None) -> None
    Show graph according the user options.
    """
    try:
      graphHold = self.checkOverplot.isChecked()
      self.canvasInfo['type'] = str( self.typeGraph.currentText() )
      self.integralMarker = False

      xid = self.dataXMenu.currentIndex()
      yid = self.dataYMenu.currentIndex()
      if (self.extension == 'gr'):
        gid = self.grMenu.currentIndex()
      if (self.extension[0] == 'e'):
        sid = self.eijMenu.currentIndex()

      data = self.dataProcessing()

      if (graphHold == False):
        self.plotTitles, self.histogramTitles = [], []
        self.graphxyAxes.hold(False)
        self.graphxyAxes.clear()
      else:
        self.graphxyAxes.hold(True)
      
      self.graphxyAxes.axis('off')
      
      
      if (self.extension == 'gr') and (self.canvasInfo['type'] != 'autocorrelation'):
        self.graphxyAxes = self.graphxyFigure.add_axes([0.075, 0.075, 0.7, 0.88], axisbg='white')
      else:
        self.graphxyAxes = self.graphxyFigure.add_axes([0.1, 0.075, 0.85, 0.85], axisbg='white')
      
      # WIDGETS RESPONSES
      if self.canvasInfo['type'] is not 'histogram':
        self.meanLabel.hide()
        self.stdDeviationLabel.hide()
      if self.canvasInfo['type'] == 'autocorrelation':
        self.oa1.setText('A1=')
        self.oa2.setText('A2=')
        self.oa3.setText('A3=')
        self.ob1.setText('B1=')
        self.ob2.setText('B2=')
        self.ob3.setText('B3=')
        self.checkOverplot.hide()
      else:
        self.checkOverplot.show()

      
      # Line and Scatter
      if (data != 1):
        if (self.canvasInfo['type'] == 'line') or (self.canvasInfo['type'] == 'scatter') or (self.canvasInfo['type'] == 'ueff'):
          if (self.canvasInfo['type'] == 'line') or (self.canvasInfo['type'] == 'ueff'):
            plot = self.graphxyAxes.plot(data[0], data[1], linestyle='-')
          elif (self.canvasInfo['type'] == 'scatter'):
            plot = self.graphxyAxes.plot(data[0], data[1], linestyle='', marker='.')
          self.horizontalUeffLine = False
          if (self.extension == 'gr'):
            self.canvasInfo['data'] = [data[0], data[1], data[2]]
            if (self.horizontalGrLine == False or graphHold == False and self.canvasInfo['type'] != 'ueff'):
              self.graphxyAxes.hold(True)
              self.graphxyAxes.axhline(y=1, c='k', linestyle='-', label='_nolegend_')
              self.horizontalGrLine = True
              self.graphxyAxes.hold(graphHold)
            if (self.horizontalUeffLine == False or graphHold == False):
              self.graphxyAxes.hold(True)
              self.graphxyAxes.axhline(y=0, c='k', linestyle='-', label='_nolegend_')
              self.horizontalUeffLine = True
              self.graphxyAxes.hold(graphHold)
            self.molDimAdjust = False
            grLabel = self.grMenuItems[gid]
            self.plotTitles.append(r'${}$'.format(grLabel))
            self.canvasInfo['title'] = '{}'.format(grLabel)
            self.graphxyAxes.legend(self.plotTitles,
                                    bbox_to_anchor = (1.05, 1),
                                    loc = 2,
                                    ncol = 1,
                                    mode = 'expand',
                                    borderaxespad = 0.,
                                    frameon = False,
                                    numpoints = 1,
                                    prop = {'size':10}, 
                                    handlelength = 0.6,
                                    borderpad = -0.8)
          else:
            self.canvasInfo['data'] = [data[0], data[1]]
            xLabel = (self.labels[ xid ]).replace('_','-')
            yLabel = (self.labels[ yid ]).replace('_','-')
            self.plotTitles.append(r'${}\, \times\, {}$'.format(xLabel, yLabel))
            self.canvasInfo['title'] = '{}-{}'.format(xLabel, yLabel)
            self.graphxyAxes.legend(self.plotTitles,
                                    bbox_to_anchor = (0., 1.052, 1., .9),
                                    loc = 3,
                                    ncol = 4,
                                    mode = 'expand',
                                    borderaxespad = 0.,
                                    frameon = False,
                                    numpoints = 1,
                                    prop = {'size':12},
                                    handlelength = 0.6,
                                    borderpad = -0.8)
         
          xmin, xmax = self.graphxyAxes.get_xlim()
          ymin, ymax = self.graphxyAxes.get_ylim()
          self.setCanvasBoundaries(xmin, xmax, ymin, ymax) 
          
        
        # Histogram
        elif (self.canvasInfo['type'] == 'histogram'):
          title = (self.labels[ yid ]).replace('_','-')
          self.histogramTitles.append(r'${}$'.format(title))
          
          try:
            numbins = int(self.binValue.value())
            if (numbins <= 0):
              numbins = 50
              self.status.showMessage('ERROR: invalid number of bins. It was replaced by the default value.', 3456)
          except (ValueError) as e:
            numbins = 50
          
          L = len(data[1])  
          frequency, bins = numpy.histogram(data[1], numbins)
          weight = [(1 / L) for i in data[1]]
      
          n, bins, patches = self.graphxyAxes.hist(data[1], numbins, weights=weight)
          
          if (self.extension == 'gr'):
            self.horizontalGrLine = False
            self.horizontalUeffLine = False
            self.graphxyAxes.legend(self.histogramTitles, 
                                    bbox_to_anchor=(1.05, 1), 
                                    loc=2, 
                                    ncol=1, 
                                    mode='expand', 
                                    borderaxespad=0., 
                                    frameon=False, 
                                    numpoints=1, 
                                    prop={'size':10}, 
                                    handlelength=0.6, 
                                    borderpad=-0.8)
          else:
            self.graphxyAxes.legend(self.histogramTitles, 
                                    bbox_to_anchor=(0.05, 1.055, 0.95, .9), 
                                    loc=3, 
                                    ncol=4, 
                                    mode='expand', 
                                    borderaxespad=0., 
                                    frameon=False, 
                                    numpoints=1, 
                                    prop={'size':12}, 
                                    handlelength=0.6, 
                                    borderpad=-0.8)
                                    
          binwidth = (bins[1] - bins[0])
          x = (min(bins) - binwidth)
          X = max(bins) + binwidth
          y = 0
          Y = max(n)
          
          decPrec = len((str(data[1][-1])).split('.')[-1])
          mean = float( sum(data[1]) / len(data[1]) )
          deviation = sum([(i-mean)**2 for i in data[1]])
          stdDev = numpy.sqrt(deviation / len(data[1]))

          points = numpy.linspace(float(bins[0]), float(bins[-1]), 250)
          self.graphxyAxes.hold(True)
          gaussian = self.graphxyAxes.plot(points, 
                                           binwidth*( ( 1 / (stdDev * numpy.sqrt(2 * 3.14)) ) * numpy.exp( -0.5 * ((points - mean) / stdDev)**2) ), 
                                           c='k', 
                                           label='_nolegend_')
          self.graphxyAxes.hold(graphHold)
          
          self.meanLabel.show()
          self.stdDeviationLabel.show()
          self.meanLabel.setText('Mean: {}'.format( round(mean, decPrec) ) )
          self.stdDeviationLabel.setText('Standard deviation: {}'.format( round(stdDev, decPrec) ) )
          
          binCenter = [ (bins[i-1] + abs(bins[i] - bins[i-1])*0.5) for i in range(1, len(bins))]

          
          xmin, xmax = self.graphxyAxes.get_xlim()
          ymin, ymax = self.graphxyAxes.get_ylim()
          self.setCanvasBoundaries(xmin, xmax, ymin, ymax)
          self.canvasInfo['title'] = '{}'.format(title)
          self.canvasInfo['data'] = [n, binCenter]
          self.canvasInfo['user parameters'] = [mean, stdDev]
          self.canvasInfo['user data'] = [binwidth*((1/(stdDev*numpy.sqrt(2*3.14)))*numpy.exp(-0.5*((i-mean)/stdDev)**2)) for i in binCenter]
          
        
        # Autocorrelation
        elif (self.canvasInfo['type'] == 'autocorrelation'):
          yLabel = (self.labels[ yid ]).replace('_','-')
          self.plotTitles.append(r'$C(t) \times t\,\,\, ({})$'.format(yLabel))
          
          QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
          x = numpy.arange( len(data[1]) )
          y = self.estimated_autocorrelation( numpy.array(data[1]) )
          QtGui.QApplication.restoreOverrideCursor()
          
          self.canvasInfo['title'] = '{}'.format(yLabel)
          self.canvasInfo['data'] = [x, y]
          
          self.graphxyAxes.plot(self.canvasInfo['data'][0], self.canvasInfo['data'][1], linestyle='', marker='.')
          self.setCanvasBoundaries(min(x), max(x), min(y), max(y))
          
          self.graphxyAxes.legend(self.plotTitles, 
                                    bbox_to_anchor=(0.05, 1.055, 0.95, .9), 
                                    loc=3, 
                                    ncol=4, 
                                    mode='expand', 
                                    borderaxespad=0., 
                                    frameon=False, 
                                    numpoints=1, 
                                    prop={'size':12}, 
                                    handlelength=0.6, 
                                    borderpad=-0.8)

      
      self.applyCanvasBoundaries()
      self.updatePlotLimits()
      
      self.graphxyAxes.axis('on')
      self.graphxyCanvas.draw()
      
    except (AttributeError) as e:
      self.status.showMessage('ERROR: failed to plot data. Please check the axes range values.', 3456)
    except (IndexError) as e:
      self.status.showMessage('ERROR: failed to plot data. Please check data and axes range values.', 3456)


  
  def applyUserParameters(self):
    """
    (None) -> None
    Get values from 'Autocorrelation options' and send to the fitting function.
    """
    if (self.canvasInfo['type'] == 'autocorrelation'):
      n = int( self.expMenu.currentIndex() )
      largT = int(self.largestT.text())
      a1 = self.A1.text()
      a2 = self.A2.text()
      a3 = self.A3.text()
      b1 = self.B1.text()
      b2 = self.B2.text()
      b3 = self.B3.text()
      par = [a1, b1, a2, b2, a3, b3]
      self.bestFit(largT, par, n)
    else:
      self.status.showMessage('ERROR: to change the guess it is necessary show an autocorrelation graph first.', 3456)

  
  
  def bestFit(self, LT, P, i):
    """
    (Int, List, Int) -> None
    Fit two exponential curves the points generated in the autocorrelation function, one using coeficients inserted
    by the user and another using coeficients generated by a fitting function.
    """
    try:
      QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
      if (i == 0):
        fit = Model(self.exponential1)
        guess = [float(k) for k in P[:2]]
      if (i == 1):
        fit = Model(self.exponential2)
        guess = [float(k) for k in P[:4]]
      if (i == 2):
        fit = Model(self.exponential3)
        guess = [float(k) for k in P]
      
      dataReal = RealData(self.canvasInfo['data'][0][:LT], self.canvasInfo['data'][1][:LT])
      modelOdr = ODR(dataReal, fit, guess)
      modelOdr.set_job(fit_type=2)
      modelOutput = modelOdr.run()
      
      xnew = numpy.linspace(0, LT, len(self.canvasInfo['data'][0]))
      if (i == 0):
        yfit = self.exponential1(modelOutput.beta, xnew)
        yuser = self.exponential1(guess, xnew)
        initial = self.exponential1(guess, self.canvasInfo['data'][0][:LT])
        bestfit = self.exponential1(modelOutput.beta, self.canvasInfo['data'][0][:LT])
        self.oa1.setText('A1={}'.format(round(modelOutput.beta[0],4)))
        self.ob1.setText('B1={}'.format(round(modelOutput.beta[1],4)))
      if (i == 1):
        yfit = self.exponential2(modelOutput.beta, xnew)
        yuser = self.exponential2(guess, xnew)
        initial = self.exponential2(guess, self.canvasInfo['data'][0][:LT])
        bestfit = self.exponential2(modelOutput.beta, self.canvasInfo['data'][0][:LT])
        self.oa1.setText('A1={}'.format(round(modelOutput.beta[0],4)))
        self.ob1.setText('B1={}'.format(round(modelOutput.beta[1],4)))
        self.oa2.setText('A2={}'.format(round(modelOutput.beta[2],4)))
        self.ob2.setText('B2={}'.format(round(modelOutput.beta[3],4)))
      if (i == 2):
        yfit = self.exponential3(modelOutput.beta, xnew)
        yuser = self.exponential3(guess, xnew)
        initial = self.exponential3(guess, self.canvasInfo['data'][0][:LT])
        bestfit = self.exponential3(modelOutput.beta, self.canvasInfo['data'][0][:LT])
        self.oa1.setText('A1={}'.format(round(modelOutput.beta[0],4)))
        self.ob1.setText('B1={}'.format(round(modelOutput.beta[1],4)))
        self.oa2.setText('A2={}'.format(round(modelOutput.beta[2],4)))
        self.ob2.setText('B2={}'.format(round(modelOutput.beta[3],4)))
        self.oa3.setText('A3={}'.format(round(modelOutput.beta[4],4)))
        self.ob3.setText('B3={}'.format(round(modelOutput.beta[5],4)))
      
      # adjust boundaries
      self.graphxyAxes.plot(self.canvasInfo['data'][0][:LT+1], self.canvasInfo['data'][1][:LT+1], linestyle='-')
      
      self.graphxyAxes.hold(False)
      plot = self.graphxyAxes.plot(self.canvasInfo['data'][0], self.canvasInfo['data'][1], linestyle='', marker='.', label=r'$C(t)$')
      x, X = self.graphxyAxes.get_xlim()
      y, Y = self.graphxyAxes.get_ylim()
      self.graphxyAxes.hold(True)
      plot = self.graphxyAxes.plot(xnew, yuser, linestyle='--', c='k', linewidth='1.5', label=r'$guess$')
      plot = self.graphxyAxes.plot(xnew, yfit, linestyle='-', c='r', linewidth='1.5', label=r'$fit$')
      
      self.graphxyAxes.legend(bbox_to_anchor = (0., 1., 1., 1.),
                                    loc = 3,
                                    ncol = 3,
                                    mode = 'expand',
                                    borderaxespad = 0.,
                                    frameon = False,
                                    numpoints = 1,
                                    prop = {'size':12},
                                    handlelength = 0.5)
      
      self.graphxyAxes.hold(self.checkOverplot.isChecked())
      
      xmin, xmax = self.graphxyAxes.get_xlim()
      ymin, ymax = self.graphxyAxes.get_ylim()
      self.setCanvasBoundaries(xmin, LT, ymin, ymax)
      self.applyCanvasBoundaries()
      self.graphxyCanvas.draw()
      
      self.canvasInfo['user data'] = [self.canvasInfo['data'][0][:LT], 
                                      self.canvasInfo['data'][1][:LT],
                                      initial,
                                      bestfit]
      self.canvasInfo['user parameters'] = [[i if i is not '' else 'None' for i in P],
                                            modelOutput.beta,
                                            self.expMenu.currentText(),
                                            LT] 
      
      self.viewAllCoord =  [x, X, y, Y]
      
      QtGui.QApplication.restoreOverrideCursor()
    
    except (IndexError) as e:
      self.status.showMessage('ERROR: invalid fitting parameters. Please check your guess then try again.', 3456)
      QtGui.QApplication.restoreOverrideCursor()
    except (ValueError) as e:
      self.status.showMessage('ERROR: invalid fitting parameters. Please check your guess then try again.', 3456)
      QtGui.QApplication.restoreOverrideCursor()
  
  
  
  def exponential1(self, C, t):
    return C[0] * numpy.exp(-t / C[1])
    
  def exponential2(self, C, t):
    return C[0] * numpy.exp(-t / C[1]) + C[2] * numpy.exp(-t / C[3])
    
  def exponential3(self, C, t):
    return C[0] * numpy.exp(-t / C[1]) + C[2] * numpy.exp(-t / C[3]) + C[4] * numpy.exp(-t / C[5])
    

  
  def estimated_autocorrelation(self, x):
    """
    (Array) -> Array
    Calculate the autocorrelation. Algorithm from: http://stackoverflow.com/q/14297012/190597
    """
    n = len(x)
    variance = x.var()
    x = x-x.mean()
    r = numpy.correlate(x, x, mode = 'full')[-n:]
    result = r/(variance*(numpy.arange(n, 0, -1)))
    return result
  

  def changeXData(self):
    """
    (None) -> None
    Update interval entries and datasets when 'data X' menu has the selected index changed.
    """
    try:
      if (self.extension == 'gr'):
        self.xData = []
        i = int(self.grMenu.currentIndex())
        j = int(self.dataXMenu.currentIndex())
        for v in (self.dataSet[i]):
          self.xData.append(float(v[j]))
      elif (self.extension[0] == 'e'):
        self.xData = [] 
        i = int(self.eijMenu.currentIndex())
        j = int(self.dataXMenu.currentIndex())
        self.labels = self.eijLabels[i]
        self.xData = self.dataSet[i][j]
      else:
        j = int(self.dataXMenu.currentIndex())
        self.xData = self.dataSet[j]

      self.intervalXMin.setText(str(min(self.xData)))
      self.intervalXMax.setText(str(max(self.xData)))
      self.plotXIntervalMin.setText(str(min(self.xData)))
      self.plotXIntervalMax.setText(str(max(self.xData)))
    except (IndexError) as e:
      self.status.showMessage('ERROR: failed to automatic change x-axis values.', 3456)

  
  def changeYData(self):
    """
    (None) -> None
    Update interval entries and datasets when 'data Y' menu has the selected index changed. 
    """
    try:
      if (self.extension == 'gr'):
        self.yData, self.nrData = [],[]
        i = int(self.grMenu.currentIndex())
        k = int(self.dataYMenu.currentIndex())
        for v in (self.dataSet[i]):
          self.yData.append(float(v[k]))
          self.nrData.append(float(v[2]))
      elif (self.extension[0] == 'e'):
        self.yData = []
        i = int(self.eijMenu.currentIndex())
        k = int(self.dataYMenu.currentIndex())
        self.labels = self.eijLabels[i]
        self.yData = self.dataSet[i][k]
      else:
        k = int(self.dataYMenu.currentIndex())
        self.yData = self.dataSet[k]

      self.intervalYMin.setText(str(min(self.yData)))
      self.intervalYMax.setText(str(max(self.yData)))
      self.plotYIntervalMin.setText(str(min(self.yData)))
      self.plotYIntervalMax.setText(str(max(self.yData)))
      
      self.largestTLabel.setText('(from {})'.format( len(self.yData) ) )
      self.largestT.setText('{}'.format( int( len(self.yData)*0.01 ) ) )
      self.histIndexMax.setMinimum(0)
      self.histIndexMax.setMaximum(len(self.yData)-1)
      self.histIndexMin.setValue(0)
      self.histIndexMax.setValue(len(self.yData)-1)
      
    except (IndexError) as e:
      self.status.showMessage('ERROR: failed to automatic change y-axis values.', 3456)
      

  
  def changeFitParameters(self):
    """
    (None) -> None
    Activate or deactivate fitting parameters entries according to selected function in the 'Fit type' menu.
    """ 
    index = self.expMenu.currentIndex()
    if index==0:
      self.A1.setEnabled(True)
      self.A2.setEnabled(False)
      self.A3.setEnabled(False)
      self.B1.setEnabled(True)
      self.B2.setEnabled(False)
      self.B3.setEnabled(False)
    elif index==1:
      self.A1.setEnabled(True)
      self.A2.setEnabled(True)
      self.A3.setEnabled(False)
      self.B1.setEnabled(True)
      self.B2.setEnabled(True)
      self.B3.setEnabled(False)
    elif index==2:
      self.A1.setEnabled(True)
      self.A2.setEnabled(True)
      self.A3.setEnabled(True)
      self.B1.setEnabled(True)
      self.B2.setEnabled(True)
      self.B3.setEnabled(True)
 
  
  
  def changeDefaultBoundaries(self):
    """
    (None) -> None
    Set new values for 'Axes range options' when the type of graph is changed.
    """    
    if (self.extension != ''):
      typeGraph = self.typeGraph.currentText()
      if (typeGraph == 'line') or (typeGraph == 'scatter'):
        self.plotXIntervalMin.setText(str(min(self.xData)))
        self.plotXIntervalMax.setText(str(max(self.xData)))
        self.plotYIntervalMin.setText(str(min(self.yData)))
        self.plotYIntervalMax.setText(str(max(self.yData)))
 
 
  
  def updatePlotLimits(self):
    """
    (None) -> None
    Update the list 'viewAllCoord' which stores boundary values of all graphs on the canvas.
    """    
    if self.checkOverplot.isChecked() == True:
      try:
        xmin, xmax = self.graphxyAxes.get_xlim()
        ymin, ymax = self.graphxyAxes.get_ylim()
        if xmin < self.viewAllCoord[0]:
          self.viewAllCoord[0] = xmin
        if xmax > self.viewAllCoord[1]:
          self.viewAllCoord[1] = xmax
        if ymin < self.viewAllCoord[2]:
          self.viewAllCoord[2] = ymin
        if ymax > self.viewAllCoord[3]:
          self.viewAllCoord[3] = ymax
      except (IndexError) as e:
        xmin, xmax = self.graphxyAxes.get_xlim()
        ymin, ymax = self.graphxyAxes.get_ylim()
        self.viewAllCoord = [xmin, xmax, ymin, ymax]
    else:
        xmin, xmax = self.graphxyAxes.get_xlim()
        ymin, ymax = self.graphxyAxes.get_ylim()
        self.viewAllCoord = [xmin, xmax, ymin, ymax]
  
  
  
  def viewAll(self):
    """
    (None) -> None
    Set new boundary values to the canvas according to values from the list 'viewAllCoord'.
    """
    try:
      gapX = abs(self.viewAllCoord[0] - self.viewAllCoord[1]) * 0.015
      gapY = abs(self.viewAllCoord[2] - self.viewAllCoord[3]) * 0.015
      self.graphxyAxes.set_xlim(self.viewAllCoord[0] - gapX, self.viewAllCoord[1] + gapX)
      self.graphxyAxes.set_ylim(self.viewAllCoord[2] - gapY, self.viewAllCoord[3] + gapY)
      self.graphxyCanvas.draw()
      self.status.showMessage("REMINDER: the 'Save' button records data from the graph according 'Axes range option' values, the 'View all' button does not change them.", 3456)
    except (IndexError) as e:
      self.status.showMessage('ERROR: failed to resize. Please check if there is some data plotted.', 4567)
      
  
  
  def setCanvasBoundaries(self, x, X, y, Y):
    """
    (Float, Float, Float, Float) -> None
    Set new values to the fields from 'Axes range options'.
    """
    try:
      xmin = str(round(x, 3))
      xmax = str(round(X, 3))
      ymin = str(round(y, 3))
      ymax = str(round(Y, 3))
      
      self.plotXIntervalMin.setText(xmin)
      self.plotXIntervalMax.setText(xmax)
      self.plotYIntervalMin.setText(ymin)
      self.plotYIntervalMax.setText(ymax)
    except (IndexError, ValueError) as e:
      self.status.showMessage('PASS.', 3456)
  
  
  
  def applyCanvasBoundaries(self):
    """
    (None) -> None
    Set new boundary values to the canvas according to the fields from 'Axes range options'.
    """
    try:
      pltYMin = float(self.plotYIntervalMin.text())
      pltYMax = float(self.plotYIntervalMax.text())
      pltXMin = float(self.plotXIntervalMin.text())
      pltXMax = float(self.plotXIntervalMax.text())
      
      if pltYMin <= pltYMax:
          self.graphxyAxes.set_ylim(pltYMin, pltYMax)
      else:
          self.status.showMessage('Minimum Y-axis > Maximum Y-axis. Default Y-axis range applied.', 3000)
      if pltXMin <= pltXMax:
          self.graphxyAxes.set_xlim(pltXMin, pltXMax)
      else:
          self.status.showMessage('Minimum X-axis > Maximum X-axis. Default X-axis range applied.', 3000)
      
      self.canvasInfo['user boundaries'] = [pltXMin, pltXMax, pltYMin, pltYMax]
      self.graphxyCanvas.draw()
    except (IndexError, ValueError) as e:
      self.status.showMessage('PASS.', 3456)
  

  
  def changeSimulationOutput(self):
    """
    (None) -> None
    When eij files are loaded, update the data menus according to the selected simulation.
    """
    menus = [self.dataXMenu, self.dataYMenu]
    i = int(self.eijMenu.currentIndex())
    self.labels = self.eijLabels[i]
    for i in menus:
      i.setDisabled(True)
      i.clear()
      i.setDisabled(False)
      i.addItems(self.labels)
    
    
  
  def applyMolDim(self):
    """
    (None) -> None
    Change the value of the RDF function according to the molecular dimensions entered by the user and show the new RDF function.
    """
    newGr = []
    r = self.canvasInfo['data'][0]
    gr = self.canvasInfo['data'][1]
    
    gid = self.grMenu.currentIndex()
    graphHold = self.checkOverplot.isChecked()
    a = float(self.molDimA.text())
    b = float(self.molDimB.text())
    c = float(self.molDimC.text())
    
    halfDr = float(r[1] - r[0])
    esfConst = ((4 * 3.1415)/3)
    
    for i, v in enumerate(gr):
      rMinus = r[i] - halfDr
      rPlus = r[i] + halfDr
      vEsf = (esfConst) * (rPlus**3 - rMinus**3)
      vPara = ((a + 2*rPlus)*(b + 2*rPlus)*(c + 2*rPlus))-((a + 2*rMinus)*(b + 2*rMinus)*(c + 2*rMinus))
      newGr.append((2 * v * vEsf) / (vPara))
    
    self.setCanvasBoundaries(min(r), max(r), min(newGr), max(newGr))
    
    self.integralMarker = False
    self.graphxyAxes.axis('off')
    self.graphxyAxes = self.graphxyFigure.add_axes([0.075, 0.075, 0.7, 0.88], axisbg='white')
    
    self.graphxyAxes.hold(graphHold)
    self.graphxyAxes.plot(r, newGr, linestyle='-')
    self.molDimAdjust = True
    if (self.horizontalGrLine == False or graphHold == False):
      self.graphxyAxes.hold(True)
      self.graphxyAxes.axhline(y=1, c='k', linestyle='-', label='_nolegend_')
      self.horizontalGrLine = True
      self.graphxyAxes.hold(graphHold)
    
    grLabel = self.grMenuItems[gid]
    self.plotTitles.append(r'${}*$'.format(grLabel))
    self.canvasInfo['title'] = '{}'.format(grLabel)
    self.graphxyAxes.legend(self.plotTitles,
                            bbox_to_anchor = (1.05, 1),
                            loc = 2,
                            ncol = 1,
                            mode = 'expand',
                            borderaxespad = 0.,
                            frameon = False,
                            numpoints = 1,
                            prop = {'size':10}, 
                            handlelength = 0.6,
                            borderpad = -0.8)
    
    self.canvasInfo['type'] = 'gr'
    self.canvasInfo['user data'] = newGr
    self.canvasInfo['user parameters'] = [a, b, c]
    
    self.updatePlotLimits()  
    self.graphxyAxes.axis('on')
    self.graphxyCanvas.draw()
      
      
  
  def clickIntegral(self, event):
    """
    (MouseEvent) -> None
    Show an x-shaped symbol on the RDF curve and show the integral value corresponding to the clicked region.
    """
    if (self.extension == 'gr' and self.canvasInfo['type'] != 'histogram'):
      nPlots = len(self.graphxyAxes.lines)
      if (self.checkOverplot.isChecked() == False):
        try:
          index = int(numpy.round((event.xdata - self.xData[0]) / (self.canvasInfo['data'][0][1] - self.canvasInfo['data'][0][0])))
          integral = self.canvasInfo['data'][2][index]
          self.integralLabel.setText('<small><b>INTEGRAL OF G(R):</b></small>   N(%.3f) = %.3f' % (self.xData[index], integral))

          if (self.integralMarker == False):
            self.graphxyAxes.hold(True)
            marker = self.graphxyAxes.plot(event.xdata, event.ydata, 'rx', label='_nolegend_')
            self.integralIndex = nPlots
            self.graphxyAxes.hold(False)
            self.integralMarker = True
          else:
            self.graphxyAxes.hold(True)
            self.graphxyAxes.lines.pop(self.integralIndex)
            marker = self.graphxyAxes.plot(event.xdata, event.ydata, 'rx', label='_nolegend_')
            self.graphxyAxes.hold(False)

          self.graphxyCanvas.draw()
        except (TypeError, IndexError) as e:
          self.status.showMessage('Please, click inside the graph.', 3000)
      else:
        self.status.showMessage('Please, disable the OVERPLOT checkbutton to view the integral of the last plotted function.', 3456)


  
  def savePlotData(self):
    """
    (None) -> None
    Write the values and information from the dictionary canvasInfo to a dat file. 
    """
    try:
      root = os.getenv('HOME')
      timetag = time.strftime('%Y%m%d%H%M%S')
      fname = self.filename.split('/')[-1]
      title = ((self.canvasInfo['title']).replace('/', '')).replace('_', '')
      
      xmin, xmax, ymin, ymax = [float(i) for i in self.canvasInfo['user boundaries']]
      
      # Line and Scatter
      if (self.canvasInfo['type'] == 'line') or (self.canvasInfo['type'] == 'scatter'):
        name = '{}_{}_{}_{}_{}.dat'.format(fname, self.extension, self.canvasInfo['type'], title, timetag)
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Save file', name)
        f = open('{}'.format(str(filename)), 'w')
        
        x = self.canvasInfo['data'][0]
        y = self.canvasInfo['data'][1]
        xmin, xmax, ymin, ymax = [float(i) for i in self.canvasInfo['user boundaries']]
        
        if (len(self.eijMenuItems) != 0):
          f.write('# {}\n'.format(self.eijMenu.currentText()))
        
        title = (self.canvasInfo['title']).split('-')
        f.write('# {:>15}{:>15}\n'.format(title[0], title[1]))
        
        if (self.extension == 'gr'):
          Nr = self.canvasInfo['data'][2]
          f.write('# {:>15}{:>20}{:>20}\n'.format('r', self.dataYMenu.currentText(), 'N(r)'))
          for index, value in enumerate(x):
            if (value >= xmin) and (value <= xmax):
              if (y[index] >= ymin) and (y[index] <= ymax):
                f.write( '{:>20e}{:>20e}{:20e}\n'.format(value, y[index], Nr[index]) )
        else:
          for index, value in enumerate(x):
            if (value >= xmin) and (value <= xmax):
              if (y[index] >= ymin) and (y[index] <= ymax):
                f.write( '{:>20e}{:>20e}\n'.format(value, y[index]) )
      
      # Histogram
      elif (self.canvasInfo['type'] == 'histogram'):
        name = '{}_{}_{}_{}_{}.dat'.format(fname, self.extension, self.canvasInfo['type'], title, timetag)
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Save file', name)
        f = open('{}'.format(str(filename)), 'w')
        
        bins = self.canvasInfo['data'][1]
        frequency = self.canvasInfo['data'][0]
        gaussian = self.canvasInfo['user data']
        xmin, xmax, ymin, ymax = [float(i) for i in self.canvasInfo['user boundaries']]
        
        if (len(self.eijMenuItems) != 0):
          f.write('# {}\n'.format(self.eijMenu.currentText()))
        
        f.write('# {}\n'.format(self.canvasInfo['title']))
        f.write('# MEAN:      {:>15e}\n# STD. DEV.: {:>15e}\n'.format(self.canvasInfo['user parameters'][0],
                                              self.canvasInfo['user parameters'][1]))      
        f.write('# {:>15}{:>20}{:>20}\n'.format('x', 'frequency(x)', 'gaussian(x)'))
        for index, value in enumerate(bins):
          if (value >= xmin) and (value <= xmax):
              f.write( '{:>20e}{:>20e}{:>20e}\n'.format(value, frequency[index], gaussian[index]) )
      
      # Autocorrelation
      elif (self.canvasInfo['type'] == 'autocorrelation'):
        name = '{}_{}_{}_{}_{}.dat'.format(fname, self.extension, self.canvasInfo['type'], title, timetag)
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Save file', name)
        f = open('{}'.format(str(filename)), 'w')
        
        if (len(self.eijMenuItems) != 0):
          f.write('# {}\n'.format(self.eijMenu.currentText()))
        
        f.write('# {} ({})\n'.format(self.canvasInfo['user parameters'][2], self.canvasInfo['title']))
        f.write('# USER GUESS\n')
        for index, value in enumerate(['A1', 'B1', 'A2', 'B2', 'A3', 'B3']):
          f.write('# {} = {}\n'.format(value, self.canvasInfo['user parameters'][0][index]))
        f.write('# BEST FIT\n')
        for index, value in enumerate(['A1', 'B1', 'A2', 'B2', 'A3', 'B3']):
          if index >= len(self.canvasInfo['user parameters'][1]):
            f.write('# {} = None\n'.format(value))
          else:
            f.write('# {} = {}\n'.format(value, self.canvasInfo['user parameters'][1][index]))
        f.write('# LARGEST T: {}\n'.format(self.canvasInfo['user parameters'][3]))
        
        t = self.canvasInfo['user data'][0]
        ct = self.canvasInfo['user data'][1]
        initial = self.canvasInfo['user data'][2]
        bestfit = self.canvasInfo['user data'][3]
        
        f.write('# {:>15}{:>20}{:>20}{:>20}\n'.format('t', 'C(t)', 'Initial', 'Best fit'))
        for index, value in enumerate(t):
          if (value >= xmin) and (value <= xmax):
            if (ct[index] >= ymin) and (ct[index] <= ymax):
              f.write( '{:>20e}{:>20e}{:>20e}{:>20e}\n'.format(value, ct[index], initial[index], bestfit[index]))  
      
      # rdf
      elif (self.canvasInfo['type'] == 'gr'):
        name = '{}_{}_{}_{}_{}.dat'.format(fname, self.extension, self.canvasInfo['type'], title, timetag)
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Save file', name)
        f = open('{}'.format(str(filename)), 'w')
        
        f.write('# MOLECULAR DIMENSIONS\n')
        for index, value in enumerate(['A', 'B', 'C']):
          f.write('# {} = {}\n'.format(value, self.canvasInfo['user parameters'][index]))
        
        r = self.canvasInfo['data'][0]
        Gr = self.canvasInfo['data'][1]
        Nr = self.canvasInfo['data'][2]
        NewGr = self.canvasInfo['user data']
        
        print(xmin, xmax, ymin, ymax)
        
        f.write('# {:>15}{:>20}{:>20}{:>20}\n'.format('r', 'New G(r)', 'G(r)', 'N(r)'))
        for index, value in enumerate(r):
          if (value >= xmin) and (value <= xmax):
            if (NewGr[index] >= ymin) and (NewGr[index] <= ymax):
              f.write( '{:>20e}{:>20e}{:>20e}{:>20e}\n'.format(value, NewGr[index], Gr[index], Nr[index]))
      
      f.close()
      self.status.showMessage('File successfully saved.', 3456)
        
    except (IndexError, ValueError) as e:
      self.status.showMessage('ERROR: failed to save data. Please try to adjust the data intervals.', 3456)
    except OSError as e:
      self.status.showMessage('ERROR: failed to save data.', 3456)
     

def main():
  """
  (None) -> None
  Initialize and displace the window.
  """
  application = QtGui.QApplication(sys.argv)
  mainWindow = graphMainWindow()

  mainWindow.move(150, 50)

  mainWindow.show()
  sys.exit(application.exec_())

if __name__ == '__main__':
  main()
