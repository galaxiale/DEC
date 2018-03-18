from tables import *
import numpy as np
import pandas as pd
import pyperclip
import matplotlib.pyplot as plt
import bokeh

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
h5file = open_file("fichier_dec.hdf5", mode = "w", title = "Fichier Distances entre cables")

#Création groupe
grp_dec = h5file.create_group("/", 'grp_dec', 'calculs distances entre cables')

#Création tables
tab_dec_brut = h5file.create_table(grp_dec, 'tab_dec_brut', DEC, "tab_dec_brut")
tab_dec_result = h5file.create_table(grp_dec, 'tab_dec_result', DEC, "tab_dec_result")

# Liste des hypothèses
hypotheses = {'Vent réduit Cond-Cond':"VR_CC",
              'Vent réduit Cond-Cdg':"VR_CG",
              'Givre différentiel Cond-Cond':"GD_CC",
              'Givre différentiel Cond-Cdg':"GD_CG",
              'Décharge de Givre Cond-Cond':"DG_CC",
              'Décharge de Givre Cond-Cdg':"DG_CG"}

liste_libelle=['Vent réduit Cond-Cond','Vent réduit Cond-Cdg',
               'Givre différentiel Cond-Cond','Givre différentiel Cond-Cdg',
               'Décharge de Givre Cond-Cond','Décharge de Givre Cond-Cdg']
liste_hyp=["VR_CC","VR_CG","GD_CC","GD_CG","DG_CC","DG_CG"]
liste_data=[0.366,0.216,0.745,0.562,0.415,0.255]

df_hypotheses=pd.DataFrame({"Libellé":liste_libelle,
                            "Hyp.":liste_hyp,
                            "data":liste_data},
                            index=[1,2,3,4,5,6])

print(df_hypotheses)

# T r a i t e m e n t

# Import contenu presse-papiers
for hyp in hypotheses.keys():
    print("* Copiez les données ",hyp," > ")
    rep=input("")
    print("* Récupération contenu presse-papiers\n")
    # Traitement lignes de résultats
    print("* DEC ",hyp," *\n")
    DEC1=tab_dec_brut.row
    DEC2=tab_dec_result.row
    print("Traitement et stockage des lignes")

    for ligne in pyperclip.paste().split("\n"):
        
        # print(ligne)
        data=ligne.split("\t")
        # print(data)
        print ("* Portée du n° ",data[0]," au n° ",data[1]," traitée *")
        DEC1['Hyp']=hypotheses[hyp]
        DEC1['SDCS'] = data[0]
        DEC1['SFCS'] = data[1]
        DEC1['SetCS'] = data[2]
        if data[3]=="Left":
            vent = -1
        else:
            vent = 1
        DEC1['DVentCS']=vent
        DEC1['SDCC'] = data[4]
        DEC1['SFCC'] = data[5]
        DEC1['SetCC'] = data[6]
        if data[7]=="Left":
            vent = -1
        else:
            vent = 1
        DEC1['DVentCC'] = vent
        DEC1['AbsDmin'] = data[8]
        DEC1['FCSDmin'] = data[9]
        DEC1['FCCDmin'] = data[10]
        DEC1['DresDmin'] = float(data[11])-10+0.366
        DEC1['Dtot'] = data[12]
        DEC1['DcompH'] = data[13]
        DEC1['DcompV'] = data[14]
        DEC1.append()

        if ((data[3]==data[7]) and (data[0]==data[4])):
            liste_resultats.append(data)
            nb_result+=1
            # Ici les calculs ========================
            if hypotheses[hyp] in ("VR_CC","VR_CG"):
                dtheoriqueVR=0.366
                dresdmin=float(data[11])-10+dtheoriqueVR
            elif hypotheses[hyp] in ("DG_CC","DG_CG"):
                dresdminH=0
                dresdminV=0
            else:
                dresdminH=0
                dresdminV=0

            # ========================================
            DEC2['Hyp']=hypotheses[hyp]
            DEC2['SDCS'] = data[0]
            DEC2['SFCS'] = data[1]
            DEC2['SetCS'] = data[2]
            DEC2['DVentCS'] = vent
            DEC2['SDCC'] = data[4]
            DEC2['SFCC'] = data[5]
            DEC2['SetCC'] = data[6]
            DEC2['DVentCC'] = vent
            DEC2['AbsDmin'] = data[8]
            DEC2['FCSDmin'] = data[9]
            DEC2['FCCDmin'] = data[10]
            DEC2['DresDmin'] = dresdmin
            DEC2['Dtot'] = data[12]
            DEC2['DcompH'] = data[13]
            DEC2['DcompV'] = data[14]
            DEC2.append()
            print("* data = ",data)
            dict_result=({'Hyp':hypotheses[hyp],
                          'SDCS':data[0],
                          'SFCS':data[1],
                          'SetCS':data[2],
                          'DVentCS':vent,
                          'SDCC':data[4],
                          'SFCC':data[5],
                          'SetCC':data[6],
                          'DVentCC':vent,
                          'AbsDmin':data[8],
                          'FCSDmin':data[9],
                          'FCCDmin':data[10],
                          'DresDmin':dresdmin,
                          'Dtot':data[12],
                          'DcompH':data[13],
                          'DcompV':data[14],
                          'Marge':float(data[12])-dresdmin,
                          'MargeH':float(data[13])-dresdminH,
                          'MargeV':float(data[14])-dresdminV})
            liste_dict.append(dict_result)
    
    tab_dec_brut.flush()
    tab_dec_result.flush()

tab_result=np.array(liste_resultats)

print(liste_dict)
df_resultats = pd.DataFrame(liste_dict)
df_resultats=df_resultats.sort_values('Marge')
print(df_resultats.head(5))
print(df_resultats.tail(5))

# liste_resultats.sort()

# Fermeture Fichier
h5file.close()