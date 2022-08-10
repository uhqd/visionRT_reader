import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import csv
import pandas as pd
import time


#from numpy import genfromtxt
#my_data = genfromtxt('my_file.csv', delimiter=',')

#############################################     IMPORTATION DU FICHIER CSV LECTURE ET TRANSFORMATION EN MATRICE     ######################################

fichier=pd.read_csv('31032022_22h29.csv') #lecture du fichier csv appelé 'nom_fichier.csv' présent dans le dossier lecturecsv
taille=fichier.shape #nous donne les dimensions du tableau csv (nb_lignes, nb_colonnes) permet de vérifier que le fichier est entièrement lu
print(taille)
f=np.array(fichier)#transformation du fichier csv en matrice pour pouvoir l'exploiter

#############################################     NOMS DES COLONNES DU FICHIER CSV     ######################################

nom_colonnes=fichier.columns #nous donne le nom des 59 colonnes (de 0 à 58)
#print(nom_colonnes)

#time.sleep(3.0)

#Index(['Date Time (ms)', 'Elapsed Time(sec)', 'Patient ID(GUID)',
#'Plan ID(GUID)', 'DICOM Isocentre X', 'DICOM Isocentre Y',
#'DICOM Isocentre Z', 'Reference Surface Name',
#'Reference Surface SurfaceID(GUID)', 'ROI name', 'ROIID', 'ROI Type',
#'Shift Surface VRT(mm)', 'Shift Surface LNG(mm)',
#'Shift Surface LAT(mm)', 'Monitoring Session ID(GUID)', 'CouchYaw(deg)',
#'ThresholdHighVRT(mm)', 'ThresholdLowVRT(mm)', 'ThresholdHighLNG(mm)',
#'ThresholdLowLNG(mm)', 'ThresholdHighLAT(mm)', 'ThresholdLowLAT(mm)',
#'ThresholdHighPitch(deg)', 'ThresholdLowPitch(deg)',
#'ThresholdHighRoll(deg)', 'ThresholdLowRoll(deg)',
#'ThresholdHighYaw(deg)', 'ThresholdLowYaw(deg)',
#'Display Coordinate System', 'D.MAG(mm)', 'D.VRT(mm)', 'D.LNG(mm)',
#'D.LAT(mm)', 'D.YAW(deg)', 'D.ROLL(deg)', 'D.PITCH(deg)',
#'Percentage Overlap', 'RMS(mm)', 'Display D.MAG(mm)',
#'Display D.VRT(mm)', 'Display D.LNG(mm)', 'Display D.LAT(mm)',
#'Display D.YAW(deg)', 'Display D.ROLL(deg)', 'Display D.PITCH(deg)',
#'Delta Smoothed', 'Is In Tolerance', 'Is BeamControl Enabled',
#'ActualBeamEnabledState', 'RequestedBeamEnabledState',
#'ReportedBeamState', 'Beamhold Delay(sec)', 'ImageSetTimeStamp',
#'SurfaceTimestamp', 'RegistrationTimestamp', 'BeamControlStatus',
#'BeamControlWatchdogResetSecondsElapsed', 'Unnamed: 58'],
#dtype='object')


###################################################   LECTURE DES COLONNES TEMPS, ROTATION TABLE ET ACTIVATION FAISCEAU   ##################################################

Elapsed_Time=fichier[['Elapsed Time(sec)']] #lecture colonne temps acquisition
#taille_Display_D_LNG=Display_D_LNG.shape #nous donne la taille de ce tableau (lignes, colonnes) 

Rotation_table=fichier[['CouchYaw(deg)']] #lecture colonne position de la table 0° 45° -45°=315° -90°=270°
Rotation_table=np.array(Rotation_table) #transformation en matrice pour exloitation dans boucle for des fonctions

#D_MAG=fichier[['D.MAG(mm)']] colonne 30, display colonne 39
#D_VRT=fichier[['D.VRT(mm)']] colonne 31, display colonne 40
#D_LNG=fichier[['D.LNG(mm)']] colonne 32, display colonne 41
#D_LAT=fichier[['D.LAT(mm)']] colonne 33, display colonne 42
#D_YAW=fichier[['D.YAW(deg)']] colonne 34, display colonne 43
#D_ROLL=fichier[['D.ROLL(deg)']] colonne 35, display colonne 44
#D_PITCH=fichier[['D.PITCH(deg)']] colonne 36, display colonne 45
#RMS=fichier[['RMS(mm)']] colonne 38

