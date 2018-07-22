#toutes sortes d'utils pour lire et calculer les dates , minutes et jours de semaine

import datetime


##################################################"
##utilitaire renvoyant tous les elements d'une date
#time est un datetime
##################################################"
def decodetime(time):
    letuple = time.timetuple()

    day = letuple.tm_day()
    hour = letuple.tm_hour()
    minute = letuple.tmmin()
    weekday = letuple.wday()
    return day,hour,minute,weekday


# ---------- decode une ligne de fichier csv ------------------
# renvoie
# #le nb minutes depuis debut du mois (1er du mois 0:00)
# la date
# la valeur de begin
#fonctionne pour une ligne de csv separre par ; contenant la date yyyymmdd hhmmss suvie dans le champ 0
def decodelinemois(laligne):
    colonnes = laligne.split(';')
    return decodesplittedline(colonnes)

def decodesplittedline(colonnes):
    # print (colonnes)
    ladate = colonnes[0]
    annee = int(ladate[0:4])
    mois = int(ladate[4:6])
    jour = int(ladate[6:8])
    heure = int(ladate[9:11])
    minute = int(ladate[11:13])
    secondes = int(ladate[13:15])
    datenumber = datetime.datetime(year=annee, month=mois, day=jour, hour=heure, minute=minute, second=secondes)
    datenumberdebut = datetime.datetime(year=annee, month=mois, day=1, hour=0, minute=0, second=0)
    deltatime = datenumber - datenumberdebut
    deltamins = int(deltatime.total_seconds()/60)

    beginvalue = colonnes[1]

   #deltamins = nb minutes depuis debut du mois
   #datenumber = la date-heure de cette mesure
    return deltamins, datenumber, float(beginvalue)


############ getdimanchefromweek ###############################
#renvoie la date du dimanche en debut de seamine (les semaines commencent un dimanche)
def getdimanchefromweek(semaine,annee):
    d = str(annee)+"-"+str(semaine).zfill(2)+"-1"
    r = datetime.datetime.strptime(d, "%Y-%W-%w") #on a la date du lundi
    rp = r-datetime.timedelta(1) #1 jour
    #print(r,rp)
    return rp.year,rp.month,rp.day

############ getsamedifromweek ###############################
#renvoie le dernier jour de la semaine
def getsamedifromweek(semaine,annee):
    d = str(annee) + "-" + str(semaine).zfill(2) + "-1"
    r = datetime.datetime.strptime(d, "%Y-%W-%w")  # on a la date du lundi
    rp = r + datetime.timedelta(6)  # +6 jour du lundi = le samedi
    return rp.year,rp.month,rp.day

#renvoie la date du dimanche commencant la semaine et le mois a lire, premier jour du mois a lire
#et le nombre de jours du mois 2 si necessaire (samedi exclus)
def getlistemois(semaine, annee):
    year,mois,day = getdimanchefromweek(semaine,annee) #dimancehe de la semaine
    leday = datetime.date(year,mois,day)
    newyear = year  #init inutil
    newmonth=mois  #init inutil
    nbjours1=6
    #bourrin on regarde la mois des 6 jours de la semaine
    for j in range(0,6):
        newmonth = (leday+datetime.timedelta(days=j)).month
        if newmonth != mois :
            nbjours1 = j
            newyear = (leday+datetime.timedelta(days=j)).year
            break
        
    nbjours2 = 6-nbjours1  #nb jours a lire dans mois 2
    if nbjours2 != 0:
        return [(nbjours1,day,mois,year),(nbjours2,1,newmonth,newyear)]
    else:
        return  [(nbjours1,day,mois,year)]
    
    


######
#pour test
if __name__=="__main__":
    #resu = getlistemois(9,2018)
    #semaine 9 : 4 jours le 25 fev (di25 lun26 ma27 me28) et 2j le 1 mars    (jeu 1, ven 2)
    resu = getlistemois(1,2018)
     #semaine 1 : 1 jours le 31 12 2017 et 5j le 1 janvier (jeu 1, ven 2)
   
    print (resu)
    

            
        
        
        
    
    
        
        
    
    
    
