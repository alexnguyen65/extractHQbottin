#
# Hydro-Québec rend disponible le bottin téléphonique de ses employés
# via son site Internet: 
#     http://rz.hydroquebec.com/RZWeb/afficherAccueil.do?init=0
#
# Cependant, on doit saisir au moins 2 caractères pour le nom et au moins
# 2 caractères pour le prénom, afin d'y effectuer la recherche.
#
# Ce script, écrit en python v2.x, permet d'extraire tout le contenu du bottin
# téléphonique, en automatisant la saisie de toutes les permutations possibles
# (A à Z) des noms et prénoms.
#
import mechanize
from bs4 import BeautifulSoup
import string
import time
import sys
import random
import datetime

reload(sys)
sys.setdefaultencoding('utf8')

url = 'http://rz.hydroquebec.com/RZWeb/afficherAccueil.do?init=o'

f = open("bottin.txt","w")
print "Debut..."
total_trouve = 0

for nom1 in string.ascii_uppercase:
   for nom2 in string.ascii_uppercase:
      for prenom1 in string.uppercase:
         br = None
         br = mechanize.Browser()
         br.open(url)
         for prenom2 in string.uppercase:
            br.select_form('listeAbonnesRechercheFB')
            br.form['nom'] = nom1 + nom2
            br.form['prenom'] = prenom1 + prenom2
            time.sleep(1)
            now = datetime.datetime.now()
            print nom1+nom2, prenom1+prenom2, now
            response = br.submit()
            soup = BeautifulSoup(response, 'html.parser')
            nb_trouve = soup.find('li').contents[0].split(' ')[0]
            if nb_trouve == "Une":
               nb_trouve = "1"
            #endif
            if nb_trouve.isdigit():
               nb_trouve = int(nb_trouve)
               all_tbody = soup.find_all('tbody')
               i = 0
               for t in all_tbody:
                  if i >= nb_trouve:
                     break
                  all_td = t.find_all('td')
                  j = 0
                  s = "|"
                  for td in all_td:
                     j = j + 1
                     if td.string is None:
                        s = s + "*|"
                     else:
                        s = s + td.string.strip() + "|"
                     #endelse
                     if j == 6:
                        i = i + 1
                        print i, s
                        f.write(s+"\n")
                        if i >= nb_trouve:
                           break
                        #endif
                        j = 0
                        s = "|"
                     #endif
                  #endfor td
               #endfor t
               print nb_trouve, "trouve"
               total_trouve = total_trouve + nb_trouve
            else:
               print "Pas trouve"
            #endelse
         #endfor prenom2
      #endfor prenom1
   #endfor nom2
#endfor nom1

f.close()
print "TOTAL TROUVE:", total_trouve
quit()

