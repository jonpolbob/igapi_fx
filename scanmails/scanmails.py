#!/usr/bin/env python

import sys
import imaplib
#import getpass
import email
import datetime
import re
import time

Encore =True


while (Encore):

    M = imaplib.IMAP4_SSL('imap.gmail.com')


    try:
        M.login('jonpolbob@gmail.com', 'pqscsq2snt')
    except imaplib.IMAP4.error:
        print ("LOGIN FAILED!!! ")
    # ... exit or deal with failure...try:

    foundvaleur=0

    rv, mailboxes = M.list()
    if rv == 'OK':
        print("Mailboxes:")
        print(mailboxes)
        M.select("inbox")  # connect to inbox.
        result, data = M.search(None, "ALL")


        ids = data[0]  # data is a list.
        id_list = ids.split()  # ids is a space separated string


        for tstemail in  id_list[-30:] :  #liste de tous les emails
            result, data = M.fetch(tstemail, "(RFC822)")  # fetch the email body (RFC822) for the given ID

            raw_email = data[0][1]
            strraw = raw_email.decode('unicode_escape')

            #print(strraw)
            email_message = email.message_from_string(strraw)

            #print(email_message['To'])

            fromstr = email.utils.parseaddr(email_message['From'])  # for parsing "Yuji Tomita" <yuji@grovemade.com>
            subject = email_message['Subject']
            print("FROM",fromstr)

            if 'jpaul.robert' in fromstr[1]:
                print(strraw)
            #  print('found')
                if email_message.is_multipart():
                    for payload in email_message.get_payload():
                        # if payload.is_multipart(): ...
                        monmess  = payload.get_payload()
                        print (monmess)

                        if 'euros' in monmess:
                            valeur = re.findall(r'\d{4,7}', monmess)
                            print("found valeur",valeur)
                            foundvaleur = int(valeur[0])
                            M.store(tstemail,'+FLAGS','\\Deleted')

                    else:
                        monmess = email_message.get_payload()
                        print(monmess)

                        if 'euros' in monmess:
                            valeur = re.findall(r'\d{4,7}', monmess)
                            print("found valeur", valeur)
                            foundvaleur = int(valeur[0])
                            M.store(tstemail, '+FLAGS', '\\Deleted')

    M.close()
    M.logout()

    time.sleep(10)

    from email.mime.text import MIMEText as text

    if foundvaleur !=0 :
        print("answer")
        import smtplib
        import mimetypes

        time.sleep(470)
        resu = (foundvaleur+44000)*50.32/100
        part = resu +26506
        mypart = part * 49.8/100

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("jonpolbob@gmail.com", "pqscsq2snt")

        msg = text("salut J.P.\r\n a "+'{0:d}'.format(foundvaleur)+" de capitaux propres pour vp, \r\n l\'estim de la part vp pour rnd vaut : "+'{0:.2f}'.format(resu) +" donc la valo de rnd vaut " + '{0:.2f}'.format(part) + "\r\n alors ne descends pas en dessous de "+'{0:d}'.format(int(mypart)) + " euros. \r\n bonne journée! \r\n Lio.")
        msg['Subject']="RE:"+subject
        msg['From'] = "jonpolbob@gmail.com"
        msg['To'] = "jpaul.robert@gmail.com"
        server.sendmail("jonpolbob@gmail.com", "jpaul.robert@gmail.com", msg.as_string())
        server.quit()
    #print(email_message.items())# print all headers

    foundvaleur =0

