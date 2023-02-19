#import des bibliothèques
import urllib3
import json
import sys
import urllib.request
from PIL import Image
from image import DrawImage

# chargement du fichier
def load_meteo(ville):
    """
    fonction load_meteo
    ville nom de la ville dont on veut les information météo
    """
    http = urllib3.PoolManager()
    url_param="http://api.weatherstack.com/current?access_key=ae53a97a4aaffb9b508ee776458312e8&query="+ville
    # appel à l'API
    r = http.request('GET',url_param)
    # chargement de la repose sous forme de json
    reponse=json.loads(r.data.decode('utf-8'))   
    # verifie si on obtient une reponse
    if 'success' in reponse and reponse["success"] == False:
        return None
    # retourne les informations de méteo
    return reponse

def show_image(url_image):
    """
    fonction show_image
    url_image url de l'image à afficher
    """
    img  = DrawImage.from_url(url_image,(48,36))
    img.draw_image()

def show_information(information):
    """
    fonction show_inforamtion
    information objet json qui contient les infroamtions à afficher 
    """
    print("Lieu: %s    Région: %s    Pays: %s" %(information["location"]["name"],information["location"]["region"],information["location"]["country"]))
    print("Date : %s" %(information["location"]["localtime"]))
    print("temps: %s"%(information["current"]["weather_descriptions"][0]))
    print("température: %s °C"%(information["current"]["temperature"]))
    print("Indce UV: %s"%(information["current"]["uv_index"]))
    print("Pression: %s"%(information["current"]["pressure"]))
    print("Visibilité: %s"%(information["current"]["visibility"]))

def main(args):
    """
    fonction main
    args arguments recupérés sur la ligne de commande
    """
    # verifie si on a bien un argument (le nom de ville)
    if len(args) !=1:
        print("nombre de parametre incorrect")
        print("usage: python3 weather.py <ville>")
        sys.exit(1)
    # recuoere les information de méteo
    info = load_meteo(args[0])
    #verifie si on a bien recu des information météos
    if info == None:
        print("erreur sur la ville. Veuillez vérifier le nom de la ville")
        sys.exit(2)
    # Affichage du resultat
    show_information(info)
    show_image(info["current"]["weather_icons"][0])

if __name__ == "__main__":
    main(sys.argv[1:])
