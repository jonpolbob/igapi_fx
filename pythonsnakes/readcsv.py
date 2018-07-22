#!/usr/bin/python
# -*- coding: latin-1 -*-


__author__ = 'cagibi'

import csv
import numpy as np



import csv2data

dseuil = 1


# trouve un point a une distance dseuil du ujeme point de data
def calcpairepts(data,j,dseuil):
       #calcul longueur arc polygon
        curpos=i+1
        distance=0
        Encore=1
        while Encore==1:
            dx= data[curpos-1][0]-data[curpos][0]
            dy= data[curpos-1][1]-data[curpos][1]
            if distance+ np.sqrt(dx*dx+dy*dy) <= dseuil :
                distance = distance+np.sqrt(dx*dx+dy*dy)
                curpos=curpos+1
                if (curpos == len(data)):
                    return 0
            else:
                return curpos

def distance(p1,p2,p3):
    xa = p1[0]-p2[0]
    ya = p1[1]-p2[1]
    a=np.sqrt(xa*xa+ya*ya)
    xb = p1[0]-p3[0]
    yb = p1[1]-p3[1]
    b = np.sqrt(xb*xb+yb*yb)
    xc = p2[0]-p3[0]
    yc = p2[1]-p3[1]
    c = np.sqrt(xc*xc+yc*yc)
    s=(a+b+c)/2
    surfcarrre = s*(s-a)*(s-b)*(s-c)
    return surfcarrre

#reduit le polygone entre debut et fin selon la methode de Ramer?Douglas?Peucker
# retourne le premier point des qu'il a change et data modifie en rajoutant/supprimant un point
def reducepoly(data,deb,fin):
    #on cherche sur tous les points de l'intervalle deb,fin le plus loin de la droite debut/fin' \
    #cad celui qui fait le plus grand triangle avec les deux bouts du segment
    # surf d'un triangle de cotes abc : A = sqrt(s (s-a)(s-b)(s-c) avec s = (a+b+c)/2
    maxdist = -100
    pttrouv=fin

    #on cherche le pt le plus eloigne de la droite debut, fin
    for pt in np.arange(deb+1,fin-1):
        surf = distance(data[deb],data[fin],data[pt])
        if maxdist==-100 or surf>mindist:
            maxdist = surf
            pttrouv = pt




# fonction pour appliquer le reducepolu
def reducepoly():
    data = csv2data.readcsv("contour1.csv")
    #larray = np.asarray(data)
    #print larray

    prvfin = 0
    for deb in np.arange(0,len(data)):
        fin=calcpairepts(data,deb,dseuil)
        deb = reducepoly(data,deb,fin)






