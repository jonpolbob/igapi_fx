#!/usr/bin/python
# -*- coding: latin-1 -*-

__author__ = 'cagibi'


import csv2data
import numpy as np


import matplotlib as mp
import matplotlib.pyplot as plt

#plt.ion() # enables interactive mode

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

#calcule la 'distance en fait la hauteur au carre du triangle de bas P1 P2) entre le segment p1 p2 et le point p3'

#retourne le cdg du triangle pondere par sa surface
def cdgpondere(p1,p2,p3):
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

    #calcul du signe produit vectoriel pour savoir le sens du tringle
    prod = 1 if (xa-xb)*(yc-yb)+(xc-xb)*(ya-yb)>0 else -1

    surf = prod*np.sqrt(surfcarrre) #surf en negatif si produit vectoriel a l'envers
    cdgx=(p1[0]+p2[0]+p3[0])/3
    cdgy=(p1[1]+p2[1]+p3[1])/3
    return cdgx,cdgy,surf


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
    return surfcarrre/a*a

#reduit le polygone entre debut et fin selon la methode de Ramer?Douglas?Peucker
# retourne le premier point des qu'il a change et data modifie en rajoutant/supprimant un point
def reducepoly(data,deb,fin):
    #on cherche sur tous les points de l'intervalle deb,fin le plus loin de la droite debut/fin' \
    #cad celui qui fait le plus grand triangle avec les deux bouts du segment
    # surf d'un triangle de cotes abc : A = sqrt(s (s-a)(s-b)(s-c) avec s = (a+b+c)/2
    maxdist = -100
    pttrouv=fin

    #on cherche le pt le plus eloigne de la droite debut, fin
    for pt in np.arange(deb+1,fin+1):
        surf = distance(data[deb],data[fin],data[pt])
        if maxdist==-100 or surf>maxdist:
            maxdist = surf
            pttrouv = pt



# fonction pour appliquer le reducepolu
def tstreducepoly():
    data = csv2data.readcsv("contour1.csv")
    #larray = np.asarray(data)
    #print larray

    prvfin = 0
    for deb in np.arange(0,len(data)):
        fin=calcpairepts(data,deb,dseuil)
        deb = reducepoly(data,deb,fin)


#fonction calculant le cdg du polygone
def cdg(data):
    fin=len(data)-1 #-1 car polygone ferme a la lecture
    c = data[0]
    b =data[1]
    sumcdgx=0
    sumcdgy=0
    sumsurf=0
    nbtraits =0

    for i in np.arange(2,fin):
        if i==fin-1:
            a = data[fin-1]
            b = data[1]
        else:
            a=b
            b = data[i]
        print c,a,b
        nbtraits = nbtraits+1
        Pcdgx,Pcdgy,surf=cdgpondere(a,b,c)
#        plotcdg([Pcdgx,Pcdgy],color="green")
        sumcdgx =sumcdgx+Pcdgx*surf
        sumcdgy =sumcdgy+Pcdgy*surf
        sumsurf =sumsurf+surf

#debug cdg
#        plotpolygone(data,color="red")
#        plt.plot([a[0],c[0],b[0]],[a[1],c[1],b[1]],color = "green")
#        plt.show()

#    print nbtraits
#    raw_input("ok")

    return sumcdgx/sumsurf,sumcdgy/sumsurf,sumsurf


#fonction trouvant les 2 points du petit diametre du polygone
#def findpetitdiametre():
#    for i in np.arange(0,len(data)):
def plotpolygone(data,color):
   dataunzip = zip(*data)
   plt.plot(dataunzip[0],dataunzip[1],color = color)

def plotcdg(cdg,color):
   xcdg = [cdg[0]+2,cdg[0]-2,cdg[0],cdg[0]]
   ycdg = [cdg[1],cdg[1],cdg[1]+2,cdg[1]-2]
   plt.plot(xcdg,ycdg,color = color)

#centre le molygone et calcul son profil angulaire
# c a d les angles successifs des segments depuis le centre
def centrepolygone (data, cdgx, cdgy):
    data[:] = [[x[0] - cdgx,x[1] - cdgy] for x in data]
    return data


#calcule la distance min entre segment p1 2 et point C
#le segment le plus proche = le plus petit triangle 2pts -> cdg
# le pt le plus proche est soit perpendiculaire au segment passant par le centre, ou un des 2 points du segment (si pprojection en dehors du segment.
# autant calculer la hauteur et
#distance d'un point XpYp a une droite ax+by+c=0
#d = abs(aXp+bYp+c)/(sqr(a*a+b*b)
def calcmindistcare(p1,p2,c):
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]
    xc = c[0]
    yc = c[1]

    if np.abs(x1-x2) <1 : # segment presque vertical
       #cas d'une droite verticale : on compare les y
        if (max(y1,y2) < yc):
            d=yc-max(y1,y2)       #distance en y du point le plus proche
        else:
            if (min(y1,y2) > yc):
                d=min(y1,y2)-yc  #ditance en y du point le plus proche
            else:
                d = 0 #point en face du segment : pas de distance en y
        return d*d+(x1-xc)*(x1-xc) #on rajoute la distance en x pour faire l'hypothenuse
    #droite pas verticale y = ax+b ou 0 = ax - y + b
    coeffa = (y1-y2)/(x1-x2)
    coeffc = y2-coeffa*x2
    #coeffb = -1

    #distance au carre
    dist = (coeffa*xc-yc+coeffc)*(coeffa*xc-yc+coeffc)/(coeffa*coeffa+1) #coeffb = -1
    dist1 = (x1-xc)*(x1-xc)+(y1-yc)*(y1-yc)
    dist2 = (x2-xc)*(x2-xc)+(y2-yc)*(y2-yc)
    if (dist2 < dist):
        dist=dist2
    if (dist1 < dist):
        dist=dist1
    return dist  #distance au carre



