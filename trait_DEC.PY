from tables import *
import numpy as np
import pandas as pd
import pyperclip

#variables
liste_resultats=[]
liste_dict=[]
nb_result=0
dresdmin=0
dresdminH=0
dresdminV=0

df_result=pd.DataFrame({'Hyp':'', 'SDCS':'', 'SFCS':'', 'SetCS':0,
                        'DVentCS':0, 'SDCC':'', 'SFCC':'', 'SetCC':0,
                        'DVentCC':0, 'AbsDmin':0.0, 'FCSDmin':0.0,
                        'FCCDmin':0.0, 'DresDmin':0.0, 'Dtot':0.0,
                        'DcompH':0.0, 'DcompV':0.0}, index=[1])

class DEC(IsDescription):
    Hyp = StringCol(5)
    SDCS = StringCol(10)
    SFCS = StringCol(10)
    SetCS = UInt8Col()
    DVentCS = Int8Col()
    SDCC = StringCol(10)
    SFCC = StringCol(10)
    SetCC = UInt8Col()
    DVentCC = Int8Col()
    AbsDmin = Float32Col()
    FCSDmin = Float32Col()
    FCCDmin = Float32Col()
    DresDmin = Float32Col()
    Dtot = Float32Col()
    DcompH = Float32Col()
    DcompV = Float32Col()

# Création Fichier
h5file = open_file("fichier_dec.hdf5", mode = "r", title = "Fichier Distances entre cables")

# lecture table résultats
table=h5file.root.grp_dec.tab_dec_result
for record in table:
    for i in range(16):
        liste_resultats.append(record[i])
    print(liste_resultats)
    liste_resultats=[]
    
# Fermeture Fichier
h5file.close()