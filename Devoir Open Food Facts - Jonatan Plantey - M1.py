# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 13:57:07 2023

@author: Jonatan Plantey
"""
# =============================================================================
# Objectif:
# Le but de ce devoir est de scraper les  informations des 6 premiers produits du site :
# 
# https://fr.openfoodfacts.org/contributeur/systeme-u?sort_by=nutriscore_score
# 
# en comparant deux méthodes d'extraction.
# 
# Les informations à scraper sont :
#     - le nom du produit
#     - sa quantité
#     - le conditionnement
#     - la marque
#     - le tableau des catégories
#    
# Première méthode : récupérer les liens des 6 produits, suivre le lien et en extraire les informations.
# Deuxième méthode : récupérer les liens des 6 produits, en extraire le code et utiliser l'API mise à disposition par openfoodfacts.
# =============================================================================

###############################################################################
########################## SCRAPING DE Open Food Facts ########################
###############################################################################


###############################################################################
###                    1ère partie - Première méthode                       ###
###############################################################################

# -- Import modules
import requests
import bs4
import csv




url = "https://fr.openfoodfacts.org/contributeur/systeme-u?sort_by=nutriscore_score"

r = requests.get(url)

if r.status_code == 200:

    soup = bs4.BeautifulSoup(r.text, 'html.parser')


#%%
###################################################
# Scraping des liens vers les 6 premiers produits #
###################################################

search_results = soup.find('div', attrs={"id": "search_results"})

soup_liste_produits = search_results.find_all('a')

liens = []

i = 1
for soup_produit in soup_liste_produits:
    if i <= 6:
        lien_produit = "https://fr.openfoodfacts.org" + soup_produit.get("href")
        liens.append(lien_produit)
        i += 1

#print(liens)


#%%
#########################################################################
# Scraping des informations demandées pour ces produits sur le site web #
#########################################################################

data_produits_html = []

for url in liens:
    
    r = requests.get(url)
    
    if r.status_code == 200:

        soup = bs4.BeautifulSoup(r.text, 'html.parser')
        
        titre_produit = soup.find("h1", class_="title-3").text
        nom_produit = titre_produit.split('-')[0].strip()
        print(nom_produit)
        
        
        produit = soup.find('div', attrs={"class": "medium-8 small-12 columns"})
        
        quantité = produit.find('span', attrs={"id": "field_quantity_value"}).text
        print(quantité)
        
        conditionnement = produit.find('span', attrs={"id": "field_packaging_value"}).text
        print(conditionnement)
        
        marque = produit.find('span', attrs={"id": "field_brands_value"}).text
        print(marque)
        
        catégories = produit.find('span', attrs={"id": "field_categories_value"}).text
        print(catégories)
        
        data_produits_html.append({'Nom du produit': nom_produit,
                                   'Quantité': quantité,
                                   'Conditionnement': conditionnement,
                                   'Marque': marque,
                                   'Catégories': catégories})


with open('data_produits_html.csv', 'w', newline='') as f:
    fieldnames = ['Nom du produit', 'Quantité', 'Conditionnement', 'Marque', 'Catégories']
    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()
    writer.writerows(data_produits_html)


#%%
###############################################################################
###                    2ème partie - Deuxième méthode                       ###
###############################################################################


##############################################
# Scraping des codes pour ces mêmes produits #
##############################################

codes_produit = []

for url in liens:
    
    if r.status_code == 200:
    
        r = requests.get(url)
    
        soup = bs4.BeautifulSoup(r.text, 'html.parser')
        
        produit = soup.find('div', attrs={"class": "medium-8 small-12 columns"})
        
        code_produit = produit.find("span", id="barcode").text
        
        codes_produit.append(code_produit)

print(codes_produit)


#%%
###################################################################
# Scraping des informations demandées pour ces produits via l'API #
###################################################################

# =============================================================================
# Aide:
# Si vous souhaitez mieux visualiser le JSON vous pouvez le copier dans un
# formatter online tel que https://jsonformatter.curiousconcept.com/#
# =============================================================================

data_produits_API = []

for code_produit in codes_produit:
    
    url = "https://world.openfoodfacts.org/api/v0/product/" + code_produit + ".json"
    
    r = requests.get(url)
    
    if r.status_code == 200:
        
        product_dict = r.json()
    
        nom_produit = product_dict['product']['product_name_fr']
        print(nom_produit)
        
        quantité = product_dict['product']['quantity']
        print(quantité)
        
        conditionnement = product_dict['product']['packaging']
        print(conditionnement)
        
        marque = product_dict['product']['brands']
        print(marque)
        
        catégories = product_dict['product']['categories']
        print(catégories)
        
        data_produits_API.append({'Nom du produit': nom_produit,
                                   'Quantité': quantité,
                                   'Conditionnement': conditionnement,
                                   'Marque': marque,
                                   'Catégories': catégories})


with open('data_produits_API.csv', 'w', newline='') as f:
    fieldnames = ['Nom du produit', 'Quantité', 'Conditionnement', 'Marque', 'Catégories']
    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()
    writer.writerows(data_produits_API)


###############################################################################
###                     Comparaison des deux méthodes                       ###
###############################################################################

''' Si l'on ne compare les deux méthodes qu'à l'issue de l'étape commune de la
récupération des liens vers chaque page des produits :
 - dans le premier cas, il ne reste plus qu'à scraper les informations demandées
dans la page
 - dans le deuxième cas, il faut tout de même scraper le code du produit dans
cette même page avant de questionner l'API
 
On voit donc dans ce cas précis, que la deuxième méthode utilise un plus grand
nombre de lignes de code.

Malgré tout, la deuxième méthode demande une recherche beaucoup plus simple et
beaucoup plus rapide des mots clés (keywords) dans le fichier JSON que ne l'est
celle des balises dans le contenu HTML.

Conclusion : L'utilisation de l'API reste plus rapide, plus confortable et donc
préférable. '''



