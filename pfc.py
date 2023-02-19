# -*-coding:Latin-1 -*
import random

# valeur de choix
PIERRE = 0
FEUILLE = 1
CISEAUX = 2

def getsigne(choix):
    """
    founction qui retourne la chaine correspondant a la valeur choix
    choix:  valeur (0,1 ou 2)
    return: Pierre, Feuille, Ciseaux
    """
    if choix == 0:
        return 'Pierre'
    if choix == 1:
        return 'Feuille'
    if choix == 2:
        return 'Ciseaux'

def joue(joueura,joueurb):
    """ 
    fonction qui definie qui a gagne ce tour
    joueura : choix du joueur A
    joueur b : choix du joueur B
    return : 1 si joueur A gagne, 0 si equalité, -1 si joueur B gagne
    """ 
    valeur  = joueura - joueurb
    if valeur == 0:
        return 0
    if valeur == 1 or valeur == -2:
        return 1
    if valeur == -1 or valeur == 2:
        return -1 

def tirechoixjoueur():
    """
    fonction qui tire le choix d'un joueur 
    return: 0,1,2 en fonction du tirage    
    """
    # initialise le generateur de nombre aleatoire
    random.seed()
    # tire une nombre aleatoire correspondant à pierre, papier, ciseaux
    return random.randint(0,2)

def tour(mise):
    """
    fonction gérant un tour de jeu
    mise: mise en jeu. c'est a dire le nombre de point en jeu pour ce tirage 
    """
    #tire les choix de joueurs
    valeura = tirechoixjoueur()
    valeurb = tirechoixjoueur()
    #augmente le score de 1
    #score = score +1 
    #obtient le resultat du tour
    resultat = joue(valeura,valeurb)
    # affiche le resultat du tirage  
    print("     Point(s) en jeu: %i - Joueur A joue: %s - joueur B joue: %s"% (mise, getsigne(valeura),getsigne(valeurb)))

    #anlyse le resultat
    if resultat == 0 :
        # si egalité on rejoue 
        return tour(mise+1)
    else :
        if resultat > 0:
            return mise
        else :
            return -abs(mise)

def main():
    #initialise la partie et les scores
    scorea = 0
    scoreb = 0
    print('debut de partie - score joueur A: ',scorea, ' score joueur B: ', scoreb)

    #lance une partie avec 50 tours
    for i in range(50):
        vainqueur =''
        # obtient le resultat d'un tour
        resultat = tour(1)
        # verifie qui a gagné le tour et change le score
        if resultat > 0:
            scorea = scorea + resultat
            vainqueur = 'A'
        else:
            scoreb = scoreb + abs(resultat)
            vainqueur = 'B'
        # affiche les scores 
        print("tour %i - vainqueur: joueur %s - point(s) en jeu: %i -  score joueur A: %i, score joueur B: %i"%( i+1, vainqueur, abs(resultat), scorea, scoreb))
        print("")
    
    if scorea==scoreb:
        print("Resultat final: equalite")
    else:
        if scorea > scoreb:
            print("Vainqueur final: joueur A  par %i à %i"% (scorea,scoreb))
        else:
             print("Vainqueur final: joueur B  par %i à %i"% (scoreb,scorea))

if __name__ == "__main__":
    main()