#cree un tableau de tous les angles entre points et cdg, aisi que leur distance
#tableau longueur,angle entre -pi/2 , pi/2
def calcanglespts(data, cdg):
    datatrigo=[]
    xc = cdg[0]
    yc = cdg[1]
    for i in enumerate(data): #utilisation d'un enumerate -> o reduit le data de 1 sinon ca deborderait
        xi = i[1][0]
        yi = i[1][1]
        dx = (xi-xc)*(xi-xc)+(yi-yc)*(yi-yc) #distance au carre
        if np.abs(xi-xc) < 1:
            xi=xc+1 #petite correction sans importance sauf cas vraiment tordus
        angle = np.arctan2(yi-yc,xi-xc)
        datatrigo.append([dx,angle])

    return datatrigo




#nouvel algo de recherche en Y
# partir d'un point et so suivant
# chercher dans le contour le point faisant un y avec le plus proche
# si on est dans le Y : on mesure et on passe a l'oppose suivant
# sinon : on avance les 2 poins et on garde le meem oppose


def chercheYmini(data,c):
    datatrigo = calcanglespts(data, c)
    fin = len(data)
    status = 0 #0 : cherche le premier point qui marche
               #1 : on a trouve un y , on avance cote pied
               #2 : on a trouve un y , on avance cote bras
                #5 : les bras sont revenus au depart : c'est fini
    bras1 = 0
    bras2 = 1
    pied =bras2+2 #on part 2 points plus loin
    brasmin=-1
    piedmin=-1
    mindist=-1


    while status != 5:

        if status == 1: # avance des pieds : avance pied ne marche plus pas marche : on avance les bras
           pied = pied-1
           status = 2

        if pied == bras1 and status ==0 :
           status = 4²

        if status == 2 or status ==4: # on est en avacnce bras : on continue
            if status ==4:
                status =0 #on reste en status 0 mais on avance les bras

            bras1 = bras2
            bras2 = bras2+1

            if bras1 == fin:
              bras1 = 0

            if bras2 == fin: # les bras on fait tout le tour : c'est fini
              status =5

        if status ==1 or status == 0:
            anglebras1 = (datatrigo[bras1][1]-datatrigo[pied][1]) #angle pied-cdg-bras1
            anglebras2 = (datatrigo[bras2][1]-datatrigo[pied][1]) #angle pied-cdg-bras2

            print anglebras1,anglebras2
            if (anglebras1*anglebras2 > 0 ): # eux angles de meme signe : on n'est pas entre les bras
                print "pas ok"
                if status == 0: # avance des pieds : avance pied ne marche plus pas marche : on avance les bras
                    pied = pied+1
                    if pied == fin:
                        pied =0


            else : # ca marche : la droite pied-cdg traverse entre les bras du y
                print "OK"
                dist = min(datatrigo[bras1] ,datatrigo[bras2]) #on prend une distance (parmi les 2 des 2 bras)
                #on utilise juste la distance aux points mais en fait il faudrait faire plus fin (style surface du triangle ?)
                if mindist == -1 or dist < mindist :  #on a trouve un point plus proche
                    mindist = dist
                    brasmin = bras1
                    piedmin = pied

                pied = pied+1 # on avance le pied d'un cran
                if pied == fin:
                    pied =0

                status =1 # on revient en mode avancer les pieds (quitte a ce que ca rate et que ca rebascule en avancer les bras

                if pied == bras1: # le pied a atteint le bras : il faut avanvcer le bras (mais il y a un gros os
                    status = 2


        plotpolygone(data,color="red")

        plt.plot([data[bras2][0],data[bras1][0],c[0],data[bras2][0],c[0],data[pied][0]],
                 [data[bras2][1],data[bras1][1],c[1],data[bras2][1],c[1],data[pied][1]],
                 color="green"
                )
        plt.show()



    return brasmin, piedmin







# ----------------------
def tstpolyfunc():
     plt.interactive(False)
     lastring = raw_input("csv to decode calque 1")
     data1 = csv2data.decodesvgpath(lastring)
     lastring = raw_input("csv to decode calque 2")
     data2 = csv2data.decodesvgpath(lastring)

     fig = plt.figure()

     ax = fig.add_subplot(111)
     xcdg,ycdg,surf = cdg(data1)

     plt.axis([xcdg-150, xcdg+150, ycdg-150, ycdg+150])
     plotpolygone(data1,color="red")

     dist,minpt = chercheYmini(data1,[xcdg,ycdg])
     plotcdg([xcdg,ycdg],color="red")

     bras,pied = chercheYmini(data1,[xcdg,ycdg])

     plt.plot([data1[minpt][0],data1[minpt+1][0]],
                   [data1[minpt][1],data1[minpt+1][1]],
                   color="purple")

     #trace des 2 petits cotes
     plt.plot([data1[bras][0],xcdg,data1[pied][0]]
              [data1[bras][1],ycdg,data1[pied][1]],
              color="orange")

     plt.show()


     data1 = centrepolygone(data1,xcdg,ycdg)


     print "rect1",surf
     xcdg,ycdg,surf = cdg(data2)
     #on rend les axes isotropes
     plt.axis([xcdg-150, xcdg+150, ycdg-150, ycdg+150])

     plotpolygone(data2,color="blue")
     plt.show()

     data2 = centrepolygone(data2,xcdg,ycdg)

     plotpolygone(data1,color="red")
     plotpolygone(data2,color="blue")
     plt.show()


     plotcdg([xcdg,ycdg],color="blue")
     print "rect2",surf


#main

tstpolyfunc()





