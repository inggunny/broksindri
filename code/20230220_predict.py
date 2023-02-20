# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 21:56:20 2023

@author: elbia
"""

import numpy as np
import pandas as pd
import mysql.connector
from mysql.connector import errorcode
import matplotlib as mpl
import matplotlib.pyplot as plt

SQLconfig = {
  'user': 'bruno',
  'password': 'nano123',
  'host': '10.243.0.96',
  'database': 'test123',
  'raise_on_warnings': True
}

try:
  cnx = mysql.connector.connect(**SQLconfig)
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
    mycursor = cnx.cursor()
    sql = "SELECT * FROM testsemana1"
    dfpred = pd.read_sql(sql,cnx)    

mycursor.close()
cnx.close()

print(dfpred)

asd2 = dfpred.copy()
asd3 = dfpred.copy()
asd4 = pd.DataFrame(columns=["ID","IPcount"])

print(asd2)
print(asd3)

zxc1=[]
zxc2=[]
zxc3=[]
qweqwe=[]

#for index, ip in dfpred:
for ind in dfpred["ID"]:
    try:
        print(ind)
        qweqwe=[]
        zxc1 = dfpred.loc[ind, "IPcount"]   
        zxc2 = asd2.loc[ind, "IPcount"]
        zxc3 = asd3.loc[ind, "IPcount"]   
        qweqwe.append(zxc1)
        qweqwe.append(zxc2)
        qweqwe.append(zxc3)
    
    
        x_train = [0,1,2]
        y_train = qweqwe
    
        print(x_train)
        print(y_train)
    
        x_test = len(qweqwe) #los indices empiezan en 0, entonces len siempre estará uno arriba

        print(x_test)
        
        try:
            model2 = np.poly1d(np.polyfit(x_train,y_train,2))
            y_test = model2(x_test)
            print(y_test)
            asd4.loc[len(asd4.index)] = [ind,y_test]
        except:
            print("No enough data")
            y_test = 0
    except KeyboardInterrupt:
        print("Salida Manual")
    except Exception:
        pass
     

print(asd4)

plt.figure()

dfpred.plot(x="ID",y="IPcount")
asd2.plot(x="ID",y="IPcount")
asd3.plot(x="ID",y="IPcount")
asd4.plot(x="ID",y="IPcount")

"""
print(dfpred)

x = 0
megalist = []
dfgroup = dfpred.groupby("IPdb")


for i in range(len(dfpred)):
#    print(dfpred.loc[i, "IPdb"], dfpred.loc[i, "IPcount"], dfpred.loc[i, "Fecha"])

    if i != 0:
        x = i-1
        if dfpred.loc[i, "IPdb"] != dfpred.loc[x, "IPdb"]:
            dffilter = dfgroup.get_group(dfpred.loc[i, "IPdb"])
            megalist.append(dffilter)
        else:
            pass
    else:
        dffilter = dfgroup.get_group(dfpred.loc[i, "IPdb"])
        megalist.append(dffilter)


for idx,elem in enumerate(megalist):
  
    
    asdqwe = megalist[idx]["IPcount"]
    asdqwe = asdqwe.reset_index(level=0)
    
    x_train = asdqwe.index.values #convierto a darray Numpy
    y_train = asdqwe["IPcount"]
    x_test = len(x_train) #los indices empiezan en 0, entonces len siempre estará uno arriba
    
    try:
        model2 = np.poly1d(np.polyfit(x_train,y_train,2))
        y_test = model2(x_test)
        print(y_test)
    except:
        print("No enough data")
        y_test = 0


    
    x_plot = x_train.tolist() #convierto a lista para graficar
    x_plot.append(x_test)
    y_plot = y_train.tolist()
    y_plot.append(y_test)

    fig, ax = plt.subplots()  # Create a figure containing a single axes.
    ax.plot(x_plot, y_plot)  # Plot some data on the axes.
    
"""
