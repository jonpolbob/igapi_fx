import os 
#pour python 3

#list les fichiers
#cree un dictionary et l'allaonge

mypath = "c:\\windows"

selection={}

def listrep():
    global selection
    selection = {}
    letternum = 0

    for element in os.listdir('c:\\windows'):
       print (element )
       if os.path.isdir('c:\\windows\\'+element):    #rajouter le chemin car on n'a que les dirs
             selection[chr(ord('A')+letternum) ]  = element
             letternum += 1

#lecture des items d'un dictionaire
    for key in selection:
         print (key, " : ", selection[key])

    return 




Encore=True

while (Encore) :
    print ("1 : listerep")
    print ("2 : aulit ")
    
    cmd = input  ('commande')
    if cmd == "1 : list":
        listrep()
        continue
    if cmd == "2 : selection":
        liste = input(' fichiers a choisir')
        #foreach lecar in liste: #ne marche pas
        print (enumerate(liste))
        for i, c in enumerate(liste):  #toutes les lettres du nom
            print ([i] , selection[c])
        
              
    
    
#lecture des items d'un dictionaire
for key,valeur in enumerate(selection):
    print (key, " : ", valeur)
   
   
 