Activation_faisceau=fichier[['ActualBeamEnabledState']] #lecture colonne état du faisceau, activé='Yes' desactivé='No'
Activation_faisceau=np.array(Activation_faisceau) #transformation en matrice pour exloitation dans boucle for des fonctions


###################################################   FONCTIONS   ##################################################

############fonction permettant de remplir un tableau à partir des valeurs de décalages souhaitées pour une position de table choisie, les valeurs ne correspondant pas à cette position de table sont mises à zéro
def decalages_selon_rotation_de_table(angle_table,numero_colonne_decalages): #angle de table 45,0,-45,-90
    tableau=[]
    x=0
    for rotation in Rotation_table:  
        if rotation==angle_table:
            #print(x,f[x,numero_colonne_decalages],f[x,1])
            tableau.append(f[x,numero_colonne_decalages])#incrémente les valeurs souhaitées
        if rotation!=angle_table:
            #print(x,"ah")
            tableau.append(0)#incrémente des 0
        x=x+1
    print('Extrema des valeurs de décalages selon la position de la table:')
    print(f'minimum={min(tableau)}')
    print(f'maximum={max(tableau)}\n')
    return tableau#nous retourne le tableau aux bonnes dimensions pour pouvoir le plot en fonction du temps


############fonction permettant de plot avec axes le tableau retourné par la fonction decalages_selon_rotation_de_table pour les translations
def plot_decalages_trans_selon_rotation_de_table(type_decalages,angle_table,nom_tableau,numero_figure):
    plt.figure(numero_figure)
    plt.plot(Elapsed_Time,nom_tableau)
    plt.grid
    plt.xlabel('Temps en s')
    plt.ylabel(f'{type_decalages} en mm')
    plt.title(f'{type_decalages} quand la table est à {angle_table}°')
    #plt.show()
 

############fonction permettant de plot avec légendes le tableau retourné par la fonction decalages_selon_rotation_de_table pour les rotations
def plot_decalages_rot_selon_rotation_de_table(type_decalages,angle_table,nom_tableau,numero_figure):
    plt.figure(numero_figure)
    plt.plot(Elapsed_Time,nom_tableau)
    plt.grid
    plt.xlabel('Temps en s')
    plt.ylabel(f'{type_decalages} en °')
    plt.title(f'{type_decalages} quand la table est à {angle_table}°')
    #plt.show()


############fonction permettant de remplir un tableau de valeur de décalages en fonction de l'activation du faisceau ou non(0)
def decalages_selon_activation_faisceau(numero_colonne_decalages):
    tableau = []
    x=0
    for activation in Activation_faisceau:
        if activation=='Yes':
            #print(x,f[x,39],f[x,1])
            tableau.append(f[x,numero_colonne_decalages])
        if activation=='No':
            #print(x,"..............no")
            tableau.append(0)
        x=x+1
    print('Extrema des valeurs de décalages selon activation du faisceau:')
    print(f'minimum={min(tableau)}')
    print(f'maximum={max(tableau)}\n')
    return tableau


############fonction permettant de plot avec axes le tableau retourné par la fonction decalages_selon_activation_faisceau pour les translations
def plot_decalages_trans_selon_activation_faisceau(type_decalages,nom_tableau,numero_figure):
    plt.figure(numero_figure)
    plt.plot(Elapsed_Time,nom_tableau)
    plt.grid
    plt.xlabel('Temps en s')
    plt.ylabel(f'{type_decalages} en mm')
    plt.title(f'{type_decalages} quand le faisceau est activé')
    #plt.show()


############fonction permettant de plot avec axes le tableau retourné par la fonction decalages_selon_activation_faisceau pour les rotations
def plot_decalages_rot_selon_activation_faisceau(type_decalages,nom_tableau,numero_figure):
    plt.figure(numero_figure)
    plt.plot(Elapsed_Time,nom_tableau)
    plt.grid
    plt.xlabel('Temps en s')
    plt.ylabel(f'{type_decalages} en °')
    plt.title(f'{type_decalages} quand le faisceau est activé')
    #plt.show()


