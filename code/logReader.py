# -*- coding: utf-8 -*-
"""
Created on Sun May 15 16:07:37 2022

@author: elbia
"""

def lectura(path,path_old,path_line):
    
    import re #regex para patrones
    import pandas as pd
    from collections import Counter #contador
    from datetime import datetime
    import numpy as np
    import matplotlib.pyplot as plt
    import configparser
    
    config = configparser.RawConfigParser()
    configFilePath = '/etc/broksindri/config.ini'
    config.read(configFilePath)
    
    miIP = str(config.get('broksindri','miIP'))
    limitIP = int(config.get('broksindri','limitIP'))


    with open(path_line) as pathline:
        readstring = pathline.readlines()
        cur_lin = int(readstring[0])

      
    # abre y lee el archivo
    """  
    with open(path) as fh:
            fstring = fh.readlines()
    """
    
    flag=0       
    
    with open(path) as fh_1:
        fstring = fh_1.readlines()[cur_lin:]
        for item in fstring:
            cur_lin += 1
        if len(fstring) == 0:
            print("vacío")
            flag = 1
    
    if flag == 1:
        print (flag)
        with open(path_old) as fh_2:
            fstring = fh_2.readlines()[cur_lin:]
        cur_lin=0
        with open(path) as fh_1:
            fstringold = fh_1.readlines()[cur_lin:]
            for item in fstringold:
                fstring.append(item)
                cur_lin += 1
        flag=0
        

          
    # Patrones Regex
    patternIP = re.compile(r'((?!'+miIP+')\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})') 
    patternDate = re.compile(r'(\d{2}\/\w{1,10}\/\d{4}\:\d{2}\:\d{2}\:\d{2})') 
    patternMixto = re.compile(r'(\A\w{1,50}\.\w{1,50}\.\w{1,10}|\A\w{1,50}\-\w{1,50}\.\w{1,10})')
    patternReq = re.compile(r'((?<=")\b[A-Z]{2,10})')
    patternURI = re.compile(r'.*\s\/(.*?)\".*')
    patternUser = re.compile(r'.*\"(.*)\".*')
    patternPort = re.compile(r'\s\d{2,4}\s')
    patternResp = re.compile(r'(?<=" )\d{3}')
    
    # Inicializo listas
    lstIP=[]
    lstDate=[]
    lstURL=[]
    lstReq=[]
    lstURI=[]
    lstUser=[]
    lstPort=[]
    lstResp=[]
      
    
    # Obtengo patrones
    for line in fstring:
        logIP = re.search(patternIP, line)
        logDate = re.findall(patternDate, line)    
        logURL = re.findall(patternMixto, line)
        logReq = re.findall(patternReq, line)
        logURI = re.findall(patternURI, line)
        logUser = re.findall(patternUser, line)
        logPort = re.search(patternPort, line)
        logResp = re.search(patternResp, line)
        if logIP and logDate and logURL and logReq and logURI and logUser and logPort and logResp:
            lstIP.append(logIP.group(0))
            lstDate.append(logDate)
            lstURL.append(logURL)
            lstReq.append(logReq)
            lstURI.append(logURI)
            lstUser.append(logUser)   
            lstPort.append(logPort.group(0))
            lstResp.append(logResp.group(0))
    
    """
    Para algunos casos, como la IP, el puerto y la respuesta
    utilizo "Search" que solo trae la primera 'match' que encuentra
    y la pone en lista. Para estos casos utilizo el append group(0)
    ya que lo que devuelve el 'Search' es un objeto tipo Match, y con
    el group(0) saco el valor
    
    Para los otros casos, utilizo findall y trae el valor. El problema es
    que trae tuplas en lugar de listas, así que me encargo en las líneas
    posteriores de convertirlas a listas. Esto no es necesario para las Search
    
    El if es para verificar que todos los elementos de la línea existen
    """
    
    
    #listas de tuplas
    
    miIPrecortada = re.search(patternMixto, miIP).group(0)#miIP pero de 3 valores. Necesaria para la URL    
    megalistaURL = []
    megainternaURL=[]
    
    
    for elem in lstURL:
        megainternaURL.extend(elem)
    
     
    for elem in megainternaURL:
        if elem == miIPrecortada:
            megalistaURL.append(miIP)
        else:
            megalistaURL.append(elem)
    
    
    megalistaReq=[]
    for elem in lstReq:
        megalistaReq.extend(elem)
    
    megalistaURI=[]
    for elem in lstURI:
        megalistaURI.extend(elem)
    
    megalistaUser=[]
    for elem in lstUser:
        megalistaUser.extend(elem)
        
    
    megalistaDate=[]
    for elem in lstDate:
        megalistaDate.extend(elem)
    
    #Hago un trabajo particular para separar la fecha y la hora
    
    megalistaFecha=[]
    megalistaHora=[]
    
    x=0
    for elem in megalistaDate:
        date_time_str = megalistaDate[x].split(":",1)
        objFecha = datetime.strptime(date_time_str[0], '%d/%b/%Y').date()
        objHora = datetime.strptime(date_time_str[1], '%H:%M:%S').time()
        megalistaFecha.append(objFecha)
        megalistaHora.append(objHora)
        x += 1
    
    
    
    #armado df final
    
    dffinal = pd.DataFrame(columns=["url",
                                    "puerto",
                                    "ip",
                                    "fecha",
                                    "hora",
                                    "tipo_request",
                                    "URI",
                                    "respuesta",
                                    "user_agent"])
    
    dffinal["url"] = megalistaURL
    dffinal["puerto"] = lstPort
    dffinal["ip"] = lstIP
    dffinal["fecha"] = megalistaFecha
    dffinal["hora"] = megalistaHora
    dffinal["tipo_request"] = megalistaReq
    dffinal["URI"] = megalistaURI
    dffinal["respuesta"] = lstResp
    dffinal["user_agent"] = megalistaUser
    
#    print(dffinal)
    
    
    
    #análisis y gráficas
    
    contadorIP = Counter(lstIP)
    IPFiltrada = { x: count for x, count in contadorIP.items() if count >= limitIP }
    
    IPsort = {k: v for k, v in sorted(IPFiltrada.items(), key=lambda item: item[1],reverse=True)}
#    print(IPsort)
    
    contadorResp = Counter(lstResp)
    Respsort={k: v for k, v in sorted(contadorResp.items(), key=lambda item: item[1],reverse=True)}
#    print(Respsort)
    
    """
    fig, (ax1,ax2) = plt.subplots(2,1,figsize=(15,7)) #ax1,ax2 refer to your two pies
    
    
    bar1 = ax1.bar(IPsort.keys(), IPsort.values())
    ax1.set_title("Cantidad de IP mayores a "+str(limitIP))
    ax1.bar_label(bar1)
    bar2 = ax2.bar(Respsort.keys(), Respsort.values())
    ax2.set_title("Cantidad de Repuestas")
    ax2.bar_label(bar2)
    
    plt.show()
    """
    
    #escritura al excel
    """
    
    with pd.ExcelWriter("C:/Users/elbia/Desktop/gunny/gunny.ods",
                        mode="w",
                        engine="odf"
                        ) as writer:
        dffinal.to_excel(writer, sheet_name="parseado")
    
    """
    
    return (IPsort, cur_lin)


