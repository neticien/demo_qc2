#!/usr/bin/env python3

import trio
import httpx
import pandas as pd

from holehe.modules.social_media.twitter import twitter

# Constantes
liste_prenoms = ("Robert","Anne","Allan")
liste_noms = ("PATE","ONYME","SMITHEE")
liste_services_mails = ("gmail.com","tutanota.com")


async def generer_mails(liste_noms, liste_prenoms, liste_services_mails):
    """Génération des courriels à tester avec Holehe"""
    liste_mails = []
    
    if (len(liste_noms) != len(liste_prenoms)):
        raise "Il n'y a pas le même nombre de noms et de prénoms ducon !"
    for i in range(len(liste_noms)):
        nom = liste_noms[i].lower()
        prenom = liste_prenoms[i].lower()
        for service_mail in liste_services_mails:
            liste_mails.append("{nom}.{prenom}@{service_mail}".format(nom=nom, prenom=prenom, service_mail=service_mail))
            liste_mails.append("{prenom}.{nom}@{service_mail}".format(nom=nom, prenom=prenom, service_mail=service_mail))
            liste_mails.append("{nom}{prenom}@{service_mail}".format(nom=nom, prenom=prenom, service_mail=service_mail))
            liste_mails.append("{prenom}{nom}@{service_mail}".format(nom=nom, prenom=prenom, service_mail=service_mail))
            liste_mails.append("{prenom}.{nom}@{service_mail}".format(nom=nom, prenom=prenom[0], service_mail=service_mail))
    
    return liste_mails

async def test_mail_twitter(liste_mails):
    """Vérification de l'utilisation de courriels pour l'inscription d'un compte Twitter"""
    result = []
    found = 0
    client = httpx.AsyncClient()

    for email in liste_mails:
        out = []
        await twitter(email, client, out)
        
        if (out[0]["exists"] == True):
            print("Found {email} on {platform} !".format(email=email, platform=out[0]["name"]))
            found += 1
            
        out[0]["email"] = email
        result.append(out[0])
    await client.aclose()
    return result,found


async def main():
    liste_mails = await generer_mails(liste_noms, liste_prenoms, liste_services_mails)
    #On test les mails générés sur Twitter
    result, found = await test_mail_twitter(liste_mails)
    # On affiche les résultats de la collecte
    print("{found}/{nbr_comptes_générés} comptes trouvés !".format(found=found, nbr_comptes_générés=len(result)))

    df = pd.DataFrame(result)
    df.to_csv (r'collecte_holehe.csv', index = None)


if __name__ == "__main__":
    trio.run(main)
