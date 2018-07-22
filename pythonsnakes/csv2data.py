#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'cagibi'

#decode une chaine de path de svg
# attention les arcs sont transfomres en droites

def decodesvgpath(lepath):
    lstx =0
    lsty=0
    nbread=0;
    nbtoread=2

    data=[]

    for item in lepath.split(' '):
        if len(item)==1: #lettre code
            if item=='m': #relatif
               mode = 1
               nbtoread=2
            if item=='l': #relatif
               mode = 1
               nbtoread=2

            if item=='M':
                mode = 2 #absolu
                nbtoread=2
            if item=='L':
                mode = 2 #absolu
                nbtoread=2

            if item=='c':
                mode = 1
                nbtoread=6
            if item=='C':
                mode = 2  #absolu
                nbtoread=6
            if item=='z' or item=='Z':
                lstx = data[0][0]
                lsty = data[0][1]
                nbtoread=0 #plus rien alire
                data.append([lstx,lsty])

        else:  #pas lettre code donc coordonnees
            lesitems = item.split(',')
            nbread = nbread+2

            if nbread == nbtoread:
               nb1 = float(lesitems[0])
               nb2 = -float(lesitems[1])

               if mode == 2:
                    lstx = nb1
                    lsty = nb2
               else:
                    lstx = lstx+nb1
                    lsty = lsty+nb2

               nbread=0
               data.append([lstx,lsty])

    return data
