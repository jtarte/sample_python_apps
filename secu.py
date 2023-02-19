import sys,getopt
import random

LEN_KEY= 32

def xor(c1,c2):
    """
    fonction xor
    retour 1 si c1=c2, 0 sinon \n
    c1,c2 characteres a comparer \n
    return '0' ou '1' suivant le resultat de la comparaison
    """
    if c1 == c2 :
        # si les charachteres sont egaux, on retourne 0
        return '0' 
    else:
        # sinon on retourne 1
        return '1'

def encrypt(m,k):
    """
    fonction encrypt
    encrypt le message m avec la cle k \n
    m message à encrypter \n
    k cle d'encryptage \n 
    return le message encrypté 
    """
    x = len(m)
    y = len(k)
    j = 0
    r=''
    # boucle sur les elements de m
    for i in range(x):
        # calcule l'indice dans k. longueur de k pouvant inferieur a longuer de m. On boucle sur sur k
        j = i % y
        # ajoute le caractere encode avec xor
        r = r + xor(m[i],k[j])
        i = i +1
        j = j +1
    return r 

def to_bin(ms):
    """
    fonction to_bin\n
    convertit un nombre sous forme de string en sa valeur binaire \n
    ms la chaine de charactere representant le nombre a convetir \n
    return la chaine de charatere representant le nombre en binaire (chaque chiffre est encode sur 4 bits)
    """
    r=""
    # boucle sur les caractères de la chaine
    for i in range(len(ms)):
        #convertit  le nombre en binaire 
        r = r + format(int(ms[i]),"b").zfill(4)
    return r

def is_valid_ssid(id):
    """
    fonction is_valid_ssid \n
    Verifie si un id est un id de securité sociale valide \n
    id l'id a verifier \n
    return True si l'id est valide, False sinon
    """
    l = len(id)
    # obient le ssid sans la cle
    num = int(id[0:l-2])
    # obtient la clé
    key = int(id[l-2:l])
    # verifie si l' id plus la clé est un multiple de 97
    if ((num + key) % 97) == 0 :
        return True 
    else:
        return False

def decode(ssid, indice):
    """
    fonction decode 
    decode un chiane de cractère pour obtenir un ssid a partir d'un indice
    ssid la chaine a decode
    indice l'indice pour de le decodage
    return la chaine décodée 
    """
    for i in range(10):
        indice2 = indice + str(i)
        key = encrypt(ssid, to_bin(indice2))[0:32]
        id = from_bin(encrypt(ssid,key))
        if is_valid_ssid(id):
            return(id,key)
    return None

def from_bin(id):
    """
    fontion qui convertit une chaine binaire (4bits par characrtère) en chaine de characteres
    id chaine binaire
    return la chaine de caractères correspondantes
    """
    i = 0
    r = ''
    while i<len(id):
        n = str(int(id[i:i+4],2))
        r = r + n
        i = i+ 4
    return r


def gen_key():
    """
        fonction gen_key
        genere un cle d'encode aléatoire 
        return une cle d'encode  
    """
    # initilaise le generateur aleatoire
    random.seed()
    # tire la clé au hasard
    return str(random.randint(0,99999999)).zfill(8)

def gen_ssid():
    """
        fonction gen_ssid
        genere aleatoirement un ssid de securite solciale 
        return un ssid de securité sociale
    """
    # initilaise le generateur aleatoire
    random.seed()
    # tire les differentes partie du ssid
    ssid=str(random.randint(1,2))
    ssid=str(ssid)+str(random.randint(0,99)).zfill(2)
    ssid=str(ssid)+str(random.randint(1,12)).zfill(2)
    ssid=str(ssid)+str(random.randint(0,99)).zfill(2)
    ssid=str(ssid)+str(random.randint(1,999)).zfill(3)
    ssid=str(ssid)+str(random.randint(0,999)).zfill(3)
    # Calcule la clé correspond au ssid tiré
    modulo = int(ssid) % 97
    key = 97 - modulo
    ssid = str(ssid)+(str(key).zfill(2))
    # verifie si le ssid calculé est valide 
    if (is_valid_ssid(ssid)):
        return ssid, None
    else:  
        return 0,"erreur le ssid calculé est invalide"

def usage():
    print("usage")
    print("python3 secu.py -h|-k|-s|(-d -e <numero_encode> -i <indice>)")
    print("     -h affiche ce message d'uage")
    print("     -s genere un ssid de securite sociale")
    print("     -k genere une cle d'encodage")
    print("     -d decode la chaine passé à partie de l'indice")
    print("         -i indice de decodeage")
    print("         -e chaine à decoder")

def main(argv):
    """
    Fonction main
    Lance le programme
    """    
    try:
        opts, args = getopt.getopt(argv,"hskde:i:",["ifile=","efile="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    decode_action = False
    encoded = ""
    indice = ""
    
    # si pas d'arguments sur la ligne de commande, on affiche l'usage
    if len(opts) == 0:
        usage()
        exit(1)

    # boucle sur les arguments
    for opt, arg in opts:
        if opt == '-h':
            usage()
            exit(1)
        elif  opt == '-s' :
            # appel à la generation d'un ssid
            print("Generation d'un ssid de sécurité sociale")
            ssid, err = gen_ssid()
            if err == None:
                print("ssid: ",ssid)
                exit(0)
            else:
                print(err)
                exit(2)
        elif opt == '-k':
            # appel à la genration d'un clé
            print("Generation d'une clé de codage")
            print("key: ",gen_key())
            exit(0)
        elif opt == '-d':
            decode_action = True
        elif opt == '-i':
            indice = arg
        elif opt == '-e':
            encoded = arg
        else :
            print(" mauvais parametre donné à la commande")
            usage()
            exit(3)
    # lance le decodage 
    if decode_action == True:
        ssid, key = decode(encoded, indice)
        print("decodage et calcul de la clé")
        print ("securite sociale id : ", ssid)
        print ("cle de codage: ", key)


if __name__ == "__main__":
    main(sys.argv[1:])