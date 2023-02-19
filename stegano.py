from PIL import Image
import sys,getopt

# programme mode
MODE_HELP=0
MODE_ENCODE=1
MODE_DECODE=2

def lsbval(a,b):
    """
    lsbval 
    a: nombre a cacher
    b: nombre qui sert à cacher l'autre
    return: le nombre encodé
    """
    a1 = a >> 5
    b1 = b & 248
    return a1 + b1

def unlsbval(c):
    """
    unlsbval
    reconstitue le nombre caché dans c
    c: nombre contenant le nombre caché
    return: le nombre reconstitué
    """
    return ((c & 7) << 5) + 16

def stegano(image_a_cacher_file,image_cible_file, image_resultat_file):
    """
    fonction stegano 
    encode l'image a cacher dans un ficher fourni en entrée et enregistre le resultat dans un troisieme fichier
    img_a: image servant à cacher l'autre image. type Image
    img_b: image ) cacher. type Image
    """ 
    #ouvre l'image cible
    try:
        img_a=Image.open(image_cible_file)
    except FileNotFoundError:
        print("fichier %s non trouve."% (image_cible_file))
        exit(4)
    # ouvre l'image à cacher
    try:
        img_b=Image.open(image_a_cacher_file)
    except FileNotFoundError:
        print("fichier %s non trouve."% (image_a_cacher_file))
        exit(4)
    
    # obtient la taille des images
    l_a,h_a = img_a.size 
    l_b,h_b = img_b.size
    # verifie si les tailles d'image sont compatibles
    if check_size(img_a,img_b) < 0:
        print("Erreur: l'image a cacher est trop grande pour l'image cible")
        exit(3)
    # cree l'image cible
    img_c = Image.new("RGB",(l_a,h_a))
    # boucle sur les pixel de img_a
    for x in range(l_a):
        for y in range(h_a):
            # obtient le pixel de img_a
            pixel_a = img_a.getpixel((x,y))
            
            # Obtient le pixel de l'img_b (image à cacher)
            # definit des pixels noirs pour les pixels pour completer la taille de l'image à cacher pour s'aligner l'image cible
            r_b = 0
            g_b = 0
            b_b = 0

            if (x < l_b) & (y<h_b):
                #obtient le pixel de l'image b
                pixel_b = img_b.getpixel((x,y))
                r_b = pixel_b[0]
                g_b = pixel_b[1]
                b_b = pixel_b[2]

            # appel de lsbval pour cacher l'information 
            r = lsbval(r_b,pixel_a[0])
            g = lsbval(g_b,pixel_a[1])
            b = lsbval(b_b,pixel_a[2])
            
            # ecrit le pixel obtenu
            img_c.putpixel((x,y),(r,g,b))
    # sauve l'image calculée
    img_c.save(image_resultat_file)
    

def check_size(img_a:Image,img_b:Image):
    """
    Fonction check_size
    Verifier si les tailles d'images sont compatibles
    img_a: image utilisée pour cacher l'autre. type Image
    img_b: image à cacher. type Image
    return : -1 si l'image à cacher est trop grand pour la cible. 1 si les images sont compatibles.
    """
    #obtient les tailles des images
    l_a,h_a = img_a.size 
    l_b,h_b = img_b.size
    #Compare les tailles d'images 
    if l_a < l_b or h_a < h_b:
        return -1
    return 1

def unstegano(image_trafiquee_file,image_reconstruite_file):
    """
    Fonction unstegano
    Decode une image et recuper une image cachée.
    input_file: le nom du fichier avec l'image à decoder. type string
    output_file: le nom du fichier où sauvegarder l'image reconstruite. type string
    """
    try:
        img=Image.open(image_trafiquee_file)
    except FileNotFoundError:
        print("fichier %s non trouve."% (image_trafiquee_file))
        exit(4)
    # obtient la taille de l'image 
    l,h = img.size 
    # crée l'image cible
    img_result = Image.new("RGB",(l,h))
    # boucle sur les pixels de l'image
    for x in range(l):
        for y in range(h):
            # obtient le pixels
            pixel = img.getpixel((x,y))
            r = unlsbval(pixel[0])
            g = unlsbval(pixel[1])
            b = unlsbval(pixel[2])
            
            # ajoute le pixel calculé dans l'image cible
            img_result.putpixel((x,y),(r,g,b))
    # retourne l'image cible
    img_result.save(image_reconstruite_file)

def usage():
    """
    Fonction usage
    Affiche l'uage du programme et donne des information sur les options à passer sur la ligne de commande.
    """
    print("programme de steganographie")
    print("python3 stegano.py MODE [ARGS] [OPTIONS]")
    print("MODE:")
    print("    -e encode une image dans une autre image.")
    print("    -d decode une image pour trouver une image cachee.")
    print("ARGS")
    print("    -i fichier source. fichier a decoder (mode decode). fichier servant a cacher l'autre image (mode encode).")
    print("    -c fichier image a cacher (mode encode seulement).")
    print("    -o fichier de sortie.")
    print("OPTIONS:")
    print("    -h affiche le message d'aide.")
    

def main(argv):
    """
    fonction Main
    argv: arguments recupérés sur la ligne de commande
    """
    # obtient les arguments passés sur la ligne de commande
    try:
        opts, args = getopt.getopt(argv,"hedi:o:c:",["ifile=","ofile=","cfile="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    mode_set = 0
    mode = MODE_HELP

    input_file =""
    output_file = ""
    input2_file = ""
    #boucle for definir les arguments de la ligne de commande et obtnire leur valeur
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt == '-e':
            if (mode_set == 0):
                mode_set = 1
                mode = MODE_ENCODE
            else:
                usage()
                sys.exit(2)
        elif opt == '-d':
            if (mode_set == 0):
                mode_set = 1
                mode = MODE_DECODE
            else:
                usage()
                sys.exit(2)
        elif opt == '-i':
            input_file= arg
        elif opt == '-o':
            output_file= arg
        elif opt == '-c':
            input2_file = arg    

    if (mode==MODE_HELP):
        # affiche le message d'aide
        usage()
        sys.exit()
    elif (mode==MODE_ENCODE):
        # encode d'une image
        # verife si on a tous les noms de fichiers
        if input_file == '' or input2_file =='' or output_file == '':
            usage()
            exit(2) 
        # lance l'encodage
        print("Encodage de l'image en cours")
        stegano(input2_file,input_file,output_file)
        print("Encodage fini")
    elif(mode==MODE_DECODE):
        # verifie la presence des noms de fichiers
        if input_file == '' or output_file == '':
            usage()
            exit(2) 
        # lance le decodage
        print("Decodage de l'image")
        unstegano(input_file,output_file)
        print("Decodage finie")
    exit()

if __name__ == "__main__":
    main(sys.argv[1:])