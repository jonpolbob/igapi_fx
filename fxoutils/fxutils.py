__author__ = 'cagibi'



# genere les 2 noms de fichiers de ces deux paires  un direct, et un inverse
# verifie que le fichier existe
def gennomfich(mois, annee,dev1,dev2):
    iannee = int(annee)
    imois = int(mois)
    surv = dev1
    paire=dev2
    nomfich1 = "E:\\stockage\\fxdata\\HISTDATA_COM_ASCII_"+surv+paire+"_M1"+"%4d%02d"%(iannee,imois)+".zip"
    nomfich2 = "E:\\stockage\\fxdata\\HISTDATA_COM_ASCII_"+paire+surv+"_M1"+"%4d%02d"%(iannee,imois)+".zip"

    return nomfich1,nomfich2




#fonctions de test

if __name__== "__main__":
    print gennomfich(1,2010,"aud","usd")

