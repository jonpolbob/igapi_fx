#!/usr/bin/env python
# -*- coding: utf-8 -*-

# readsemcsv
# utilisatires pour lire une semain dans les csv de mois

# le fichier zip doit s'appeler BIDAAABBBmmyy

# la fonction presentzip(paire,mois,year) dit si le zip est dispo
# la fonction creenomzip(paire mois year) renvoie la liste des zip correspondant a la semaine


import zipfile
import datesemaineutils as datesm
import read_selenium
import ReadWebWindows
# renvoie la liste des csv a utiliser pour pouvoir charger cette semaine
# accompagnée de la date (jour, mois annee du premier jour alire dans ce fichier
#le nom du csv est yyymmpaire et du nombre de jours a lire dans chaque fichier
def creenomcsv(paire, semaine, annee):
    listemois = datesm.getlistemois(semaine, annee)
    listezips = []
    for mois in listemois:
        zipname = "%04d%02d%s.csv" % (mois[3],mois[2],paire)
        jourdumois = mois[1]
        nbjours = mois[0]
        listezips.append([nbjours,jourdumois,mois[2],mois[3],zipname])
    print(listezips)
    return listezips

# import zipfile

# rep ou sont les donnees
datarep = "c:\\tmp"


################## readlines ####################
# : lecture de qq jous dans un fichier mois
# lit nbjours dans un fichier csv contenant le mois pour une paire
# a partir du jour du mois =  jour
# ligne par ligne
# renvoie le nb de minutes entre la ligne et datedeb
# yield la date et la valeur
# renvoie le nb de jours lus quand le balayage est fini (None, nbjourslus)
# charge dans le tableau le nombre de jourd nbjours a partir du jour jour
def readlinescsv(nbjours, jour, nomcsv, paire):
    # on lit le zip sur le disque
    nbjourslus = 0
    lstday = -1
    delta = 6-nbjours #delta en jours depuis le debut de la semain, pour calcul de la coordonnee de la valeur en jour par rapport au dimanche
    with open("c:\\tmp\\"+nomcsv, mode='r') as read1:
        for laligne in read1:
            numsample, date, begin = datesm.decodelinemois(laligne)  # lecture de la ligne
            if lstday != date.day:  # la date a changé
                if nbjourslus != 0:  # on a commence a lire des jours
                    nbjourslus = nbjourslus + 1  # un nouveau jour
                else:
                    print("\rjour", date.day, )  # on n'a pas commence a lire des jours : on saute

            lstday = date.day

            if date.day == jour:  # on a atteint le jour recherche
                nbjourslus = 1  # on commence

            if nbjourslus > nbjours:  # on a lu le bon nombre de jours
                break  # fin du for

            if nbjourslus != 0:
               # delta = date - datedeb  # delta depuis debut semaine
                yield nbjourslus, date, int(delta*24*60), begin  # date, valeur debut heure en minutes


import os.path

#genere un tableau contenant toutes les donnees pour cette paire et cette semaine
def generesemaine(paire,semaine, annee):
    ok=False
    listezip = creenomzip(paire, semaine, annee) #liste jour du mois, mois, annee, nomzip
    #regarde si les zip existent
    for nomfich in listezip:
        nomfich = datarep+"\\"+nomfich[3]
        print(nomfich)
        if os.path.isfile(nomfich):
            ok = True
        else:
            readwebfile(paire,nomfich[1],nomfich[2])






######
#pour test
if __name__=="__main__":
    driver = ReadWebWindows.initwebwindows()
  
    
    paire = "EURUSD"
    semaine=9
    annee = 2018
    semainestr = "{0:02}".format(semaine)
    anneestr = "{0:04}".format(annee)
    print(semainestr, anneestr)
    toread = creenomcsv(paire, semainestr, anneestr)
    for filesourc in toread:
        print(filesourc)
        read_selenium.loadpairemoisan(driver,paire,"{0:02}".format(filesourc[2]),"{0:04}".format(filesourc[3])) #download le fichier dans tmp
        jourdeb = filesourc[1] #j1er jour du mois a lire
        nbjours = filesourc[0]
        #lecture a partir de datedeb nbjours, nom du csv
        laloop = readlinescsv(nbjours, jourdeb, filesourc[4], paire)
        for i in laloop:
            print (i)
            

    #generesemaine("aaabbb",1,2013)
    #laliste = creenomzip("aaabbb",1,2013)
#print (laliste)