############fonction permettant de remplir un tableau de valeur de décalages en fonction de la position de table et de l'activation du faisceau à partir du tableau obtenu par la fonction decalages_selon_rotation_de_table
def decalages_selon_rotation_table_et_faisceau(nom_tableau_decalages_selon_rotation_table):
    tableau = []
    x=0
    for activation in Activation_faisceau:
        if activation=='Yes':
            #print(x,f[x,39],f[x,1])
            tableau.append(nom_tableau_decalages_selon_rotation_table[x])
        if activation=='No':
            #print(x,"..............no")
            tableau.append(0)
        x=x+1
        print('Extrema des valeurs de décalages selon la rotation de table et activation du faisceau:')
        print(f'minimum={min(tableau)}')
        print(f'maximum={max(tableau)}\n')
    return tableau


############fonction permettant de plot avec axes le tableau retourné par la fonction decalages_selon_rotation_table_et_faisceau pour les translations
def plot_decalages_trans_selon_rotation_table_et_faisceau(type_decalages,angle_table,nom_tableau,numero_figure):
    plt.figure(numero_figure)
    plt.plot(Elapsed_Time,nom_tableau)
    plt.grid
    plt.xlabel('Temps en s')
    plt.ylabel(f'{type_decalages} en mm')
    plt.title(f'{type_decalages} quand la table est à {angle_table}° et que le faisceau est activé')
    #plt.show()


############fonction permettant de plot avec axes le tableau retourné par la fonction decalages_selon_rotation_table_et_faisceau pour les rotations
def plot_decalages_rot_selon_rotation_table_et_faisceau(type_decalages,angle_table,nom_tableau,numero_figure):
    plt.figure(numero_figure)
    plt.plot(Elapsed_Time,nom_tableau)
    plt.grid
    plt.xlabel('Temps en s')
    plt.ylabel(f'{type_decalages} en °')
    plt.title(f'{type_decalages} quand la table est à {angle_table}° et que le faisceau est activé')
    #plt.show()

#######################################    DECALAGES EN TRANSLATIONS ET ROTATIONS TABLE A 0°  ###############################################################

print('Table à 0°:\n')
print('Translations:\n')
print('Décalages verticaux\n')
D_VRT=decalages_selon_rotation_de_table(0,31)
plot_decalages_trans_selon_rotation_de_table('Décalages verticaux',0,D_VRT,1)
D_VRT1=decalages_selon_rotation_table_et_faisceau(D_VRT)
plot_decalages_trans_selon_rotation_table_et_faisceau('Décalages verticaux',0,D_VRT1,2)

print('Décalages longitudinaux\n')
D_LNG=decalages_selon_rotation_de_table(0,32)
plot_decalages_trans_selon_rotation_de_table('Décalages longitudinaux',0,D_LNG,3)
D_LNG1=decalages_selon_rotation_table_et_faisceau(D_LNG)
plot_decalages_trans_selon_rotation_table_et_faisceau('Décalages longitudinaux',0,D_LNG1,4)

print('Décalages latéraux\n')
D_LAT=decalages_selon_rotation_de_table(0,33)
plot_decalages_trans_selon_rotation_de_table('Décalages latéraux',0,D_LAT,5)
D_LAT1=decalages_selon_rotation_table_et_faisceau(D_LAT)
plot_decalages_trans_selon_rotation_table_et_faisceau('Décalages latéraux',0,D_LAT1,6)

print('Rotations:\n')
print('Décalages rotation\n')
D_ROT=decalages_selon_rotation_de_table(0,34)
plot_decalages_trans_selon_rotation_de_table('Décalages rotation',0,D_ROT,7)
D_ROT1=decalages_selon_rotation_table_et_faisceau(D_ROT)
plot_decalages_trans_selon_rotation_table_et_faisceau('Décalages rotation',0,D_ROT1,8)

print('Décalages roulis\n')
D_ROLL=decalages_selon_rotation_de_table(0,35)
plot_decalages_trans_selon_rotation_de_table('Décalages roulis',0,D_ROLL,9)
D_ROLL1=decalages_selon_rotation_table_et_faisceau(D_ROLL)
plot_decalages_trans_selon_rotation_table_et_faisceau('Décalages roulis',0,D_ROLL1,10)

print('Décalages tangage\n')
D_PITCH=decalages_selon_rotation_de_table(0,36)
plot_decalages_trans_selon_rotation_de_table('Décalages tangage',0,D_PITCH,11)
D_PITCH1=decalages_selon_rotation_table_et_faisceau(D_PITCH)
plot_decalages_trans_selon_rotation_table_et_faisceau('Décalages tangage',0,D_PITCH1,12)


#plt.show()   #enlever commentaire pour afficher les plot