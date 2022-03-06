#########################################
# groupe MI 3
# Iliassy Asmaa
# Chennig Mohammed
# Berthome-Laurent Alexis
# https://github.com/uvsq22106122/projet_tas_de_sable
#########################################

#Import de module ----------------------#


import tkinter as tk
import random

#Constantes-----------------------------#
LARGEUR = 500
HAUTEUR = 500
CASES = 100
LARG_CASES = LARGEUR//CASES
HAUT_CASES = HAUTEUR//CASES

#Variable Global------------------------#

configuration_courante = []


#Fonction-------------------------------#

def empty_map(size) :
    """Renvoie une nouvelle configuration
       vide de taille size"""
    return [[0]*size for i in range(size)]

def map_add (map1, map2) :
    """Renvoie la somme de deux configurations de même taille"""
    size = len(map1)
    return [[map1[i][j]+map2[i][j] for j in range(size)] for i in range(size)]

def map_sub (map1, map2) :
    """Renvoie la difference de deux configurations de même taille"""
    size = len(map1)
    res=empty_map(size)
    for i in range(size) :
        for j in range(size) :
            if map1[i][j] < map2[i][j] :
                res[i][j] = 0
            else :
                res[i][j] = map1[i][j]-map2[i][j]
    return res


def cell_stable (map, x, y) :
    """Renvoie true si la case est stable"""
    return map[x][y] < 4

def map_stable (map) :
    """Renvoie true si la configuration est stable"""
    size = len(map)
    for i in range(size) :
        for j in range(size) :
            if not cell_stable(map,i,j) :
                return False
    return True

def next_state (map) :
    """Renvoie l'etape suivante d'une configuration"""
    size = len(map)
    changes = empty_map(size) #map des changements a effectuer 
    #parcours de la map
    for i in range(size) :
        for j in range(size) :
            # si la case est instable
            if not cell_stable(map,i,j) :
                #on retiens les changements
                changes[i][j] -= 4
                if i>0 :
                    changes[i-1][j] += 1
                if i<size-1 :
                    changes[i+1][j] += 1
                if j>0 :
                    changes[i][j-1] += 1
                if j<size-1 :
                    changes[i][j+1] += 1

    #on utilise la soustraction pour eviter les valeurs negatives
    return map_add(map, changes) 

def stabilize(map) :
    state = 0
    while not map_stable(map) :
        map = next_state(map)
        state+=1
    return map

def random_map(size) :
    """Renvoie une nouvelle configuration
       aleatoire de taille size"""
    return [[random.randint(0,3) for j in range(size)] for i in range(size)]

def centeredStack_map(size, N) :
    """Renvoie une nouvelle configuration de taille size
       avec la case du mileu a N et les autres a 0"""
    csmap = empty_map(size)
    csmap[(size-1)//2][(size-1)//2] = N
    return csmap

def maxStable_map(size) :
    """Renvoie une nouvelle configuration de taille size
       ou chaque case a 3 grains"""
    return [[3]*size for i in range(size)]

def identity_map(size) :
    """Renvoie une configuration identite
       de taille size"""
    #double max stable
    msmap = maxStable_map(size)
    dmsmap = map_add(msmap, msmap)
    #stable double max stable
    sdmsmap = stabilize(dmsmap)
    idmap = map_sub(dmsmap,sdmsmap)
    idmap = stabilize(idmap)
    return idmap

def maj_affichage(CASES, LARG_CASE, HAUT_CASE):
    "met à jour l’affichage de la grille à partir de la configuration courante"
    global configuration_courante
    COULEUR = ['black', 'yellow', 'green', 'blue']
    for i in range(CASES):
        for j in range(CASES):
            if configuration_courante[i][j] < 4:
                canvas.create_rectangle((i*LARG_CASE), (j*HAUT_CASE), ((i+1)*LARG_CASE), ((j+1)*HAUT_CASE), fill=COULEUR[configuration_courante[i][j]], outline = COULEUR[configuration_courante[i][j]])
            else :
                canvas.create_rectangle((i*LARG_CASE), (j*HAUT_CASE), ((i+1)*LARG_CASE), ((j+1)*HAUT_CASE), fill="red", outline = "red")

def Sauvegarde():
    """sauvegarde la configuration actuelle"""
    global configuration_courante
    with open('save', 'w') as f:
        for i in range(CASES):
            f.write(f'{configuration_courante[i]}\n')


#Main-----------------------------------#


#---------------Fenetre------------------#
racine = tk.Tk()

#----------------Widget------------------#

#---Canvas---#
canvas = tk.Canvas(racine, bg="white", width=500, height=500)
canvas.grid(row=0, column=1)

#----Menu----#
menu = tk.Canvas(racine, bg="black", width=100, height=500)
menu.grid(row=0, column=0)


configuration_courante = random_map(CASES)
maj_affichage(CASES, LARG_CASES, HAUT_CASES)
# Sauvegarde()

racine.mainloop()