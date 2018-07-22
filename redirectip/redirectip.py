__author__ = 'cagibi'
import os
import urllib2
import re
import time
from ftplib import FTP

def check_in():
    ext_ip = urllib2.urlopen('http://jpaulrobert.free.fr/getip.php').read()
    m=re.findall(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}", ext_ip)
    print m[0]
    print m[1]
    return m[0],m[1]

def updateftp(cur,prv):
    fichier = open('getip.php','w')
    fichier.write(r'<html> <head>  <title>Test PHP</title> </head> <body>currentip= <?php echo $_SERVER["REMOTE_ADDR"];?></p>previousip= ')
    fichier.write("85.170.128.102 ") #pour debug
    fichier.write("dummyip= ")
    fichier.write(cur)
    fichier.write("date= ")
    fichier.write(time.strftime('%d/%m/%y %H:%M',time.localtime()))
    fichier.write(r'</body></html>')
    fichier.close()

    fichier = open('raspi.php','w')
    fichier.write(r"<?php header('Location: http://")
    fichier.write(cur)
    fichier.write(r"/dokuwiki'); exit; ?><html></html>")
    fichier.close()



    ftp = FTP('ftpperso.free.fr','jpaulrobert','ks11nhw2')   # connect to host, default port
    ftp.storlines('STOR '+'getip.php',open("getip.php"))
    ftp.storlines('STOR '+'raspi.php',open("raspi.php"))
    ftp.retrlines('LIST')     # list directory contents


while True :
    cur=''
    prv=''
    cur,prv = check_in()
    if cur!=prv :
        updateftp(cur,prv)

    time.sleep(10)


