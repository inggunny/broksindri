# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 11:35:07 2022

@author: elbia
"""

#generatedLists

path_list = "C:/Users/elbia/Desktop/gunny/lists.txt"

command = "block"
newIP = "2.2.2.2"



with open(path_list,'r+') as wl:
    readline = wl.readlines() #Lee todas las lineas
    wl.seek(0) #va al inicio y lo trunca
    wl.truncate(0)
    try:
        for index,elem in enumerate(readline):
            wl.write(elem) #re-escribe cada elemento leído
            if command == "block": 
                if elem == "blacklist\n": #si el comando el block, y si está en la línea blacklist   
                    wl.write(newIP+"\n")
                else:
                    pass
            elif command == "allow":
                if elem == "allowlist\n": #si el comando es allow, y está en la linea allowlist   
                    wl.write(newIP+"\n")
                else:
                    pass
            else:
                pass
    except:
        print("hubo un error en la actualización de la blacklist")
        for index,elem in enumerate(readline): #si encuentra un error, re-escribe la list como estaba
            wl.write(elem)





